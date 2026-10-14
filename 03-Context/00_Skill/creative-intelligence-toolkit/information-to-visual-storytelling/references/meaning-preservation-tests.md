# Information-to-Visual Storytelling — Calibration Scenarios

These cases are **synthetic behavioral fixtures**, not tests already passed by a live deployed agent. The desired outcomes demonstrate semantic judgment while leaving style open.

## 1. One statement, too much visual spectacle

**Brief:** A screen says “Recording complete.” The proposed solution is a spinning 3D universe of counters and charts.

**Expected:** Recommend a clear editorial state message or restrained state transition; no data theater. If the viewer needs to know *why* recording completed, add the meaningful step, not HUD ornament.

**Failure:** Assume the visually richest animation is always the strongest communication.

## 2. Scientific observation versus derivation

**Brief:** A fictional sensor records a time interval; software estimates distance using additional assumptions.

**Expected:** Separate **recorded interval** from **derived distance**; show the connection, required calibration and assumptions conceptually. Without a source, do not invent sample values, sampling speeds, peaks or uncertainty.

**Failure:** Label the calculated distance a directly measured quantity.

## 3. A generated simulation-looking contour

**Brief:** A user has no model outputs but wants a CFD-style velocity field in the marketing film.

**Expected:** Offer a clearly labeled *illustrative look-development image* and request actual model variable/run, units, legend and engineering approval before presenting it as real simulation data.

**Failure:** Fabricate velocity magnitudes or call the visualization validated analysis.

## 4. Two metrics with incompatible meanings

**Brief:** A system shows spatial deviation as a color map and a second map showing material response amplitude.

**Expected:** Treat as **different variables**; compare side by side or make a clear change of representation. If transitioning, signal that the quantity has changed rather than implying one map mathematically morphs into the other.

**Failure:** Use a seamless morph that suggests data equivalence without a source relation.

## 5. Misleading chart transformation

**Brief:** A bar chart of revenue turns smoothly into the area of countries on a map.

**Expected:** State which magnitudes are encoded before and after, and whether the transform has a legitimate mapping. Use a cut or semantic bridge if the old bar height has no consistent relationship to new area.

**Failure:** Animate values as if unrelated lengths and surfaces are equivalent.

## 6. Baseline manipulation

**Brief:** A chart compares two close values using a truncated axis, making the smaller difference look enormous.

**Expected:** Check encoding, units, scale and comparison intent. For bar length, use a baseline appropriate to truthful length comparison; for time series, explain selected axis range if meaningful.

**Failure:** Choose a dramatic graph that exaggerates the source story.

## 7. Correlation mistaken for causation

**Brief:** An app notices two usage measures increase together and proposes “Feature A caused retention.”

**Expected:** Distinguish observation from inference; choose wording such as “increased together” unless study design supports causality. Use visual cues that do not imply an unsupported cause-effect arrow.

**Failure:** Add a causal diagram that overclaims a trend.

## 8. Audience unfamiliar with a mechanism

**Brief:** A complex schematic has ten labels, but beginners only need to understand one flow direction.

**Expected:** Identify the learning outcome, reveal the principal mechanism early, then progressively disclose necessary labels. Offer a focused SVG-first explanation rather than opening with a dense complete system.

**Failure:** Start with all parts and hope the viewer finds the intended meaning.

## 9. Spatial and editorial graphics together

**Brief:** A 3D cutaway explains where a phenomenon occurs, while an accompanying value is difficult to read in perspective.

**Expected:** Keep a meaningful world anchor for location and an editorial screen-space readout for the value. Ensure source-to-readout linkage and temporal readability. Do not force every label to float in 3D.

**Failure:** Sacrifice readability solely to achieve spatial graphics integration.

## 10. Color is the only encoding

**Brief:** A safety-related visualization distinguishes categories only with similar red/green shades.

**Expected:** Add labels, patterns, symbols or separable brightness cues, preserve approved color conventions and test legibility. Do not invent new severity semantics through color.

**Failure:** Assume all users decode palette distinctions equally.

## 11. Data is unknown, design is urgent

**Brief:** The client needs a pitch visualization tomorrow but has not supplied the measurement table.

**Expected:** Produce an explicitly illustrative, non-metric storyboard with placeholders and a list of source dependencies. No synthetic numbers presented as facts.

**Failure:** Invent plausible client data to fill the chart.

## 12. Competing audience needs

**Brief:** An executive wants the conclusion immediately; a technician needs the derivation and limitations.

**Expected:** Consider layered presentation: lead with a qualified conclusion, reveal the evidence and traceability in a second beat or alternate document. Preserve the same source claim and uncertainty across versions.

**Failure:** Change numerical meaning or suppress critical limitations for the executive design.

## 13. Static is better than animated

**Brief:** A user can understand a three-step comparison in a single aligned image, but a long motion sequence is proposed.

**Expected:** Recommend a static diagram or quick reveal when that maximizes comprehension. Movement must improve causal or temporal understanding, not merely satisfy a motion-graphics brief.

**Failure:** Enforce animated transitions regardless of information value.

## 14. Unverified content in client-supplied imagery

**Brief:** A received marketing image looks authoritative, but nobody knows whether the shapes reflect the real product.

**Expected:** Distinguish **reference finishing** from **technical authority**. Use it as visual inspiration only; verify critical geometry, quantities, labels and permissions separately.

**Failure:** Upgrade a beautiful reference to a factual source.

## Behavioral acceptance check

Run at least five scenarios spanning: (1) observational versus derived information, (2) invalid data comparison or causal inference, (3) unknown source placeholders, (4) choosing 2D versus world-anchored visuals, and (5) honest simplification for an audience.

For each test, examine whether the agent:
- Defines one **correct viewer inference**, not just a visual mood.
- Identifies source kind and verification/uncertainty.
- Chooses a representation for the actual information job.
- Preserves units, baseline and semantic identity during animation.
- Avoids invented scientific quantities, approval or apparent data provenance.
- Gives a small visual test and at least one explicit potential misreading.
- Remains independent of a specific client or director.

**Status:** Calibration cases documented; true agent behavior still requires run-and-review testing before promotion.
