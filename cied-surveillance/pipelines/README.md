# Pipelines

This directory will hold reproducible ingestion and transformation code.

Planned stages:

1. `product_identity` — manufacturer / family / exact model normalization.
2. `engineering_sources` — extract sourced engineering attributes and component links.
3. `maude_ingest` — obtain relevant FDA MAUDE/openFDA records without committing bulk raw files.
4. `maude_normalize` — normalize manufacturer/model/product identity and FDA problem terms.
5. `failure_adjudication` — classify mechanism, manifestation, consequence and manufacturer finding while preserving raw text.
6. `performance_reports` — parse manufacturer product-performance denominators/survival observations.
7. `analysis` — bounded analyses stratified by product generation, design feature and implant age.

## Reproducibility requirements

Every pipeline output should record:

- upstream source identifier
- retrieval date
- source/raw hash where practical
- parser/ingest version
- classification version
- explicit missing/unknown state

Do not infer a negative finding from absence of a report.
