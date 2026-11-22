"""Apartado 8.4: solidez del resultado frente a la lista de 30 unidades.

Pregunta: ¿depende el resultado de la prueba con significados de unas pocas unidades, o de que todos los
significados propuestos sean correctos?

Para cada diccionario se calcula una sola vez, unidad por unidad, la distancia real y la del azar en cada uno de
500 sorteos (misma definición que la prueba con significados). Con esa tabla, el valor z de cualquier subconjunto
de unidades es la media de sus columnas.
 (a) Quitando una unidad cada vez.
 (b) Subconjuntos al azar de 20, 15 y 10 unidades (2.000 de cada tamaño).
 (c) Por origen del significado: dato externo; casilla documental; apoyo de la toponimia; y por niveles de procedencia según la Monografía IV.
 (d) Retirada adversa: se quitan una a una las unidades más favorables al euskera (menor distancia real).
 (e) Significados cambiados: a k unidades al azar se les da el significado de otra de ellas (rotación al azar),
     300 repeticiones por k; diccionarios del euskera.
En (a), (b) y (d) las lenguas son las del Wikcionario con candidatas para al menos el 40 % de las unidades.
Uso / Usage:  python3 t15_solidez_unidades.py
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from ibcomp import fuentes
from ibcomp.clases import reducida
from ibcomp.distancia import dist
from ibcomp.pruebas import z2, generador, sustituye, _z

SORTEOS = 500
EXTERNO = {'A1', 'A2', 'A3', 'A17', 'A30'}; TOPONIMIA = {'A24', 'A25', 'A26', 'A27', 'A28', 'A29'}
# Procedencia según la tabla 5 de la Monografía IV (inventario cerrado): nivel I = EXTERNO (A3 no tiene candidatas en euskera: el grupo nominal es de cinco y el euskera se compara con cuatro); nivel III = TOPONIMIA (clase c, convergente); nivel II = el resto (clase a, propuesta propia por casilla)
PARALELO = {'A8', 'A10', 'A14', 'A15', 'A19', 'A20'}          # nivel II para las que la Monografía IV señala, después de obtenido el significado, una correspondencia vasca

def tabla(unidades, dic, clave, campo, sorteos=SORTEOS):
    """Devuelve ids, real[n] y azar[sorteos, n] para las unidades con candidatas en el diccionario (sorteos como en la prueba con significados)."""
    rnd = generador('solidez', clave, dic.nombre); ids = []; real = []; F = []; C = []
    for u in unidades:
        c = dic.candidatas(u, campo)
        if not c: continue
        ri = [reducida(x) for x in u['formas']]; ids.append(u['id']); F.append(ri); C.append(sorted(c)); real.append(min(dist(a, b) for a in ri for b in c))
    azar = np.empty((sorteos, len(ids)))
    for s in range(sorteos):
        azar[s] = [min(dist(a, b) for b in cs for a in ri) for ri, cs in zip(F, sustituye(rnd, C, dic.por_longitud))]
    return ids, np.array(real), azar

def pares(unidades, dic, campo, sorteos, rnd):
    """Para cada pareja (unidad i, significado de la unidad j): distancia real R[i, j] y distancias del azar A[i, j] (una por sorteo)."""
    ids = [u['id'] for u in unidades]; F = {u['id']: [reducida(x) for x in u['formas']] for u in unidades}
    C = {u['id']: sorted(dic.candidatas(u, campo) or []) for u in unidades}; con = [j for j in ids if C[j]]
    R = {(i, j): min(dist(a, b) for a in F[i] for b in C[j]) for i in ids for j in con}; A = {k: np.empty(sorteos) for k in R}
    for s in range(sorteos):
        for j, cs in zip(con, sustituye(rnd, [C[j] for j in con], dic.por_longitud)):
            for i in ids: A[i, j][s] = min(dist(a, b) for a in F[i] for b in cs)
    return R, A

def z_de(real, azar, sel):
    """Valor z del subconjunto de columnas `sel`; None si la desviación de los sorteos es cero (guarda común, `pruebas._z`)."""
    return _z(real[sel].mean(), azar[:, sel].mean(axis=1))

def agrega_quitando_una(a):
    """Agregados del apartado (a) a partir de {unidad: tupla de `puesto`}. Los puestos sin z del euskera definido se
    cuentan como indefinidos y no entran en los agregados; si no queda ninguno definido, los agregados son None (null en
    el JSON), nunca un error ni NaN (fase 4f)."""
    def r2(x): return None if x is None else round(x, 2)
    av = [v for v in a.values() if v[0] is not None]
    return dict(z_mas_debil=r2(max(v[0] for v in av)) if av else None, z_mas_fuerte=r2(min(v[0] for v in av)) if av else None,
                primero_en=sum(v[1] == 1 for v in av), casos=len(a), indefinidos=len(a) - len(av),
                menor_separacion=r2(min(v[3] - v[0] for v in av)) if av else None)

if __name__ == '__main__':
    U = fuentes.unidades_plomos(); N = len(U); res = {}
    W = fuentes.wikcionario(); T = {}
    for l, d in W.items():
        ids, real, azar = tabla(U, d, 'plomos', 'terminos_en')
        if len(ids) >= 0.4 * N: T[l] = (ids, real, azar)
    print(f'Lenguas del Wikcionario con candidatas suficientes: {len(T)}'); sys.stdout.flush()
    def puesto(quitar):
        """z de cada lengua sin las unidades de `quitar`; devuelve (z del euskera, puesto, segunda lengua, su z)."""
        zs = {}
        for l, (ids, real, azar) in T.items():
            sel = [i for i, x in enumerate(ids) if x not in quitar]
            if len(sel) >= 4:  # mínimo de cuatro unidades comparables para que una lengua entre en la comparación
                z = z_de(real, azar, sel)
                if z is not None: zs[l] = z
        if 'Basque' not in zs or len(zs) < 2: return None, None, None, None, len(zs)  # sin z del euskera (nulo constante o menos de cuatro unidades) no hay puesto; None, nunca NaN
        o = sorted(zs, key=zs.get); otra = next(l for l in o if l != 'Basque')
        return zs['Basque'], o.index('Basque') + 1, otra, zs[otra], len(zs)
    todas = [u['id'] for u in U]; ids_eu = T['Basque'][0]; base = puesto(set())
    def r2(x): return None if x is None else round(x, 2)
    if base[0] is None: print('Completo: sin z del euskera definido'); 
    else: print(f'Completo: euskera {base[0]:.2f}, puesto {base[1]}; siguiente {base[2]} {base[3]:.2f}')
    # (a)
    a = {x: puesto({x}) for x in todas}
    res['a_quitando_una'] = agrega_quitando_una(a)   # los puestos sin z definido se cuentan aparte y no entran en los agregados
    print('(a) quitando una unidad:', res['a_quitando_una'])
    # (b)
    rnd = generador('solidez', 'subconjuntos'); res['b_subconjuntos'] = {}
    for k in (20, 15, 10):
        r = [puesto(set(todas) - set(rnd.sample(todas, k))) for _ in range(2000)]; zb = sorted(v[0] for v in r if v[0] is not None)
        res['b_subconjuntos'][k] = dict(primero=sum(v[1] == 1 for v in r), de=len(r), indefinidos=len(r) - len(zb), z_mediano=r2(float(np.median(zb))) if zb else None, z_peor=r2(zb[-1]) if zb else None, z_percentil_95=r2(zb[int(0.95 * len(zb))]) if zb else None)
        print(f'(b) {k} unidades al azar:', res['b_subconjuntos'][k]); sys.stdout.flush()
    # (c)
    res['c_por_origen'] = {}
    casilla = set(todas) - EXTERNO - TOPONIMIA; LAT = {'A6', 'A9', 'A11', 'A13'}
    for nombre, G in (('dato externo', EXTERNO), ('apoyo de la toponimia', TOPONIMIA), ('casilla documental', casilla), ('niveles I y II: clase (a) de la Monografía IV', set(todas) - TOPONIMIA),
                      ('nivel II con correspondencia vasca señalada después', PARALELO), ('nivel II sin correspondencia señalada', casilla - PARALELO), ('nivel II sin correspondencia señalada y sin los préstamos latinos', casilla - PARALELO - LAT)):
        v = puesto(set(todas) - G); res['c_por_origen'][nombre] = dict(unidades_del_grupo=len(G), comparables_con_el_euskera=len(G & set(ids_eu)), z_euskera=r2(v[0]), puesto=v[1], siguiente=v[2], z_siguiente=r2(v[3]), lenguas_comparadas=v[4])
        print(f'(c) {nombre}:', res['c_por_origen'][nombre])
    # (d)
    ids, real, azar = T['Basque']; orden = [ids[i] for i in np.argsort(real)]; quit_ = set(); pasos = []
    for x in orden:
        quit_.add(x); quedan = len(ids) - len(quit_)
        if quedan < 5: break
        v = puesto(quit_)
        if v[1] is None: pasos.append(dict(quitadas=len(quit_), ultima=x, quedan=quedan, z_euskera=None, puesto=None, siguiente=None, z_siguiente=None)); continue  # sin z del euskera no hay puesto: se anota y no se compara
        pasos.append(dict(quitadas=len(quit_), ultima=x, quedan=quedan, z_euskera=round(v[0], 2), puesto=v[1], siguiente=v[2], z_siguiente=round(v[3], 2)))
    res['d_retirada_adversa'] = dict(pasos=pasos, hasta_perder_el_primer_puesto=next((p['quitadas'] for p in pasos if p['puesto'] is not None and p['puesto'] > 1), None),
                                     hasta_z_mayor_que_menos_3=next((p['quitadas'] for p in pasos if p['z_euskera'] is not None and p['z_euskera'] > -3), None))
    print('(d) retirada adversa: unidades que hay que quitar para perder el primer puesto:', res['d_retirada_adversa']['hasta_perder_el_primer_puesto'],
          '| para que el valor suba de −3:', res['d_retirada_adversa']['hasta_z_mayor_que_menos_3'])
    for p in pasos: print('    ', p)
    sys.stdout.flush()
    # (e)
    res['e_significados_cambiados'] = {}
    for nombre, d, campo in (('Open Data Euskadi', fuentes.opendata(), 'terminos_es'), ('Wikcionario', W['Basque'], 'terminos_en'), ('WordNet', fuentes.wordnet()['Euskera, WordNet'], 'terminos_es')):
        if d is None: continue
        rnd = generador('solidez', 'cambiados', nombre); S = 200; R, A = pares(U, d, campo, S, rnd)
        def z_asig(asig):
            ps = [(i, j) for i, j in asig.items() if (i, j) in R]
            return _z(np.mean([R[p] for p in ps]), np.mean([A[p] for p in ps], axis=0))
        fila = {0: z2(z_asig({i: i for i in todas}))}
        for k in (5, 10, 15, 20, 30):
            zs = []
            for _ in range(300):
                g = rnd.sample(todas, k); h = g[1:] + g[:1]; asig = {i: i for i in todas}; asig.update(dict(zip(g, h))); zs.append(z_asig(asig))
            indefinidos = sum(z is None for z in zs); zs = sorted(z for z in zs if z is not None)  # un z no definido (nulo constante) se cuenta y se excluye
            if not zs: fila[k] = dict(indefinidos=indefinidos); continue
            fila[k] = dict(mediana=round(float(np.median(zs)), 2), percentil_5=round(zs[int(0.05 * len(zs))], 2), percentil_95=round(zs[int(0.95 * len(zs))], 2), mas_marcado=round(zs[0], 2), menos_marcado=round(zs[-1], 2), indefinidos=indefinidos)
        res['e_significados_cambiados'][nombre] = fila; print(f'(e) significados cambiados, {nombre}:', fila); sys.stdout.flush()
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', 'resultados', 't15_solidez_unidades.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
