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
      max-width: 100%;          /* nunca más ancha que la pantalla */
      word-wrap: break-word;    /* corta palabras largas */
      overflow-wrap: anywhere;  /* compatibilidad extra */
    }
    .acciones { 
      margin-top: 8px; 
      display: flex;
      gap: 8px;
      flex-wrap: wrap; /* permite que los botones salten de línea */
    }
    .acciones form { 
      display: inline; 
      margin: 0;
    }
    .acciones button {
      padding: 8px 14px;
      font-size: 14px;
      margin: 0;
      border-radius: 6px;
      min-width: 90px; /* 🔹 mismo ancho mínimo */
      text-align: center;
    }
    .btn-delete {
      background: #ef4444;
      color: white;
    }
    .btn-copy {
      background: #10b981;
      color: white;
    }
    .btn-copy:hover {
      background: #059669;
    }
    .copied {
      background: #6366f1 !important;
    }
    .error {
      background: #dc2626 !important;
    }
  </style>
  <script>
    async function copiarTexto(texto, boton) {
      console.log('Intentando copiar:', texto);
      const original = boton.textContent;
      boton.disabled = true;

      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(texto);
          boton.textContent = '✓ Copiado';
          boton.classList.add('copied');
        } else {
          // Fallback con textarea oculto
          const ta = document.createElement('textarea');
          ta.value = texto;
          ta.setAttribute('readonly','');
          ta.style.position = 'absolute';
          ta.style.left = '-9999px';
          document.body.appendChild(ta);
          ta.select();
          ta.setSelectionRange(0, ta.value.length);
          const ok = document.execCommand('copy');
          document.body.removeChild(ta);
          if (!ok) throw new Error('execCommand falló');
          boton.textContent = '✓ Copiado';
          boton.classList.add('copied');
        }
      } catch (err) {
        console.error('Error copiando:', err);
        try { window.prompt('Copia manualmente con Ctrl/Cmd + C:', texto); } catch(e){}
        boton.textContent = '❌ Error';
        boton.classList.add('error');
      } finally {
        setTimeout(() => {
          boton.textContent = original;
          boton.disabled = false;
          boton.classList.remove('copied','error');
        }, 2000);
      }
    }

    // Delegación de eventos para todos los botones .btn-copy
    document.addEventListener('click', function(e) {
      const btn = e.target.closest('.btn-copy');
      if (!btn) return;
      let texto = btn.dataset.text;
      if (texto === undefined) return;
      try {
        if (texto.startsWith('"') || texto.startsWith("'")) {
          texto = JSON.parse(texto);
        }
      } catch(e) { /* ignorar parse fallido */ }
      copiarTexto(texto, btn);
    });
  </script>
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
    {% for t in notas|reverse %}
      <div class="nota">
        {{ t }}
        <div class="acciones">
          <button type="button" class="btn-copy" data-text='{{ t|tojson }}'>📋 Copiar</button>
          <form method="POST" action="{{ url_for('delete', idx=loop.revindex0) }}">
            <button type="submit" class="btn-delete">🗑️ Borrar</button>
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
