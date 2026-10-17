# Section 04 — Accuracy Guardrails / What to Verify

## Distinguish the three reference layers

1. **Approved cinematic choice:** the specific user-selected generated image composition (separated in this package).
2. **Mechanical/engineering reference:** MIT datasheet, accepted mechanism logic, client corrections and verified CAD.
3. **Final animation:** must reconcile both layers in a coherent, testable 3D scene. Do not use image-generation artifacts as ground-truth geometry.

## Before 3D storyboard lock

- Verify actual ENP3 imaging-sensor faces and their common axial plane (three sensors at 120° intervals per brochure), instead of guessing from the generated tool shape.
- Verify casing size and tool clearance (datasheet: 12-inch maximum tool OD; 12.3-inch minimum casing internal diameter).
- Check position of the existing casing shoe versus the deeper open hole, and confirm the upward BHA retrieval/scan representation.
- Confirm from MIT how the cased-hole ringing comparison should be illustrated and whether the simplified waveforms accurately communicate relative decay.
- Confirm whether blue in cement evaluation is an explicitly classified water-filled region or a broader fluid/weak-support acoustic response. Do not overclaim a precise material identity from coloration alone.
- Keep cement on the OUTSIDE of the casing, in the annular sheath between steel and rock; one axial fluid region may occur along one side.
- For casing integrity, keep groove on the INNER casing wall. Relate it to local measured internal radius, not generic exterior corrosion. If quantitative casing metal loss is claimed, verify how it is inferred from data.

## Image-specific warnings

**A:** Image makes casing-shoe architecture attractive, but may not use exact CAD/BHA dimensions. In upward retrieval, ECCO is uphole of the bit and reaches casing before the bit.

**B:** The two waveform displays are a visual comparison of fast and slower decay. Do not copy numerical curves, color semantics or depicted transducer geometry literally; do not imply visible sound through steel.

**C:** The blue channel resembles a moving fluid stream. Treat it as a *revealed fluid-filled / cement-free region* unless fluid-flow evidence is supplied. Keep only on one azimuthal side of the casing sheath.

**D:** The reference groove is quite deep/blocky. Refine to a believable wear scar consistent with MIT's description of local metal loss and increased internal radius. Outer diameter stays unchanged in this explanatory comparison.

## Handoff status

Only Step 1 direction is approved as the selected option. Atomic keyframe designs, 3D blocking and engineering proof remain to be completed; render approval must not be inferred.
