# Boston ACCOLADE-family PaceSafe / algorithm surveillance summary

Scope: FDA MAUDE bulk files, Boston Scientific ACCOLADE-family pacemakers/CRT-Ps (ACCOLADE, PROPONENT, ESSENTIO, VISIONIST, VALITUDE; ALTRUA 2 where identified), 2015 through current 2026 feed.

## Under-reporting caveat

MAUDE is a passive reporting system. Device user facilities are not required to report device malfunctions unless a reportable death/serious injury criterion is met; manufacturers report reportable malfunctions once they become aware of them. Therefore clinic-observed algorithm behavior that is corrected locally and never escalated to the manufacturer may not appear in MAUDE.

## PaceSafe is not Abbott AutoCapture

Boston's PaceSafe RAAT/RVAT performs automatic threshold testing and adjusts output based on measured thresholds.

Important architectural differences:
- RAAT does not provide beat-to-beat capture verification or backup atrial pacing.
- RVAT performs automatic threshold measurement and can provide backup pacing during commanded threshold testing.
- Tests can suspend, retry or fail because of low evoked response, noise, fusion/competing rhythm, high thresholds or other conditions.
- Therefore many MAUDE PaceSafe mentions represent the algorithm detecting or reacting to a lead/patient problem rather than causing one.

## Raw MAUDE burden

Across 44,366 ACCOLADE-family MDR keys screened from 2015 through current 2026, 623 MDRs contained explicit PaceSafe / RAAT / RVAT / automatic-threshold language (~1.4% of already-reported family MDRs).

This is not an incidence rate and cannot be compared directly with Abbott AutoCapture because manufacturer narrative conventions, installed base, device age and reporting behavior differ.

Yearly PaceSafe mentions:
- 2015: 0 / 3 family MDRs
- 2016: 0 / 10
- 2017: 0 / 17
- 2018: 3 / 390
- 2019: 20 / 2,384
- 2020: 31 / 3,021
- 2021: 34 / 3,861
- 2022: 38 / 4,522
- 2023: 118 / 4,513
- 2024: 142 / 5,091
- 2025: 144 / 7,729
- 2026 current: 93 / 12,825 (92 exact-narrative groups)

The rise in recent years should not be interpreted as worsening incidence.

## High-recall phenotype classes

Automated triage frequently identifies:
- automatic threshold test / clinical interaction,
- test suspension or retry,
- evoked-response / threshold diagnostic interaction,
- output/longevity changes,
- and clinical events occurring while automatic threshold testing is mentioned.

Manual review shows many are secondary to lead abnormalities or changing capture thresholds rather than primary PaceSafe malfunction.

## Recurring genuine algorithm-behavior phenotypes

### 1. False or unstable loss-of-capture classification

Examples include:
- myopotential/noise on the atrial evoked-response channel producing a positive signal during paced events and causing RAAT to declare loss of capture despite otherwise stable threshold/impedance;
- RVAT/RAAT threshold estimates substantially higher than manual measurements, with fusion, low-amplitude evoked response or competing rhythm identified as contributors.

These are measurement/decision limitations rather than hardware failure.

### 2. Automatic-test suspension / retry

PaceSafe may suspend or repeatedly retry when it cannot obtain a valid evoked response or when thresholds exceed programmed conditions.

This is often appropriate algorithm behavior, but it can leave:
- less useful automatic-threshold data,
- high fixed outputs,
- or delayed alerts/escalation.

A current ACCOLADE case documents that an RVAT-related alert is generated only after repeated failed tests over several days, illustrating alert-latency semantics rather than instantaneous loss-of-capture protection.

### 3. Threshold-test / clinical interaction

A small set of reports describe intermittent loss of capture, bradycardia, pacing inhibition or symptoms occurring during/around automatic threshold testing.

Causality is often difficult because the same patients may already have high/variable thresholds, electrolyte changes, lead noise or true lead dysfunction.

Examples worth retaining include:
- 2019 ACCOLADE hospitalization with syncope/asystole in which engineers investigated whether RVAT suspension/timing related to the event, without definitive causal proof;
- 2026 ESSENTIO intermittent ventricular loss of capture observed during an RVAT test, leading to programming changes;
- 2026 PROPONENT atrial loss of capture during RAAT testing;
- 2026 ACCOLADE loss of synchrony/syncope temporally associated with a stored RVAT event, with causality unresolved.

### 4. Diagnostic-data interaction

Several narratives describe automatic threshold retries/tests affecting stored episode duration, trends or clinician interpretation rather than directly compromising pacing.

## Broader ACCOLADE algorithm risks

PaceSafe is not the only or necessarily the most clinically important algorithmic workstream.

### RYTHMIQ

Published and MAUDE cases describe clinically important edge cases when intrinsic AV conduction deteriorates:
- asynchronous VVI backup pacing,
- blanking-related functional undersensing,
- R-on-T pacing,
- and ventricular arrhythmia in a published case.

This appears more compelling for targeted algorithm-safety surveillance than PaceSafe alone.

### Safety Mode / SMR software

Separate from PaceSafe, Boston Scientific's high-battery-impedance ACCOLADE issue evolved into a major Safety Mode/software-management problem. FDA's March 2026 correction covers all ACCOLADE-family pacemakers/CRT-Ps and addresses software behavior around battery-impedance testing and ZIP telemetry. FDA reported four deaths and 2,557 serious injuries associated with the overall issue as of March 18, 2026.

Do not conflate this with automatic-threshold behavior.

## Bottom line

Boston ACCOLADE has real algorithmic edge cases, but PaceSafe MAUDE mentions are mostly **algorithm-as-observer/tester** rather than proof that the automatic threshold algorithm itself is defective.

The more defensible hierarchy is:

1. common: automatic-threshold irregularity/suspension/high output while another lead/threshold issue is present;
2. less common: false loss-of-capture classification or inaccurate automatic threshold measurement;
3. uncommon but clinically important: threshold-test/algorithm timing plausibly associated with loss of capture, pacing inhibition or symptoms;
4. separate higher-concern algorithm workstream: RYTHMIQ timing/blanking interactions;
5. separate formal safety issue: ACCOLADE Safety Mode / battery-impedance software corrections.
