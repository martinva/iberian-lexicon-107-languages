"""ibcomp — Comparación matemática del léxico ibérico con el de otras lenguas.

Paquete de réplica del modelo final del estudio. Módulos:
  texto          limpieza de formas y constantes de alfabeto
  clases         paso de sonidos y grafías a clases de sonidos SCA (List 2012)
  normalizadores reglas de paso de la ortografía de cada lengua a una grafía común
  distancia      distancia de edición ponderada entre formas reducidas
  fuentes        lectura de cada fuente léxica
  pruebas        prueba con significados, perfil de combinaciones de sonidos, utilidades de azar
Cada función está descrita, con el mismo nombre, en 5_especificacion/.
"""
SEMILLA = 20261120

# La salida usa UTF-8 en cualquier sistema (en Windows la consola no lo usa por defecto y
# fallaría al imprimir ś, ŕ o el signo −). / Force UTF-8 output on every system.
import sys as _sys
for _flujo in (_sys.stdout, _sys.stderr):
    try:
        _flujo.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
