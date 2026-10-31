# Section 2 video-generation assets — 31 October 2026

## Recommendation within the requested 30–60 credit target

Start with **Seedance V1.5 Pro**, a **5-second** pilot, **720p**, **16:9**, camera fixed off, audio off. The authenticated Weavy model catalog returned an approximate default cost of **31 credits**. This is a catalog estimate, not a price guarantee for changed settings. Confirm the displayed node quote stays at or below 60 before running.

Connect `appearance/01-look.png` as First Frame and `appearance/04-look.png` as Last Frame. Paste `pilot/prompt-5s.txt`. The last appearance image is an approximate guide from the selected f358 still, not an exact rendered f360 boundary. `pilot/first_frame.png` and `pilot/last_frame.png` are the exact grayscale motion-reference boundaries for comparison, not finished product images.

This pilot covers the first five seconds of Section 2, including approach, outgoing pulse and echo. It does not contain the history reveal. It retains native timing rather than compressing the whole 12-second sequence into five seconds.

## Full sequence

For the full scene, Seedance V1.5 Pro supports a **12-second** duration in the current Weavy contract. Connect `appearance/01-look.png` as First Frame and `appearance/06-look.png` as Last Frame; use `prompt-12s.txt`. Try 480p if you want a lower-cost full-sequence proof, but check the actual node quote: the catalog does not expose a reliable price for these changed settings. The 31-credit default estimate must not be treated as a quote for 12 seconds. No paid test has been run.

Seedance V1.5 Pro accepts first/last images, not a reference video or arbitrary multi-image appearance sheet. Therefore the timed prompt guides the intermediate action; the Blender motion asset cannot be wired into that model as a driving video. Do not connect the whole six-panel sheet as its first frame, which could animate the collage.

If precise video-driven transfer is more important than the strict budget, the catalog lists **Seedance 2.0 Mini Reference to Video** at approximately **65 credits by default**, with mixed image/video references and 4–15-second output. That default is above the requested ceiling. Use `prompt-reference-video.txt`, `motion_reference-color.mp4` and `appearance/six-shot-look.png` if choosing that route and the configured node quote is acceptable. Its 12-second cost is unverified and may be higher. Kling o1 Reference Video to Video lists about82 credits by default and accepts3–10-second reference video, so it is not the first choice for this12-second budget test.

Wan 2.2 Animate Move/Replace lists about48 credits but its contract describes character-image animation. That is not sufficient evidence that it will preserve this non-character industrial camera journey; it is not the recommended pilot.

## What is supplied

- `motion_reference-color.mp4`: complete12-second Blender-preview motion and meaningful cyan/green/blue measurement graphics. Prefer this for actual reference-video inputs.
- `motion_reference.mp4`: the same12-second motion in grayscale, useful for camera/geometry study; history and signal separation are weaker in grayscale.
- `first_frame.png`, `last_frame.png`, `events/`: exact samples extracted from the encoded grayscale reference.
- `pilot/`: faithful first5seconds, exact grayscale boundaries and a complete budget-pilot prompt.
- `appearance/`: exact copy of the supplied13:54:55 generated sheet, plus six extracted single-view crops. This is the latest image actually supplied locally, not an unseen render from the later luminous-history prompt. Desired extra history glow is specified in the video prompts.
- `scene-description.md`, `manifest.json`, `review.json`: scene, provenance, timing and technical/visual checks.
- `inspection/*.gz`: losslessly compressed read-only Blender inspection, including raw animation keys and100 evaluated samples. No geometry/animation edits were made.

The supplied generated sheet is1696x624 and not a mathematically exact8:3 canvas. Crops retain native pixels without stretching; their slightly wide aspect may be reframed by a16:9 model. Original source motion remains16:9.

## Evidence and limitations

The selected saved scene still lacks its historical linked ECCO master. A fresh incomplete render was deliberately avoided. Motion was extracted from the verified complete existing v011 review video: decoded indices72–359 map to native Blender frames241–528,24fps,288frames,12seconds. The source preview was960x540; reference export is upscaled to1280x720, which adds no source detail.

The live Blender file is a different dirty project and was queried read-only, left untouched. Inspection of the selected saved scene is retained, with its missing dependency and procedural-history warnings. No fresh complete-scene motion fingerprint certification is claimed. Visual review used phase and one-second timeline sheets; this is not a claim of having played every frame in real time. Both full videos were decoded for technical QA. No external upload, credit spend or generated video result is claimed.

The skill's standard render/package/finalize pipeline was not used to certify a new render: this is an explicitly documented complete-existing-video fallback with custom extraction/decode QA. Inputs and prompt are ready for a generator attempt, with the stated limitations.

Model contracts and approximate prices were read directly from the authenticated Weavy MCP catalog on31October2026. Weavy explains that duration/resolution can change price and that the configured node shows the quote: https://help.weavy.ai/en/articles/12267166-figma-weave-credit-system
