#!/usr/bin/env python3
"""
Servidor Python + API para el juego RPG 2D de notas finales (Edición Premium):
"La Búsqueda del Saber" — Instituto FEB (Bibliotecario de Instituciones Educativas).

Equipo Docente:
- Nastasi, Mariana
- Moriondo, Silvia
- Ruiz Chaves, Eduardo
- Coria, Emiliano

Ejecución:
    python app.py
Luego abrir en el navegador: http://localhost:8000
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from urllib.parse import urlparse

PORT = int(os.environ.get("PORT", 8000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

DOCENTES = [
    "Nastasi, Mariana",
    "Moriondo, Silvia",
    "Ruiz Chaves, Eduardo",
    "Coria, Emiliano",
]

NOTAS_FINALES = [
    {
        "id": "tecnologias",
        "materia": "Tecnologías aplicadas a las bibliotecas",
        "nota": 10,
        "nota_texto": "Diez",
        "estado": "Aprobada",
        "sello": "Sello Tecnológico",
    },
    {
        "id": "comunicacion",
        "materia": "Comunicación y cibercultura",
        "nota": 10,
        "nota_texto": "Diez",
        "estado": "Aprobada",
        "sello": "Sello Digital",
    },
    {
        "id": "formacion",
        "materia": "Formación de usuarios",
        "nota": 10,
        "nota_texto": "Diez",
        "estado": "Aprobada",
        "sello": "Sello de Autonomía",
    },
]


class JuegoHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/notas":
            self._send_json({
                "ok": True,
                "docentes": DOCENTES,
                "notas": NOTAS_FINALES,
            })
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/completar":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                data = {}
            self._send_json({
                "ok": True,
                "estudiante": data.get("estudiante", ""),
                "personaje": data.get("personaje", "bibliotecario"),
                "libros_magicos": data.get("libros_magicos", 0),
                "docentes": DOCENTES,
                "notas": NOTAS_FINALES,
            })
            return
        self._send_json({"ok": False, "error": "Ruta no encontrada"}, status=404)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), JuegoHandler)
    print(f"Servidor iniciado en http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        server.server_close()
