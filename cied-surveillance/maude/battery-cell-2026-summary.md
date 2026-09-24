# 2026 battery cell-mechanism adjudication

Calibrated against the FDA MAUDE current-year bulk artifact on 2026-09-24.

This file deliberately separates **battery-cell mechanisms** from generic premature depletion, generator current drain, capacitor behaviour, telemetry/firmware effects and generator-package failures.

## Candidate filter result

The original high-recall battery pilot produced:
- 44 cell-mechanism MDR rows,
- 109 apparent battery-interconnect rows,
- 1,898 generator-load rows,
- 1,101 depletion-phenotype-only rows.

After tightening the interconnect rule, **all 109 apparent interconnect candidates disappeared** from the priority bucket. They were overwhelmingly laboratory phrases such as disconnecting/removing the battery from the electronic module for analysis, not field interconnect failures.

The corrected current-year pull therefore has:
- 44 cell-mechanism MDR rows,
- 0 high-specificity battery-interconnect candidates,
- 1,913 generator-load candidates,
- 1,124 depletion-phenotype-only candidates.

## Manual cell adjudication

The 44 MDR rows collapse to **42 exact-narrative event groups**.

Adjudication status:
- **33 confirmed cell mechanisms**
- **6 probable cell mechanisms**
- **2 probable cell-internal shorts based on device data without returned-cell confirmation**
- **1 mechanism ruled out**: lithium plating was present on destructive analysis but explicitly judged not to affect battery performance.

Mechanism distribution in the 42 groups:
- 12 lithium-plating shorts
- 7 lithium-cluster shorts
- 7 internal shorts without a more specific resolved mechanism
- 6 internal-insulation-damage shorts
- 4 latent anode–cathode leakage events
- 3 internal-self-depletion events without more specific mechanism
- 1 copper-dendrite separator-breach short
- 1 lithium-cluster + silver-contamination event
- 1 incidental/non-causal lithium-plating finding

## Manufacturer-pattern signal

This is **not incidence** and must not be compared as raw rates. It is a useful engineering phenotype map:

- **Medtronic current-year high-specificity cell cases** in this calibration are dominated by plated-lithium internal shorts across Visia/Evera/Claria/Viva families.
- **Abbott / legacy St Jude** cases are dominated by lithium-cluster mechanisms in Fortify Assura-era advisory products, with one current Plus and one Quadra Assura event.
- **Boston Scientific** includes latent anode–cathode leakage, probable internal-short behaviour, and one copper-dendrite separator-breach case.
- **Biotronik** includes internal insulation damage, internal short/self-depletion, and one case where lithium plating was explicitly present but non-causal.

The next valuable step is to join these event phenotypes to exact battery supplier/cell model/chemistry and production generation where the engineering spine supports that join.

## Guardrails

- One MAUDE MDR is not one unique clinical event; duplicate report keys are collapsed where exact narratives match.
- Manufacturer analysis can support a mechanism but does not create an exposure denominator.
- Presence of lithium plating does not automatically mean the plating caused depletion.
- Generic battery depletion remains phenotype-only until a mechanism is demonstrated.
