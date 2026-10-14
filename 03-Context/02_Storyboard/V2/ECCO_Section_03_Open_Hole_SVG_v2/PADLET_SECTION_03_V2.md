# ECCO ENP3 — Storyboard V2 / Section 03

**0:22–0:40 | OPEN HOLE — Geometry and Formation Imaging**  
**Status:** Client-feedback reconciliation draft (Ahmed comments C01, C02, C03). Requires technical approval.  
**Continuity:** Section 2 has already explained pulse/echo round-trip timing, so Section 3 does not repeat a full waveform lesson. Section 6 will later show the explicit 3D-cylinder-to-flat-2D unwrapping transition.

## Section introduction — Padlet-ready

Section 3 introduces the two open-hole outputs of ECCO's ultrasonic measurements. First we compare the nominal drill-bit hole size with the actual measured borehole. White represents nominal size; progressively darker blue marks larger-than-nominal radii, while red identifies locally undersized or tight areas. By combining measurements through depth, ECCO can reveal geometric irregularities, including spiral-like patterns that may be associated with drilling conditions. The story then shifts to another property of the same returned echo: its amplitude, represented as a separate yellow/brown formation image.

**Core message:** One ultrasonic measurement process supplies complementary information about borehole geometry and acoustic formation variation.

## Panel 1 — White: Nominal drill-bit diameter (0:22–0:25)
**SVG:** `01_White_Nominal_Bit_Size.svg`

We begin with a circular reference representing the nominal hole diameter expected from the drill bit. The reference is shown in white and establishes the baseline against which measured hole size will be compared. This is not a claim that every actual cross-section is perfectly circular.

## Panel 2 — Blue enlargement and red tight spots (0:25–0:29)
**SVG:** `02_Blue_Enlargement_Red_Tight_Spots.svg`

ECCO's measurements reveal how the actual wall differs from the nominal diameter. The white ring remains as the reference: light to darker blue identifies increasing enlargement beyond nominal radius, while red marks areas smaller than nominal size, or tight spots. These variations could reflect washout, restriction or other causes that require engineering interpretation. Colors are conceptual and demonstrate Ahmed's intended color convention; they are not a calibrated quantitative color scale.

## Panel 3 — Spiral-shaped irregularities through depth (0:29–0:33)
**SVG:** `03_Spiral_Geometry_Through_Depth.svg`

As ECCO rotates and moves through the well, measurements from successive depths combine into a three-dimensional picture of the wall. Alongside simple enlargement and tight spots, the visualization can reveal a spiralling variation in hole geometry. This type of pattern may be related to drilling parameters or drill-string behavior rather than only formation enlargement. The white outlines indicate nominal reference geometry, blue shows enlargements and red indicates a local undersized area. The helix is a conceptual example, not a diagnosis from actual field data.

## Panel 4 — The same echo also has amplitude (0:33–0:36)
**SVG:** `04_Same_Echo_Two_Properties.svg`

The same returning ultrasonic echo provides more than its arrival time. Section 2 already demonstrated how timing supports radius measurement. We now introduce echo amplitude: the strength of the reflected acoustic signal. Rather than repeating the waveform tutorial, a single pulse/echo moment leads into two distinct interpretations — blue-toned geometry and warm-toned amplitude information.

## Panel 5 — Formation amplitude image (0:36–0:40)
**SVG:** `05_Yellow_Brown_Formation_Image.svg`

Repeated amplitude measurements around the borehole and through depth produce a 360° acoustic formation image. We use the yellow/brown shades Ahmed specified, showing acoustic variations and apparent formation patterns. The colors represent signal responses, not the actual optical colors of rock. The complete cylindrical-to-flat unwrapping animation is reserved for the revised Section 6.

## Engineering and production review notes
- White = nominal bit-size hole, blues = increasing radius/enlargement, red = undersize/tight-spot region. **Color mapping is illustrative; actual thresholds and legend need MIT confirmation if shown numerically.**
- A spiral irregularity can have multiple causes; don't present the animation as proof of one particular drilling parameter without MIT-specific evidence.
- Tool rotation and downward drilling progress happen together in rotating drilling mode; sliding mode is another operating mode. Do not animate a stationary drill string as the sole normal scanning operation.
- Section 2 owns the detailed waveform timing explanation; don't duplicate that scene here.
- Both outputs derive from pulse-echo measurements, but *amplitude is not transformed from geometry* and yellow/brown is a separate colormap from hole-size blue/red.
- These SVGs explain intended mechanics. The visible tool and its sensor positions are diagrammatic, not engineering-approved hardware geometry.
- Section 6 V2 will animate 3D cylinder -> vertical split -> unwrapped 2D -> actual Mi-VU log, following client comment C09.
