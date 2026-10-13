# Blender execution and data contract

## Source and connection

Use a read-only MCP query first. Follow current AGENTS.md. The author uses the official Blender Lab server `blender` v1.0.3; do not assume that setup or its paths on another machine. Prefer MCP scene queries/Python. If the MCP CLI helper cannot find Blender, discover the installed binary rather than replacing the server.

Check live filepath and dirty state. An unsaved scene may differ from disk: obtain a separate authorized snapshot when current changes are the requested source. Never silently render stale disk data or overwrite the original. A different open project must remain untouched.

## Scripts

Run the first two inside Blender; run packaging with Python containing Pillow and imageio-ffmpeg. Discover available/bundled runtimes instead of installing unnecessarily. Resolve actual paths and shell quoting.

```text
<blender> -b <source.blend> -t 8 --python <skill>/scripts/inspect_blender.py -- --config <job.json>
<blender> -b <source.blend> -t 8 --python <skill>/scripts/render_reference.py -- --config <job.json>
<python> <skill>/scripts/package_reference.py --config <job.json>
<python> <skill>/scripts/finalize_package.py --config <job.json> --review <review.json>
```

Use JSON for names/paths instead of shell-built code. Blender can exit zero after a Python traceback: require expected manifests, not just a process exit code. Keep logs and bounded waits. Config-relative paths resolve relative to the JSON file. `source_blend` must match the loaded file. `scene` optionally chooses a scene. `camera` optionally overrides camera selection and must be recorded; omit it to preserve authored camera cuts.

Omit `resolution` to derive a 720-high even-sized export retaining source display aspect, including non-square source pixels; output pixels are square. An explicit different aspect is recorded and flagged for framing review. Perspective and orthographic cameras are supported; panorama or cropped-border sources need an alternative faithful export or authorized adaptation rather than silently changed projection/crop.

Finalization is not an automatic visual reviewer. The agent must view the actual assets and author the scene description/prompts first. Fill the review file with actual findings and inspected relative filenames, including required event images; explicitly resolve warnings. The finalizer rejects missing/unfilled documents, unreviewed assets, altered video/boundary images and changed sources. It does not verify that the agent's semantic interpretation is correct or that an external generator will follow it.

`inspect.sample_step` defaults to one source frame; add fractional `extra_frames` around fast events. `inspect.objects` optionally chooses tracked subjects, otherwise all objects are tracked. Raw keys include all Actions, not just active transform curves. Read action associations/users before treating unused Actions as requirements. Layered and legacy Actions are supported. Drivers, NLA and constraints need interpretation; action-key times under NLA are not necessarily scene times. Evaluated samples are the authority for resulting motion.

Enable `inspect.pose_bones` for skeletal actions and `inspect.evaluated_geometry` for deformations, Geometry Nodes, simulated meshes or engine-dependent silhouettes. These can be expensive. Cached simulations may need warm-up/bake before random-access sampling; helpers report risks but do not bake. External render-engine displacement, shader alpha silhouettes, volumetric subjects and third-party procedural objects may need a different reference method. Workbench is a default, not proof of compatibility with every Blender feature.

The helper exports scene-camera geometry, including marker-bound camera cuts. It bypasses the compositor and video sequencer for a clean reference. Before using it, inspect whether a meaningful reveal, reframing, edit or transition depends on those stages, material alpha, instancing or another unsupported representation. Use a suitable alternative export or a documented authorized proxy when needed; do not call a missing effect faithful just because transform checks pass. Do not substitute scene-camera output for a sequencer-edited animation without checking the actual edit.

## Timing

Source start/end are inclusive sample endpoints. Duration D and FPS F produce N=D×F frames; N must be an integer and at least two. Sample i uses:

```text
source(i) = start + (end-start) × i/(N-1)
time(i) = i/F, for i=0..N-1
```

The last image is displayed through D. Frames 55..86 over 2s/24fps mean 48 evaluated samples, not 32 frames relabeled. Original frames 1..192 over 8s/24fps remain the original integer samples. Reverse ranges are allowed when requested. Omitted duration uses inclusive source duration and must be representable at the target FPS. Retiming changes absolute world speed; disclose it.

Keep Blender's source FPS unchanged while evaluating stills: time-dependent drivers and simulations may read it. Output FPS is applied during video encoding, not by changing the source scene's clock.

Adjacent generated segments may share a boundary image, but concatenating both images can add a one-frame dwell. Decide whether to remove a duplicate and adjust final duration or use disjoint samples under one master mapping. Verify pose/velocity/lens/state across the join. Do not concatenate blindly or promise a seamless result without checking it.

## Reference controls

`grey_groups` contains explicit glob patterns and neutral values; default geometry uses `base_grey`. Identify grouping from scene/visual evidence. `alpha_groups` and `hide_objects` are optional visibility adaptations, recorded in manifests. Alpha below one must not be called faithful opacity. Changes to camera/reveals require a separately authorized source copy; the helper makes none.

Conservatively detect volume-only materials by connected output sockets; do not remove mixed surface/volume geometry automatically. Particle render modifiers may be suppressed while retaining the emitter mesh. Meaningful particle/volume subjects require intentional preservation or an honest limitation. Inspect Geometry Nodes separately. Animated environmental effects can be drivers of the story, not decorations.

Start with simple studio shading, cavity/cast shadows disabled if they create artifacts, restrained greys and anti-aliasing. Cavity can expose tessellation; transparency can dither; colored studio lights can tint greys. Packaging converts frames to greyscale. Review images instead of assuming a preset always works.

Landmarks are object-local points projected into the camera. **Inside frustum is not visible**: no occlusion test is performed. Inspect the actual image at endpoint requirements. Fixing an unreadable endpoint by changing the camera is a documented adaptation, not a shading tweak.

The renderer fingerprints source geometry/keys and evaluated camera/object motion at every output sample before/after appearance overrides. Optional evaluated mesh comparisons catch changed silhouettes. Altered render flags are listed separately. Preservation failure aborts. Checks are not a cache bake, physical validator or proof of arbitrary render-engine equivalence.

Blender curve bounds/dimensions may be lazy or sentinel-sized until a draw engine evaluates them. Do not treat a changed cached bound as proof of changed geometry; compare source curve data and evaluated mesh geometry. Preservation failures write `preservation_failure.json` with the first measured differences for diagnosis.

Optional `save_reference_blend` saves a separate viewport-shaded source-animation copy. It retains source keys; video retiming lives in the manifest. Do not claim that playing that .blend automatically reproduces the exported retimed timeline.
