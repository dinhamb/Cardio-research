# Boston Scientific header / spring-contact lineage

## Executive summary

There **was** a formal Boston Scientific safety action related to the same broader lead-header interaction, but it was framed around **minute-ventilation (MV) signal oversensing and pacing inhibition**, not around transient high impedance / Lead Safety Switch as a standalone failure mode.

### 2017 formal action

Boston Scientific initiated a field action on 7 December 2017 and sent a physician letter on 19 December 2017 for ACCOLADE, ESSENTIO, PROPONENT, VALITUDE, VISIONIST and ALTRUA 2 pacemakers/CRT-Ps.

FDA later classified affected models under a **Class II recall**. Boston reported that MV-sensor oversensing was more likely when affected generators were connected to Medtronic or Abbott/St Jude pacing leads.

### Separate high-impedance / Lead Safety Switch phenomenon

The 2019 peer-reviewed hybrid-system report described a distinct but likely related phenomenon: transient high pacing impedance, Lead Safety Switch activation and apparent lead-fracture signals caused by lead-header interaction. The paper characterized this as an **unreported hazard**, not as the subject of a separate Boston recall.

### 2019 hardware modification

FDA PMA supplements approved on 18 September 2019 explicitly describe:

> hardware modifications to the IS-1 lead bore cavity and spring coil in the IS-1 pulse-generator header

for all pacemakers and CRT-Ps within the Accolade family and selected NG3/NG4 ICD/CRT-D families.

This provides a strong regulatory design boundary.

### 2020 implementation

Boston Scientific MAUDE manufacturer narratives from 2020 onward repeatedly state that:

- intermittent high impedance can arise from the spring-contact / lead-terminal-ring interface;
- repeated small terminal-ring movements, contact-force variation and surface roughness can contribute;
- later narratives describe wear particles accumulating/oxidizing;
- a **design enhancement was implemented in 2020** to stabilize the electrical connection.

The working interpretation is that the 2020 implementation corresponds to the hardware modification approved in September 2019. This is high-confidence but should remain explicitly sourced as an inference until a direct Boston manufacturing-change document or exact lot/serial transition is located.

## Research implication

The most useful exposure variable is not simply "Boston generator" or "DF4".

It is:

`header/contact generation -> pre/post 2019-2020 enhancement -> IS-1 vs DF4 contact -> lead manufacturer/model -> implant age -> intermittent-impedance / LSS phenotype`

The formal 2017 recall should be modelled separately as an **MV oversensing safety action** because it overlaps mechanistically but is not identical to the later high-impedance / spring-contact phenotype.
