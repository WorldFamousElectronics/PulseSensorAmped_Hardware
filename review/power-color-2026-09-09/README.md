# PulseSensor — larger front, polarity and full-color paths

DEVELOPMENT / manufacturing REVIEW candidates • 2026-09-09

Selected monochrome revision: **mono-08**. Selected PCBWay full-color iteration: **color-10**. Earlier mono-06 and color-07 are retained; the minus sign and LED-current arrow color were refined after viewing them. Color-09 retains a rejected renderer-color checkpoint; color-10 uses explicit opaque RGBA color metadata. KiCad still applies the F mask appearance across its render of both faces. Therefore the intended optical-front view uses mono-08, whose B-side geometry and black mask are identical. The uncorrected color-10/front.png render is retained as renderer evidence, not the intended optical finish.

## Front

The curved pulsesensor.com wordmark now has **1.35 mm x-height**, up from 0.80 mm (68.8%). This is the largest fit found in a 0.01 mm height / 0.025 mm radius search with the selected Arial Bold outlines, tracking and at least 0.20 mm wordmark-to-heart and edge gaps. It is not a claim that no other font/layout could be larger. A 0.20 mm rounding operation softens the bottom tip. The source website badge and optical macro photograph were visually inspected. The heart is still a reconstruction, not recovered historical-master artwork.

- [Website badge](https://pulsesensor.com/cdn/shop/files/1_150x@2x.png?v=1690061808)
- [Official optical front macro photograph](https://pulsesensor.com/cdn/shop/products/PulseSensorAmpedFinger-web_2_grande.jpg)

The optical window, D1, U1, every other footprint, copper segment, via, copper zone and board outline are unchanged from candidate-05. All five new native revisions passed that exact structural comparison. All have zero unconnected nets, zero schematic mismatches and only the original optical courtyard exception.

## Back and color key

- **Red:** positive input supply, /VDD_IN.
- **Amber:** diode-protected supply, /VDD_PROTECTED; also the separate LED cathode/current-limiting branch /LED_K. These are different nets: similar color does not connect them.
- **Cyan:** ground connections; **dark blue area:** the actual F-side ground plane, geometrically simplified for printing.
- **Purple:** retained logical signal guides.
- **+ / −:** supply and ground reference near the JST connector. Minus means GND / 0 V, not a separate negative-voltage supply. Pin 1 ground, pin 2 supply, pin 3 signal.

Solid colored routes follow F copper segments. Dashed colored routes project B-side segments into the same top view; they are not exposed F-side metal. Gaps keep labels and solder openings clear. A ground plane distributes return current across an area; its fill is not a prescribed single current trajectory. The LED current arrow is amber and points from the LED cathode toward R1. The purple circuit path represents signal processing, not DC passing through capacitor dielectric.

All colored routes are **printed ink over intact solder mask**. No copper has been exposed and no electrical rerouting was needed. The full-color back preview is a CAD-aligned vector positioning proof with schematic component bodies, not a photorealistic 3D rendering. The front and monochrome views are KiCad 3D renders; source model/tented-via appearance limitations remain.

## Manufacturing artifacts

- `mono-08-package`: updated conventional Gerber/drill/CPL/BOM/native/schematic review package.
- `color-10-package`: same electrical design, with PCBWay UV artwork and positioning files in `UV_PRINT`.
- `color-10/F-color-print.pdf`: exact 1:1, 15.875 mm square page. Also SVG and 2400 × 2400 transparent PNG (3840 dpi). The circle and all openings are registered to native board coordinates.
- F means the circuit back. UV is requested only on F. B is the black/white optical front.
- Full-area color F is white solder mask with dark UV ink background. Request black B mask; supplier must confirm the mixed-side process. PCBWay F silkscreen Gerber is a placement reference for the supplied color replacement, **not an additional white overprint**. B white silkscreen remains conventional.
- User.1–User.4 contain native reference paths for input supply, protected supply, ground and LED cathode respectively. Standard KiCad 3D cannot display the multicolor legend; the UV artwork is authoritative for color.
- Minimum measured colored artwork to mask-opening distance is 0.1536 mm. Optical front minimum is 0.1584 mm. New wordmark edge gap is 0.2241 mm. These are geometric checks, not supplier print-registration approval.

## Release status

Both packages remain **on HOLD for release review**. Retain the original optical-courtyard exception for formal review, verify the mesh-only D1/D2/U1 mechanical models and required independent mechanical evidence, complete the hardware workflow's repeat-build and human Gerber/assembly reviews, reconcile the supplier process and obtain release approval. No new layout bench testing or supplier print proof has occurred. Original BOM/population selections remain unchanged; old lot identifiers/quantities are provenance, not authorization for a new order. No upload, order or supplier message was sent.

See [SUPPLIERS.md](SUPPLIERS.md), [verification.json](verification.json), the individual DRC reports and [review.html](review.html). The shared contact-sheet collection has been extended without replacing sheets 01–09. The routing-attempt ledger retains the earlier partial/rejected native files locally.
