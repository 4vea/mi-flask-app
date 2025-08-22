from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# almacenamiento en memoria (simple)
notas = []

PAGE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mis Notas</title>
  <style>
    body {
      background: #0b0f14;
      color: #e6edf3;
      font-family: Arial, sans-serif;
      margin: 0; padding: 20px;
    }
    h1 { color: #6ee7ff; }
    form { margin-bottom: 20px; }
    textarea {
      width: 100%; height: 80px;
      border-radius: 8px;
      border: 1px solid #444;
      background: #121a26;
      color: #e6edf3;
      padding: 10px;
      font-size: 16px;
    }
    button {
      margin-top: 10px;
      padding: 10px 16px;
      border: none;
      border-radius: 8px;
      background: linear-gradient(90deg, #6ee7ff, #8b5cf6);
      color: #081017;
      font-weight: bold;
      cursor: pointer;
    }
    .nota {
      background: #121a26;
      border: 1px solid #333;
      border-radius: 8px;
      padding: 12px;
      margin-bottom: 10px;
      white-space: pre-wrap;
    }
    .acciones { margin-top: 8px; }
    .acciones form { display: inline; }
    .acciones button {
      background: #ef4444;
      color: white;
      padding: 6px 10px;
      font-size: 14px;
      margin-top: 0;
    }
  </style>
</head>
<body>
  <h1>📝 Mis Notas</h1>
  <form method="POST" action="{{ url_for('index') }}">
    <textarea name="texto" placeholder="Escribe tu nota aquí..." required></textarea>
    <br>
    <button type="submit">Guardar nota</button>
  </form>

  {% if notas %}
    <h2>Notas guardadas ({{ notas|length }})</h2>
    {% for t in notas %}
      <div class="nota">
        {{ t }}
        <div class="acciones">
          <form method="POST" action="{{ url_for('delete', idx=loop.index0) }}">
            <button type="submit">Borrar</button>
          </form>
        </div>
      </div>
    {% endfor %}
  {% else %}
    <p>No hay notas todavía.</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        texto = (request.form.get("texto") or "").strip()
        if texto:
            notas.append(texto)
        return redirect(url_for("index"))
    return render_template_string(PAGE, notas=notas)

@app.post("/delete/<int:idx>")
def delete(idx):
    if 0 <= idx < len(notas):
        notas.pop(idx)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
