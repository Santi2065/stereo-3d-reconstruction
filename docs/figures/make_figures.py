"""Regenerates the figures shown in the README.

Figure 1 is a diagram. Figures 2-4 are the outputs saved in
reconstruccion_3d_catedra.ipynb (the course dataset is not versioned in this repo,
so they cannot be recomputed here); the script extracts them, blanks the Spanish
panel titles (the README captions replace them) and stores optimized PNGs.
Figure 5 is an Open3D screenshot that was committed once and removed later;
it is read back from the git history and cropped.

    pip install numpy matplotlib pillow
    python docs/figures/make_figures.py
"""
import base64
import io
import json
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for f in Path("/usr/share/fonts/lm").glob("lm*10-*.otf"):  # Latin Modern, if installed
    font_manager.fontManager.addfont(str(f))
plt.style.use(HERE / "paper.mplstyle")
C = plt.rcParams["axes.prop_cycle"].by_key()["color"]


def save(fig, name):
    fig.savefig(HERE / name, metadata={"Date": None})
    plt.close(fig)


# ---- Figure 1: pipeline diagram
STEPS = [
    ("Calibration", "$K_L, K_R$, $R, T$"),
    ("Rectification", "stereoRectify\n+ remap"),
    ("Disparity", "CREStereo\n(ONNX)"),
    ("3D points", "$Z = fB/d$"),
    ("World pose", "ArUco markers\n+ solvePnP"),
    ("Fusion", "crop, denoise,\n1 mm voxels"),
    ("Mesh", "Ball Pivoting,\nheight"),
]
fig, ax = plt.subplots(figsize=(7.2, 1.35))
ax.set_xlim(0, len(STEPS))
ax.set_ylim(0, 1)
ax.axis("off")
for i, (title, sub) in enumerate(STEPS):
    edge = C[0] if i < 4 else C[1]
    ax.add_patch(FancyBboxPatch((i + 0.06, 0.12), 0.88, 0.76, boxstyle="round,pad=0,rounding_size=0.06",
                                fc="white", ec=edge, lw=0.9))
    ax.text(i + 0.5, 0.66, title, ha="center", va="center", fontsize=7.8, color="#1a1a1a")
    ax.text(i + 0.5, 0.34, sub, ha="center", va="center", fontsize=6.5, color="#4d4d4d", linespacing=1.2)
    if i:
        ax.annotate("", xy=(i + 0.06, 0.5), xytext=(i - 0.06, 0.5),
                    arrowprops=dict(arrowstyle="-|>", lw=0.7, color="#1a1a1a", shrinkA=0, shrinkB=0))
ax.text(2.0, 0.98, "per stereo pair (geometry)", ha="center", va="center", fontsize=7, color=C[0])
ax.text(5.5, 0.98, "multi-view (world frame)", ha="center", va="center", fontsize=7, color=C[1])
save(fig, "fig1-pipeline.svg")

# ---- Figures 2-4: saved outputs of the course-dataset notebook
nb = json.loads((ROOT / "reconstruccion_3d_catedra.ipynb").read_text(encoding="utf-8"))


def notebook_png(cell):
    for out in nb["cells"][cell]["outputs"]:
        if "image/png" in out.get("data", {}):
            return Image.open(io.BytesIO(base64.b64decode(out["data"]["image/png"]))).convert("RGB")
    raise ValueError(f"cell {cell} has no image output")


def export(img, name, blank=(), crop_top=0, width=1600, palette=True):
    draw = ImageDraw.Draw(img)
    for box in blank:  # (x0, y0, x1, y1) of a Spanish panel title
        draw.rectangle(box, fill="white")
    img = img.crop((0, crop_top, img.width, img.height))
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    if palette:  # 256-colour palette keeps photos small; smooth colormaps stay RGB
        img = img.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
    img.save(HERE / name, optimize=True)


# cell 5: rectified pair 0 with epipolar lines and one template-matched point
export(notebook_png(5), "fig2-rectified-pair.png", crop_top=31)
# cell 8: rectified left image and CREStereo disparity of pair 0
export(notebook_png(8), "fig3-disparity.png", blank=[(0, 58, 770, 82), (770, 78, 1470, 102)], width=1300,
       palette=False)
# cell 15: fused point cloud, top / side / height views
export(notebook_png(15), "fig4-point-cloud.png", blank=[(0, 8, 600, 33), (600, 141, 1180, 163), (1200, 60, 1660, 84)])

# Open3D screenshot of the reconstruction, recovered from the repository history
SHOT = "ScreenCapture_2026-05-20-00-19-30.png"
added = subprocess.run(["git", "-C", str(ROOT), "log", "--all", "--diff-filter=A", "--format=%H", "--", SHOT],
                       capture_output=True, text=True, check=True).stdout.split()[-1]
shot = subprocess.run(["git", "-C", str(ROOT), "show", f"{added}:{SHOT}"], capture_output=True, check=True).stdout
img = Image.open(io.BytesIO(shot)).convert("RGB")
x0, y0, x1, y1 = Image.eval(img.convert("L"), lambda v: 255 if v < 250 else 0).getbbox()
export(img.crop((max(x0 - 20, 0), max(y0 - 20, 0), min(x1 + 20, img.width), min(y1 + 20, img.height))),
       "fig5-rendering.png")

for p in sorted(HERE.glob("fig*")):
    print(f"{p.name}: {p.stat().st_size / 1024:.0f} KB")
