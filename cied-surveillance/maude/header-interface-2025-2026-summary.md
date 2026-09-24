# MAUDE header-interface 2025–2026 calibration summary

Generated from the public FDA MAUDE bulk files on 2026-09-24.

This is a **candidate corpus**, not a failure-rate estimate.

## Pull size

| Period | CIED MDR keys before narrative filter | Candidate MDR rows | Exact narrative event groups |
|---|---:|---:|---:|
| 2025 | 95,020 | 5,232 | 4,006 |
| 2026 current file | 119,529 | 2,039 | 1,722 |
| Combined | — | 7,271 | 5,697 |

Across the combined artifact:
- 2,061 MDR rows sit inside exact-narrative duplicate groups.
- 487 exact-narrative groups contain more than one MDR row.
- 31 exact narrative hashes appear in both period partitions.

Therefore MDR row count is not an acceptable proxy for number of clinical/device events.

## High-recall narrative terms after exact-text deduplication

| Term | 2025 event groups | 2026 current event groups |
|---|---:|---:|
| header | 2,012 | 733 |
| setscrew | 1,081 | 551 |
| ingress / contamination | 679 | 227 |
| reseat / reconnect | 497 | 268 |
| spring contact | 252 | 96 |
| terminal pin | 235 | 50 |
| crosstalk | 230 | 155 |
| generic current leakage | 121 | 10 |
| connector bore | 110 | 45 |
| under-insertion | 86 | 48 |
| lead pin | 79 | 28 |
| intermittent connection/contact | 58 | 20 |

These terms overlap. They are triage signals, not mutually exclusive mechanisms.

## Important false-positive lesson: "inter-contact short"

The v0.9 rule surfaced 11 high-priority 2025 records as possible physical inter-contact shorts. Manual review found that all 11 were **not** demonstrated DF4/header cross-contact failures.

Examples included:
- internal ring-electrode-to-RV-conductor shorts caused by insulation abrasion beneath a shock coil,
- ring-to-coil impedance drops consistent with lead-body insulation breach,
- a near-connector IS-1 construction fault causing inner-to-outer-coil shorting.

The rule has therefore been tightened so `ring electrode` or generic conductor-to-conductor shorting no longer qualifies. A high-priority physical connector short now requires explicit connector-contact / terminal-ring / pole localization, conductive bridging, or connector-localized current leakage.

**Current result:** this first two-period screen has not yet produced a convincingly described physical current leak/short *between DF4 header contact regions*. That is a negative search result, not evidence that the phenomenon cannot occur.

## What the narratives do capture well

The corpus contains highly specific proximal-interface mechanisms that would be lost in a simple "fracture / high impedance / noise" analysis, including:
- incomplete terminal-pin seating,
- lead retention/contact abnormalities despite normal analyzer testing,
- spring-contact displacement,
- setscrew/torque-driver/septum failures,
- blood or tissue adhesion inside connector bores,
- device-specific abnormal impedance that resolves with another generator,
- internal header electrical discontinuities,
- explicit interface rule-outs where returned-product analysis instead confirms near-terminal or lead-body failure.

See `header-interface-adjudication-v1.csv` for the manually reviewed calibration set.

## Ageing cohort

Do not use all interface candidates for the DF1-vs-DF4 ageing question.

The primary ageing cohort is restricted to events arising after prior successful service where evidence localizes to the proximal connection system and does not better fit:
- implant technique,
- procedural setscrew damage,
- residual-blood contamination,
- lead-body fracture/abrasion,
- generator package/hermetic failure,
- or signal-only oversensing.

Generator-change fit/compatibility events remain valuable but form a separate cohort.

## MAUDE limitation

FDA MDRs are suitable for signal discovery and failure-phenotype research. They do not provide a reliable exposure denominator, reporting completeness, or causal verification sufficient to calculate incidence or comparative safety. Manufacturer performance/exposure data must remain a separate layer.
