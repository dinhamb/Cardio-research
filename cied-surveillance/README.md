# CIED Engineering Surveillance

Research workspace for joining cardiac implantable electronic device (CIED) engineering design, regulatory/product history, manufacturer performance data, recalls/advisories, and adverse-event reports.

## Core research questions

1. **Generator failure mechanisms**
   - battery supplier / cell family / chemistry
   - cell-internal failure mechanisms
   - battery header/feedthrough and battery-to-electronics interconnect
   - generator feedthrough design and hermeticity
   - can weld / package integrity
   - header construction, connector block and sealing
   - capacitor/electronics/telemetry/firmware-related current drain

2. **Lead and connector ageing**
   - DF-1 / IS-1 versus DF4 connector architecture
   - seal location (lead-carried versus header-carried)
   - terminal-body and inter-contact insulating materials
   - lead-terminal ↔ generator-header interface failures over implant age
   - conductor geometry/material
   - individual conductor insulation versus outer lead-body insulation
   - coaxial / multilumen / lumenless / stylet-driven architecture
   - fixation, diameter, shock-coil construction and design revisions

3. **Failure pathway**
   - engineering mechanism
   - electrical manifestation
   - how detected
   - symptoms/signs
   - clinical consequence
   - intervention
   - returned-product / manufacturer finding

## Evidence rule

A reported event is **not** evidence that an engineering attribute caused the event.

Engineering facts, adverse-event observations, manufacturer analysis, recalls/advisories, and inferred classifications are stored as separate layers with explicit provenance and confidence.

MAUDE is used for signal discovery and failure-phenotype research. It must **not** be used alone to estimate incidence, prevalence, comparative safety, or failure rates because exposure denominators and reporting completeness are inadequate.

## Layout

```
cied-surveillance/
  README.md
  schema/
  taxonomy/
  provenance/
  engineering/
  maude/
  pipelines/
  docs/
```

Local/reproducible bulk data belong under:

```
cied-surveillance/data-raw/
cied-surveillance/warehouse/
```

These paths are gitignored. Raw FDA bulk files, PDFs, DuckDB databases and Parquet extracts should not be committed.

## Initial bounded analyses

- DF-1 versus DF4 proximal connector/sealing failure phenotype by implant age.
- DF4 terminal-body / inter-contact material by manufacturer and generation.
- Lead-terminal ↔ generator-header interface events: under-insertion, intermittent contact, setscrew/spring-contact issues, seal ingress, inter-contact leakage/shorting, and mimics.
- Generator premature depletion split into cell-internal, battery header/feedthrough, battery interconnect, generator electronics/current-drain, capacitor and unknown mechanisms.
- Shared battery cell families across nominally different generator manufacturers/models.

## Data-quality states

Every nontrivial claim should carry source/provenance and confidence. Missing data stays missing.

Recommended confidence values:
- `CONFIRMED_PRIMARY`
- `CONFIRMED_SECONDARY`
- `HIGH_CONFIDENCE_INFERRED`
- `CANDIDATE`
- `UNRESOLVED`

## Privacy

Do not place identifiable patient information in this repository. Any future prospective clinical-encounter dataset must be handled as a separate governed dataset and must not be mixed into this public engineering/adverse-event warehouse.
