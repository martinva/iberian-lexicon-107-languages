"""Tablas 6 y 7: prueba con significados, 30 unidades de los plomos y léxico metrológico, todos los diccionarios.

Uso:  python3 t06_t07_significados.py     (salida: ../resultados/t06_t07_significados.json y un resumen en pantalla)

Exclusión a voluntad (declaración 22): con la variable de entorno EXCLUIR (identificadores de unidad o formas,
separados por comas; p. ej. EXCLUIR="A7,A11" o EXCLUIR="bale,oŕtin") se quitan esas unidades de la lista de los
plomos antes de calcular. La salida va entonces a ../resultados/t06_t07_significados_excluir.json y no toca la
salida de referencia. Sin EXCLUIR, el programa hace exactamente lo mismo que antes.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes, pruebas

def diccionarios():
    wik = fuentes.wikcionario(); wn = fuentes.wordnet(); ap_es = fuentes.apertium('es'); ap_en = fuentes.apertium('en')
    grupos = {
        'Wikcionario y diccionarios históricos': list(wik.values()) + [fuentes.azkue(), fuentes.trask_reconstruido()],
        'Diccionarios bilingües, puente castellano': [fuentes.opendata()] + list(ap_es.values()),
        'Diccionarios bilingües, puente inglés': list(ap_en.values()),
        'Concepto a concepto (WordNet)': list(wn.values()),
    }
    return grupos

def aplicar_exclusion(unidades, texto):
    """Quita las unidades cuyo id o alguna de cuyas formas figure en texto (separado por comas)."""
    pedidas = {t.strip().lower() for t in (texto or '').split(',') if t.strip()}
    if not pedidas:
        return unidades, []
    quedan, quitadas = [], []
    for u in unidades:
        claves = {u['id'].lower()} | {f.lower() for f in u.get('formas', [])}
        (quitadas if claves & pedidas else quedan).append(u)
    sin_uso = sorted(pedidas - {c for u in quitadas for c in ({u['id'].lower()} | {f.lower() for f in u.get('formas', [])})})
    if sin_uso:
        print('Aviso: no corresponden a ninguna unidad:', ', '.join(sin_uso))
    return quedan, quitadas

if __name__ == '__main__':
    plomos, quitadas = aplicar_exclusion(fuentes.unidades_plomos(), os.environ.get('EXCLUIR', ''))
    if quitadas:
        print(f"EXCLUIR: quitadas {len(quitadas)} unidades ({', '.join(u['id'] + ' ' + '/'.join(u['formas']) for u in quitadas)}); quedan {len(plomos)}")
    nombre_plomos = f'{len(plomos)} unidades de los plomos' if quitadas else '30 unidades de los plomos'
    salida = 't06_t07_significados_excluir.json' if quitadas else 't06_t07_significados.json'
    conj = {nombre_plomos: plomos, 'léxico metrológico (numerales)': fuentes.unidades_numerales()}
    res = {}
    for g, dics in diccionarios().items():
        for nombre, us in conj.items():
            # mínimo de unidades con candidatas: 40 % en el Wikcionario (como en el diseño original), 30 % en los demás grupos
            minimo = max(4, (0.4 if g.startswith('Wikcionario') else 0.3) * len(us))
            filas = [r for r in (pruebas.prueba_significados(us, d, nombre, minimo=minimo) for d in dics) if r]
            filas.sort(key=lambda r: r['z']); res[f'{g} | {nombre}'] = filas
            print(f'\n== {g} | {nombre} ({len(filas)} diccionarios)')
            for i, r in enumerate(filas, 1):
                if i <= 6 or 'uskera' in r['diccionario'] or r['diccionario'] in ('Basque', 'Latin'):
                    print(f"  {i:2d}. {r['diccionario']:44s} formas {r['formas']:6d} | unidades {r['unidades']:2d} | real {r['real']} azar {r['azar']} | z {r['z']:6.2f} p {r['p']}")
            sys.stdout.flush()
            json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', salida), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
