# TP2 — Reconstrucción 3D con Cámara Estéreo

**I308 — Visión Artificial · Universidad de San Andrés**
**Autor:** Santiago Luis Groba Alonso

> Extensión máxima: 6 páginas. Tres secciones obligatorias: introducción, método y resultados.

---

## 1. Introducción

Objetivo y motivación: reconstruir en 3D un objeto rígido (buda) a partir de pares de imágenes RGB capturadas con una cámara estéreo. Se obtiene una nube de puntos métricamente coherente fusionando información de múltiples vistas mediante un marco de coordenadas único definido por un patrón conocido en escena.

Aplicaciones del problema: visión robótica, escaneo de objetos, fotogrametría a baja escala.

---

## 2. Método

### 2.1 Datos

- Cámara estéreo **ELP-USB3D1080P02-H120** (1920×1080 por cámara, baseline ~60 mm).
- Dataset propio capturado en clase con `N_calib` pares de calibración y `N_capt` pares del objeto.
- Patrón de calibración: checkerboard **10×7**, lado **24.2 mm**.
- Patrón de referencia para pose: _ChArUco / checkerboard_ con `<dimensiones>`.

### 2.2 Calibración estéreo

Se utilizó la herramienta de cátedra [i308-calib](https://github.com/udesa-vision/i308-calib) para obtener `stereo_calibration.pkl` (intrínsecos `K_L`, `K_R`, distorsiones `D_L`, `D_R`, extrínsecos `R`, `T`) y `stereo_maps.pkl` (mapas de rectificación y matriz `Q`).

Reportar:
- Error de reproyección promedio.
- Baseline estimado (`||T||`).
- Comparación con el baseline declarado por el fabricante (~60 mm).

### 2.3 Rectificación

`cv2.stereoRectify` + `cv2.initUndistortRectifyMap` precomputan los mapas; en runtime se aplica `cv2.remap`. Las líneas epipolares quedan paralelas a las filas → la disparidad pasa a ser 1D.

_Figura 1: par estéreo original vs rectificado._

### 2.4 Disparidad

Se experimentó con:
- **StereoBM** (clásico): baseline rápido.
- **StereoSGBM** (Semi-Global Block Matching): elegido por su mejor cobertura en zonas de textura pobre.
- (Opcional) **CRE-Stereo** vía [stereodemo](https://github.com/nburrus/stereodemo) para comparar con métodos basados en redes neuronales.

Parámetros finales de SGBM:
- `numDisparities = 128`, `blockSize = 5`
- `P1 = 8·3·blockSize²`, `P2 = 32·3·blockSize²`
- `uniquenessRatio = 10`, `speckleWindowSize = 100`, `speckleRange = 2`

_Figura 2: mapa de disparidad para un par representativo._

### 2.5 Pose de cámara respecto al mundo

El marco de mundo se define como el frame del patrón de referencia en escena. Para cada par estéreo:

1. Detección del patrón en la imagen izquierda (`cv2.aruco` o `cv2.findChessboardCorners`).
2. Estimación de pose con `cv2.solvePnP` → `(rvec, tvec)` en Rodrigues.
3. Conversión a transformación homogénea `T_wc` (mundo → cámara) y su inversa `T_cw`.

_Figura 3: ejes del mundo proyectados sobre la imagen y pose de la cámara visualizada en Open3D._

### 2.6 Reconstrucción y fusión

Por cada par:
1. `cv2.reprojectImageTo3D(disparidad, Q)` → puntos 3D en frame de cámara.
2. Filtrado por rango de profundidad razonable (100–2000 mm).
3. Transformación al frame del mundo: `p_w = T_cw · p_c`.
4. Recorte por bounding box `bbox_world_mm` para descartar fondo / patrón.
5. `remove_statistical_outlier` + `voxel_down_sample` (Open3D).

Las nubes parciales se acumulan en una única `o3d.geometry.PointCloud` y se exportan a `.PLY` binario.

### 2.7 Estimación del tamaño

Altura del buda = extensión de la nube acumulada sobre el eje vertical del mundo (eje `Z` si el patrón yace en el plano `XY`).

---

## 3. Resultados

### 3.1 Calibración

| Métrica | Valor |
|---|---|
| Error de reproyección | _xx_ px |
| Baseline `||T||` | _xx_ mm |
| Resolución | 1920×1080 |

### 3.2 Reconstrucción

| Métrica | Valor |
|---|---|
| Pares procesados / totales | _xx / xx_ |
| Puntos antes de fusión | _xx_ |
| Puntos finales tras downsample | _xx_ |
| Alto estimado del buda | _xx_ mm |

_Figura 4: nube de puntos parcial (un par) en Open3D._
_Figura 5: nube acumulada con todas las vistas._

### 3.3 Discusión

- Calidad del matching estéreo según textura del objeto.
- Errores de pose cuando el patrón aparece oclusivo o muy oblicuo.
- Trade-off entre voxel_size, densidad y calidad visual.

### 3.4 Limitaciones

- Zonas reflectantes o sin textura → disparidad poco confiable.
- Sensibilidad a la calibración: un error pequeño en `K` o `T` se amplifica al fusionar muchas vistas.
- ChArUco tolera oclusión parcial pero su precisión depende del tamaño de los marcadores en pixels.

---

## 4. Referencias

- Consigna del TP — Departamento de Ingeniería, UdeSA, 2026.
- Hartley & Zisserman, _Multiple View Geometry in Computer Vision_, Cambridge, 2004.
- OpenCV docs — _Camera Calibration and 3D Reconstruction_.
- Burrus N., _stereodemo_, <https://github.com/nburrus/stereodemo>.
- Cátedra I308 — herramienta `i308-calib`, <https://github.com/udesa-vision/i308-calib>.
