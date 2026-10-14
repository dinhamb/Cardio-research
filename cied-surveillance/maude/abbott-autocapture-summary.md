# Abbott AutoCapture MAUDE surveillance summary

Scope: FDA MAUDE bulk files, 2010 through current 2026 bulk feed, Abbott/St Jude/Pacesetter pacemaker generators.

## Raw frequency

Across 225,387 Abbott/St Jude/Pacesetter pacemaker MDR keys screened, 887 MDRs contained explicit AutoCapture/capture-algorithm language (~0.39% of pacemaker MDRs).

This is **not an incidence rate**. MAUDE has no implanted-device denominator, reporting intensity varies by era/product, and manufacturers frequently mention AutoCapture while explaining normal battery depletion.

Approximate exact-narrative deduplication leaves 881 event groups.

## What the 887 mentions contain

High-recall automated classification across the 881 groups:
- 32 explicit algorithm/capture-failure language
- 47 capture events with reprogramming
- 55 capture-event AutoCapture mentions
- 416 longevity reports where depletion/anomaly was normal or not confirmed
- 149 longevity/high-output reports
- 182 other AutoCapture mentions

These automated classes are candidate strata only.

## Manual adjudication lesson

The 32 "explicit" flags substantially overestimate true algorithm-caused clinical failures. False/secondary examples include:
- lead noise or damaged leads causing loss of capture while AutoCapture was enabled;
- elevated thresholds, electrolyte disturbance, lead dislodgement or insulation failure;
- normal threshold-test behavior;
- duplicate generator and lead MDRs for one clinical event.

Nevertheless, a recurrent, real algorithm-behavior phenotype remains.

### High-confidence / strong-probability phenotypes observed

1. **Failure to recognize true noncapture**
   - true ventricular loss of capture visible on EGM but no AutoCapture backup pulse;
   - normal/manual threshold measurements can subsequently look satisfactory;
   - fixed-output programming resolves the issue in several reports.

2. **False noncapture detection / inappropriate backup pulse**
   - AutoCapture interprets a captured/fused beat as noncapture and delivers the 5 V backup pulse;
   - several reports associate the closely coupled backup pulse with short ventricular tachycardia episodes.

3. **Capture-threshold-test interaction**
   - loss of capture or symptomatic bradycardia during automatic/related capture testing;
   - at least one 2022 Abbott Technical Services review explicitly confirms an event was due to the AutoCapture algorithm.

4. **High/unstable automatic thresholds**
   - algorithm drives output high or records out-of-range thresholds despite lower/manual thresholds;
   - usually a longevity/diagnostic issue rather than dangerous pacing failure.

## Modern-year candidate burden

Raw AutoCapture-mentioned MDRs:
- 2020: 83
- 2021: 82
- 2022: 114
- 2023: 89
- 2024: 55
- 2025: 72
- 2026 current: 42

Manual review of 2020-24 suggests the clinically interesting algorithm-related events are **a small minority** of these mentions, on the order of a few events per year, not dozens per year.

The strongest modern examples include:
- 2020: inappropriate backup pacing followed by VT; failure/difficulty recognizing loss of capture; symptoms resolving with reprogramming.
- 2021: true loss of capture not appropriately detected; recurrent false loss-of-capture classification; syncope/presyncope reports improved after AutoCapture/fixed-output reprogramming.
- 2022: loss of capture during AutoCapture/threshold testing, including an Abbott-reviewed event explicitly attributed to the algorithm.
- 2024: pacemaker-dependent Endurity cases where loss of capture occurred without expected backup pacing; one report explicitly states ineffective pacing was due to the AutoCapture algorithm and resolved with reprogramming.
- 2025-current: no cases met the automated strict "explicit algorithm-caused capture failure" phrase rule; most mentions are normal-longevity/high-output explanations.

## Context from clinical literature

AutoCapture abnormal threshold behavior is much more common than clinically dangerous algorithm failure. A 160-patient long-term series reported abnormal AutoCapture threshold patterns in 73/160 patients (45.6%), mostly threshold variability/out-of-range readings that can increase output and battery drain.

Conversely, modern Abbott AutoCapture experience in 619 LBBAP patients showed close agreement between automatic and manual thresholds in 97.6% and no clinical complications attributed to AutoCapture over roughly two years.

Therefore MAUDE should be interpreted as demonstrating **rare but recurrent edge-case behavior**, not evidence that AutoCapture is generally unsafe.

## Research conclusion

The interesting question is not "does AutoCapture fail often?"

The supported conclusion is:

> AutoCapture-related clinical edge cases recur over many product generations, but serious events appear uncommon relative to overall use. The recurring mechanisms are failure to recognize true noncapture, false loss-of-capture classification with backup pacing, and threshold-test interactions. The far more common abnormality is unstable/high automatic threshold behavior affecting output or longevity.

No MAUDE-derived incidence rate should be reported without an implanted-device exposure denominator.
