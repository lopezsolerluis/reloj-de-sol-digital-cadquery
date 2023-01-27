""" Digital Sundial - Continuous and Digital

Derivative from the wonderful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.

"""

import cadquery as cq
from math import trunc, radians, tan
from collections import defaultdict

__all__ = list()

#
# default configuration for the package, if not read from 'config.json'
#
config = defaultdict(lambda: None)

hemisphere = "sur"
text_1 = "NON EST AD ASTRA..."
text_2 = "...MOLLIS E TERRIS VIA"
pixel_height = .75
pixel_width = 6
delta_height = 6.5
delta_width = 1.5
border = 10
semicylinder_radius = 30
length_coupling = 20
pins_height = 7
pins_width = 5
pins_angle = 60
pins_length = 8
pin_distance = semicylinder_radius * .6
axis_radius = 2.5
base_radius = semicylinder_radius + 15
base_height = 2
pillar_width = 5
pillar_separation = .2

#
# end of config
#

H = semicylinder_radius + 10
sundial_length = 21 * pixel_width + 20 * delta_width + 2 * border
delta_x = pixel_width + delta_width


digits = [[[0, 1, 1, 0],  # zero
           [1, 0, 0, 1],
           [1, 0, 1, 1],
           [1, 1, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 0]],
          [[0, 1, 0, 0],  # one
           [1, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [1, 1, 1, 0]],
          [[0, 1, 1, 0],  # two
           [1, 0, 0, 1],
           [0, 0, 0, 1],
           [0, 1, 1, 0],
           [1, 0, 0, 0],
           [1, 1, 1, 1]],
          [[0, 1, 1, 0],  # three
           [1, 0, 0, 1],
           [0, 0, 1, 1],
           [0, 0, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 0]],
          [[1, 0, 0, 1],  # four
           [1, 0, 0, 1],
           [1, 0, 0, 1],
           [1, 1, 1, 1],
           [0, 0, 0, 1],
           [0, 0, 0, 1]],
          [[1, 1, 1, 1],  # five
           [1, 0, 0, 0],
           [1, 1, 1, 0],
           [0, 0, 0, 1],
           [0, 0, 0, 1],
           [1, 1, 1, 0]],
          [[0, 1, 1, 0],  # six
           [1, 0, 0, 0],
           [1, 1, 1, 0],
           [1, 0, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 0]],
          [[1, 1, 1, 0],  # seven
           [0, 0, 1, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0],
           [0, 1, 0, 0]],
          [[0, 1, 1, 0],  # eight
           [1, 0, 0, 1],
           [0, 1, 1, 0],
           [1, 0, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 0]],
          [[0, 1, 1, 0],  # nine
           [1, 0, 0, 1],
           [1, 0, 0, 1],
           [0, 1, 1, 1],
           [0, 0, 0, 1],
           [0, 1, 1, 0]]]

__all__.append("digits")


def digit_of_number(n, p):
    return trunc(n / 10 ** p) % 10


def alpha_south(hour):
    return 270 - 15 * hour


def alpha_north(hour):
    return 15 * hour - 90


def hour_to_alpha(hour):
    if hemisphere == "sur":
        return alpha_south(hour)
    else:
        return alpha_north(hour)


def sun_beam(alpha1, alpha2):
    alpha_min = min(alpha1, alpha2)
    alpha_max = max(alpha1, alpha2)
    D1 = H / tan(radians(alpha_min))
    D2 = H / tan(radians(alpha_max))
    vertices = [(-pixel_height / 2, 0, 0),
                (D2 - pixel_height / 2, H, 0),
                (D1 + pixel_height / 2, H, 0),
                (pixel_height / 2, 0, 0)]
    return cq.Workplane("YZ").polyline(vertices).close().extrude(pixel_width / 2, both=True)


def digit(number, alpha1, alpha2):
    digit = digits[number]
    result = cq.Workplane()
    for i in range(6):
        for j in range(4):
            if (digit[i][j] == 1):
                x = -(j - 1.5) * (pixel_width + delta_width)
                y = (i - 2.5) * (pixel_height + delta_height)
                result.add(sun_beam(alpha1, alpha2).translate((x, y, 0)))
    return result


def delimiter(alpha1, alpha2):
    result = cq.Workplane()
    for i in [-1, 1]:
        result.add(sun_beam(alpha1, alpha2).translate([0, i * 0.5 * (pixel_height + delta_height), 0]))
    return result


def sun_hour(hours, minutes):
    hour = hours + minutes / 60;
    # assert(hour>6 && hora<18,"La hora debe encontrarse entre las 6:00 y las 18:00.");
    alpha = hour_to_alpha(hour)
    tens_of_hours = digit_of_number(hours, 1)
    units_of_hour = digit_of_number(hours, 0)
    tens_of_minutes = digit_of_number(minutes, 1)
    units_of_minutes = digit_of_number(minutes, 0)

    result = cq.Workplane()
    # hours
    if (tens_of_hours != 0):
        result.add(digit(tens_of_hours, alpha, alpha).translate([8.5 * delta_x, 0, 0]))
    result.add(digit(units_of_hour, alpha, alpha).translate([3.5 * delta_x, 0, 0]))
    # minutes
    result.add(digit(tens_of_minutes, alpha, alpha).translate([-3.5 * delta_x, 0, 0]))
    result.add(digit(units_of_minutes, alpha, alpha).translate([-8.5 * delta_x, 0, 0]))
    # delimiter
    result.add(delimiter(alpha, alpha))
    return result


def text_to_cut(text, x):    
    delta_a = 160 / (len(text) - 1)
    result = cq.Workplane("XY")
    for i in range(len(text)):
        c = text[i]
        if c != " ":
            result.add(cq.Workplane().text(c, 5, 2).
                       rotate((0, 0, 0), (0, 0, 1), 90).
                       translate((x, 0, semicylinder_radius - 2)).
                       rotate((0, 0, 0), (1, 0, 0), -i * delta_a + 90 - 10))
    return result


def sundial_body():
    body = (cq.Workplane("YZ").cylinder(height=sundial_length,
                                        radius=semicylinder_radius,
                                        angle=180)
            .faces(">X").edges("<Z")
            .workplane(centerOption="CenterOfMass")
            .center(0, pins_height / 2)
            .pushPoints([(-pin_distance, 0), (pin_distance, 0)])
            .sketch()
            .trapezoid(pins_width, pins_height, -pins_angle)
            .finalize()
            .cutBlind(-pins_length)
            )
    body = (body.cut(text_to_cut(text_1, -sundial_length / 2 + 5))
            .cut(text_to_cut(text_2, sundial_length / 2 - 5)))
    return body


def discrete_sundial(vector_hours):
    '''Digital sundial for some selected hours. 'vector_hours' is a vector with the hours and minutes the user wishes to show; p ej.: [(12,00), (7,13), (16,23)] represents 12:00, 7:13 y 16:23.'''
    c = sundial_body()
    for hour, minutes in vector_hours:
        c = c.cut(sun_hour(hour, minutes))
    return c


def continuous_sundial():
    '''Digital sundial with the hours from 9:00 to 15:10, in intervals of 20 minutes.'''
    c = sundial_body()
    # units of minutes
    c = c.cut(digit(0, hour_to_alpha(9), hour_to_alpha(15 + 10 / 60)).translate([-8.5 * delta_x, 0, 0]))
    # tens of minutes
    for hour in range(9, 15):
        for minutes in (0, 20, 40):
            tens_of_minutes = digit_of_number(minutes, 1)
            c = c.cut(digit(tens_of_minutes,
                            hour_to_alpha(hour + minutes / 60),
                            hour_to_alpha(hour + (minutes + 10) / 60)).translate([-3.5 * delta_x, 0, 0]))
    c = c.cut(digit(0, hour_to_alpha(15), hour_to_alpha(15 + 10 / 60)).translate([-3.5 * delta_x, 0, 0]))
    # delimiter
    c = c.cut(delimiter(hour_to_alpha(9), hour_to_alpha(15 + 10 / 60)))
    # units of hours
    for hour in range(9, 16):
        units_of_hour = digit_of_number(hour, 0)
        c = c.cut(digit(units_of_hour,
                        hour_to_alpha(hour),
                        hour_to_alpha(hour + 50 / 60 if hour < 15 else hour + 10 / 60)).translate(
            [3.5 * delta_x, 0, 0]))
    # tens of hours
    c = c.cut(digit(1, hour_to_alpha(10), hour_to_alpha(15 + 10 / 60)).translate([8.5 * delta_x, 0, 0]))
    return c


def base():
    base = (cq.Workplane("XY")
            .cylinder(height=base_height, radius=base_radius)
            .faces(">Z").workplane().tag("top-face")
            .center(base_radius - 18, -5)
            .cylinder(5, 5, centered=False)
            .faces(">Z")
            .cskHole(4, 8, 82, depth=None)
            .workplaneFromTagged("top-face")
            .pushPoints([(0, base_radius - semicylinder_radius / 2 + pillar_width / 2 + pillar_separation),
                         (0, -(base_radius - semicylinder_radius / 2 + pillar_width / 2 + pillar_separation))])
            .rect(semicylinder_radius, pillar_width).extrude(semicylinder_radius + base_height / 2)
            .faces(">Z").edges("|Y").fillet(semicylinder_radius / 2.01)
            .faces(">Y").workplane()
            .center(0, semicylinder_radius / 2 + base_height / 2)
            .circle(2 * axis_radius).cutThruAll()
            )
    return base


def coupling():
    body = (cq.Workplane("YZ")
            .cylinder(height=length_coupling,
                      radius=semicylinder_radius, angle=180)
            .translate((-length_coupling / 2 - 1, 0, 0))  # Why can't I put this _on_ YZ' plane?
            .faces("<X").edges("<Z")
            .workplane(centerOption="CenterOfMass")
            .center(0, pins_height / 2)
            .pushPoints([(-pin_distance, 0), (pin_distance, 0)])
            .sketch()
            .trapezoid(pins_width, pins_height, -pins_angle)
            .finalize()
            .extrude(pins_length)
            .copyWorkplane(cq.Workplane("XZ"))
            .center(0, semicylinder_radius / 2)
            .cylinder(height=2 * semicylinder_radius,
                      radius=semicylinder_radius / 2)
            .faces("XZ").workplane()
            .circle(2 * axis_radius).cutThruAll()
            )
    return body


if __name__ == '__main__':
    print("WARN: module not intended to be run direcly")
    #
    b = base()
    c = coupling().rotate((0, 0, semicylinder_radius / 2), (0, 1, semicylinder_radius / 2), 30).translate((0, 0, 2))
    sundial_discrete_rotated = discrete_sundial([(12, 0)]).translate((-sundial_length / 2 - 40, 0, 2)).rotate(
        (0, 0, semicylinder_radius / 2), (0, 1, semicylinder_radius / 2), 30)
    # sundial_rotated = continuous_sundial().translate((-sundial_length/2-40,0,2)).rotate((0,0,semicylinder_radius/2),(0,1,semicylinder_radius/2),30)
    # sundial_1 = continuous_sundial()
    # sundial_2 = discrete_sundial([(12,0),(15,23),(8,10)])
