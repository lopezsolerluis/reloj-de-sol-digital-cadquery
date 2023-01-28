""" Digital Sundial - Continuous and Digital

Derivative from the wonderful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.

This demo at main.py will:

1. create a discrete sundial
2. export the sundial to STL and SVG
3. show the rendered model (ifn run in QC-editor > Editor window > Run )

"""
import pathlib,sys
import digital_sundial as dsd

# README:
#           replace next path with the actual location where you cloned/downloaded the project
#
sys.path.append("../reloj-de-sol-digital-cadquery")
f_out = pathlib.Path.home() / "digital_sundial"

def under_cq_editor() -> bool:
    """
    test whether run in QC-editor > Editor window
    :return: bool
    """
    return "show_object" in dir()

print("="*80+f"\n{__doc__}\n"+"="*80)
#
# 1st demo
#
if not under_cq_editor():
    print(
f"""- to manipulate the sundial under QC-Editor: 
        - copy the contents of main.py in "editor" window
        - correct the line that starts with "sys.path.append" (line ~18)
        - push "render" button (play) 
""")
b = dsd.base()
c = dsd.coupling().rotate((0, 0, dsd.semicylinder_radius / 2), (0, 1, dsd.semicylinder_radius / 2), 30).translate((0, 0, 2))
sundial_discrete_rotated = dsd.discrete_sundial([(12, 0)]).translate((-dsd.sundial_length / 2 - 40, 0, 2)).rotate(
    (0, 0, dsd.semicylinder_radius / 2), (0, 1, dsd.semicylinder_radius / 2), 30)
#
# 2nd demo
#
ext=".svg"
print(f"- exporting {ext.upper()} picture to {f_out}{ext}")
sundial_discrete_rotated.exportSvg(str(f_out)+ext)
#
# 3rd demo
#
ext=".stl"
print(f"- exporting {ext.upper()} model to {f_out}{ext}")
dsd.cq.exporters.export(sundial_discrete_rotated, fname=str(f_out)+ext)


