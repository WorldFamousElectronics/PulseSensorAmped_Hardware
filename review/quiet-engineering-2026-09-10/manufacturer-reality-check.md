# Manufacturer reality check

Reviewed 2026-09-10. Classification: DEVELOPMENT feasibility research. This is a review of official published information, not vendor correspondence, a quotation or approval of our actual files. No supplier was contacted and no order was placed.

## Verdict

PCBWay and JLCPCB advertise a process capable of multicolor graphic areas like these. That does not establish exact matching of our RGB swatches. MacroFab advertises custom colors, but its published capabilities do not explicitly confirm six-color image printing on one PCB face. My practical first-proof recommendation is PCBWay; JLCPCB is an alternative with more file-preparation constraints.

## PCBWay — full-color process confirmed

Offers multicolor UV printing, matte by default, with a white solder-mask base on a fully printed side. Requires artwork, positioning reference and Gerbers together. The guidance supports common image/PDF formats, says normal prints survive SMT reflow, and requires avoiding pad openings. It also distinguishes the less durable printed ink from the mask beneath it. [Official color-printing guide](https://www.pcbway.com/blog/News/Unlock_Color_PCB_Printing_with_PCBWay_0939d559.html).

For this design: seek a matte sample, explicit confirmation that the opposite black optical mask stays unchanged, and approval of our small lettering/dotted boundaries. No exact color tolerance is published in the cited guide.

## JLCPCB — full-color process confirmed, workflow constrained

Requires EasyEDA Pro color-production exports. Listed options include white mask, 2/4 layers, 1 oz outer copper and ENIG. Assembly requires edge rails; panelization guidance needs careful reconciliation with the actual exported color files. [Official workflow](https://jlcpcb.com/help/article/how-to-design-multi-color-silkscreen-using-easyeda).

Our KiCad project plus an arbitrary image upload is not yet a compliant package. Their white-mask requirement leaves preservation of our opposite black optical face unresolved; a black printed overlay is not assumed optically equivalent to black mask.

Their general silkscreen guide recommends 0.15 mm lines and 0.8 mm text. The current 0.14 mm dots are smaller than that general line recommendation; obtain full-color-specific approval or revise the dots before fabrication. [General silkscreen guidance](https://jlcpcb.com/blog/pcb-silkscreen-printing-guide). This is not evidence of a confirmed 0.15 mm full-color dot limit.

## MacroFab — custom color possible; multicolor artwork unconfirmed

Lists standard colors and custom colors on request. Published rules include 0.127 mm minimum silkscreen size and 0.8 mm text height. These do not establish support for full-color image printing or exact matching of six adjacent colors. [Official capabilities](https://www.macrofab.com/capabilities).

Ask whether its fabrication partner can perform multicolor UV artwork plus assembly, with the existing black optical face. Treat this as a custom process inquiry, not a standard supported option.

## What needs a physical proof

The six deep board colors are design targets. Substrate, white underbase, ink, surface finish and curing can alter the result. Neither a hex code nor this screen rendering establishes a press color guarantee. The card uses deliberately lighter related tints, so the intended match is hue family rather than identical darkness across paper and PCB.

Before ordering the boards, request an actual-size sample or coupon with these swatches, 0.14 mm dots at 0.28 mm pitch, the smallest existing labels and the desired pad clearances. Ask for registration tolerance, minimum printable features, repeat-order color consistency, cleaning/reflow behavior, and the preferred image color space. Do not invent a CMYK conversion without the printer's process/profile.

The positioning SVG includes component illustrations and is a visual proof, not the production print layer. Prepare ink-only artwork, correct side orientation, native fab files and an explicit optical-face restriction before a supplier release. The board's 15.875 mm diameter makes fine-feature and registration review more consequential than the number of colors.

## Draft supplier inquiry — not sent

We are evaluating matte full-color artwork for the circuit face of a 15.875 mm circular, two-layer sensor PCB. The opposite optical face must retain its existing black solder mask, LED placement and optical window. Can your process print six adjacent muted color areas with white references and black dotted borders, while leaving all pad openings clear? Please confirm minimum text/line/dot sizes, registration and color tolerance, artwork/color-space requirements, assembly/reflow compatibility, and whether a physical color/legibility coupon can be supplied before a board order. Please explicitly confirm preservation of the opposite optical mask rather than substituting black printed ink.
