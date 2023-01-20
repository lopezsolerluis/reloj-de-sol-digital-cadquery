import cadquery as cq
from math import trunc, radians, tan

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

digitos = [
[[0, 1 ,1, 0], # cero
 [1, 0, 0, 1],
 [1, 0, 1, 1],
 [1, 1, 0, 1],
 [1, 0, 0, 1],
 [0, 1, 1, 0]],
[[0, 1, 0 ,0], # uno
 [1, 1, 0, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0],
 [1, 1, 1, 0]],
[[0, 1 ,1, 0], # dos
 [1, 0, 0, 1],
 [0, 0, 0, 1],
 [0, 1, 1, 0],
 [1, 0, 0, 0],
 [1, 1, 1, 1]],
[[0, 1 ,1, 0],  # tres
 [1, 0, 0, 1],
 [0, 0, 1, 1],
 [0, 0, 0, 1],
 [1, 0, 0, 1],
 [0, 1, 1, 0]],
[[1, 0 ,0, 1],  # cuatro
 [1, 0, 0, 1],
 [1, 0, 0, 1],
 [1, 1, 1, 1],
 [0, 0, 0, 1],
 [0, 0, 0, 1]],
[[1, 1 ,1, 1],  # cinco
 [1, 0, 0, 0],
 [1, 1, 1, 0],
 [0, 0, 0, 1],
 [0, 0, 0, 1],
 [1, 1, 1, 0]],
[[0, 1 ,1, 0],  # seis
 [1, 0, 0, 0],
 [1, 1, 1, 0],
 [1, 0, 0, 1],
 [1, 0, 0, 1],
 [0, 1, 1, 0]],
[[1, 1 ,1, 0],  # siete
 [0, 0, 1, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0],
 [0, 1, 0, 0]],
[[0, 1 ,1, 0],  # ocho
 [1, 0, 0, 1],
 [0, 1, 1, 0],
 [1, 0, 0, 1],
 [1, 0, 0, 1],
 [0, 1, 1, 0]],
[[0, 1 ,1, 0],  # nueve
 [1, 0, 0, 1],
 [1, 0, 0, 1],
 [0, 1, 1, 1],
 [0, 0, 0, 1],
 [0, 1, 1, 0]]]
 
def alfa_sur(hora):
    return 270-15*hora

def alfa_norte(hora):
    return 15*hora-90

def alfa(hora):
  if hemisferio=="sur":
      return alfa_sur(hora)
  else:
      return alfa_norte(hora)
  
def haz_de_sol(alfa1,alfa2):
  alfa_min = min(alfa1,alfa2)
  alfa_max = max(alfa1,alfa2)
  D1 = H/tan(radians(alfa_min))
  D2 = H/tan(radians(alfa_max))
  vertices = [(-alto_pixel/2,0,0),
              (D2-alto_pixel/2,H,0),
              (D1+alto_pixel/2,H,0),
              (alto_pixel/2,0,0)]
  return cq.Workplane("XZ").polyline(vertices).close().extrude(ancho_pixel,both=True)
    
cuerpo = cq.Workplane("XZ" ).cylinder(height=largo_reloj,
                                      radius=radio_semicilindro,
                                      angle=180)

reloj = cuerpo.cut(haz_de_sol(45,60))