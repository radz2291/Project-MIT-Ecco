# Waveform v015 — shared asset and separate demo

This delivery has **two Blender files only**:

1. `04-Production/Shared/Assets/Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend` — reusable waveform at the origin. Exactly two objects: `WF_LIVE_FIELD` and `WF_MASTER_CONTROLS`. Two meshes, one material, two Geometry Nodes groups, zero cameras, lights or linked libraries. No rig, earth, history, datasets or earlier experimental fields.
2. `04-Production/Records/Tasks/T-056/Demos/Waveform_demo_v015.blend` — separate minimal sensor/wall demonstration. Eleven objects: the two linked shared objects, sensor and wall fixtures, one camera, two lights and four causal cues. Its sole linked library is the relative v015 shared file. Cue timing reads the same linked controls.

Open the shared file, select **WF_MASTER_CONTROLS**, and use the **Modifiers** panel. Speed, frequency, strength, echo strength, decay, timing, dimensions and appearance remain native controls. The opening view is centered on the waveform and the control object is selected. The text datablock **START HERE — shared waveform** explains usage. Local overrides and the illustrative open/cased selector remain on **WF_LIVE_FIELD**.

Save shared edits and reopen the demo to reload the link. The demonstration runs frames1–96 at24fps. Its sensor emits, wall contact responds, the weaker field returns, and the measurement cue follows reception. Both files work with script auto-execution disabled; no Python handlers are required. The visual remains an authored cinematic waveform, not measured RF or calibrated pressure.

Saved/reopened checks confirm default active geometry matches v014 at ten sampled frames, including empty quiet states. A saved shared Strength=.8 edit changes the reopened demo; restoring the shared file byte-for-byte restores the baseline geometry. All cue control references resolve to v015. Previous files were preserved; v014's original hash is recorded in `repackage-build_v015.json`.

Earlier integrated scenes remain historical test material and are **not part of this delivered list**. No new shot integration is included. Exact hashes and permitted publication paths are in `publication-manifest_repackage_v015.json`. Native files remain local, with no remote-media or backup claim. Final owner inspection remains pending.

The corrected minimal-demo frame30 rendered at640x360/Eevee16 in1.627seconds including image write. The first wall-block framing was occluded despite a2.004second timing; its failed evidence is retained locally. The delivered demo uses a small contact disk and separate side review camera, with sensor on the left and wall on the right. Shared geometry is unchanged. Reproduce by running `repackage_waveform_v015.py`, then `fix_demo_view_v015.py` against the demo.
