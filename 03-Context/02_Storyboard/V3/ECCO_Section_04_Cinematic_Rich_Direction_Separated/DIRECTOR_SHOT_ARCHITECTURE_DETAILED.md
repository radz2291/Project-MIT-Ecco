# ECCO ENP3 — SECTION 04: CASED-HOLE EVALUATION

**Film timing:** 0:40–0:58 (18 seconds)  
**Stage:** Step 1 — cinematic shot architecture for AI Director / controlled 3D storyboard agent  
**Images:** Four independent cropped images extracted from the EXACT four-shot composite selected by the project owner.  
**Approval:** The owner selected this visual option as the working cinematic direction. **This is not MIT engineering sign-off, verified hardware, an animatic or a camera-keyframe lock.**

## Section's narrative intention

Section 3 explained open-hole geometry and formation amplitude. Now we reveal **a separate world, inside steel casing**, with two complementary measurement capabilities:

1. **Cement evaluation:** ultrasonic casing response gives information about material supporting casing behind steel.
2. **Casing integrity:** travel-time distance measurements reveal changes to the steel's internal profile, including local wear grooves.

The emotional and spatial progression is deliberate: **enter casing → listen through steel → reveal a hidden axial cement channel → detect internal steel wear**.

The audience should experience each discovery through continuous photographic space—not watch four variations of a mechanical diagram. Camera geography, the actual model and the layers behind steel must be consistent across shots.

## Shot map

| Shot | Time | Length | Principal screen subject | Dramatic objective | Individual reference image |
|---|---|---:|---|---|---|
| S04-A — Entering the Cased World | 0:40–0:44 | 4s | Bit/BHA/ECCO approaching and entering pre-existing casing shoe | Establish a change in operating environment | `S04_A_Entering_the_Cased_World.png` |
| S04-B — What Lies Behind Steel | 0:44–0:49 | 5s | Sensor, casing ringing, material immediately behind steel | Explain how acoustic response depends on casing support | `S04_B_What_Lies_Behind_Steel.png` |
| S04-C — The Hidden Channel | 0:49–0:54 | 5s | Steel casing, cement annulus, one axial fluid-filled region | Give the local acoustic anomaly spatial meaning | `S04_C_The_Hidden_Channel.png` |
| S04-D — The Damage Within | 0:54–0:58 | 4s | Casing inner wall, nominal-vs-worn inner profile | Reveal local casing metal loss / increased inner radius | `S04_D_The_Damage_Within.png` |

## Cinematic continuity and operating timeline

This is not a single uninterrupted drilling descent. Section 3's open-hole sensing transitions to a **later upward BHA movement after drilling a deeper section**, entering casing already installed in an earlier well-construction phase. A visual temporal bridge is permitted. Do not show casing growing around ECCO.

BHA order must remain credible: the bit sits below ECCO on the assembly; on upward retrieval, the *upper portions of the BHA and then ECCO* cross the casing shoe before the lower bit. Use verified relative positioning. The camera should not silently flip uphole/downhole direction between every frame.

In cased-hole shots, keep the conceptual layer order consistent: **tool / well fluid → casing steel → cement annulus (with a possible localized fluid channel) → surrounding rock**. The steel is opaque in reality; selective transparency is a story device, not an optical capability of ultrasound.

Visual continuity: brushed/satin industrial metal, rough formation, dramatic near-darkness, restrained cyan pulse visualization and warm cement environment. Avoid bright magic beams, floating fluid streams, excessive particle effects and any implication that the casing is moving independently of the stationary borehole.

## Generated-image fidelity caveats

The four accepted images are annotated **comparison illustrations**, not clean film stills. Their arrow labels, mini waveforms and numeric-looking graphics aid the review board and can be recreated/omitted selectively in post; they are not hard requirements for in-scene Blender materials.

**S04-A:** Casing-shoe ring geometry and BHA look are conceptual; correct physical location and bit/ECCO order in the controlled scene.  
**S04-B:** Waveforms represent *relative damping concepts*, not verified quantitative waveforms, and color does not itself identify water.  
**S04-C:** The blue channel is a localized fluid-filled/no-cement region **outside** casing, not an actively moving blue river.  
**S04-D:** The groove is an internal wear scar. The reference's gouge is visually heavy; execute a shallow, localized recess into steel, not a full wall break.

## Technical invariants for AI agents

- ENP3 uses **three outward-facing imaging sensors 120° apart, one sensor plane**, per MIT datasheet. Verify their actual positions in real product CAD before attaching emitters; a generated image may show a fictitious emitter.
- One sensor emits ultrasound toward casing and measures the returning response. No separate back-wall camera or true see-through-steel optical imaging.
- Good bonding/coupling to cement generally damps casing ringing more than a fluid-backed or poorly supported region, but interpretation is complex and requires proper calibration / signal processing.
- Never claim fluid chemistry is directly proven by a color overlay; Ahmed's yellow/brown cement and blue water/no-cement coloring is the **intended interpretive visual convention**.
- Cement channels in this concept run **axially along one side** of casing and may not remain perfectly straight in real logged data.
- Worn casing grooves remove metal at the **inner wall**, giving local increase of internal radius (diameter may be affected depending on azimuth) while external shape remains unchanged for this illustration.
- ENP3 maximum specified OD **12 in**; minimum casing internal diameter **12.3 in**, per MIT datasheet. The illustrated scale is artistic; verify clearance from CAD and actual well information before animation.
- The user-approved image option is the basis for look/composition; exact CAD, light effects, measured waveforms and data interpretation are not frozen by it.

## Hand-off boundary

**This is Step 1 — shot architecture only.** Before Blender production, split each film shot into several **atomic camera/key moments**: camera XYZ/aim/focal length, tool and geology placement, visibility/opacity states, waveform state and the intended transition. Establish those in a controlled 3D storyboard/animatic. Blender should then execute rather than invent the narrative.

## Section-level acceptance

1. Four distinct shots total exactly 18 seconds.
2. S04-A establishes *upward return to existing casing* rather than spontaneous casing creation.
3. S04-B physically connects acoustic ringing to material directly behind casing.
4. S04-C makes a single-sided **axial** channel outside the casing unmistakable.
5. S04-D reveals internal casing wear by a geometric distance comparison—not a through-wall fracture.
6. Same ENP3 model, same casing dimensions and consistent scene geography across all images/animation.
7. Final image of S04-D motivates the next Section 5 focus on hydraulic body geometry.

---

## Detailed shots

## Shot S04-A — Entering the Cased World

**Film time:** 0:40–0:44 · **Duration:** 4 seconds  
**Approved-image crop:** `S04_A_Entering_the_Cased_World.png`

### Cinematic purpose

The audience has just seen formation amplitude information in open hole. Now we must change the physical environment without pretending that steel materializes around the tool. Establish that a previous portion of the well is already lined and cemented, while the latest drilled section is deeper and still open to rock. The BHA, with bit below ECCO, is **moving upward** into that pre-existing casing after the deeper drilling operation.

### Camera composition

Use a legible three-quarter longitudinal view along a **deviated** borehole. The deeper, irregular rock wall occupies the foreground/lower direction; the smooth steel interior continues upward into the background. The lower casing shoe must be visible as a definite, continuous end of the existing casing—not two floating semi-pipes or a steel tube being assembled in place. The actual ECCO body should be recognizable as part of the BHA, not a disconnected heroic prop. Keep the bit visibly below/farther downhole than the imaging sensor position when a wider view permits.

Compose a dynamic diagonal axis with enough negative space at the casing shoe that the transition is readable on first watch. The selected image shows a close, dramatic perspective; the *production* camera may need a slightly wider start state than the still image to establish this spatial relationship.

### What happens

Begin on the tail of S03-C's dark rock environment and its imaging overlay fading away. After a readable change of phase, the BHA moves upward. The existing casing shoe comes into the same spatial frame. During upward retrieval, ECCO is above the bit on the BHA, so **ECCO passes into the casing before the lower bit**. Show ECCO crossing the casing shoe while the bit still remains farther downhole in the exposed-rock section. Preserve this order.

The view transitions from irregular rock to reflective, manufactured steel. This is an operating-phase transition rather than a physically continuous extension of open-hole drilling. The surrounding rock need not disappear all at once; a translucent exterior window can help reveal where the casing begins.

### Camera movement

Track upward with a modest rearward drift, so both the tool and casing shoe stay in the composition. The primary subject motion is axial BHA travel. Avoid a fast orbit that obscures which end of the assembly is uphole.

### Audience experience

*“ECCO is now passing into a different part of the well—steel casing that has already been installed.”*

### Final visual state and transition to S04-B

By the end of 0:44, ECCO's sensing region is inside casing; the context of the casing shoe is established. Cut or ease closer to the imaging sensor and the steel inner wall, holding the same local well-axis orientation as much as practical.

### Direct-image limitations / animation-agent instructions

- The image's text and arrow overlays are explanatory annotations, not mandatory final-film graphics.
- Do not use the depicted shiny steel shapes as engineering-approved casing-shoe geometry.
- Do not infer true dimensions or tool position from the image. Validate the clearance between a 12-inch max-OD ENP3 model and casing size using MIT's actual well spec; the ENP3 datasheet cites 12.3-inch minimum casing ID.
- Need actual BHA or at least relative ECCO/bit positioning, based on verified project facts.

### Suggested internal beats (illustrative, not locked keyframes)

- 0:40–0:41: Rock-dominated downhole environment, beginning of upward BHA movement.
- 0:41–0:42.5: Casing shoe becomes clearly visible; shift visual emphasis to steel.
- 0:42.5–0:44: ECCO enters casing; prepare a closer view of the casing inner wall.

### Acceptance test

A non-engineer can say where the casing already is, where the open hole is, which direction ECCO travels, and why the next shot occurs inside steel.


---

## Shot S04-B — What Lies Behind Steel

**Film time:** 0:44–0:49 · **Duration:** 5 seconds  
**Approved-image crop:** `S04_B_What_Lies_Behind_Steel.png`

### Cinematic purpose

Teach how ECCO can infer variations in material support behind an opaque steel casing using the **casing's ultrasonic ringing/decay**. This is *not* a reprise of open-hole geometry or a light beam passing straight through steel to photograph hidden cement.

### Camera composition

Close, intimate oblique side view of the sensing module inside an inclined section of casing. The metal is physically continuous and recognizable. Use a deliberately **limited, gradually expanding translucent reveal** outside the steel—not an impossible permanent window where the entire casing appears missing. The revealed outer annulus should place cement (warm yellow/brown) immediately behind the steel. In the comparison region, show weak bonding or a fluid-filled region immediately behind the casing.

The selected image pairs attractive wavefronts with two tiny waveform diagrams. The agent should keep the composition and the contrast, not assume those precise wave curves are derived from measured data.

### What happens

One ultrasonic pulse leaves a verified outward-facing imaging sensor, travels through the well fluid, and excites a response in the steel casing. On a supported section, the casing ring-down is relatively damped. In the comparison section with a weakly supported or fluid-like annulus, the casing's response persists longer. Convey this by localized subtle vibration/radiating graphic treatment and a brief waveform comparison—not by moving steel dramatically, and not by showing orange and cyan lasers as if two actual sources were firing through the metal simultaneously.

The outer cement/annulus becomes gradually translucent at the relevant locations **only as a representation of processed acoustic interpretation**. The casing itself does not need to vanish. Hold the causality: sensor → steel response → comparison of damping → inferred backing condition.

### Camera movement

A small lateral track / dolly through the casing section, with a camera hold long enough to perceive a faster decay versus a prolonged ring. The camera may create a subtle change of framing to reveal both locations without teleporting the sensor. Do not cut to an isolated technical screen that loses physical context.

### Audience experience

*“The return signal changes depending on how steel is supported behind the casing.”*

### Final visual state and transition to S04-C

A short distinctive fluid/poor-support zone is now localized. Leave an anchored highlight on this zone. Expand the view along the casing axis in the next shot to determine whether the finding continues as an axial channel.

### Direct-image limitations / animation-agent instructions

- Blue versus orange waves in the image are **graphic shorthand**, not a real physics-calibrated color code; the waveform illustrations are exemplary, not real measured amplitudes or decay constants.
- Never claim a single echo proves water specifically, no cement at all, or quantitative bond strength without the necessary log interpretation.
- The three imaging sensors occupy one circumferential sensor plane, 120 degrees apart; do not relocate independent sensors along the body to match visual convenience.
- Outer annulus must not be mistaken for inside casing.

### Suggested internal beats (illustrative, not locked keyframes)

- 0:44–0:45: Re-establish the sensor and the inside surface of steel casing.
- 0:45–0:46.5: Pulse-echo contact, casing ringing rendered subtly.
- 0:46.5–0:48: Brief contrasting decay treatments and partial translucency exposing backing condition.
- 0:48–0:49: Keep the anomalous backing location highlighted, lead camera into channel reveal.

### Acceptance test

The viewer understands **why** the two responses differ, which solid layer is vibrating, and that the material condition is *behind* that same layer.


---

## Shot S04-C — The Hidden Channel

**Film time:** 0:49–0:54 · **Duration:** 5 seconds  
**Approved-image crop:** `S04_C_The_Hidden_Channel.png`

### Cinematic purpose

Turn a local acoustic anomaly into a geographically intelligible finding: along a pre-existing steel casing, a **fluid-filled region in the cement annulus** may continue axially and occupy only one side of the circumference. It is not a pipe inserted inside casing, and it is not an optical image taken through steel.

### Camera composition

Continue from S04-B by pulling back to a three-quarter longitudinal view. ECCO stays visible inside casing. Use selective transparency on the OUTER environment to reveal the outside of casing, surrounding yellow/brown cement and a narrow blue strip alongside the *outer steel wall* within the space where cement would normally be. The line of sight may be artificially cut away through geology, but the physical layers must remain logically ordered: **tool/well fluid → casing steel → cement annulus with localized fluid channel → rock**.

The approved generated image expresses the axial geometry effectively. In the final render, keep the blue feature narrow, localized to one circumferential side, and visually stable rather than looking like an open stream of water visibly rushing along the casing.

### What happens

The localized patch from Shot B becomes a longer revealed interval as the camera moves along the casing. The surrounding material gradually grows translucent. A yellow/brown cement sheath emerges outside the steel, interrupted on **one side** by a blue fluid-like area that persists along the borehole axis. The viewer now grasps the spatial nature of the problem.

Optionally allow an understated circumferential trace or short follow-along data band to reinforce that ECCO samples around the casing. **Do not perform the full 3D cylinder-to-flat-2D unwrapping here**; we have reserved that signature transformation for Section 6.

### Camera movement

Gentle pullback and an oblique arc along the length of casing, letting the feature's axial continuity reveal itself. Avoid circling so far around the casing that the channel appears to move from one side to another due to a camera cut.

### Audience experience

*“A hidden issue could occupy a narrow path along one side of the casing, rather than uniformly surrounding it.”*

### Final visual state and transition to S04-D

The viewer holds the image of the exterior annular channel briefly. Then selective transparency recedes and attention shifts back **inside** the steel casing, where ECCO can measure a different risk: local wear on its inner wall.

### Direct-image limitations / animation-agent instructions

- Blue signifies the scenario Ahmed described—water/no-cement in this storyboard—not absolute fluid chemistry determined solely by an image pixel.
- Cement is outside casing, not lining its interior.
- Do not animate a free-flowing surface river unless MIT specifically confirms fluid movement; the real story is localized filling/absence of cement.
- The image's textual labels are board annotations and need not be composited into the final film.

### Suggested internal beats (illustrative, not locked keyframes)

- 0:49–0:50: Local anomaly remains anchored from B.
- 0:50–0:52: Camera reveals wider axial context and translucent cement sheath.
- 0:52–0:53.5: A narrow blue annular channel becomes spatially clear.
- 0:53.5–0:54: Hold the finding and pivot attention back inside casing.

### Acceptance test

Without labels, a viewer can identify where steel is, where cement surrounds it, and where the local channel persists along the length of the casing.


---

## Shot S04-D — The Damage Within

**Film time:** 0:54–0:58 · **Duration:** 4 seconds  
**Approved-image crop:** `S04_D_The_Damage_Within.png`

### Cinematic purpose

Reveal a second cased-hole capability: assessing the **inner profile of casing** for wear or deformation. Cement mapping investigated material behind steel; this shot inspects steel's *inner geometry itself*. The viewer must understand localized loss of metal from the inside rather than believing ECCO sees a crack, hole through casing or large external cavity.

### Camera composition

An intimate three-quarter perspective **inside casing**, grazing the curved steel interior. ECCO's sensing region is in the left foreground, with a localized inner-wall groove farther ahead and to one side. The steel is strongly directional and glossy but not so polished that the depression becomes invisible. Preserve the reference's dark-metal, restrained cyan sensing aesthetic. A small, precise nominal-versus-measured contour comparison may appear as a scientific overlay, with labels kept separate from the 3D objects if added at all.

The groove should ideally be a **smooth localized longitudinal wear scar**, most plausibly on the low side of the deviated casing where drill-string contact may occur. It should not look like shattered concrete, a rectangular excavation, a through-wall fracture, or general corrosion unless separately verified by MIT.

### What happens

The sensor directs an ultrasonic pulse toward a nominal inner casing surface. The measured return distance is consistent with a regular interior profile. Tracking slightly along the wall, the sensor reaches a local worn groove where the inner wall has receded INTO the steel; the sensor-to-wall distance increases locally (after accounting for tool eccentricity/centering). A subtle overlaid nominal inner-wall reference remains while the measured inner-wall contour steps outward into missing material. The casing **outer diameter remains unchanged** in this conceptual example.

The groove predates this scan. ECCO is detecting wear rather than actively making it. Do not show metal flying away as ECCO fires its pulses.

### Camera movement

Glide parallel to the casing's inner surface with a small reveal/settle on the groove. This is a more intimate angle than S04-C; the closer wall move lets the story land in four seconds. Preserve axial geography but allow a purposeful cinematic cut.

### Audience experience

*“ECCO can measure where the steel's internal profile has changed, potentially indicating metal loss.”*

### Final visual state and transition to Section 5

After revealing the groove and its difference from the nominal inner wall, the camera begins to withdraw toward the product. Shift visual attention away from sensing and toward the ENP3 **outer body geometry**, setting up the hydraulic enhancement section.

### Direct-image limitations / animation-agent instructions

- The selected generated image's groove is relatively blocky, and its labels are baked in; do not reproduce a deep rectangular slot literally. Build a shallow internal groove in verified casing geometry.
- Radius change is a distance geometry observation; do not equate it with a direct ultrasonic wall-thickness measurement unless separately justified.
- The outer casing profile stays unchanged in this explanatory scenario.
- The imaging sensor location and entire ENP3 shape must follow real CAD, not the generated probe's styling.

### Suggested internal beats (illustrative, not locked keyframes)

- 0:54–0:55: Close view of a generally smooth casing inner wall near ECCO.
- 0:55–0:56.5: Scan crosses the groove; nominal and measured distances diverge.
- 0:56.5–0:57.5: Hold the revealed groove long enough to recognize local internal wear.
- 0:57.5–0:58: Camera eases toward a product-oriented exit into S05 hydraulics.

### Acceptance test

The observer can point to the **inner steel wall**, identify a groove cut *into the metal from the interior*, and see how ECCO's travel-time measurement detects a locally increased radius.
