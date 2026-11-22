# Respuestas de la declaración 15 (predicción prospectiva, versión 2)

**Envío (21-11-2026, 20:07–20:25).** Tres jueces, modelos de tres fabricantes, en sesiones nuevas sin memoria
(Mistral: chat temporal; Grok: chat nuevo, modo Fast; DeepSeek: chat nuevo, Pensamiento Profundo activado y
búsqueda desactivada). Mensaje idéntico a los tres: el encargo de `../ENCARGO_prospectiva_v2.md` seguido de
`---` y del contenido íntegro de `../FICHAS_prospectiva_v2.md`.

**Integridad del mensaje.** Tras detectarse que un primer envío a Mistral contenía texto corrupto (véase
`DESCARTADA_Mistral_envio1.md`), el mensaje de los tres envíos válidos se construyó DENTRO de la página del
navegador a partir de los bytes del archivo publicado (subido a un input creado al efecto y leído con
`File.text()`), y solo se envió tras verificar en la propia página su SHA-256:

- SHA-256 del archivo de fichas: `e566f2f13d82df90e7a5aa5487a9862716e483667877190fb724674607db3722`
- SHA-256 del mensaje completo enviado: `e9c0db43c3add413020081ef7c3d807c96ede90df90e95de3729229f69ef680f`

Las respuestas íntegras, la clave en claro (`CLAVE_prospectiva_v2.tsv`) y el cruce se publican aquí al
recibirlas. El SHA-256 de la clave se publicó antes del envío (`../clave_sha256.txt`, commit `60913fb`).
