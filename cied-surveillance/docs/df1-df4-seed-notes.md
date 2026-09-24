# DF1 → DF4 engineering seed

Seeded: 2026-09-24

## Purpose

Create a sourced engineering lineage before attaching MAUDE events. The aim is not to ask whether one manufacturer has "more failures"; it is to test whether connector/sealing/material architecture is associated with different **failure phenotypes**, particularly at long implant age.

## First four manufacturer lineages

| Manufacturer | DF1 control | DF4 successor | Pair quality | Important current finding |
|---|---|---|---|---|
| Biotronik | Linoxsmart | Protego | **Very strong** | FDA says the distal lead is unchanged; principal changes are DF4 connector + transition. Protego DF4 terminal insulator is explicitly labelled **PEEK 450G**. |
| Medtronic | Sprint Quattro 6935 / 6947 | 6935M / 6947M | **Strong / very strong** | Exact 6935M Medtronic manual specifies **PEEK in the sealing zone**; FDA says 6947M is identical to 6947 except the proximal four-pole connector. |
| Abbott | Durata 7122 | 7122Q | **Strong family match** | Same Durata single-coil active-fixation family and Optim lead-body insulation. Production DF4 connector-body material remains unresolved. |
| Boston Scientific | ENDOTAK RELIANCE DF1 | ENDOTAK RELIANCE 4-Site | **Confounded** | 4-Site terminal molding is **polyurethane 75D**, but FDA also documents HV cable-conductor, proximal tubing and suture-sleeve changes. |

## Architecture hypothesis

DF1 and DF4 move the sealing burden to different sides of the interface:

- **DF1:** seal rings are lead-carried and remain implanted with the lead.
- **DF4:** seals between connector contacts are in the generator header and are therefore replaced with a generator change.

That makes very-late ageing a plausible natural experiment. It is a hypothesis, not evidence that DF1 or DF4 is safer.

## Material question

The user's recalled PEEK-versus-softer-polymer distinction now has stronger support:

- **Biotronik Protego:** PEEK 450G is explicitly labelled around the DF4 connector contacts in the FDA review.
- **Medtronic Sprint Quattro 6935M:** the exact Medtronic technical manual states **seal zone: PEEK**. Official Japanese PMDA labeling independently lists PEEK among 6935M materials. FDA's original DF4 master review says the seal-zone material was a new tissue-contacting material, but redacts its identity.
- **Boston ENDOTAK RELIANCE 4-Site:** terminal molding is specified as **polyurethane 75D** in the manufacturer manual.
- **Abbott Durata DF4:** production material remains unresolved. A 2009-priority Pacesetter/St Jude patent for IS4/DF4 connector construction lists **Tecothane, PEEK or polysulfone** as possible connector-body polymers, so the patent cannot be used to put Durata in a "soft polymer" bucket.

This means the initial remembered split is only partly right: **Biotronik and Medtronic can now be placed in the PEEK group with useful evidence; Boston is clearly polyurethane; Abbott remains unknown.**

## Medtronic-specific design note

The FDA master review is unusually useful for matching:
- DF4 connector bore contains the sealing rings and contacts.
- 6947M is described as identical to 6947 except for the proximal four-pole connector.
- FDA records connector-ring manufacturing changes after corrosion-related bench failures during tensile testing.
- FDA states the new lead material creating the seal with the header was the only DF4-system material not identical to predecessor materials, but the material name is redacted in the public memo.

These details make Medtronic a strong second natural experiment after Biotronik.

## Analysis guardrails

1. Keep engineering attributes independent from event classifications.
2. Do not infer material from manufacturer identity.
3. Do not treat a MAUDE narrative as proof of root cause unless a returned-product/manufacturer analysis supports it.
4. Do not calculate comparative incidence from MAUDE counts alone.
5. Stratify by implant age and product generation before interpreting any apparent difference.
6. Preserve matched-pair quality. Boston RELIANCE 4-Site is not a connector-only conversion.
7. Treat missing material data as `UNRESOLVED`, not "other".
8. Patent "may comprise" material lists are candidate design evidence, not proof of production composition.

## Next work

1. Keep searching for product-specific Abbott SJ4/Durata connector material.
2. Expand exact model/variant crosswalks for each seed family.
3. Add generator-header construction and contact/seal materials matched to each lead family.
4. Add manufacturer product-performance denominators and confirmed-malfunction categories.
5. Only then pull a bounded MAUDE sample focused on proximal connector/header/seal phenomena.
