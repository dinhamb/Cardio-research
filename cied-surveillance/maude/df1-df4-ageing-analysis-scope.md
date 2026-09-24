# DF1/DF4 late-age interface analysis scope

The broad MAUDE header-interface corpus is **not** the ageing cohort.

## Primary late-age cohort

Include an event only when all of the following are reasonably supported:

1. the lead–generator connection had previously functioned after implantation;
2. the abnormality arose during in-service follow-up or after a period of successful service;
3. evidence localizes the problem to the proximal connector/header system, or the interface is the leading unresolved mechanism after lead-body testing;
4. the event is not better explained by implant technique, a stripped/incorrectly operated setscrew, residual blood on the terminal at implant, lead-body fracture, generator-package hermetic failure, or signal-only oversensing;
5. connector standard and product family can be resolved sufficiently for stratification.

Examples in the v1 calibration set:
- **EVT2026-016** — high relevance: chronic Sprint Quattro DF4, reproducible noise/impedance change with pocket manipulation, lead normal on analyzer, abnormal retention/contact behaviour at header, replacement generator normal.
- **EVT2026-017** — high-value negative control: chronic Sprint Quattro DF4 with high impedance, but direct push/pull inspection found the header connection fully seated and stable; generator retained.

## Secondary compatibility / generator-change cohort

Keep separately when a chronic lead will not seat, release, or make normal electrical contact in a replacement generator.

These cases may reveal:
- terminal dimensional change with ageing,
- seal-ring swelling/hardening,
- terminal-body deformation,
- manufacturer tolerance stack,
- generator-header bore/contact tolerance,
- cross-manufacturer compatibility issues.

They **cannot by themselves** demonstrate spontaneous in-vivo header failure because the problem is observed during a new connection procedure.

Examples:
- EVT2026-013
- EVT2026-014
- EVT2026-015
- EVT2026-021
- EVT2026-022
- EVT2026-023

## Procedure-associated cohort

Retain for engineering surveillance but exclude from the late-age numerator:

- incomplete pin seating at implant/revision,
- setscrew over-rotation or stripping,
- torque-driver/septum interference,
- setscrew left obstructing a bore,
- procedural lead dislodgement,
- contamination introduced during connection.

These events are useful for studying connector usability and failure tolerance, not polymer/seal ageing.

## Chronic contamination / adhesion cohort

Keep separate from spontaneous electrical failure.

Blood or tissue contamination can become clinically important years later by:
- bonding a chronic lead to the connector bore,
- calcifying within a setscrew cavity,
- preventing lead release at generator change.

This is a genuine long-term connector consequence, but if returned-product analysis attributes it to residual blood at the original implant it should not be counted as intrinsic seal/material degradation.

## Adjacent generator-header mechanisms

Retain but exclude from DF1-vs-DF4 lead-interface comparisons:
- internal header ribbon/setscrew-block opens,
- header-to-case bond failure,
- feedthrough damage,
- package hermetic breach,
- antenna/header arc-over.

## Required reporting

For any DF1/DF4 comparison report separately:
- total MDR rows,
- deduplicated event groups,
- manually adjudicated unique events,
- primary late-age interface events,
- generator-change compatibility events,
- procedure-associated interface events,
- chronic contamination/adhesion events,
- interface mimics/rule-outs,
- signal-only/crosstalk events.

Do not combine these into one "header failure rate."
