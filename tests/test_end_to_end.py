"""End-to-end tests (per slice). Run: python -m pytest tests -q"""
import os

from src import capacity_model as cm
from src import dataset
from src import gate
from src import manifest
from src.oracle import oracle_slices
from src.baselines import ThresholdStateMachine, HPA, PredictThenThreshold
from src.forecaster import LinearForecaster
from src.kpi_predictor import MLPRegressor
from src.mcp_server import call_tool
from src.llm_compiler import build_payload, call_stub
from src import benchmark as bench

DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "datasets", "generation_netwok_slicing_dataset",
    "2.2.1-10kprocessed", "results_slicing_WFQ_1000_routing_7800_7899")


def _load():
    states, delays, losses = dataset.load_result_dir(DATA)
    return dataset.sorted_by_load(states, delays, losses)


def test_dataset_per_slice():
    states, delays, losses = _load()
    assert len(states) == 100
    assert set(states[0].keys()) == set(cm.SLICES)
    assert all(sum(s.values()) > 0 for s in states[:5])
    assert all(d >= 0 for d in delays)


def test_capacity_model():
    nf = cm.NFConfig(cap_per_replica_mbps=50.0, min_replicas=1, max_replicas=5)
    assert cm.delay(40, 1, nf) > cm.delay(10, 1, nf)
    assert cm.required_replicas(1e9, nf) == 5
    assert cm.required_replicas(0.0, nf) == 1
    cfgs = cm.build_slice_configs({"eMBB": 50, "URLLC": 30, "mMTC": 10}, 0.001)
    assert set(cfgs.keys()) == set(cm.SLICES)
    assert cfgs["URLLC"].delay_budget < cfgs["eMBB"].delay_budget


def test_env_multi_slice():
    from src.telemetry_env import SlicingEnv
    cfgs = cm.build_slice_configs({"eMBB": 50, "URLLC": 30, "mMTC": 10}, 0.001)
    states = [{"eMBB": 20.0, "URLLC": 10.0, "mMTC": 5.0} for _ in range(3)]
    env = SlicingEnv(states, cfgs)
    obs = env.reset()
    assert set(obs["slices"].keys()) == set(cm.SLICES)
    obs, r, done, info = env.step({"eMBB": 99, "URLLC": 0, "mMTC": 3})
    assert obs["slices"]["eMBB"]["replicas"] == cfgs["eMBB"].max_replicas
    assert obs["slices"]["URLLC"]["replicas"] == cfgs["URLLC"].min_replicas
    obs, r, done, info = env.step({"eMBB": 1, "URLLC": 1, "mMTC": 1})
    obs, r, done, info = env.step({"eMBB": 1, "URLLC": 1, "mMTC": 1})
    assert done


def test_oracle_slices():
    cfgs = cm.build_slice_configs({"eMBB": 50, "URLLC": 30, "mMTC": 10}, 0.001)
    lbs = {"eMBB": [10] * 7, "URLLC": [10, 10, 200, 200, 200, 200, 200],
           "mMTC": [5] * 7}
    chosen = {"eMBB": 1, "URLLC": 1, "mMTC": 1}
    o = oracle_slices(lbs, 0, chosen, cfgs, horizon=5, d=1)
    assert o["URLLC"][1] == "up"
    assert o["eMBB"][1] == "hold"


def test_gate_slices():
    cfgs = cm.build_slice_configs({"eMBB": 50, "URLLC": 30, "mMTC": 10}, 0.001)
    assert gate.check_slices({"eMBB": 2, "URLLC": 2, "mMTC": 2}, cfgs)[0]
    assert not gate.check_slices({"eMBB": 2, "URLLC": 99, "mMTC": 2}, cfgs)[0]
    assert not gate.check_slices({"eMBB": 2, "URLLC": 2}, cfgs)[0]


def test_manifest_and_mcp():
    text = manifest.emit({"kind": "Deployment", "metadata": {"name": "x"},
                          "spec": {"replicas": 3}})
    assert manifest.parse(text) == ("Deployment", 3)
    cfgs = cm.build_slice_configs({"eMBB": 50, "URLLC": 30, "mMTC": 10}, 0.001)
    assert call_tool("estimate_capacity", {"slice_type": "URLLC", "load_mbps": 200.0}, cfgs) >= 1
    assert call_tool("scale_replicas", {"slice_type": "URLLC", "replicas": 3}, cfgs)["ok"]
    assert not call_tool("scale_replicas", {"slice_type": "URLLC", "replicas": 99}, cfgs)["ok"]
    assert call_tool("add_nf_instance", {"slice_type": "eMBB", "region": "edge-1"}, cfgs)["ok"]


def test_llm_payload_and_stub():
    states, delays, losses = _load()
    cfgs = bench.build_cfgs(states, delays)
    obs = {"t": 0, "slices": {s: {"load": states[0][s], "replicas": 1,
                                 "delay": 0.001, "loss": 0.0} for s in cm.SLICES}}
    payload = build_payload(obs, 100.0, 0.5, cfgs)
    assert set(payload["slices"].keys()) == set(cm.SLICES)
    r = call_stub(payload, cfgs)
    assert set(r["actions"].keys()) == set(cm.SLICES)
    assert all(1 <= r["actions"][s] <= 5 for s in cm.SLICES)


def test_full_loop_all_methods():
    states, delays, losses = _load()
    cfgs = bench.build_cfgs(states, delays)
    agg_nf = bench.build_agg_nf(states, delays)
    agg = [sum(s.values()) for s in states]
    predictor = MLPRegressor().fit(agg, delays)
    methods = bench.make_methods(cfgs, agg_nf, predictor)
    for name, decide in methods.items():
        out = bench.run_method(states, cfgs, decide)
        m = bench.metrics(out)
        assert 0 <= m["viol%"] <= 100
        assert m["mae"] >= 0
