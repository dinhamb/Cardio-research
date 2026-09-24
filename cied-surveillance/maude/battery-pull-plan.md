# Targeted MAUDE pull: generator battery and power-path mechanisms

## Question

Among pacemaker, ICD and CRT generator reports, what engineering mechanism is actually supported when a device presents with premature depletion, abrupt loss of power, inability to interrogate, or abnormal longevity?

The primary outcome is **mechanism**, not the phrase "premature battery depletion".

## Mechanism layers

1. **Cell internal**
   - internal short
   - lithium cluster / bridging
   - lithium plating
   - latent anode-cathode leakage path
   - separator/electrode-barrier problem
   - cell seal/electrolyte problem

2. **Battery package**
   - battery header
   - battery feedthrough
   - cell seal / hermeticity

3. **Battery-to-electronics interconnect**
   - terminal pin/post corrosion
   - spring connector/contact
   - weld/interconnect/open connection

4. **Generator electronics / load**
   - abnormal current drain or current consumption
   - capacitor charging/reforming
   - telemetry/communications
   - firmware/software behaviour

5. **Generator package adjacent**
   - generator feedthrough
   - can/package hermetic breach
   - fluid ingress causing secondary power loss

6. **Phenotype only**
   - premature depletion / rapid depletion / unexpected longevity change with no root cause demonstrated

## Narrative candidate terms

Cell-specific:
- lithium cluster / lithium bridge
- lithium plating / lithium re-plating
- internal battery short / internal short
- anode / cathode leakage
- leakage path within battery
- internal self-depletion
- separator / electrode barrier

Package/interconnect:
- battery header
- battery feedthrough
- battery terminal pin / battery post
- corroded terminal
- spring connector/contact
- battery-to-hybrid / battery-to-electronics
- open connection at battery

Load/electronics:
- abnormal current drain
- current consumption
- capacitor charging / capacitor reform
- telemetry drain
- firmware / software battery drain

Phenotype:
- premature battery depletion
- rapid battery depletion
- accelerated depletion
- unexpected battery depletion
- battery depleted earlier than expected
- abrupt battery depletion

## Adjudication

- `CONFIRMED_CELL_MECHANISM`
- `CONFIRMED_BATTERY_PACKAGE`
- `CONFIRMED_BATTERY_INTERCONNECT`
- `CONFIRMED_ELECTRONIC_LOAD`
- `PROBABLE_MECHANISM`
- `DEPLETION_PHENOTYPE_ONLY`
- `MECHANISM_RULED_OUT`
- `UNRESOLVED`

Manufacturer analysis may support a mechanism; a reporter's suspicion alone does not confirm one.

## Component join

Join a mechanism to battery supplier/cell model only when exact device family/model and production era are sourced in `engineering/battery-component-lineage.csv` or another primary engineering source.

Never infer:
- supplier from manufacturer,
- supplier from chemistry,
- cell failure from depletion phenotype,
- common root cause merely because two products share a supplier.

## Counting

As with header analysis, report:
- MDR rows,
- deduplicated narrative event groups,
- adjudicated unique events,
- returned-product-confirmed mechanisms,
- phenotype-only events.

MAUDE counts are not incidence denominators.
