# 2024 late in-service header-interface seed

The 2024 bulk pull completed successfully and produced:
- 5,368 candidate device rows,
- 5,357 unique MDR keys,
- 3,821 exact-narrative event groups.

This is a high-recall corpus, not a failure count.

The first manual late/in-service review shows a conspicuous cluster of Boston Scientific spring-contact / lead-terminal-ring interaction narratives. These reports describe intermittent high pacing or shock impedance, lead safety switches, noise/pacing inhibition, and in some cases symptoms, while static returned-device dimensional/electrical testing may remain normal.

Several manufacturer narratives explicitly state that:
- repeated small movements of the lead terminal ring,
- variation in contact force,
- and surface roughness

can affect the electrical connection with the spring contact and produce intermittent impedance changes. They also refer to a 2020 design enhancement intended to stabilize that connection.

That is highly relevant to the engineering-spine approach because it points to a dynamic tribological/contact-interface mechanism rather than lead fracture.

## Important separation

Do not pool:
- lead-terminal/spring-contact interaction,
- generator header-bond/hermetic failures,
- implant under-insertion/setscrew problems,
- lead-body fracture,
- and generator-change fit/compatibility problems.

They can produce overlapping clinical signatures but belong to different engineering layers.

The manually adjudicated seed is in 'header-interface-adjudication-2024-late-seed.csv'.

## Current interpretation

This seed is not yet a DF4-versus-DF1 comparison. Some events involve IS-1 pace/sense contacts, some high-voltage systems, and several mixed-manufacturer lead-generator combinations. The next join should resolve:
1. exact connector standard for each affected contact,
2. lead manufacturer/model,
3. generator header generation,
4. whether the device predates or postdates the stated 2020 header/contact enhancement,
5. implant age and generator-change history where available.

## Spring-contact candidate stratum

After exact-narrative deduplication, the 2024 corpus contains 202 event groups carrying the spring-contact narrative term.

Overlapping features within those 202 groups:
- 132 contain high-impedance language,
- 30 contain Lead Safety Switch / LSS language,
- 30 explicitly mention a non-Boston / other-manufacturer lead,
- 57 contain design-enhancement / enhanced-spring-contact / updated-header language.

These counts are triage strata, not confirmed mechanism counts. Cross-device duplicate clustering remains important because a generator and a non-Boston lead can generate separate MDRs with differently worded narratives for one clinical event.
