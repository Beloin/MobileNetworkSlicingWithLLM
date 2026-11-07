# 6G Slicing Architecture — Literature Cross-Reference Matrix

Reference for the two-tier control plane. Saved 2026-11-02.

## Corrections (verified against local files)

- DeepSlice target = 3 classes {eMBB, URLLC, mMTC}. No "Master Slice".
- DeepSlice inputs = 8: Use Case Type, UE Category, Technology Supported, Day, Time, GBR, Packet Loss Rate, Packet Delay Budget. No QCI, no Duration.
- DeepSlice = slice *selection* classifier, not load->KPI, not time series. Rule-synthetic, label-imbalanced (33600/14784/14784).
- Rows below not yet verified, mark **[verify]** before citing: SliceNFV, CS-AC, AutoRAN, AgentRAN, Ferrag, IJWOS, SliceOps.
- Bandara arXiv id differs between PLAN.md (`2602.13227`) and this matrix (`2502.14536`) — verify.

## Component -> source mapping

| Module | Role | Sources |
|---|---|---|
| Tier 1 fast ML | numeric signals (forecast, violation prob, slice class) | DeepSlice (Thantharate 2019); SliceNFV (Alnaim & Alwakeel 2026) [verify]; CS-AC (Rezazadeh) [verify] |
| Tier 2 LLM + MCP | translate signals -> K8s/Helm change | AutoRAN (Maxenti 2025); Bandara et al. 2025; AgentRAN [verify]; Ferrag [verify] |
| Telemetry / env | dataset replay -> Gymnasium | Farreras 2024 (Zenodo 10610616); AdapShare (Gopal/NIST); DeepSlice |
| Oracle + gates | offline hindsight + schema/policy gate | IJWOS [verify]; SliceOps [verify] |

## Datasets

| Dataset | Contents | Paper |
|---|---|---|
| AdapShare | LTE PRB demand (hourly, ~36 days) + synthetic NR (TimeGAN) | Gopal et al., O-RAN DSS [verify venue] |
| Network slicing dataset | 10k sims, WFQ slicing, per-slice delay/jitter/loss | Farreras et al. 2024, Zenodo 10610616 |
| DeepSlice | 63k UE-context -> slice type | Thantharate et al. 2019, UEMCON |

## BibTeX

```bibtex
@inproceedings{thantharate2019deepslice,
  title={DeepSlice: A Deep Learning Approach towards an Efficient and Reliable Network Slicing in 5G Networks},
  author={Thantharate, Anurag and Paropkari, Ruutuja and Walunj, Vijay and Beard, Cory},
  booktitle={2019 IEEE 10th Annual Ubiquitous Computing, Electronics \& Mobile Communication Conference (UEMCON)},
  pages={0762--0767},
  year={2019},
  doi={10.1109/UEMCON47517.2019.8993066}
}

@misc{gopal_adapshare,
  title={AdapShare: An RL-Based Dynamic Spectrum Sharing Solution for O-RAN},
  author={Gopal, Sneihil and others},
  institution={NIST},
  note={LTE PRB demand (BladeRF+OWL) + TimeGAN synthetic NR. [verify venue/year]}
}

@article{farreras2024generation,
  title={Generation of a network slicing dataset: The foundations for AI-based B5G resource management},
  author={Farreras et al.},
  journal={Data in Brief},
  year={2024},
  doi={10.5281/zenodo.10610616}
}

@misc{maxenti2025autoran,
  title={AutoRAN: Automated and Zero-Touch Open RAN Systems},
  author={Maxenti et al.},
  journal={arXiv preprint arXiv:2504.11233},
  year={2025}
}

@misc{bandara2025agentic,
  title={An Agentic AI Control Plane for 6G Network Slice Orchestration, Monitoring, and Trading},
  author={Bandara et al.},
  journal={arXiv preprint},
  year={2025},
  note={arXiv id to verify: 2502.14536 vs PLAN.md 2602.13227}
}

@article{alnaim2026slicenfv,
  title={Network-Slice-Aware VNF Orchestration for Mission-Critical IoT in 6G Networks: A Multi-Objective Deep Reinforcement Learning Approach},
  author={Alnaim, Abdullah and Alwakeel, Ali},
  journal={MDPI Sensors},
  year={2026}
}
```
