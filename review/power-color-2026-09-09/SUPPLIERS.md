# Color printing supplier comparison

Checked 2026-09-09. Public documentation only; no supplier contacted, files uploaded, price quoted or order placed.

| Supplier | Verified capability | Consequence for this design |
| --- | --- | --- |
| PCBWay | Matte UV multicolor printing; separate print image and positioning reference accepted alongside Gerbers. Full-area printing uses white mask on that side. | Primary artwork package uses a dark UV background over white F mask; black B optical mask is requested and needs quote reconciliation. Keep the 1:1 PDF/PNG and positioning proof together. |
| JLCPCB | Multicolor service, with current documentation requiring EasyEDA Pro color production files. Listed constraints include white mask, 2/4 layers, 1 oz copper and ENIG. Assembly requires customer panel edge rails. | Concept is visually portable, but this KiCad package is not a JLC color-order file. Requires a separately verified EasyEDA/panel export and finish/mask reconciliation. |
| MacroFab | Official documentation lists selectable silkscreen colors. No official full-color UV/CMYK offering was found. | Do not assume multiple simultaneous colors are available; treat full-color as unconfirmed and retain the monochrome candidate. |

Primary sources:

- [PCBWay UV color-printing instructions](https://www.pcbway.com/blog/News/Unlock_Color_PCB_Printing_with_PCBWay_0939d559.html)
- [PCBWay color-printing mask policy](https://www.pcbway.com/blog/PCB_Manufacturing_Information/How_should_the_solder_mask_color_be_chosen_for_color_printed_PCBs_65c898fe.html)
- [JLCPCB color design/export instructions](https://jlcpcb.com/help/article/how-to-design-multi-color-silkscreen-using-easyeda)
- [MacroFab PCB specifications](https://help.macrofab.com/knowledge/pcb-specifications-and-drc)
- [MacroFab specification PDF](https://help.macrofab.com/hubfs/PCB_Specifications.pdf)

PCBWay's standard legend guidance specifies 0.8 mm text height and 0.15 mm stroke. We retained these conservative design targets rather than assuming UV printing permits smaller marks. Color registration and minimum isolated UV features require supplier confirmation; RGB screen previews are not contractual printed-color matches.

[PCBWay legend guidance](https://www.pcbway.com/helpcenter/design_instruction/How_to_make_my_silkscreen_clear_and_beautiful_on_PCB__.html)
