# Speaking Script — Section IX: "Potential Technologies for 6G"
Paper: *6G: The Intelligent Network of Everything* (H. Pennanen et al., IEEE Access, vol. 13, 2025, DOI: 10.1109/ACCESS.2024.3521579)
Target length: ~15 minutes (~2,000 words at a normal speaking pace)

---

## Timing plan

| Time  | Part                                          |
|-------|-----------------------------------------------|
| 0:00  | Opening & roadmap                              |
| 1:00  | A. Spectrum: THz + OWC                        |
| 2:30  | B. Antenna systems: UM-MIMO, RIS, HMIMO       |
| 4:00  | C. Transmission schemes                       |
| 5:00  | D. Network architecture: NTN, UDN, IAB, cell-free |
| 6:30  | E. Network intelligence: core, edge, air interface |
| 8:00  | F. Beyond-communication: i3C, ISAC, WET       |
| 9:30  | G. Energy-aware technologies                  |
| 10:30 | H. End-device: D2D, V2X, UAV                  |
| 11:30 | I. Service-oriented: private networks         |
| 12:00 | J. Security                                   |
| 13:00 | Closing                                       |

---

## OPENING (0:00 – 1:00)

Good [morning/afternoon] everyone.

In this part, I'll walk you through Section nine of the paper, "Potential Technologies for 6G". This is the technical core of the survey: the authors identify and review **twenty-seven candidate technologies, organized into ten categories**.

[gesture to Figure 11 if showing slides]

Before diving in, two things to keep in mind:

First, every technology in this section is described using the **same template**: vision, introduction, past and present, opportunities and challenges, and literature with future directions. So the structure repeats — which makes it easy to follow.

Second, the key message of the whole section is this: 6G will not be built on one single breakthrough. It will be a **large and heterogeneous system**, and each of these ten categories solves a different piece of the puzzle — spectrum, antennas, transmission, architecture, intelligence, and so on.

Let's go through them category by category.

---

## A. SPECTRUM-LEVEL TECHNOLOGIES (1:00 – 2:30)

The first category is the **spectrum**. Here the paper reviews two technologies.

**Number one: Terahertz communication.**

[slow down — this is the flagship technology]

The THz band ranges from 0.1 to 10 terahertz. Because of the **massive amount of unused spectrum** there, THz is seen as *the* key enabler for the extreme capacity targets of 6G — including the headline goal of **one terabit per second peak rate**.

The trade-off is harsh propagation: high path loss, molecular absorption, and easy blockage. So THz means **short range** — which is fine for hotspots, close-proximity links, and data-hungry applications like holographic telepresence or wireless XR.

Where do we stand today? Industry demos are already impressive: Samsung achieved 6.2 gigabits per second at 140 gigahertz; Nokia with NTT reached 25 gigabits per second at 144 gigahertz; and Keysight went above 100 gigabits per second at 300 gigahertz. On the regulatory side, WRC-2023 identified **five frequency bands above 100 gigahertz** for potential IMT-2030 use, with a decision expected at WRC-2031. So 6G would be the **first generation to go beyond 100 gigahertz** — just like 5G was the first to go above 6 gigahertz.

The main challenges: propagation losses, beam misalignment in ultra-massive MIMO, hardware impairments like phase noise, and power consumption. The paper points to RIS and hybrid beamforming as mitigation paths.

**Number two: Optical wireless communication — OWC.**

OWC complements radio in **special scenarios**: visible light communication for short-range indoor access, and free-space optics — FSO — for long-range outdoor point-to-point links, like backhaul. Modern FSO experiments already demonstrated **multi-terabit per second** rates over kilometers, and even petabit-class over short links. The catch: atmospheric turbulence, beam divergence, and the need for line of sight, which limit reliability in practice.

**Transition:** So that's where the spectrum comes from. Next — how do we actually exploit it at the antenna level?

---

## B. ANTENNA SYSTEM TECHNOLOGIES (2:30 – 4:00)

Three technologies here, and they're all about pushing antennas to their limits.

**First, ultra-massive MIMO.** This is the natural evolution of massive MIMO, with **hundreds to thousands of antenna elements**, possibly embedded in surfaces around the device. Its role in 6G is to make THz communication viable in cellular environments — the high beamforming gains compensate for the huge path losses I mentioned. With very narrow beams also come **beyond-communication benefits**: high-accuracy sensing and localization.

**Second — and this is the most revolutionary one — Reconfigurable Intelligent Surfaces, RIS.** [pause]

The idea is simple and powerful: instead of adapting to the wireless environment, we **program the environment itself**. An RIS is a panel of many low-cost, passive, electronically controlled elements that reflect incident signals with adjustable phase — creating "passive beamforming" toward the receiver. Benefits: better signal quality, coverage extension, and — very relevant for THz — **bypassing blockages**. Because passive RIS barely consumes power, it's cheap and energy efficient. That's why the paper calls it a potential game-changer: turning the unpredictable wireless channel into a **controllable, programmable entity**.

**Third, holographic MIMO.** Think of it as the theoretical limit of this trend: a surface with a virtually continuous — almost infinite — number of elements. Active holographic surfaces act as transceivers; passive ones are actually related to RIS. The promise is **very high spatial multiplexing gains**, approaching the fundamental limits of MIMO theory.

**Transition:** Antennas give us the pipes — but what do we transmit through them?

---

## C. TRANSMISSION SCHEME TECHNOLOGIES (4:00 – 5:00)

Four elements here, and I'll group them.

**Multi-waveform scheme.** 6G must operate from sub-6 gigahertz up to THz — conditions change dramatically across that range. So instead of one-size-fits-all, 6G is expected to support a **flexible, tunable multi-waveform** air interface: the waveform adapts to the band and scenario.

**Advanced modulation and coding.** Classic PHY-layer work, but now adapted for wide bandwidths, hardware impairments, and integration with sensing — for example, modulation schemes that are also good for radar-like functions.

**NOMA — non-orthogonal multiple access.** Serving multiple users on the same time-frequency resource improves spectral efficiency. The paper highlights a very 6G-specific use case: **massive IoT** in combination with grant-free access.

**And that's the fourth one: grant-free medium access.** Today, a device must request a grant before transmitting. In ultra-massive IoT, that signaling would collapse. Grant-free access lets devices **transmit instantly, without scheduling** — saving latency, signaling, and energy.

**Transition:** Now, how do we organize all of this at the network level?

---

## D. NETWORK ARCHITECTURAL TECHNOLOGIES (5:00 – 6:30)

The network becomes a **three-dimensional, hybrid system**. Four technologies:

**Integrated non-terrestrial and terrestrial networks — INTNs.** This is the space-air-ground architecture: satellites, HAPS, drones, and terrestrial base stations working as one network. The goal is **truly global coverage** — land, sea, and air — plus applications like remote-area connectivity and worldwide IoT monitoring.

**Ultra-dense networks.** Remember THz has short range — so to deliver extreme capacity, cells must become very small and very dense. UDN is essentially the flip side of the THz coin.

**Integrated access and backhaul — IAB.** If you deploy thousands of small cells, you can't dig fiber to each one. IAB lets cells **serve users and backhaul each other over the same wireless link**. It already exists in 5G, but its role grows as densification continues.

**Cell-free massive MIMO.** A break from the cellular paradigm: many distributed access points serve each user **jointly and cooperatively** — no cell edges. The motivation is **stable, uniform quality of service** everywhere in the coverage area.

**Transition:** So far, everything is conventional engineering. The next category is the big paradigm shift: making the network itself intelligent.

---

## E. NETWORK INTELLIGENCE TECHNOLOGIES (6:30 – 8:00)

This is where AI and machine learning move from being an add-on to being **native** to the network. The paper places intelligence at three levels:

**Intelligent core.** 5G core was about softwarization — virtualized network functions. 6G goes further: pervasive AI/ML makes the core **self-managing, automated, and proactive**. The authors frame it as an evolution "from cloud to cloud intelligence."

**Intelligent edge.** With AI distributed to the edge, latency-critical and privacy-sensitive services can run close to the user — this is **edge intelligence**, enabling new applications with reduced latency and less communication overhead.

**Intelligent air interface.** Even the PHY layer gets AI: ML for channel estimation, beam management, CSI feedback, scheduling. This could change the way the air interface is **designed, standardized, and implemented** — moving from hand-crafted models to learned components.

Context worth noting: AI/ML entered 3GPP standards in Release 18, under 5G-Advanced. 6G is expected to make it pervasive.

**Transition:** And once you have intelligence everywhere, the network can take on jobs that go beyond communication.

---

## F. BEYOND-COMMUNICATION TECHNOLOGIES (8:00 – 9:30)

This category is my personal highlight of the section — the real paradigm shift.

**First, integrated communication, computation, and caching — "i3C".** The joint design of these three capabilities at the edge, exploiting their synergies. Compute and storage become network resources that are scheduled like spectrum.

**Second — the star of this group — integrated sensing and communication, ISAC.** [pause]

With 6G, the network **senses the environment while it communicates**. Massive antennas, wide bandwidths, and dense deployments make the network a giant distributed sensor. Applications: environment monitoring, gesture recognition, health monitoring, even "dark vision" — seeing through obstacles at THz frequencies. The paper calls ISAC a **revolutionary technology**, expanding mobile networks beyond communication toward ubiquitous sensing.

**Third, wireless energy transfer.** Radiating power to energize lightweight IoT devices — battery-free sensors that harvest energy over the air.

**Transition:** Talking about energy — that's exactly the next category.

---

## G. ENERGY-AWARE TECHNOLOGIES (9:30 – 10:30)

Energy efficiency is not optional in 6G — with denser networks and THz power demands, it's a make-or-break issue. Three technologies:

**Green networks**: energy-efficient design at every level — components, link adaptation, resource management, network operation — for both ecological and economic reasons.

**Energy harvesting**: low-power IoT devices collecting energy from ambient sources — solar, RF, motion — enabling sustainable, self-powered sensor networks.

**Backscatter communications**: the extreme low-power play. A device communicates by **reflecting an existing carrier signal** instead of generating its own. Combined with wireless energy transfer, this enables tags and sensors that communicate with **micro-watts** of consumption.

**Transition:** These lightweight devices are part of a bigger trend — the explosion of end devices.

---

## H. END-DEVICE-ORIENTED COMMUNICATION (10:30 – 11:30)

Three device-centric technologies:

**D2D — device-to-device.** Nearby devices talk **directly**, without going through a base station. Offloads the network, reduces latency, supports scenarios from cellular offload to industrial and aerial proximity links.

**V2X — vehicle-to-everything.** Key enabler of intelligent transportation: vehicle-to-vehicle, to infrastructure, to pedestrians, to network. In the 6G era, it's the backbone of **connected autonomous vehicles**.

**Cellular-connected UAVs.** Drones served by — and flying inside — the cellular network. This enables aerial applications while the network must also **handle** these aerial users, whose mobility is truly three-dimensional.

**Transition:** When the network touches all these industries, a new service model emerges.

---

## I. SERVICE-ORIENTED TECHNOLOGIES (11:30 – 12:00)

One technology here: **private networks**.

Public networks serve consumers; private networks are tailored to a **vertical customer** — a factory, a hospital, a port. 5G introduced non-public networks in Release 16, but 6G is expected to take them to the next level with **extreme performance, pervasive AI, and integrated sensing**. The paper positions them as a core enabler of Industry 4.0 and of mobile networks penetrating all levels of society — plus a major **new business opportunity** for operators.

---

## J. SECURITY TECHNOLOGIES (12:00 – 13:00)

Last category — and appropriately so: if society depends on 6G, 6G must be **trustworthy**.

The technology here is the **holistic network security architecture**. The authors propose a three-phase approach:

One — identify the **entire threat landscape**, across all network layers, and keep it updated.
Two — develop **technological solutions** for each identified threat.
Three — integrate everything into a **comprehensive architecture** covering security, privacy, and trust.

Note that the threat landscape grows with 6G itself: new technologies like AI, non-terrestrial networks, and V2X create **new attack surfaces**. And the paper makes an interesting observation: AI/ML is a **double-edged sword** — a powerful defense tool, but also a novel attack target.

---

## CLOSING (13:00 – 14:30)

Let me wrap up with the three takeaways of this section.

**One — heterogeneity is the design philosophy.** No single technology defines 6G. Twenty-seven technologies across ten categories — spectrum from sub-6 to THz and optical, antennas that program the environment, flexible transmission, 3D hybrid architectures, native intelligence, sensing and energy integration, energy-aware design, massive device ecosystems, private services, and security.

**Two — most pieces already exist in early form.** Many of these — IAB, private networks, AI/ML in RAN — started in 5G-Advanced. 6G's job is to make them pervasive, integrated, and extreme.

**Three — the biggest shifts are conceptual.** RIS turns the environment into software. ISAC turns the network into a sensor. Pervasive AI turns it into a self-managing system. That's why the paper calls 6G *the intelligent network of everything*.

Thank you — happy to take questions.

---

## Backup facts (for Q&A)

- THz band: 0.1–10 THz; transmission windows above ~800 GHz absorption limit
- IEEE 802.15.3d-2017: first THz standard, fixed point-to-point at 252–321 GHz
- WRC-2023 candidate bands >100 GHz: 102–109.5, 151.5–164, 167–174.8, 209–226, 252–275 GHz
- 5G FR2-1: 24.5–52.6 GHz (Rel-15); FR2-2: 52.7–71 GHz (Rel-17)
- Samsung 2021: 6.2 Gbit/s @ 140 GHz, 50 ft; LG 2022: 320 m outdoor THz link @ 155–175 GHz; Nokia/NTT/Docomo 2023: 25 Gbit/s @ 144 GHz; Keysight 2023: >100 Gbit/s @ 300 GHz
- OWC history: Bell's photophone, 1880; modern FSO: 13.16 Tbit/s over 10.45 km (2018)
- Private networks in 5G: public-network-integrated and stand-alone NPN (Rel-16)
- 6G security: 3 phases — threat identification → per-threat solutions → holistic architecture
- 27 technologies / 10 categories — same review template for each (vision, introduction, past & present, opportunities & challenges, literature & future directions)