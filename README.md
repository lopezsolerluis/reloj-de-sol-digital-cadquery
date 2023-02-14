# A digital sundial in CadQuery

![digital-sundial](https://github.com/lopezsolerluis/reloj-de-sol-digital-cadquery/blob/main/sundial-cadquery.png)

## Yet another digital sundial...

Some time ago, I wanted to lean some [OpenSCAD](https://openscad.org/), and decided to replicate the wonderlful [digital sundial](https://www.thingiverse.com/thing:1068443) created by **Mojoptix**.

Now, thanks to **Leandro Batlle**, I came across [a new language](https://github.com/CadQuery/cadquery) to describe 3D objects. And I thought there could be worse ways of learning it than trying to rewrite [that version of mine of the digital sundial](https://github.com/lopezsolerluis/reloj-de-sol-digital).

So here I am... 😊

If you want to read a (too long) explanation of how I did my own version in OpenSCAD, you can find a *very* verbose way [here](https://github.com/lopezsolerluis/reloj-de-sol-libro) (in spanish only).

# Un reloj de sol digital escrito en CadQuery

## Aún *otro* reloj de sol digital...

Gracias a **Leandro Batlle** me enteré de la existencia de [un nuevo lenguaje](https://github.com/CadQuery/cadquery) para (des)escribir objetos tridimensionales. Y se me ocurrió que no podía ser la peor manera de aprenderlo intentar reescribir la versión del [reloj de Sol digital](https://github.com/lopezsolerluis/reloj-de-sol-digital) que hiciera, hace un tiempo, con [OpenSCAD](https://openscad.org/). 

Así que aquí estamos... 😊

Si quieren leer una explicación *muy extensa* de cómo logré mi propia versión en OpenSCAD, pueden encontrarla [aquí](https://github.com/lopezsolerluis/reloj-de-sol-libro).

## Instalación (entorno para *editar* el modelo)

Los archivos STL  (carpeta **output**) ya están listos para imprimir. Si no tenés intención de editar el modelo, no es necesaria ésta instalación.

### Entorno Python

Si ya tenés instalado un entorno con la biblioteca [CadQuery](https://cadquery.readthedocs.io/en/latest/)  podés saltear ésta sección, directo a `Entorno de Edición`

```bash
conda env create -f environment.yml
```

Si algo falla, instalá un entorno de CadQuery según [éstas instrucciones](https://cadquery.readthedocs.io/en/latest/installation.html#installing-cadquery)



### Entorno de Edición

1. Activar un Entorno Python adecuado según la sección anterior

```bash
conda activate cadquery
```

1. probar el entorno ejecutando `main.py`

```bash
python main.py
```

### Editar con CQ-Editor

1. Abrir CQ-Editor
2. Menú **File** > **Open** y elegir `main.py`
3. Menú **Run** > **Render** 

![cq-edit](https://github.com/lopezsolerluis/reloj-de-sol-digital-cadquery/blob/main/cq-edit-screenshot.png)
