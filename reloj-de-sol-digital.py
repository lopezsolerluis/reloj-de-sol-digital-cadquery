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
 
def n_a_digito(n,p):
  return trunc(n/10**p)%10

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
  return cq.Workplane("YZ").polyline(vertices).close().extrude(ancho_pixel/2,both=True)
    
def digito(numero,alfa1,alfa2):
    result = cq.Workplane()
    for i in range(6):
      for j in range(4):
        digito = digitos[numero]
        if (digito[i][j]==1):
            x = -(j-1.5)*(ancho_pixel+delta_ancho)
            y =  (i-2.5)*(alto_pixel+delta_alto)            
            result.add(haz_de_sol(alfa1,alfa2).translate((x,y,0)))
    return result
  
def separador(alfa1,alfa2):
  result = cq.Workplane()  
  for i in [-1,1]:
      result.add(haz_de_sol(alfa1,alfa2).translate([0,i*0.5*(alto_pixel+delta_alto), 0]))
  return result

def hora_solar(horas, minutos):
  hora = horas+minutos/60;
  #assert(hora>6 && hora<18,"La hora debe encontrarse entre las 6:00 y las 18:00.");
  alpha = alfa(hora)
  hora_decenas = n_a_digito(horas,1)
  hora_unidades = n_a_digito(horas,0)
  minuto_decenas = n_a_digito(minutos,1)
  minuto_unidades = n_a_digito(minutos,0)
                    
  delta_y = ancho_pixel+delta_ancho
  
  result = cq.Workplane()
  # horas    
  if (hora_decenas != 0):    
      result.add(digito(hora_decenas,alpha,alpha).translate([8.5*delta_y,0,0]))
  result.add(digito(hora_unidades,alpha,alpha).translate([3.5*delta_y,0,0]))
  # minutos
  result.add(digito(minuto_decenas,alpha,alpha).translate([-3.5*delta_y,0,0]))
  result.add(digito(minuto_unidades,alpha,alpha).translate([-8.5*delta_y,0,0]))
  # separador
  result.add(separador(alpha,alpha))
  return result

def cuerpo():
    return cq.Workplane("YZ" ).cylinder(height=largo_reloj,
                                        radius=radio_semicilindro,
                                        angle=180)
      
def reloj_de_sol_discreto(vector_horas):
    horas = cq.Workplane()         
    for hora_minutos in vector_horas:
      hora=hora_minutos[0];
      minutos=hora_minutos[1];
      horas.add(hora_solar(hora,minutos))
    return cuerpo().cut(horas)
    
r = reloj_de_sol_discreto([(12,0),(15,23),(8,10)])
#reloj = cuerpo.cut(hora_solar(12,0))

