# Boston RV-DF4 shock-impedance / spring-contact candidate stratum

This is a **candidate** dataset, not a confirmed-failure series and not an incidence analysis.

## Why it exists

The Boston Scientific IS-1 spring-contact workstream demonstrates that dynamic terminal-ring/header contact behavior can produce intermittent electrical abnormalities that disappear on static testing.

A separate pattern appears in Boston ICD/CRT-D systems whose **RV high-voltage port is DF4**:

- abrupt or sporadic high shock impedance,
- values often returning to normal on the next transmission or in-office check,
- sometimes no noise on stored EGMs,
- sometimes a non-Boston RV defibrillation lead,
- Technical Services repeatedly raising spring-contact/device-lead interface as a differential alongside lead fracture.

The manually selected calibration table contains 21 event records from 2020–2024. Some are deliberately retained as ambiguous or complex controls.

## What this does not show

It does **not** show:
- that DF4 is defective,
- that Boston DF4 headers fail more often than another manufacturer,
- that the terminal polymer is causal,
- or that a sporadic high shock impedance is necessarily a header problem.

Several records explicitly retain lead fracture, setscrew/connection, EMI, or lead-body damage in the differential.

## High-specificity phenotype

The most interesting pattern is:

`stable baseline shock impedance -> isolated/sporadic extreme value -> clean EGM or no lead-integrity evidence -> normal subsequent office/test-shock value -> recurrence -> spring-contact/interface differential`

That is mechanistically different from a fixed conductor fracture and should be adjudicated separately.

## Next joins

For each event resolve:
1. exact RV lead manufacturer/model,
2. implant dates for generator and lead,
3. single- vs dual-coil lead and programmed shock vector,
4. DF4 terminal-body / seal-zone material,
5. generator header generation/contact architecture,
6. whether returned-product analysis exists,
7. whether a low-/max-energy commanded shock reproduced normal impedance.

Only after those joins should this be compared with DF1 systems or other manufacturers.
