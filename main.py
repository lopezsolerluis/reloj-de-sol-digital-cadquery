""" Digital Sundial - Continuous and Digital

Inspired in the wonderful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.
Adapted from [one of the authors' version in OpenSCAD](https://github.com/lopezsolerluis/reloj-de-sol-digital).

This demo at main.py will:

1. create a discrete sundial
2. export the sundial to STL and SVG
3. same with the base (loop previous steps)
4. if run in QC-editor, will show the rendered model. Instructions:
    1. menu **file** > **open**
    2. menu **run** > **render** or hit `Run` button
    3. please, check `Log Viewer` window

"""
import os, pathlib, sys, random, logging
import digital_sundial as dsd

# Parts available for creation. Each item is: key: Part name, value: a) color index, 
# b) parameters to give to the corresponding part, and 
# c) parameters for the corresponding rotations or translations
parts_available = {
    "base": [1,None,[]],
    "coupling": [4,None,[[dsd.rotation_axis_origin, dsd.rotation_axis_end, 30],
                             [[0, 0, 2]]]],
    "sundial": [1,[(12,0)],[[[-dsd.sundial_length / 2 - 40, 0, 2]], # For discrete sundial
                                [dsd.rotation_axis_origin, dsd.rotation_axis_end, 30]]] 
#         ["sundial",1,None,[[[-dsd.sundial_length / 2 - 40, 0, 2]],  # For continuous sundial
#                            [dsd.rotation_axis_origin, dsd.rotation_axis_end, 30]]]
}
# Parts to create.
parts = ["base", "coupling", "sundial"]
# Extensions to export
file_types = ["svg", "stl"]

# README:
#           You might need to replace next path with the actual location where you cloned/downloaded the project
#
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
        - might need to correct the line that starts with "sys.path.append" (line ~18)
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

for name in parts:
    if part_props := parts_available.get(name):
        color_index_int, params, transforms = part_props
        color_index = str(color_index_int)
        asm.add(exportRotoTranslate(name, params, transforms), name=name, color=dsd.cq.Color(base_color + color_index))


if under_cq_editor():
    show_object(asm)
else:
    pass