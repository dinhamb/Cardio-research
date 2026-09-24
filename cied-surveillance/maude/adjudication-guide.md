# Header-interface adjudication guide

## Unit of analysis

The primary unit is a **clinical/device event**, not an MDR row.

MAUDE may generate multiple MDR keys for the same event when a generator and lead are each reported. Exact normalized narrative hashing in the pipeline is used as an initial duplicate detector; manual clustering can override it.

## Core adjudication states

- `CONFIRMED_INTERFACE_RETURNED_PRODUCT` — manufacturer/returned-product analysis directly confirms an interface mechanism.
- `CONFIRMED_INTERFACE_CLINICAL` — direct operative/clinical inspection confirms the interface mechanism.
- `CONFIRMED_INTERFACE_IMAGING` — imaging confirms connector/terminal malposition.
- `PROBABLE_INTERFACE` — evidence strongly localizes to the interface but no definitive returned-product or visual root cause is available.
- `INTERFACE_RULED_OUT_CLINICAL` — interface was specifically examined and evidence points elsewhere.
- `INTERFACE_RULED_OUT_RETURNED_PRODUCT` — returned-product analysis confirms another mechanism.
- `INTERFACE_NOT_CONFIRMED` — interface is in the differential but evidence does not support it.
- `CONFIRMED_CONTAMINATION_NOT_FAILURE` — connector contamination is present but no clinically relevant connector malfunction is demonstrated.
- `MIXED_EVENT_SECONDARY_INTERFACE_PROBLEM` — an interface issue occurred during management of another problem and must not be back-attributed to the original presentation.

## Mechanism families

Keep these separate:

1. lead terminal seating/retention,
2. terminal-to-header electrical contact,
3. spring contact displacement/fretting,
4. setscrew / torque-driver / septum problems,
5. connector-bore contamination or adhesion,
6. seal/ingress failure,
7. generator-header internal electrical path,
8. header-to-case/feedthrough/hermetic failure,
9. lead-body or near-terminal mimics,
10. signal-only/crosstalk without physical proof.

## Counting rule

For future summaries report at least:

- MDR rows,
- exact-narrative event groups,
- manually adjudicated unique events,
- confirmed interface events,
- probable interface events,
- interface mimics/rule-outs,
- procedure-associated interface events,
- spontaneous/late interface events.

Do not combine procedure-associated implant problems with late spontaneous connector ageing when testing DF1/DF4 material or seal hypotheses.

## Current seed

`header-interface-adjudication-v1.csv` contains the first 25 manually reviewed 2026 event groups. It is a calibration set, not a prevalence estimate.


## Duplicate hierarchy

Exact normalized narrative hashes are only the first deduplication layer.

A single clinical event may generate separate MDRs for the generator and lead with similar but non-identical wording. The 2025 calibration contains clear examples:
- DYNAGEN X4 generator MDR + CapSureFix Novus lead MDR describing the same year-long high-impedance/suspected spring-contact episode.
- paired generator/lead MDRs describing the same ~16-month intermittent impedance/threshold episode.

Therefore final event counts should use:
1. exact narrative hash,
2. device/date/clinical-pattern candidate clustering,
3. manual adjudication for high-value cohorts.

Do not assume one MDR key or one exact-text hash equals one clinical event.
