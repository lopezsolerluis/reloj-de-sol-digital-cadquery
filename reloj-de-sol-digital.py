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
                    
  delta_x = ancho_pixel+delta_ancho
  
  result = cq.Workplane()
  # horas    
  if (hora_decenas != 0):    
      result.add(digito(hora_decenas,alpha,alpha).translate([8.5*delta_x,0,0]))
  result.add(digito(hora_unidades,alpha,alpha).translate([3.5*delta_x,0,0]))
  # minutos
  result.add(digito(minuto_decenas,alpha,alpha).translate([-3.5*delta_x,0,0]))
  result.add(digito(minuto_unidades,alpha,alpha).translate([-8.5*delta_x,0,0]))
  # separador
  result.add(separador(alpha,alpha))
  return result

def cuerpo():
    return cq.Workplane("YZ").cylinder(height=largo_reloj,
                                       radius=radio_semicilindro,
                                       angle=180)
      
def reloj_de_sol_discreto(vector_horas):
    '''Reloj de Sol de algunas horas puntuales. 'vector_horas' es un vector con las horas y minutos que el usuario desea mostrar; por ej.: [(12,00), (7,13), (16,23)] representa las 12:00, 7:13 y 16:23.'''   
    c = cuerpo()       
    for hora_minutos in vector_horas:
      hora = hora_minutos[0];
      minutos = hora_minutos[1];
      c = c.cut(hora_solar(hora,minutos))
    return c

def reloj_de_sol_continuo():
  '''Reloj de Sol con las horas desde las 9:00 a las 15:10, en intervalos de 20 minutos.'''
  delta_x = ancho_pixel+delta_ancho
  c = cuerpo()
  # unidades de minuto
  c = c.cut(digito(0,alfa(9),alfa(15+10/60)).translate([-8.5*delta_x,0,0]))
  # decenas de minuto
  for hora in range(9,15):
      for minutos in (0,20,40):
          minuto_decenas = n_a_digito(minutos,1)
          c = c.cut(digito(minuto_decenas,
                           alfa(hora+minutos/60),
                           alfa(hora+(minutos+10)/60)).translate([-3.5*delta_x,0,0]))
  c = c.cut(digito(0,alfa(15),alfa(15+10/60)).translate([-3.5*delta_x,0,0]))
  # separador
  c = c.cut(separador(alfa(9),alfa(15+10/60)))
  # unidades de hora       
  for hora in range(9,15):
      hora_unidades = n_a_digito(hora,0)
      c = c.cut(digito(hora_unidades,
                       alfa(hora),
                       alfa(hora+50/60 if hora<15 else hora+10/60)).translate([3.5*delta_x,0,0]))
  # decenas de hora
  c = c.cut(digito(1,alfa(10),alfa(15+10/60)).translate([8.5*delta_x,0,0]))
  return c

# reloj = reloj_de_sol_continuo()
# reloj = reloj_de_sol_discreto([(12,0),(15,23),(8,10)])


