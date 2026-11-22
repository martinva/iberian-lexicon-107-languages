"""Comprobación rápida de la instalación y de los datos (menos de un minuto).

Verifica los resultados que NO dependen de sorteos: reglas de reducción a clases
de sonidos, medida de distancia, perfil de combinaciones de sonidos y valores
reales de la prueba con significados en cuatro diccionarios del euskera. Si todo
coincide, el paquete y los datos están completos y se leen como se espera.

Quick check of the installation and the data (under a minute). It verifies the
results that do NOT depend on random draws: reduction rules, distance measure,
sound-combination profile and the real values of the meaning-based test for four
Basque dictionaries.

Uso / Usage:  python3 comprobacion_rapida.py      (código de salida 0 si todo coincide)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas
from ibcomp.clases import reducida, red_ib, proyecta
from ibcomp.distancia import dist

fallos = []

def comprueba(nombre, obtenido, esperado, tolerancia=0.0):
    if isinstance(esperado, float):
        bien = abs(obtenido - esperado) <= tolerancia
    else:
        bien = obtenido == esperado
    print(f"  {'bien ' if bien else 'FALLO'} | {nombre}: obtenido {obtenido!r}, esperado {esperado!r}")
    if not bien:
        fallos.append(nombre)

print('1. Reducción a clases de sonidos (especificación, apartado 2)')
for forma, esperada in [('śalir', 'SaLiR'), ('zilar', 'SiLaR'), ('hamar', 'aMaR'), ('lagun', 'LaKuN'), ('etxe', 'eCe'), ('iaun', 'JauN')]:
    comprueba(f'reducida({forma})', reducida(forma), esperada)
for forma, esperada in [('abaŕ', 'aPaR'), ('śalir', 'SaLiR'), ('borste', 'PoRSTe')]:
    comprueba(f'red_ib({forma})', red_ib(forma), esperada)
comprueba("proyecta(['aMaR', 'BeCe'])", sorted(proyecta(['aMaR', 'BeCe'])), ['PeSe', 'aNaR'])

print('2. Medida de distancia (apartado 3.1)')
for a, b, d in [('LuRa', 'LuR', 0.182), ('SaLiR', 'SiLaR', 0.25), ('LaKu', 'LaKuN', 0.286), ('aPaR', 'aMaR', 0.333), ('SaLiR', 'SaLiR', 0.0)]:
    comprueba(f'dist({a}, {b})', round(dist(a, b), 3), d, 0.0005)

print('3. Perfil de combinaciones de sonidos (apartado 3.3)')
p = pruebas.perfil(['SaLiR'])
comprueba('pares de SaLiR', sorted(p), sorted(['^S', 'Sa', 'aL', 'Li', 'iR', 'R$']))
comprueba('divergencia de un perfil consigo mismo', round(pruebas.divergencia(p, p), 6), 0.0, 1e-9)
comprueba('divergencia de perfiles sin pares comunes', round(pruebas.divergencia(p, pruebas.perfil(['KoTuN'])), 6), 1.0, 1e-6)

print('4. Datos: número de unidades y de inscripciones')
U = fuentes.unidades_plomos(); N = fuentes.unidades_numerales()
comprueba('unidades de los plomos', len(U), 30)
comprueba('unidades de la serie numeral', len(N), 10)
if os.path.exists(os.path.join(fuentes.RAIZ, 'iberico', 'hesperia_iberico_1599.csv')):
    comprueba('inscripciones de Hesperia', len(fuentes.hesperia()), 1599)
else:
    print('  (omitido: el corpus de Hesperia no está descargado; véase 1_fuentes_lexicas/iberico/descargar_hesperia.py)')

print('5. Prueba con significados: valor real y unidades con candidatas (tabla 6; no dependen de sorteos)')
for carga, unidades_esp, real_esp in [(fuentes.azkue, 30, 0.503), (fuentes.opendata, 30, 0.452),
                                      (fuentes.trask_reconstruido, 15, 0.557)]:
    d = carga()
    r = pruebas.prueba_significados(U, d, 'comprobación', sorteos=20, minimo=4)
    comprueba(f'{d.nombre}: unidades con candidatas', r['unidades'], unidades_esp)
    comprueba(f'{d.nombre}: distancia media real', r['real'], real_esp, 0.0005)

print()
if fallos:
    print(f'HAY {len(fallos)} DIFERENCIAS: ' + '; '.join(fallos)); sys.exit(1)
print('Todo coincide. / All checks passed.')
