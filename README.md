🔮 Generador de Sigilos con AIQ BKR
Este proyecto implementa un generador automático de sigilos basado en la tabla AIQ BKR de la tradición cabalística.
El script convierte cualquier palabra latina a hebreo, calcula su valor guemátrico y genera una imagen trazando el recorrido de las letras sobre la tabla.
✨ Características
- Transliteración automática de caracteres latinos a hebreo.
- Cálculo de guematría (suma de valores numéricos de las letras).
- Ubicación precisa de cada letra en la tabla AIQ BKR (3x9).
- Dibujo automático de sigilos conectando las letras en orden.
- Numeración automática de los sigilos generados (sigilo_01.png, sigilo_02.png...).
- Compatible con imágenes .jpg y .png de la tabla.
- Opción de usar fuente TTF personalizada para mejorar el renderizado de caracteres hebreos.
🖼 Ejemplo de uso
1. Ejecuta el script en tu terminal:

python AIQ_BKR.py

2. Escribe la palabra que deseas sigilizar cuando el programa lo pida:

👉 Escribe la palabra que quieres sigilizar: LUZ

3. Resultado en consola:

Palabra en hebreo: לוז
Valor numérico: 43
✅ Sigilo guardado en: sigilo_01.png

4. Revisa la carpeta del proyecto: encontrarás la imagen generada.
📂 Estructura del proyecto
AIQ_BKR/
│
├── AIQ_BKR.py           # Script principal
├── tabla_hebreo.jpg     # Imagen base de la tabla AIQ BKR
├── contador.txt         # (Generado automáticamente)
└── sigilo_01.png        # (Ejemplo de salida)
⚙️ Requisitos
- Python 3.8+
- Librerías:
  - Pillow (para manejo de imágenes)

Instalación de dependencias:

pip install pillow
🖋 Fuente opcional
Si deseas usar una fuente TTF para mejorar la legibilidad de los caracteres hebreos,
colócala en la carpeta del proyecto y asigna su ruta en el script:

fuente_ttf = here("DejaVuSans.ttf")
📜 Sobre AIQ BKR
La tabla AIQ BKR es un sistema cabalístico que reorganiza las 22 letras hebreas en una grilla de 3x9,
asignando relaciones de sustitución y valores numéricos.
Este script automatiza el trazado geométrico para crear sigilos, tal como se hace en prácticas mágicas y meditativas.
⚠️ Aviso
Este proyecto se ofrece con fines educativos y experimentales.
Su uso para prácticas espirituales queda bajo la responsabilidad del usuario.
📖 Licencia
MIT — Libre para modificar y compartir.
