# Boston connector-port crosswalk and interpretation guardrail

The Boston Scientific spring-contact/fretting workstream is a useful proof-of-concept for engineering-to-clinical linkage, but it must **not** be treated as evidence of a general DF4 connector problem.

FDA's September 2019 modification specifically describes the **IS-1 lead-bore cavity and spring coil in the pulse-generator header**.

Many reviewed ICD/CRT-D generators contain both:
- an RA IS-1 port, and
- an RV DF4 port.

The clinically reported spring-contact event must therefore be mapped to the affected channel before assigning connector standard.

Examples:
- DYNAGEN D152 has RA IS-1 + RV DF4. Reviewed 2021 D152 spring-contact cases are explicitly **RA** events, so they belong to the IS-1 workstream.
- DYNAGEN G158 has RA IS-1 + RV DF4 + LV IS4. Reviewed spring-contact cases are again predominantly RA events.
- DYNAGEN G156 has RA IS-1 + RV IS-1/DF-1 + LV IS4; a 2022 RV event explicitly stated the device lacked the enhanced header.

The separate DF1-vs-DF4 ageing hypothesis remains open and should use only events localized to the relevant RV high-voltage connector system.
