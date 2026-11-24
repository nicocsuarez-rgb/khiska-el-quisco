/* Videos del portal. Para sumar uno:
   - archivo en assets/video/ → { titulo, archivo, poster }
   - reel publicado en Instagram/TikTok/YouTube → { titulo, enlace, poster }
   El primero de la lista se muestra destacado. */
window.KHISKA_VIDEOS = [
  {
    titulo: "El Quisco no termina en la playa",
    archivo: "assets/video/v01-trailer.mp4",
    poster: "assets/video/poster-v01.jpg"
  },
  {
    titulo: "Ahora El Quisco se puede explorar desde un solo lugar",
    archivo: "assets/video/v00-el-quisco-desde-un-solo-lugar.mp4",
    poster: "assets/video/poster-v00.jpg"
  },
  {
    titulo: "Elige, prepara y comienza",
    archivo: "assets/video/v07-elige-prepara-comienza.mp4",
    poster: "assets/video/poster-v07.jpg"
  },
  {
    titulo: "Una ruta completada hace florecer tu Khiska",
    archivo: "assets/video/v12-haz-florecer-tu-khiska.mp4",
    poster: "assets/video/poster-v12.jpg"
  }
];

/* Video de fondo de la portada (toma aérea de El Quisco, horizontal, sin audio).
   Déjalo en assets/video/ y escribe su ruta en "video". Mientras esté vacío,
   la portada muestra las ilustraciones del territorio en movimiento. */
window.KHISKA_FONDO = {
  video: "",
  poster: ""
};
