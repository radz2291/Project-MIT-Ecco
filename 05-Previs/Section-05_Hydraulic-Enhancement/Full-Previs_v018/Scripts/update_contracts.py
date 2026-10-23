from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
common='''Owner's v018 production handoff releases the full 18-second low-cost S05 previs using approved v017. This controls older 12-second allocations, circulation-only choices and pending implementation gates below. Prior records remain historical; no final engineering or finished-film approval is claimed.

Current implementation: `05-Previs/Section-05_Hydraulic-Enhancement/Full-Previs_v018/Scenes/S05_full-cinematic_v018.blend`, one shared 432-frame timeline at 24 fps / 1280 x 720. Two motivated camera cuts at frames 121 and 289; all hydraulic regions operate continuously. Source hardware, 2.400 m length and 0.155575 m borehole radius remain unchanged. One connected hardware rotation is clockwise viewed from the surface, illustrated at 5 degrees/s, with no axial tool translation. Flow remains independently advected.

Reuse: v017 translucent amber fluid and long tapered trails; original central tracked-fragment positions and speed appear at frames 151–246. Extended paths use v004 geometry-aware routes and globally connected clearance candidates. Three persistent cohorts of three source-shaped fragments serve the broader framing, with matte warm mineral materials. Formation remains fixed and already sectioned; its outer presentation extent increases to 0.42 m while the hole radius stays fixed. Camera and materials are editable.

Truth limits: T48's source-X windows [1.35,1.56], [0.88,1.35], [0.50,0.88] m map to world-Z [-0.06,0.15], [0.15,0.62], [0.62,1.0] m. They are morphological working regions. O07 exact functional stage-face and pin/box identity remain unresolved. Flow is illustrative, with no CFD, pressure map, measured RPM, calibrated speed or performance claims. The visible temporary source caps/plates retain their existing provisional provenance.

Verification: 863 integer/half-frame samples clear steel and wall; rock-to-rock overlap checks pass. Full fluid-boundary overlap check passes. Prior v017 and shared source hashes are unchanged; relative library resolves. Source and frame-by-frame camera evidence live in `Full-Previs_v018/Records/`. Agent checks do not substitute for owner viewing or engineering approval.

Editorial conflict: new provisional film window 0:58–1:16 replaces the former 0:58–1:10, adding six seconds. S06, S07, narration and full-film assembly are untouched; Radzi decides downstream timing.
'''
beats={
'A':('0–5 seconds / frames 1–120','Medium oblique lower-body view includes solid formation, annular fluid and incoming cuttings. A gentle upward push moves toward the lower raised region; the tightening passage and bending amber paths provide the qualitative local flow change. No numeric acceleration is displayed.'),
'B':('5–12 seconds / frames 121–288','Motivated scale cut into the approved v017-style three-quarter pad view. A very small upward drift preserves observation time. The original four-second fragment interaction is reused at its original rate, preceded by entry context and followed by continued transport; it is not stretched to seven seconds.'),
'C':('12–18 seconds / frames 289–432','Cut follows upward transport into the upper working region. A short observation interval leads into a controlled pullback showing all three regions together. Paths become less curved downstream; the ending presents the connected hydraulic body while circulation and rotation continue. This is qualitative flow organization, not a measured pressure-recovery/wake result.')}
for part,(timing,description) in beats.items():
 p=ROOT/f'04-Production/Shots/S05/S05-{part}/direction.md';text=p.read_text(encoding='utf-8');heading,rest=text.split('\n',1)
 assert '## Controlling v018 full cinematic previs' not in text
 addition=f'\n## Controlling v018 full cinematic previs — 23 October 2026\n\n{common}\n**This composition: {timing}.** {description}\n\nStatus: owner-authorized previs implementation; return complete animation for owner review. Final finishing, client publication and film assembly remain outside scope.\n\n---\n'
 p.write_text(heading+'\n'+addition+rest,encoding='utf-8')
print('Updated the three existing S05 contracts; no competing direction document created.')
