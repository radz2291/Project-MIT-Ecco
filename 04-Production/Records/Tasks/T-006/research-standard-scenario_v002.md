# T6 — researched standard configuration proposal v002

15 October 2026. Authorized by Radzi's request to research normal/expected configurations and visit MIT Technologies. Task `0d01c109-a994-461b-b4c1-2fd3661f6fac`; research run `78113b14-f800-4fc8-8c9e-d154a1c1b440`; worker `codex-t006-research-01a13f79`. Fresh handoff and live dependencies/pinned roadmap v2 checked. T5 remains accepted. This is a sourced proposal, not MIT deployment approval or an engineered well design.

## Practical proposal

Use two different intervals in one explanatory well: **13-3/8in casing cemented in a 17-1/2in host hole**, then **12-1/4in open hole below the casing shoe**. This resolves the apparent mismatch between a large casing and the smaller next-stage drilling section. Do not place 13-3/8in casing inside a 12-1/4in host hole.

SLB documents this size progression in an actual Indonesian operation. It establishes a real industry example, not prevalence statistics or MIT's chosen deployment. Its casing-drilling equipment is not proposed for our animation: only the interval sizes and subsequent 12-1/4in PDC drilling are relevant. [SLB original case](https://www.slb.com/resource-library/case-study-with-navigation/bdt/direct-xcd-indonesia-cs).

| Element | Proposed reference | Basis / status |
|---|---|---|
| Product | Accepted T5 temporary plugged v002; measured max OD 304.800154mm | Existing source preserved; O04/O14 limitations retained |
| Lower open hole / bit gauge | 12.25in / 311.150mm | SLB field example and Ahmed's brief; specific ENP3 deployment unconfirmed |
| Upper casing host hole | 17.5in / 444.500mm | SLB field example; not the lower open hole |
| Casing OD | 13.375in / 339.725mm | Tenaris published size |
| Candidate casing weight / body wall | 61lb/ft / 0.430in (10.922mm) | Tenaris reference row; no grade, connection procurement or load design selected |
| Nominal body ID | 12.515in / 317.881mm | Derived from OD minus twice wall, consistent with published reference; not minimum local connection ID |
| Published reference drift | 12.359in / 313.9186mm using inch value | Tenaris reference row; rounded metric column differs slightly |
| Generic collar reference | 8.25in OD / 2-13/16in ID, 6-5/8 REG connection | NOV public configuration; not verified MIT BHA or direct FH compatibility |

Tenaris lists multiple weights for the same casing OD. The 61lb/ft reference has a larger drift than the 68lb/ft row (12.259in). Thus casing OD alone cannot establish the passage envelope; the latter drift is below ENP3's stated 12.3in minimum and is not the conservative proposal here. The nominal body ID and connection bores must remain distinct. [Tenaris manufacturer table, p3, revision 10 dated 20 January 2016](https://www.tenaris.com/media/lqxjon4r/blanking_wedge_521.pdf). This is a published geometry reference, not a claim that this historical connection revision is specified for MIT.

## Expected BHA and connection boundary

SLB describes a BHA as including the bit, subs, optional motor, stabilizers, collars and other drilling/measurement tools; its composition varies. For our schematic, ECCO belongs within that assembly, rather than replacing the entire drilling string. Exact ECCO-to-bit distance and optional equipment remain unknown. [SLB BHA definition](https://glossary.slb.com/terms/b/bottomhole_assembly).

NOV lists an 8.25in collar with 2-13/16in bore and 6-5/8 REG connection. This gives a sourced generic collar reference. ENP3's supplied brochure specifies 6-5/8 F.H. Box/Pin and an optional REG crossover. Equal nominal connection sizes do not establish matching threadforms. Use a labeled unresolved adapter interface; do not model a certified thread or invent adapter length. [NOV public collar table, p2](https://assets.nov.com/NCP4N68N/at/kf3z37rbhs5v2xc842bnh9x/SpiralWate_DC_flyer_-_Letter_-_Web_22May2025.pdf), [SLB crossover definition](https://glossary.slb.com/en/terms/c/crossover).

## Measured compatibility, not an operating clearance recommendation

Centered straight-envelope calculations using the measured 304.800154mm tool:

- Tool to 12.25in open hole: **3.174923mm radial**.
- Tool to candidate casing nominal body ID: **6.540423mm radial**.
- Tool to reference drift: **4.559223mm radial**.
- 12.25in bit gauge to reference drift: **1.384300mm radial**.
- Ideal cement annulus between 17.5in host hole and 13.375in casing OD: **52.387500mm radial**, before eccentricity/washout. This follows the chosen sourced geometry; it is not a prescribed cement design/thickness.

These calculations establish plausible nominal geometry only. They do not certify connection restrictions, tolerances, collars/stabilizers, couplings/shoe, dogleg passage, flexure, load ratings, wear or operating safety. In particular the small lower open-hole gap limits illustrative inward rugosity/eccentricity: do not silently generate a colliding tight-hole variant. Preserve actual interference as a labeled failure case if that is the intended explanation. Spiral/rugosity amplitude and pitch are illustrative authoring parameters, not field measurements.

## MIT website finding

Visited the [public products index](https://mit-technologies.com/products/) and [smart drilling page](https://mit-technologies.com/smart-drilling-products/). The accessible material provides product/R&D context but no inspected ENP3 deployment schematic or dimensional BHA specification. The [motors page](https://mit-technologies.com/motors/) is password protected; it was not accessed past that boundary. Therefore the supplied ENP3 brochure and accepted T5 remain the product authority; another MIT product is not used as a surrogate ECCO specification.

## What this changes for T6

We now have a credible, source-backed **provisional illustration candidate**, rather than needing Radzi to supply every standard size. [Machine-readable proposal](../../../Shared/Assets/WellAssembly/config_researched-proposal_v002.json) records separate intervals and provenance. [Comparison diagram](Previews/researched-scenario_v002.png) shows the concentric envelopes to one scale. [Arithmetic checks](Evidence/researched-scenario-checks_v002.json) reproduce the values.

Actual MIT deployment O05 remains unresolved. Producer selection of this researched illustrative scenario is separate from MIT engineering approval. Complete certified BHA geometry, placement/datum and operational clearance cannot be inferred from these sources. No production configuration or current fixture has been silently overwritten, no downstream mechanism started, and no engineering decision is marked closed. T6 remains incomplete; the sourced candidate is ready for provisional-visual selection and later construction/review under the project boundaries.

## Local / remote state

All new outputs under `04-Production`; uncommitted/local, no push or client contact. Existing T5 and T6 evidence preserved. Source table screenshots were requested through web tools; only extracted text/numeric rows were available for inspection in this turn. No screenshot-based visual verification of manufacturer drawings is claimed. A recorded source reference is not an acquired reusable CAD asset or permission to republish manufacturer artwork. Report and candidate references are attached to T6; research completion does not complete the full construction ticket.

Research closure: four exact local output references attached to T6 alongside the original five. Bounded research run ended with cancelled execution status to avoid submitting incomplete full-ticket construction to Review; the research deliverables themselves are complete. T6 remains Blocked with the updated, narrower disposition: a researched provisional configuration is available, actual MIT deployment and placement/interfaces are unconfirmed. No task cancellation or self-acceptance is implied.
