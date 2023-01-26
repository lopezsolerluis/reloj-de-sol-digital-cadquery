""" Digital Sundial - Continuous and Digital

Derivative from the wonderful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.

This demo at main.py will:

- create a discrete sundial
- export the sundial to STL and SVG

"""
import digital_sundial as dsd
import pathlib

f_out = pathlib.Path.home() / "digital_sundial"
b = dsd.base()
c = dsd.coupling().rotate((0, 0, dsd.semicylinder_radius / 2), (0, 1, dsd.semicylinder_radius / 2), 30).translate((0, 0, 2))
sundial_discrete_rotated = dsd.discrete_sundial([(12, 0)]).translate((-dsd.sundial_length / 2 - 40, 0, 2)).rotate(
    (0, 0, dsd.semicylinder_radius / 2), (0, 1, dsd.semicylinder_radius / 2), 30)
print("="*80+f"\n{__doc__}\n"+"="*80)
#
# 1st demo
#
ext=".svg"
print(f"exporting {ext.upper()} picture to {f_out}{ext}")
sundial_discrete_rotated.exportSvg(str(f_out)+ext)
#
# 2nd demo
#
ext=".stl"
print(f"exporting {ext.upper()} model to {f_out}{ext}")
dsd.cq.exporters.export(sundial_discrete_rotated, fname=str(f_out)+ext)


