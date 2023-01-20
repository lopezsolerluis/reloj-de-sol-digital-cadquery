import cadquery as cq

hemisferio = "sur"
texto_1 = "Ab Revolutionibus Astri..."
texto_2 = "...Girum Orbis Noscimus"
alto_pixel = .75
ancho_pixel = 6
delta_alto  = 6.5
delta_ancho = 1.5
borde = 10
radio_semicilindro = 30
H = radio_semicilindro+10
largo_reloj = 21*ancho_pixel + 20*delta_ancho + 2*borde

cuerpo = cq.Workplane("XZ" ).cylinder(height=largo_reloj,
                                      radius=radio_semicilindro,
                                      angle=180)