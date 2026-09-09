# PulseSensor JST educational board — review candidate

DEVELOPMENT • 2026-09-09 • PulseSilverBookPro

This is a concrete native CAD and manufacturing-export candidate, not an approved production release. No supplier upload or order has been made.

## Design

15.875 mm circular board, 1.6 mm thick. Black solder mask, white silkscreen on both sides. User-facing optical front is KiCad B side; circuit back is KiCad F side. D1, U1, J1 and board outline are unchanged. Twelve passive/diode parts were rearranged and copper rerouted; all original pin-to-net connections and local pad geometries are preserved.

The front uses a photo-reconstructed heart and curved pulsesensor.com wordmark. It is not verified against an original historical artwork master. Back lettering identifies parts and functional groups; dotted guides describe signal connections with deliberate gaps at crossings and text. They are explanatory ink, not a complete depiction of copper or current flow. The solid arrow describes conventional current on the LED cathode-to-resistor branch. Capacitors do not carry steady DC through their dielectric. The full component-function key is in the review page.

## Evidence

All 16 geometry/electrical comparison checks passed: zero unconnected nets, zero schematic parity issues, ERC clear, fixed optics preserved, correct 16-component placement export and unchanged controlled component selections. Native candidate SHA-256: 035ff099151d272f77bd0d54e158b8264b486bc1b7c166ecc0c92d3a766d4b6a.

DRC retains one original D1 optical NPTH / U1 courtyard exception. No new DRC warnings. Measured silk-to-opening clearance is at least 0.1536 mm on F and 0.1584 mm on B. Lettering targets 0.8 mm height and 0.15 mm strokes; full glyph stem metrology and supplier print reconciliation remain to be completed. See VALIDATION.

## Manufacturing review notes / hold points

- This package is on HOLD for release. Existing optical courtyard exception needs the formal review/waiver required by the hardware workflow.
- D1, D2 and U1 source models are mesh-only; verified STEP-capable models and independent mechanical inspection remain outstanding. Rendered component bodies are illustrative and do not constitute mechanical proof.
- Ten populated views are supplied. KiCad renders can display via holes/rings despite native tenting flags. Fabrication mask data and supplier tenting capability govern actual appearance; verify tenting for the 0.30 mm drills.
- Gerbers, drill and CPL share the original auxiliary origin (92.0625, 107.9375). CPL uses the native KiCad side/rotation convention. Confirm the supplier’s assembly interpretation before release.
- The controlled BOM and population matrix are byte-for-byte copies of the original submitted selections. Their original lot quantities/identifiers are provenance, not authorization for a new order. Reconcile the new lot explicitly before ordering.
- Human Gerber and assembly review, required repeat-build evidence, fabricator reconciliation and CEO release approval remain pending. This rearranged layout has not been bench validated.

## Provenance

Submitted source archive SHA-256: 0afda167b52ab0b0251cf22f91fd92fefa5dcf5e74f67b36446e7ec775acf792.
Submitted native PCB SHA-256: b439dcff82c4553731ac35ebcd27276899f8dfbbfcd35f2351d8101497eb4ad4.
Source: PulseSensor-Amped-B-PCBWay-EVT-RC3-R1-FINAL / SOURCE_SUPPORT / PulseSensor-Amped-B-JST.kicad_pcb.

Python crash dialogs were traced to KiCad pcbnew helper shutdown. Final metadata edits used standard Python text parsing and KiCad CLI checks/exports; the crash-prone helpers are no longer used.
