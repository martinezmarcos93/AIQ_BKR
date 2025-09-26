from PIL import Image, ImageDraw, ImageFont
import os
import sys

# ==========================
# 1. Diccionario de transliteración básica
# ==========================
latin_to_hebrew = {
    "A": "א", "B": "ב", "C": "כ", "K": "כ", "D": "ד", "E": "ה", "F": "פ", "G": "ג",
    "H": "ח", "I": "י", "J": "י", "L": "ל", "M": "מ", "N": "נ", "O": "ו", "P": "פ",
    "Q": "ק", "R": "ר", "S": "ס", "T": "ט", "U": "ו", "V": "ו", "W": "ו", "X": "קס",
    "Y": "י", "Z": "ז"
}

# ==========================
# 2. Valores guemátricos
# ==========================
gematria_values = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ך": 500, "ל": 30, "מ": 40, "ם": 600, "נ": 50, "ן": 700,
    "ס": 60, "ע": 70, "פ": 80, "ף": 800, "צ": 90, "ץ": 900, "ק": 100, "ר": 200,
    "ש": 300, "ת": 400
}

# ==========================
# 3. Posiciones en la tabla (3 filas x 9 columnas)
# ==========================
positions_grid = {
    "ש": (0,0),"ל": (0,1),"ג": (0,2),"ר": (0,3),"כ": (0,4),"ב": (0,5),"ק": (0,6),"י": (0,7),"א": (0,8),
    "ם": (1,0),"ס": (1,1),"ו": (1,2),"ך": (1,3),"נ": (1,4),"ה": (1,5),"ת": (1,6),"מ": (1,7),"ד": (1,8),
    "ץ": (2,0),"צ": (2,1),"ט": (2,2),"ף": (2,3),"פ": (2,4),"ח": (2,5),"ן": (2,6),"ע": (2,7),"ז": (2,8),
}

# ==========================
# Utilidades de rutas (NUEVO)
# ==========================
def here(*parts):
    """Devuelve una ruta absoluta basada en la carpeta del .py."""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)

def safe_open_image(path_candidate):
    """Intenta abrir la imagen; si falla, lanza error con la ruta absoluta informativa."""
    abs_path = os.path.abspath(path_candidate)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"No se encontró la imagen de tabla en: {abs_path}")
    try:
        return Image.open(abs_path).convert("RGBA")
    except OSError as e:
        raise OSError(f"No se pudo abrir la imagen en: {abs_path}. Detalle: {e}")

# ==========================
# 4. Función principal
# ==========================
def crear_sigilo(nombre, tabla_img_path, fuente_ttf=None):
    # Normalizar a mayúsculas
    nombre = nombre.upper()

    # Transliteración al hebreo
    hebreo = "".join(latin_to_hebrew.get(ch, "") for ch in nombre)

    # Calcular gematría
    valor_total = sum(gematria_values.get(l, 0) for l in hebreo)

    # Abrir tabla base (ROBUSTO)
    img = safe_open_image(tabla_img_path)
    w, h = img.size
    cols, rows = 9, 3
    cell_w, cell_h = w / cols, h / rows

    # Obtener coordenadas de las letras
    coords = []
    for l in hebreo:
        if l in positions_grid:
            r, c = positions_grid[l]
            x = c * cell_w + cell_w/2
            y = r * cell_h + cell_h/2
            coords.append((x, y))

    # Capa de dibujo
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Fuente (OPCIONAL pero recomendable para hebreo)
    font = None
    if fuente_ttf and os.path.exists(fuente_ttf):
        try:
            font = ImageFont.truetype(fuente_ttf, int(min(cell_w, cell_h) * 0.35))
        except Exception:
            font = None  # fallback a la fuente por defecto

    # Conectar letras
    if len(coords) >= 2:
        draw.line(coords, fill=(0, 0, 0, 220), width=5)

    # Marcar puntos y letras
    radius = int(min(cell_w, cell_h) * 0.08)
    for (x, y), letter in zip(coords, hebreo):
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(200, 30, 30, 230))
        # Desplazamos un poco el texto a la derecha del punto
        tx, ty = x + radius + 2, y - radius
        draw.text((tx, ty), letter, fill=(0, 0, 0), font=font)

    result = Image.alpha_composite(img, overlay)

    # ==========================
    # Guardar con contador automático
    # ==========================
    contador_file = here("contador.txt")
    if os.path.exists(contador_file):
        with open(contador_file, "r", encoding="utf-8") as f:
            s = f.read().strip()
            contador = int(s) if s.isdigit() else 0
    else:
        contador = 0

    contador += 1
    with open(contador_file, "w", encoding="utf-8") as f:
        f.write(str(contador))

    output_path = here(f"sigilo_{contador:02d}.png")
    result.convert("RGB").save(output_path)

    return hebreo, valor_total, output_path

# ==========================
# 5. Programa interactivo
# ==========================
if __name__ == "__main__":
    # Ruta de la tabla:
    #   - Si la imagen está en la MISMA carpeta que este .py: "tabla_hebreo.png"
    #   - Si está dentro de subcarpeta "Aiq Bkr": here("Aiq Bkr", "tabla_hebreo.png")
    # Evitamos usar barras invertidas crudas que puedan formar \t, \n, etc.
    posibles_rutas = [
        here("tabla_hebreo.png"),
        here("Aiq Bkr", "tabla_hebreo.png"),
        here("Aiq Bkr", "tabla_hebreo.jpg"),
        here("tabla_hebreo.jpg"),
    ]

    # Elegimos la primera que exista
    ruta_tabla = None
    for p in posibles_rutas:
        if os.path.exists(p):
            ruta_tabla = p
            break

    if ruta_tabla is None:
        # Mensaje claro y salida
        print("❌ No encontré la imagen de la tabla. Probé estas rutas:")
        for p in posibles_rutas:
            print("  -", os.path.abspath(p))
        sys.exit(1)

    # (Opcional) Fuente TTF para hebreo; poné la ruta si la tenés:
    fuente_ttf = None
    # ejemplo: fuente_ttf = here("DejaVuSans.ttf")

    palabra = input("👉 Escribe la palabra que quieres sigilizar: ")
    hebreo, valor, archivo = crear_sigilo(palabra, ruta_tabla, fuente_ttf=fuente_ttf)
    print(f"\nPalabra en hebreo: {hebreo}")
    print(f"Valor numérico: {valor}")
    print(f"✅ Sigilo guardado en: {archivo}")
