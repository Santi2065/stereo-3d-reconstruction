# TP2 — Reconstrucción 3D con cámara estéreo

**I308 · Visión Artificial · Universidad de San Andrés**

Reconstrucción 3D de un objeto rígido (un buda de cerámica) a partir de pares estéreo. Pipeline: calibración estéreo → rectificación → disparidad → reproyección a 3D → pose con ChArUco → fusión de nubes en un mundo común → mesh (Ball Pivoting) → altura en mm.

## Autores

| Nombre | Email |
|---|---|
| Santiago Luis Groba Alonso | sgrobaalonso@udesa.edu.ar |
| Valentino Nallib Fadel | vfadel@udesa.edu.ar |
| Joaquín Gustavo Di Cola | jdicola@udesa.edu.ar |

## Hardware y patrones

- **Cámara:** ELP-USB3D1080P02-H120 (1920×1080 por lado, baseline ~63 mm).
- **Calibración:** chessboard 7×10 cuadrados en A4 (6×9 esquinas internas, square 30 mm).
- **Escena:** ChArUco 5×7 `DICT_6X6_250`, square 52.6 mm / marker 31.3 mm (provisto por cátedra).

## Notebooks

- `reconstruccion_3d_catedra.ipynb` — **entregable principal**. Pipeline completo sobre el dataset oficial de cátedra (`datasets/stereo_budha_charuco/`). Termina exportando `buda_catedra.ply` + mesh + viewer interactivo.
- `reconstruccion_3d.ipynb` — pipeline sobre el dataset que capturamos en clase (`datasets/stereo_propio/`). La fusión final no llega a una reconstrucción usable del buda; se mantiene como registro del intento (ver disclaimer al inicio del notebook).

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cómo correrlo

```powershell
jupyter lab reconstruccion_3d_catedra.ipynb
```

Correr todas las celdas en orden. El modelo `.onnx` de CREStereo (~30 MB) se descarga la primera vez a `models/`.

## Estructura del repo

```
tp2_reconstruccion_3d/
├── reconstruccion_3d_catedra.ipynb   # entregable
├── reconstruccion_3d.ipynb           # dataset propio (intento)
├── aruco.py, calib.py                # helpers de cátedra
├── requirements.txt
├── ejemplos clase/                   # material provisto por cátedra
├── datasets/
│   ├── stereo_propio/
│   ├── stereo_budha_board/
│   └── stereo_budha_charuco/
└── models/                           # ONNX de CREStereo (gitignored)
```

## Referencias

- Consigna: `I308 Vision Artificial - TP2 - Reconstrucción 3D.pdf`.
- Calibración de cátedra: <https://github.com/udesa-vision/i308-calib>
- OpenCV 3D: <https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html>
