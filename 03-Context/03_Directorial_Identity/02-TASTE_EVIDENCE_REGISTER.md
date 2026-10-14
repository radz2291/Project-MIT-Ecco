# Taste Evidence Register — v0.1

**Updated:** 14 October 2026  
**Purpose:** Preserve source feedback **separately** from our analysis, so an AI agent can distinguish user-confirmed taste from suggestions.  
**Source:** Rolladice × MIT creative-reference conversation, 14 October 2026. Quotes below are from the director's statements in that conversation. Minor spelling preserved.

## Evidence vocabulary

- **Direct / explicit:** director stated the like/dislike or reason.
- **Inferred / tentative:** interpretation proposed by the assistant; requires visual comparison or confirmation.
- **Unexplored:** topic is identified as important but has no specific preference evidence.
- **Scope of reaction:** first impression vs a particular linked work vs detailed attribute. Never generalize a dislike of one work to all work by that artist.

## Reference reactions

### E001 — First-glance preference ranking

**Director, verbatim:**  
> "Nidia not at first glance. Tendril yes at first glance. Territory Studio is interesting. FutureDeluxe is double yes. Gmunk no, oblivion no."

| Reference | Direct reaction | Scope | Confidence in reaction |
|---|---|---|---|
| FutureDeluxe | Double yes | Initial portfolio/reference impression | High |
| Tendril | Yes | Initial linked work / first impression | High |
| Territory Studio | Interesting | Initial linked work / first impression | High |
| Nidia Dias | Not at first glance | Initial impression only | High |
| GMUNK / Oblivion | No / Oblivion no | GMUNK and specifically Oblivion in presented context | High |

**Avoid over-inference:** This does not authorize inventing colors, lenses, moods or universal design bans.

### E002 — FutureDeluxe, detailed positive rationale

**Director, verbatim:**
> "The overall creativity and visual direction. I think it's very good at playing with space, and able to showcase an object to become bigger than life. And even any of their still speaks, convey something, a message, emotion. They don't have to do complex things to show sophistication and they are not extravagance. And also the angle and subject framing, positioning, all are quite unique. The depth are also good too. Every picture speaks differently. I can feel like their arts, their output are breathing. not straining."

**Directly supported attributes:** overall creative direction; playful/intentional space; monumental object presence; expressive stills; sophistication without complexity/extravagance; distinctive angles, subject positioning and framing; depth; diverse compositions; a breathing/unstrained quality.

**Our interpretation (not additional quotes):** expressive spatial authorship; effortless monumentality; each composition should make its own statement; complexity must be justified.

**Reference:** https://futuredeluxe.com/work  
**Confidence:** High for preference descriptions; medium for how exactly to reproduce them in a new scene until tested.

### E003 — Tendril, detailed positive rationale

**Director, verbatim:**
> "I think what's good about Tindril are they feel very much premium and simple. And also I feel like they portray technological advances, advancement pretty good and well showcase. And there's something about their camera animation is very nice. looking at your provided link"

**Directly supported attributes:** premium look; simplicity; effective portrayal and showcasing of technology; attractive camera animation.

**Our interpretation:** refined technological presence; camera motion contributes to apparent advancement and high-end product treatment.

**Reference viewed:** https://tendril.studio/work/figure02/  
**Confidence:** High for these attributes; unknown for the specific camera mechanics until E004.

### E004 — Tendril camera, detailed behavior

**Director, verbatim:**
> "The way the camera flows fluidly and navigate the object, Each stop is a showcase and that transition in between is very fluid as if it creating a sub-narrative through timing, acceleration and rhythm."

**Directly supported attributes:** fluid navigation around an object; purposeful showcased views/stops; continuous transitions; sub-narrative through timing, acceleration and rhythm.

**Our interpretation:** a camera path is a sequence of information-bearing arrivals linked by meaningful motion phrasing; evaluate travel *and* destination; create micro-compositions.

**Reference viewed:** https://tendril.studio/work/figure02/  
**Confidence:** High for preference; medium for untested implementation suggestions such as particular splines, easing curves or move durations.

### E005 — Important scope correction: beyond templates

**Director, verbatim (excerpt):**
> "It's like a favor, taste, which is good, which is bad, which we like, which we dislike, which we are preferred, which we are not preferred, which will do/highlight certain things better, which is not."

**Additional director statement (excerpt):**
> "And of course, motion graphic, the text, fit strongly into this too."

**Directly supported:** the system must encode aesthetic judgment, negative as well as positive examples, contextual tradeoffs, motion graphics, text and taste—not just parameters/templates. Lighting and camera configuration should be designed for a scene such as an invisible environment.

**Our interpretation:** preference evidence + case-based artistic reasoning + critiques + executable shot directives should be different layers.

**Confidence:** High.

## Reconciliation of previous assistant suggestions

| Earlier suggestion | Current status | Reason |
|---|---|---|
| "Effortless Monumentality" | **Useful provisional label** | Emerges from E002; director has not explicitly adopted the label |
| "Camera as Guided Discovery" / "Choreographed Reveal" | **Useful provisional label** | E004 strongly supports behavior; label itself is assistant-authored |
| "FutureDeluxe + Tendril + Territory" as a blend | **Exploratory**, not a prescription | Territory has only "interesting" feedback; no trait selection |
| Prefer specific darkness, metallic recipe, slow/fast tempo, camera lens or graphic grid | **Unverified** | No user selection on these parameters |
| Lack of interest in GMUNK means no neon/HUDs | **Invalid overgeneralization** | E001 is a reference reaction, not a universal prohibition |
| "Every frame must look like a still" | **Too rigid** | E002 values meaningful stills; transitional motion frames serve other purposes |

## How to add future evidence

Append a new entry with:

```text
Evidence ID:
Date:
Artist/studio and exact work + URL/timestamp:
User statement (verbatim or faithful short transcription):
What is liked:
What is disliked:
Context / target shot:
Confirmed judgment vs assistant hypothesis:
Counterexample or exception:
Follow-up test / resulting shot decision:
```

Never silently replace the director's original words with assistant terminology. Version this register as new comparisons are made.
