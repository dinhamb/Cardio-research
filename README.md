# Cardio Research

Public research workspace for reproducible cardiac-device and cardiovascular research.

## Current workstreams

### CIED engineering surveillance

`cied-surveillance/` joins:
- device and lead engineering design,
- regulatory/product history,
- manufacturer performance data,
- recalls/advisories,
- FDA MAUDE adverse-event narratives,
- and explicit failure-mechanism adjudication.

The first bounded analyses focus on DF1/DF4 connector and header-interface ageing, and generator battery/power-path failure mechanisms.

## Important limitations

This repository is a research workspace, not a clinical decision-support system.

MAUDE is used for signal discovery and failure-phenotype research. MAUDE counts alone must not be interpreted as incidence, prevalence, comparative safety, or failure rates.

Do not commit identifiable patient information. Any prospective clinical-encounter research must use a separate governed dataset.

## Data storage

Raw FDA bulk downloads and analytical warehouses are intentionally excluded from git. Pipelines should be reproducible from public sources and should emit compact derived outputs only.
