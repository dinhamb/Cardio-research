# 2022 header-interface calibration summary

The 2022 FDA MAUDE pull completed successfully:
- 9,597 candidate device rows,
- 9,587 unique MDR keys,
- 4,833 exact-narrative event groups.

After exact-text deduplication:
- 299 event groups contain spring-contact language,
- 188 of those contain high-impedance language,
- 38 contain Lead Safety Switch / safety-switch language,
- 42 explicitly mention a non-Boston / other-manufacturer lead,
- 187 contain the 2020 design-enhancement language,
- 230 contain terminal-ring / fretting / microscopic-particle / oxidation language.

These categories overlap and are not confirmed-event counts.

## Direct header-generation evidence

2022 contains several records that explicitly state a device **did not have the enhanced header**.

Particularly useful examples include:
- DYNAGEN X4 CRT-D G156: Technical Services noted no enhanced header while evaluating impedance spikes and positional noise.
- ACCOLADE EL DR L321: competitor RA lead, Lead Safety Switch, and explicit no-enhanced-header statement.
- ACCOLADE MRI DR L311: competitor RA lead, Lead Safety Switch, and explicit no-enhanced-header statement.
- DYNAGEN EL ICD DR D153: Technical Services stated recurrent RA impedance spikes were related to the spring-contact issue and that resolution required a new generator with the enhanced header, not simply replacement of the atrial lead.

This substantially strengthens the pre/post-2020 header-generation hypothesis.

## Static-testing limitation

Several returned devices with field intermittent-impedance phenotypes later passed:
- visual header inspection,
- connector-port pin-gage testing,
- simulated heart-load tests,
- and standard electrical tests.

The repeated finding is therefore compatible with a **dynamic contact/fretting phenomenon** that may not be reproduced by static returned-product testing.

## Research interpretation

The emerging Boston variable is more specific than connector standard alone:

pre-enhancement header contact generation + lead terminal design/manufacturer + time in service -> dynamic high-impedance / LSS / MV-noise phenotype

This remains a postmarket signal-analysis framework, not an incidence comparison.
