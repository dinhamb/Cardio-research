# 2020 header-interface calibration summary

The 2020 FDA MAUDE pull initially produced:
- 3,701 candidate device rows,
- 3,701 unique MDR keys,
- 3,329 exact-narrative event groups.

The original priority classifier surfaced one apparent physical cross-contact event. Manual review showed it was **not a connector event**: an Abbott/St Jude ACCENT pacemaker had premature depletion with silver traces on battery separators and a conductive bridge between battery anode and cathode. The pipeline was corrected so conductive bridge only enters the physical connector bucket when connector/header-localized language is also present.

## Clinically important proximal-interface cases

### ESSENTIO DR L101 — MDR 9550413
- non-Boston RV lead,
- intermittent threshold and impedance spikes,
- loss of capture,
- >2 seconds of asystole,
- Boston Technical Services considered a spring-contact issue.
Returned-product analysis later documented a **hole in the RV seal plug**, but port dimensions and static electrical testing were normal and Boston did not attribute the clinical event to a device characteristic. This is therefore a valuable physical sealing observation but not a confirmed causal seal failure.

### BIOTRONIK ENTICOS 4 DR — MDR 9592506
- loss of capture,
- ventricular impedance >2500 ohms in both uni- and bipolar configurations,
- reconnection to the pacemaker restored normal values,
- clinical suspicion of poor header contact.
Returned-product analysis found normal header bores, setscrews, spring elements and long-term electrical performance. This is a useful non-Boston dynamic-interface candidate/negative-control case.

## RV DF4 shock-impedance pattern

2020 also contains multiple Boston ICD/CRT-D systems with confirmed RV DF4 ports and a different phenotype:
- intermittent/spiky high shock impedance,
- later normal measurements or normal low-energy test shock,
- lead-fracture versus spring-contact differential,
- sometimes a non-Boston RV defibrillation lead.

Representative MDRs:
- 9550427 — RESONATE X4 G447
- 9924584 — DYNAGEN D150
- 9995614 — INOGEN D140
- 10619695 — INOGEN D142

These are now tracked in boston-df4-shock-contact-candidates-v1.csv.

## Interpretation

The Boston IS-1 spring-contact/MV issue and the emerging RV-DF4 shock-contact candidates must remain separate engineering strata. The former has a defined 2019 FDA-approved IS-1 header modification and 2020 implementation narrative. The latter is currently a postmarket candidate phenotype without a demonstrated DF4-wide design defect.
