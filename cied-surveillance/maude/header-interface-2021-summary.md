# 2021 header-interface calibration summary

The 2021 FDA MAUDE pull completed successfully:
- 5,283 candidate device rows,
- 5,280 unique MDR keys,
- 4,391 exact-narrative event groups.

After exact-text deduplication:
- 283 event groups contain spring-contact language,
- 195 of those contain high-impedance language,
- 25 contain Lead Safety Switch / safety-switch language,
- 48 explicitly mention a non-Boston / other-manufacturer lead,
- 201 contain 2020 design-enhancement/enhanced-header language,
- 227 contain terminal-ring / fretting / microscopic-particle / oxidation language.

These categories overlap.

## Strong calibration examples

### Provoked header phenomenon
INOGEN X4 CRT-D G148: the physician pressed on the generator header and reproduced MV oversensing together with an impedance increase. A competitor atrial lead was present and an enhanced-header generator was discussed as a future option.

### Enhanced-header negative control
An INGEVITY+ 7841 lead triggered >3000-ohm impedance and Lead Safety Switch, but the generator was documented as already having the enhanced header. The event was later localized to visible lead insulation damage at the original suture site.

### Clinical consequence
A MOMENTUM CRT-D event combined intermittent-impedance/MV oversensing with inappropriate mode switching and pacing inhibition exceeding two seconds; a non-Boston atrial lead was present.

### Very-old-lead control
One ESSENTIO system used competitor RA/RV leads reported as >20 years old. Spring contact was considered, but chest imaging reportedly ruled out a header issue. This is directly relevant to the original question about very-late lead/connector ageing and should remain a separate control phenotype.

## Interpretation

2021 gives us evidence in both directions:
- field behavior that can be physically provoked at the header,
- and high-impedance/LSS events in enhanced-header systems where another lead failure is ultimately demonstrated.

That makes header-generation status useful as an adjudication feature rather than merely a manufacturer-era label.
