# Targeted MAUDE pull: proximal lead–header interface

## Question

How many CIED adverse-event reports contain evidence specifically localizing a problem to the **lead terminal ↔ generator header interface**, rather than merely showing fracture, high impedance, noise, or oversensing?

## Why narratives are mandatory

FDA downloadable MAUDE data separates device/model records, structured device-problem codes, and MEDWATCH B5/H3/H10 narrative text, all linked by MDR Report Key. Structured codes such as high impedance or fracture are useful candidate filters but do not identify the anatomical/electrical root cause reliably.

## Candidate query layers

### Structured-code candidate layer
Prioritize records containing one or more of:
- Loose or Intermittent Connection (1371)
- Misconnection (1399)
- Connection Problem (2900)
- Electrical Shorting (2926)
- Difficult to Insert (1316)
- Fitting Problem (2183)
- Signal Artifact/Noise (1036)
- High impedance (1291)
- Over-Sensing (1438)
- Failure to Capture (1081)

Do **not** require any one code.

### Narrative candidate layer
Search event + manufacturer narratives for:
- header
- connector block / connector bore / connector port
- terminal pin / lead pin
- set screw / setscrew
- spring contact
- incomplete insertion / under-insertion / not fully inserted
- re-seat / reseat / reinsert / reconnect / detach and re-attach
- fluid / blood / moisture / contamination / ingress / seal
- cross-contact / conductive bridge / leakage / short
- crosstalk / cross-talk

Crosstalk is a candidate term only. It must not be treated as proof of physical inter-contact current leakage.

## Adjudication states

- CONFIRMED_INTERFACE: returned-product, imaging, direct visual/procedural or manufacturer analysis confirms interface mechanism.
- PROBABLE_INTERFACE: correction by reseating/reconnecting or highly specific evidence strongly supports interface origin.
- SUSPECTED_INTERFACE: interface explicitly proposed but not demonstrated.
- INTERFACE_RULED_OUT: header/interface evaluated and a different cause confirmed.
- SIGNAL_ONLY: electrical manifestation such as crosstalk/noise with no physical interface evidence.
- GENERATOR_HEADER_NONLEAD: failure is within generator header but not lead-contact interface.
- UNRESOLVED.

## Core output fields

MDR key; manufacturer; exact model; connector standard; event date; implant/manufacture date; calculated implant age where possible; structured problem codes; narrative; suspected/confirmed location; mechanism; electrical manifestation; clinical consequence; intervention; returned-product status; manufacturer finding; adjudication state; confidence.

## Count to report

The primary count is **not** all reports with high impedance/noise/fracture.

Report:
1. number of candidate MDRs,
2. number narratively reviewed,
3. confirmed interface,
4. probable interface,
5. suspected interface,
6. ruled-out interface mimics,
7. signal-only/crosstalk-without-physical-proof,
8. generator-header non-lead failures,
9. unresolved.

Then stratify confirmed + probable interface events by DF1/DF4, model family and implant age.

## Denominator warning

MAUDE supplies a numerator-like signal corpus, not an incidence denominator. Manufacturer performance reports or other exposure datasets must be joined separately before any rate comparison.


## Pilot filter lesson — 2026-09-24

The first current-year bulk pilot showed that the phrase `current leakage` by itself is **not** specific for the lead-header interface. Strong false positives included:

- battery-internal anode/cathode leakage with lithium re-plating,
- generator feedthrough leakage,
- high-voltage capacitor leakage,
- narratives explicitly documenting *no* current leakage.

The pipeline therefore requires connector-localised language near leakage/short terms for the highest-priority physical cross-contact bucket. Generic current-leakage narratives are diverted to a non-interface bucket.

Conversely, the broad narrative layer contains highly specific lead-header events that structured codes alone would not distinguish, including incomplete lead-pin seating, displaced connector spring contacts, setscrew/header failures, connector-bore obstruction, and blood/moisture within connector ports.
