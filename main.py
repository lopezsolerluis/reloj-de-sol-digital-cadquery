""" Digital Sundial - Continuous and Digital

Inspired in the wonderful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.
Adapted from [one of the authors' version in OpenSCAD](https://github.com/lopezsolerluis/reloj-de-sol-digital).

With this demo at main.py you can:

1. create a discrete or continuous sundial, both in one part or two halves
2. create a base and a copupling
3. export everything to STL and SVG
4. if run in QC-editor, will show the rendered model. Instructions:
    1. menu **file** > **open**
    2. menu **run** > **render** or hit `Run` button
    3. please, check `Log Viewer` window

"""
import os, pathlib, sys, random, logging
import digital_sundial as dsd

# Parts available for creation. Each item is: I) key: part name; II) value: a) color index,
# b) parameters for the corresponding rotations or translations (possibly empty)
parts_available = {
    "base": [1,[]],
    "coupling": [4,[[dsd.rotation_axis_origin, dsd.rotation_axis_end, 30],
                    [[0, 0, 2]]]],
    "sundial": [1,[[[-dsd.sundial_length / 2 - 40, dsd.semicylinder_radius*1.2, 2]],
                   [dsd.rotation_axis_origin, dsd.rotation_axis_end, 30]]],
    "sundial_top": [1,[[[-dsd.sundial_length / 2 - 55, -dsd.semicylinder_radius*1.2, 2]],
                       [dsd.rotation_axis_origin, dsd.rotation_axis_end, 30]]],
    "sundial_bottom": [1,[[[-dsd.sundial_length / 2 - 40, -dsd.semicylinder_radius*1.2, 2]],
                          [dsd.rotation_axis_origin, dsd.rotation_axis_end, 30]]]
}
# Parts to create. If any part has parameters (as a discrete sundial), they must be declared in a vector.
#parts = ["base", "coupling", "sundial", "sundial_top", "sundial_bottom"]
parts = ["base", "coupling", ["sundial", [(12,0)]], ["sundial_top", [(12,0)]], ["sundial_bottom", [(12,0)]]]
#parts = ["base", "coupling", ["sundial",[(12,0),(15,40)]]] # Discrete sundial
#parts = ["base", "coupling", "sundial"] # Continuous sundial
# Extensions to export
file_types = ["svg", "stl"]

# You might need to replace next path with the actual location where you cloned/downloaded the project
sys.path.append("../reloj-de-sol-digital-cadquery")
# files will be created at the directory: d_out_base/d_out
d_out_base = pathlib.Path.home()
d_out = "digital sundial"

try:
    os.mkdir(d_out_base / d_out)
    raise FileExistsError
except FileExistsError as e:
    d_out = d_out_base / d_out
except Exception as e:
    logger.info(f"ERR: creating directory {e}")
    d_out = d_out_base


def under_cq_editor() -> bool:
    """
    test whether run in QC-editor > Editor window

    :return: bool
    """
    return "show_object" in globals()


def exportRotoTranslate(name, params, transforms):
    """
    posponing rototranslation in cq.Assembly after STL exports

    :param: name, params, transforms
    :return:
    """

    part_func_name = getattr(dsd, name)
    part = part_func_name(params) if params else part_func_name()

    def export_part(ext):
        #
        # parts export
        #
        global d_out
        nonlocal name

        f_out = d_out / (name + "." + ext)
        ext_type = "picture" if ext=="svg" else "model"
        logger.info(f"- exporting {ext.upper()} {ext_type} to {f_out}")
        dsd.cq.exporters.export(part, fname=str(f_out))

    for ext in file_types:
        export_part(ext)

    result = part
    for transform in transforms:
        result = result.translate(transform[0]) if len(transform)==1 else result.rotate(transform[0], transform[1], transform[2])
    return result


if under_cq_editor():
    #
    # Running CQ-Editor , please check "LOG VIEWER" window
    #
    log_format = "%(levelname)s - %(message)s"
else:
    log_format = "%(message)s"

logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger()

logger.info("=" * 80 + f"\n{__doc__}\n" + "=" * 80)
#
# 1st demo
#
if under_cq_editor():
    print("=" * 80 + f"\n output is redirected to `Log Viewer` window in CQ-Editor\n" + "=" * 80)
else:
    logger.info(
        f"""- to manipulate the sundial under QC-Editor: 
        - open `main.py` (menu **file**)
        - might need to correct the line that starts with "sys.path.append" (line ~38)
        -.change (if you will) the parts to create in line ~30
        - push **render** button (play) 
""")

#
# building the assembly and exporting each part
#

asm = dsd.cq.Assembly()

#
# asm colors from https://dev.opencascade.org/doc/refman/html/_quantity___name_of_color_8hxx.html
#            from https://techoverflow.net/2019/06/14/overview-of-all-standard-colors-available-in-opencascade/
#
base_color = ["darkslategray", "deepskyblue", "coral", "lightblue"] # "grey6"  # has to have 4 or more variants
base_color = random.choice(base_color)

for part in parts:
    has_params = type(part)==list
    name = part[0] if has_params else part
    if part_props := parts_available.get(name):
        color_index_int, transforms = part_props
        params=part[1] if has_params else None
        color_index = str(color_index_int)
        asm.add(exportRotoTranslate(name, params, transforms), name=name, color=dsd.cq.Color(base_color + color_index))


if under_cq_editor():
    show_object(asm)
else:
    pass
