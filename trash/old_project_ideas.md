# Which project to do? — Implementation notes from the paper stack

> This note expands each project idea with concrete implementation guidance extracted from the papers in `article/papers/`. No images are used; everything is text-only. A difficulty estimate is added as inline text and as an HTML comment at the end of each section.

---

## 1. Self-Sustaining RAN Slicing

**The Open Challenge:** Traditional 5G slicing requires manual operator intervention when unexpected traffic spikes or radio channel anomalies occur[4]. 6G aims for **Self-Sustaining Networks (SSNs)** that autonomously predict, adapt, and repair slice performance without human oversight.

**What to model:** Simulate dynamic user movement and sudden traffic bursts across two slices (e.g., Tactile Internet vs. eMBB)[4][5]. Compare a classic rule-based MAC scheduler against a **Hierarchical Deep Reinforcement Learning (DRL)** agent (such as DDPG or Double DQN)[5] that dynamically adjusts time-frequency resource blocks (RBs) and mini-slot allocations to prevent SLA violations[4][5].

### Paper-backed implementation plan

- The 6G roadmap survey (Wang et al., *On the Road to 6G: Visions, Requirements, Key Technologies and Testbeds*, 2023) frames the paradigm shift from SON to SSN and cites Mei et al. for an "intelligent self-sustained RAN slicing framework" that combines self-management of multi-granularity network resources, self-optimization/self-learning of slice control performance, and adaptive control under unpredictable conditions[4]. The same survey also highlights a hierarchical DRL framework that mixes modified **DDPG** with **double deep Q-network** to maximize long-term QoS of services and the spectral efficiency of network slices[5].
- Pennanen et al. (*6G: The Intelligent Network of Everything*, 2025) argue that MAC-layer resource allocation is an inherently non-convex combinatorial problem that is well suited to DRL, because DRL naturally handles sequential decision-making. They recommend hybrid offline-online learning to cope with rapidly varying channels and diverse QoS requirements[5].
- **Recommended simulator stack:** Python with NumPy/PyTorch, MATLAB 5G Toolbox, or ns-3/Simu5G. Build a time-frequency grid per TTI. Two slices: a Tactile-Internet/uRLLC slice (1 ms latency, small packets) and an eMBB slice (throughput-hungry). Users move along random waypoints; traffic is bursty (e.g., Pareto or Markov-modulated arrivals).
- **Hierarchical DRL design (as in the papers):**
  - *Top-level policy:* selects the slice priority/weight and the mini-slot split for the coming TTI. This is a mixed continuous-discrete action, so use **DDPG** for the continuous mini-slot fraction and **Double DQN** for the discrete priority class, exactly as the hierarchical framework in the literature[5].
  - *Low-level policy:* assigns specific RBs to users inside each slice (discrete action → DQN).
  - *State:* buffer occupancy per user, per-RB channel quality (CQI), SLA deficit counters, predicted traffic over the next few TTIs, and user positions.
  - *Reward:* weighted sum of SLA satisfaction (−latency violation penalty), throughput, spectral efficiency, and Jain’s fairness index.
- **Baselines to beat:** (i) round-robin + strict uRLLC priority; (ii) proportional-fair scheduler; (iii) fixed mini-slot reservation. Compare cumulative SLA violations, average throughput, RB utilization, and outage probability.
- **Key KPIs:** uRLLC latency/reliability, eMBB throughput, spectral efficiency, slice isolation, and frequency of manual reconfigurations needed.
- **Key paper references:** Mei et al., *Intelligent radio access network slicing for service provisioning in 6G: A hierarchical deep reinforcement learning approach* (IEEE Trans. Commun., 2021)[5]; Mei et al., *An intelligent self-sustained RAN slicing framework for diverse service provisioning in 5G-beyond and 6G networks* (Intelligent and Converged Networks, 2020)[4]; Nassar & Yilmaz, *Deep reinforcement learning for adaptive network slicing in 5G for intelligent vehicular systems and smart cities* (IEEE Internet Things J., 2022)[5].
- **Recommended ML/optimization tools:** Python with PyTorch or TensorFlow; Ray RLlib or Stable Baselines3 for the DRL loop; a custom OpenAI Gym environment for the scheduler; optional ns-3/Simu5G or the MATLAB 5G Toolbox for channel/traffic traces.

*Estimated difficulty: **Hard**.* The main friction points are training a hierarchical DRL agent with both continuous and discrete actions, building a realistic enough mobility/traffic/channel model, and keeping the DRL training stable across slice configurations.

<!-- Difficulty: Hard. Rationale: combines hierarchical DRL (DDPG + Double DQN), per-RB scheduling, and dynamic mobility/traffic; training instability and reward shaping are the main risks. -->

---

## 2. Digital Twin Slicing Predictor

**The Open Challenge:** In complex 6G topologies, testing a new slice or reconfiguring bandwidth on live physical infrastructure can cause unexpected Quality of Service (QoS) degradation[3][5].

**What to model:** Build a graph-based simulation (using **Graph Neural Networks / GNNs**)[5] that mirrors a physical cell layout. The Digital Twin simulates "what-if" scenarios (e.g., doubling vehicular slice demand) in virtual space first[5][6], predicting end-to-end latency and packet error rates before pushing updated scheduling policies back to the physical nodes[5].

### Paper-backed implementation plan

- Wang et al. (*A graph neural network-based digital twin for network slicing management*, IEEE Trans. Ind. Informat., 2022) is the closest technical match: a scalable digital twin that predicts end-to-end slice performance in unknown environments and supports intelligent slicing management[5]. Naeem et al. (*Digital twin-empowered network slicing in B5G networks: Experience-driven approach*, IEEE GLOBECOM Workshops, 2021) build digital twins of slices with graphs, use GNNs to learn the complex relationships of network slices, and then feed the learned state into a deep distributed Q-network to learn the optimal slicing strategy[5].
- The 6G roadmap paper describes digital-twin-based 6G architecture as a virtual network interactively mapped to the physical network in real time, performing closed-loop simulation and optimization before touching live nodes[3]. Pennanen et al. also highlight digital-twin-assisted network management and AI/ML at the edge as key enablers of 6G autonomy[5].
- **Recommended stack:** Python with PyTorch Geometric or DGL for the GNN; a discrete-event simulator (ns-3/Simu5G or a custom Python event loop) for the physical twin.
- **Graph construction:** Nodes = gNBs, UEs, MEC hosts, core network functions, and transport links. Edge features = link capacity, latency, current load, distance/hop count. Node features = available CPU/RAM/cache, traffic intensity, channel quality, slice demand, historical latency/PER.
- **What-if scenarios to test:** (a) double vehicular slice demand; (b) add a new uRLLC slice; (c) degrade one backhaul link by 30%; (d) migrate a slice to a different MEC host. The twin predicts per-slice end-to-end latency and packet error rate over a short horizon (e.g., 100 TTIs).
- **GNN architecture:** GraphSAGE or GAT to produce node embeddings, followed by a small MLP that predicts latency and PER per slice. Train on historical snapshots; validate with k-fold cross-validation on synthetic traces and, if available, real traces.
- **Policy push loop:** If the twin predicts SLA compliance for a candidate policy, push the new scheduling policy to the physical nodes; otherwise keep the old policy. Maintain a rollback counter and a drift metric (difference between twin prediction and real measurement) to measure model aging.
- **Key KPIs:** prediction MSE for latency/PER, reduction in SLA violations after rollout, policy rollout success rate, twin-physical drift, and time saved compared with live-only experimentation.
- **Key paper references:** Wang et al., *A graph neural network-based digital twin for network slicing management* (IEEE Trans. Ind. Informat., 2022)[5]; Naeem et al., *Digital twin-empowered network slicing in B5G networks: Experience-driven approach* (IEEE GLOBECOM Workshops, 2021)[5]; Nguyen et al., *Digital twin for 5G and beyond* (IEEE Commun. Mag., 2021)[3].
- **Recommended ML/optimization tools:** PyTorch Geometric or DGL for the GNN; ns-3/OMNeT++ or a Python event loop to generate the physical traces; Pandas/JAX for policy search; Kubernetes/OpenStack or Mininet/ONOS if you want to emulate the control-plane orchestrator.

*Estimated difficulty: **Expert**.* The hardest parts are keeping the digital twin synchronized with a dynamic physical network, constructing a meaningful graph from real RAN/topology data, training the GNN with limited labeled data, and safely deploying the policies without harming live services.

<!-- Difficulty: Expert. Rationale: graph construction and GNN training for a digital twin are non-trivial; keeping the twin synchronized with a dynamic physical network and guaranteeing safe policy rollout adds research-level complexity. -->

---

## 3. Physical Layer Predictive Puncturing vs. Spectral Efficiency

**The Open Challenge:** In 5G, slicing allocated data rate and latency (eMBB, uRLLC, mMTC)[1][7]. In 6G, a single slice must allocate **multi-modal resources**: radio bandwidth, Terahertz radar sensing beams (ISAC), and Multi-Access Edge Computing (MEC) processing power simultaneously.

**What to model:** Implement a physical/MAC layer slot simulator comparing random puncturing, static mini-slot reservation, and DRL-predictive preemption. Quantify the exact trade-off between mission-critical latency guarantees and overall spectral efficiency.

### Paper-backed implementation plan

- Dogra et al. (*A Survey on Beyond 5G Network With the Advent of 6G*, 2020) describe 5G NR mini-slots as the smallest Resource Blocks (RBs) that can be allocated, enabling very small packet transmissions for low latency[7]. They cite Esswie & Pedersen for a **null-space-based preemptive scheduler** that forcefully transmits uRLLC traffic together with eMBB, reducing queuing delay without influencing overall capacity[7], and Alsenwi et al. for an eMBB-uRLLC **risk-sensitive resource-slicing** approach[7]. Hou et al. use prediction-and-communication co-design to improve uRLLC reliability[7].
- For multi-modal allocation, Pennanen et al. frame 6G as integrating communication, computation, and caching (i3C) at the network edge, with **ISAC** as a revolutionary beyond-communication technology. They explicitly note that resource management becomes complicated because of multiple resource types and diverse performance requirements, calling for AI/ML-aided solutions[5].
- Mach & Becvar (*Mobile Edge Computing: A Survey*, 2017) split MEC offloading into three sub-problems: offloading decision, computing-resource allocation, and mobility management[1]. For the simulator this means the MEC dimension needs a CPU-cycle budget and a per-task offloading decision.
- **Recommended simulator:** Python or MATLAB. One TTI = 1 slot (or a mini-slot). Maintain a resource grid: RBs × radar/sensing beams × MEC CPU cycles.
- **Three schemes to compare:**
  1. *Random puncturing:* whenever a uRLLC packet arrives, randomly puncture/pause an ongoing eMBB RB.
  2. *Static mini-slot reservation:* permanently reserve the first N mini-slots of each slot for uRLLC/ISAC traffic.
  3. *DRL-predictive preemption:* a DRL agent observes the predicted uRLLC/ISAC arrival process, eMBB buffer state, CSI, and MEC queue, then decides (a) which RBs to preempt, (b) which beams to use for sensing, (c) how much MEC compute to allocate to each task.
- **DRL reward (multi-objective):** −latency violation penalty − MEC overload penalty − spectral-efficiency loss + reliability bonus. The agent must handle both discrete RB/beam choices and continuous compute-share decisions; a hybrid actor-critic architecture (e.g., PPO or DDPG with a discrete head) is a good starting point.
- **ISAC modeling:** Model a THz radar beam as an additional resource dimension that consumes time/frequency resources and yields a sensing utility (e.g., detection probability or ranging accuracy). The scheduler must balance communication RBs versus sensing beams, reflecting the ISAC trade-off described in the 6G papers[5].
- **MEC modeling:** Each user task has a required CPU-cycle count; the scheduler decides local vs. edge execution and the MEC CPU share. Include both offloading latency and backhaul/fronthaul load.
- **Metrics:** uRLLC latency/reliability, eMBB throughput and spectral efficiency (bits/s/Hz), ISAC detection/ranging performance, MEC utilization, energy per task, and a Pareto front of latency-vs-spectral-efficiency.
- **Key paper references:** Esswie & Pedersen, *Opportunistic spatial preemptive scheduling for URLLC and eMBB coexistence in multi-user 5G networks* (IEEE Access, 2018)[7]; Alsenwi et al., *EMBB-URLLC resource slicing: A risk-sensitive approach* (IEEE Commun. Lett., 2019)[7]; Hou et al., *Prediction and communication co-design for ultra-reliable and low-latency communications* (IEEE Trans. Wireless Commun., 2020)[7]; Liu et al., *Integrated sensing and communication: Toward dual-functional wireless networks* (the ISAC survey)[5].
- **Recommended ML/optimization tools:** A Python or MATLAB slot-level simulator; PyTorch/TensorFlow RL with PPO/DDPG/DQN; optional Sionna for waveform-level PHY or OMNeT++ for system-level simulation; custom Gym environment exposing the multi-modal resource grid.

*Estimated difficulty: **Hard / Expert**.* This is the most complex of the three because it requires cross-layer PHY/MAC/MEC modeling, hybrid communication-sensing-compute resource allocation, a DRL agent that handles both discrete and continuous actions, and realistic ISAC/THz channel/beam models.

<!-- Difficulty: Hard/Expert. Rationale: the most complex of the three; requires modeling THz/ISAC beams, MEC compute allocation, and a DRL agent that simultaneously handles discrete RB preemption and continuous beam/compute allocation, all while optimizing conflicting latency and spectral-efficiency objectives. -->

---

## Quick comparison

| Project | Core technique | Main paper anchor | Difficulty | Main risk |
|---|---|---|---|---|
| 1. Self-Sustaining RAN Slicing | Hierarchical DRL (DDPG + Double DQN) | Mei et al. (2021) [5] | Hard | DRL training instability and realistic traffic/mobility modeling |
| 2. Digital Twin Slicing Predictor | GNN + digital twin + deep Q-network | Wang et al. (2022) [5] | Expert | Twin-physical drift and safe policy rollout |
| 3. Predictive Puncturing vs. Spectral Efficiency | Multi-modal DRL (RBs + ISAC beams + MEC) | Esswie & Pedersen (2018) [7], Pennanen et al. (2025) [5] | Hard / Expert | Cross-layer modeling and conflicting objectives |

> Note: one PDF in `article/papers/` (`a610bc6e-...pdf`) is a language-proficiency certificate, not a research paper, so it was skipped.

---

## Cross-cutting takeaways

1. **Start from 5G NR building blocks** (OFDMA, scalable numerology/mini-slots, massive MIMO/hybrid beamforming) and then add the 6G extensions: AI-native control, digital twins, ISAC/THz, and MEC/edge computing.
2. **DRL/RL is the dominant proposed method for autonomous slicing** in the surveyed 6G literature, but the papers repeatedly flag stability, online learning, and multi-agent coordination as open issues.
3. **Digital twins are consistently described as the way to test policies before touching physical infrastructure**, with GNNs specifically proposed for slice-level E2E prediction; the hard parts are data alignment, real-time twin maintenance, and safe closed-loop deployment.
4. **Project 3 sits at the intersection of several open 6G challenges**: ISAC sensing-vs-communication trade-offs, THz hardware/channel limitations, and simultaneous allocation of radio + sensing + compute resources — exactly the “integrated communications, sensing, and computing” challenge raised in Wang et al. (2023).

> **Reusable software-stack note:** A Python or ns-3 based simulator, PyTorch Geometric for any GNN component, and Stable-Baselines3 / Ray RLlib for the DRL agents cover all three projects.
