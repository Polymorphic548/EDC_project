# Trimmer photo review — 28 October 2026

The user supplied three photos of a small green, round, three-terminal preset and reported an approximate 7.5 mm body dimension. The photos have no measurement scale and do not show a legible model/resistance marking or an unambiguous bottom view of the lead centres.

**Finding:** the visible construction resembles an RM065-style single-turn carbon trimmer. This is a candidate identification, not a confirmed manufacturer/model. It differs from the original inventory's description of a 500 ohm multiturn trimmer. Three pins and an approximate body diameter are insufficient to select the final PCB footprint.

Cross-checked against the manufacturer-authored Runtron RM065/RM063 datasheet, hosted at:

https://uelectronics.com/wp-content/uploads/2018/09/Preset-Potentiometer-Trimpot.pdf

The sheet identifies these as single-turn parts and includes a 7.5 mm dimension in the RM065 outline. It specifies different mechanical styles for RM065 and RM063; body dimensions must not be mistaken for hole spacing. Its resistance table maps **501 to 500 ohm** (502 would mean 5 kohm). The photos do not establish either code. The installed KiCad library includes both Runtron RM-065 and RM-063 footprints, but neither is selected based on this tentative identification.

Before applying a footprint, obtain the model/marking or measure the pin centres and their offset from the body. Verify the wiper electrically. With the loose component disconnected, the two end terminals have a roughly constant total resistance while turning; resistance from the wiper to an end varies. Confirm the total resistance is approximately the intended 500 ohm and that a setting near 119.8 ohm is attainable. Do not assume the physically middle pin is the wiper without checking the part or its datasheet.

**Design action:** no copper, schematic connection, or footprint changes were made from this tentative photo identification. RV1 remains `Project:RV1_PENDING`. The reserved space is still available for the confirmed part.
