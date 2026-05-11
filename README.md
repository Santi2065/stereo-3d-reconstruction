# TP2 — Reconstrucción 3D con Cámara Estéreo

**I308 - Visión Artificial · Universidad de San Andrés**

Reconstrucción 3D de un objeto rígido a partir de pares de imágenes RGB capturadas con una cámara estéreo. El pipeline integra calibración estéreo, rectificación, estimación de disparidad, recuperación de pose mediante un patrón conocido (ChArUco) y fusión de nubes de puntos en un marco de coordenadas único.

---

## Autor

| Nombre | Email |
|---|---|
| Santiago Luis Groba Alonso | _grobaalonsos@udesa.edu.ar_ |

---

## Hardware y patrones utilizados

- **Cámara estéreo:** ELP-USB3D1080P02-H120 (1920×1080 por cámara, baseline ~60 mm).
- **Patrón de calibración:** checkerboard 10×7, lado 24.2 mm.
- **Patrón de referencia en escena:** ChArUco 5×7 con `DICT_6X6_250` (square 52.6 mm / marker 31.3 mm) — _confirmar y editar en la sección 0 del notebook si difiere._

---

## Pipeline (resumen)

```
captures L/R → rectificación → disparidad (SGBM) → reproyección a 3D (Q)
            → detección ChArUco + solvePnP → transformación al mundo
            → filtrado + acumulación → buda_reconstruido.ply + alto en mm
```

---

## Setup

```powershell
# crear venv (Python 3.10 u 3.11 — Open3D no soporta todas las versiones)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Cómo correrlo

```powershell
jupyter lab reconstruccion_3d.ipynb
```

Correr de arriba hacia abajo. La sección **0. Setup y configuración** tiene todas las variables editables (dataset, patrón, parámetros de SGBM, bbox de filtrado).

Salida principal: `buda_reconstruido.ply` en la raíz del repo.

---

## Estructura del repo

```
tp2_reconstruccion_3d/
├── reconstruccion_3d.ipynb       # pipeline completo de cabo a rabo
├── aruco.py                      # helpers ChArUco (copiados de code_examples/)
├── requirements.txt
├── README.md
├── .gitignore
├── informe/
│   └── informe.md                # esqueleto del informe (≤6 páginas)
├── datasets/
│   ├── stereo_propio/            # capturado en clase (calib pkl precomputada)
│   ├── stereo_budha_board/       # provistos por cátedra
│   └── stereo_budha_charuco/
└── code_examples/                # ejemplos provistos por cátedra
```

---

## Referencias

- Consigna: `I308 Vision Artificial - TP2 - Reconstrucción 3D.pdf` (raíz del repo).
- Herramienta de calibración de cátedra: <https://github.com/udesa-vision/i308-calib>
- `stereodemo` (matching estéreo + Open3D): <https://github.com/nburrus/stereodemo>
- OpenCV — Calibration and 3D Reconstruction: <https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html>
