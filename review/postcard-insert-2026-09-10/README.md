# PulseSensor hardware postcard insert

DEVELOPMENT / packaging proof for the JST educational board. 2026-09-10.

## Accepted scope

Yury accepted the color-10 PCB back as a major milestone on 2026-09-10. Its source and graphics are unchanged. Front PCB graphic design is deferred. This work creates a packaging insert only.

The insert is hardware-only: exact PCB artwork, simplified schematic, reference BOM, color legend and TL;DR. It contains no fingers, anatomy, PPG explanation, or sensing-science illustration. A first image-generation direction was rejected by the user and is excluded from every final print file.

## Deliverables

- `output/PulseSensor-4x4-card.pdf`: two upright 4 × 4 inch faces.
- `output/PulseSensor-4x4-card-bleed.pdf`: two 4.25 × 4.25 inch pages, 4 × 4 trim box and 0.125 inch bleed on each edge.
- `output/card-1.png`, `output/card-2.png`: rendered review proofs.
- `build_postcard.py`: editable vector layout and schematic source, using ReportLab and embedded Arial fonts.

Print at 100%, with no fit-to-page scaling. Both faces are upright; the printer should confirm duplex orientation and paper/ink profile. Body/BOM text is approximately 7–9 points; schematic labels are 6.5 points. Inspect a physical-size proof before a packaging run. RGB artwork and colors require the printer's normal color conversion; this is not a certified PDF/X press profile.

## Accuracy and reading conventions

The board image is the unchanged `power-color-2026-09-09/color-10/back.png` artwork. It is a CAD-aligned illustration, enlarged on the postcard. U1 is on the other face and is explicitly identified as such.

The schematic is a manually laid-out, simplified electrical diagram. The 16 component references and 37 connected terminals were checked against the native exported netlist; see verification.json for the exact counted terminal total. Named labels carry shared connections: +V is input supply, PROT is the supply after D2, VREF is the bias midpoint, and OUT is J1 pin 3. U2's supply rails are stated as named connections; unused U1 pins are omitted. The LED branch remains electrically separate from the signal chain.

The compact BOM groups identical values. R1 is identified by its current-limit function because no single numeric resistance is established in the selected reference. No internal testing/population wording appears on the postcard. The table is a reader's reference, not an assembly purchasing BOM; full orderable MPNs and assembly instructions remain in the hardware package.

## Visual history and generation

`iterations/01-hardware-map` retains the first hardware-only proof; `iterations/02-bom-fit` retains the first BOM layout before margin refinements; `iterations/03-margin-check` retains the last spacing proof. The final postcard is appended to the shared contact sheets as sheet 21.

The built-in image-generation tool was used for an initial illustration concept, which the user rejected. The final PCB is existing native artwork; the schematic, BOM and text are vector-authored for fidelity and print clarity. No generated biology artwork is used in the final design. No PCB edits, supplier message, packaging order, or public product promotion was made.
