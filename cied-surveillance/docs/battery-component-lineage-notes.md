# Battery component lineage notes

This table maps **specific historical device generations** to battery supplier, cell model, chemistry and capacity where a source supports the relationship.

It must not be used as a manufacturer-wide supplier map.

## Strong historical cross-manufacturer pattern

The 2003–2010 CRT-D cohort is useful because one source compiled battery specifications from device manuals across five manufacturers:

- Greatbatch cells appear in Boston Scientific, Sorin and St Jude families, and as alternate configurations in the listed Biotronik Lumax families.
- Biotronik also used Litronik cells; FDA independently documents Litronik model LiS 3150 in earlier Actros+/Kairos generators and later regulatory changes to Litronik battery materials.
- Boston Scientific's Cognis generation is listed with a Boston Scientific 401988 Li/MnO2 battery rather than Greatbatch.
- Medtronic families in the cohort are listed with Medtronic-labelled 161253 and 161455 Li/SVO cells.

This is precisely why battery surveillance should be component-centric: nominally competing generator brands can share a battery supplier or chemistry, while successive families from one manufacturer can change supplier/chemistry.

## Guardrails

- A supplier relationship in one generation is not evidence of the supplier in later generations.
- A cell model is not a failure mechanism.
- Similar chemistry across models is not proof of common construction.
- Manufacturer-labelled cells may still contain upstream supplier components; do not infer without sourcing.
- For families with two listed battery configurations, retain both until exact model/region/production-era mapping is found.
