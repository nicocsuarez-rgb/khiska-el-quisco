/* Sonidos de El Quisco (paisajes sonoros y relatos en voz local).
   Para sumar uno: deja el mp3 (128 kbps) en assets/audio/ y agrega una línea abajo.

   { id, lugar, tipo, titulo, archivo, transcripcion, credito }
   - lugar: "el-quisco" (sonido general, para escucha.html) o el id del lugar:
            el-batro · las-petras · mirador-neptuno · punta-de-tralca · isla-negra · el-totoral · caleta
   - tipo:  "paisaje" (sonido del lugar) o "relato" (voz de una persona de El Quisco)
   - archivo: ruta desde la raíz del portal, por ejemplo "assets/audio/paisaje-el-batro.mp3"
   - transcripcion: texto completo de lo que se escucha (obligatorio en relatos)
   - credito: en relatos, "Nombre, oficio" (se muestra como "Voz de Nombre, oficio")

   Reglas: solo grabaciones reales en terreno y voces reales con autorización firmada.
   Nunca voces generadas con IA para relatos de vecinos, pescadores u oficios.
   Un relato sin archivo, transcripción o crédito no se muestra. Si el archivo no carga, tampoco.

   Ejemplos (quita las // para activarlos cuando exista el archivo):
   { id: "paisaje-el-quisco", lugar: "el-quisco", tipo: "paisaje", titulo: "Mar en las rocas, aves y brisa", archivo: "assets/audio/paisaje-el-quisco.mp3", transcripcion: "", credito: "" },
   { id: "relato-caleta-nombre", lugar: "caleta", tipo: "relato", titulo: "Lo que es la caleta para mí", archivo: "assets/audio/relato-caleta-nombre.mp3", transcripcion: "Texto completo del relato…", credito: "Nombre Apellido, pescador de la caleta" },
*/
window.KHISKA_AUDIOS = [
];
