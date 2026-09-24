# 2023 header-interface calibration summary

The 2023 FDA MAUDE bulk pull completed successfully:
- 8,018 candidate device rows,
- 8,006 unique MDR keys,
- 4,913 exact-narrative event groups.

After exact-text deduplication, 323 event groups contain spring-contact language.

Overlapping features in that stratum:
- 218 contain high-impedance language,
- 50 contain Lead Safety Switch / LSS language,
- 41 explicitly mention a non-Boston / other-manufacturer lead,
- 114 contain design-enhancement / enhanced-spring-contact / updated-header language.

These are triage counts, not confirmed failures.

## More specific engineering mechanism

The 2023 narratives add an important physical mechanism beyond generic spring contact.

Manufacturer engineering text states that repeated small movements of the lead terminal ring can wear the terminal surface and generate microscopic particles. Those particles may accumulate and oxidize over time, degrading the connection between the spring contact and lead terminal ring and producing intermittent impedance changes.

This is consistent with a fretting/contact-debris mechanism and is now represented in the taxonomy as HEADER_FRETTING_PARTICLE_OXIDATION.

## Why adjudication remains necessary

The same manufacturer boilerplate can appear in records later shown to have another cause. A 2023 ACCOLADE event in the seed was amended after imaging demonstrated lead fracture and dislodgement; that event is explicitly classified as INTERFACE_RULED_OUT_CLINICAL.

Therefore manufacturer mechanism text is useful for defining the engineering hypothesis but cannot be treated as proof that every matching MDR is a header failure.

## Direction

The 2023 and 2024 strata now justify a dedicated Boston contact-system workstream:
- resolve generator/header generation and 2020 design-revision boundary,
- map affected lead manufacturer/model and connector standard,
- distinguish IS-1 pace/sense versus DF4 high-voltage contact involvement,
- cluster cross-device duplicate MDRs more aggressively,
- compare pre/post-enhancement phenotype distributions without using MAUDE as an incidence denominator.
