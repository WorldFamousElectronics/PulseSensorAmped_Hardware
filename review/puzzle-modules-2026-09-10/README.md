# Puzzle module background iteration

Classification: DEVELOPMENT appearance study, 2026-09-10.

[Comparison](comparison.png) · [Back preview](puzzle-01-back.png) · [Editable vector proof](puzzle-01-back.svg) · [Visual history](review.html).

Six complementary colored areas replace the routed-net overlays, ground-plane shading, pad halos and dotted signal guides. Rounded puzzle tabs connect the visual regions:

- Teal: FILTER (C1, C3, C4).
- Purple: AMP + GAIN (U2, R5, R6).
- Berry: BIAS (R3, R4).
- Ochre: LED (D1, R1).
- Green: SENSE / input coupling (R2, C2; U1 is on the opposite face).
- Blue: POWER / connector (D2, C5, J1).

Colors describe functional areas, not shared electrical nets. White component references, module names and + / - markings remain. Shape seams are nominally 0.11 mm. Native component and pad geometry were copied in their exact board coordinates from color-10; no copper, footprint, LED or optical geometry was edited. The accepted back and deferred front artwork remain unchanged.

This is a vector positioning/appearance proof, not revised fabrication output. Color printing separations and supplier print review have not been prepared for this alternative.

`build_puzzle.py` rebuilds the SVG and PNG from existing native-derived vector polygons using Shapely and Pillow. It does not repaint raster board images. `log_iteration.py` appends contact sheet 23 and artifact 60. The first fit is retained in `iterations/01-first-fit/`; final cleanup removes tiny residual dotted-guide fragments from the source label polygons.
