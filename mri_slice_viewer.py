"""Loads a public MRI and explores three slice directions."""
from pathlib import Path
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

folder = Path(__file__).resolve().parent
path = folder / "data" / "sub-01_ses-test_T1w.nii.gz"
if not path.exists():
    raise SystemExit(
        "MRI file missing."
    )

image = nib.as_closest_canonical(nib.load(path))
data = image.get_fdata(dtype=np.float32)
if data.ndim != 3 or not np.isfinite(data).all():
    raise SystemExit("Use a finite, single 3D MRI image for this.")
dx, dy, dz = nib.affines.voxel_sizes(image.affine)
print("Shape:", data.shape)
print("Voxel sizes:", np.round([dx, dy, dz], 4), image.header.get_xyzt_units()[0])
print("Nearest axis directions:", nib.aff2axcodes(image.affine))
print("These are tilted voxel planes, not exact world-aligned anatomical cuts.")

x = data.shape[0] // 2
y = data.shape[1] // 2
z = data.shape[2] // 2
assert 0 <= x < data.shape[0]
assert 0 <= y < data.shape[1]
assert 0 <= z < data.shape[2]
vmin, vmax = np.percentile(data[data > 0], [1, 99])

fig, axes = plt.subplots(1, 3, figsize=(12, 5))
fig.subplots_adjust(bottom=0.28, wspace=0.35)
axial = axes[0].imshow(data[:, :, z].T, cmap="gray", origin="lower",
                        aspect=dy / dx, vmin=vmin, vmax=vmax)
axes[0].set(title=f"Axial-like | z={z}", xlabel="L → R (x)", ylabel="P → A (y)")
coronal = axes[1].imshow(data[:, y, :].T, cmap="gray", origin="lower",
                          aspect=dz / dx, vmin=vmin, vmax=vmax)
axes[1].set(title=f"Coronal-like | y={y}", xlabel="L → R (x)", ylabel="I → S (z)")
sagittal = axes[2].imshow(data[x, :, :].T, cmap="gray", origin="lower",
                           aspect=dz / dy, vmin=vmin, vmax=vmax)
axes[2].set(title=f"Sagittal-like | x={x}", xlabel="P → A (y)", ylabel="I → S (z)")

z_slider = Slider(fig.add_axes([0.13, 0.17, 0.75, 0.025]), "z", 0,
                  data.shape[2] - 1, valinit=z, valstep=1)
y_slider = Slider(fig.add_axes([0.13, 0.12, 0.75, 0.025]), "y", 0,
                  data.shape[1] - 1, valinit=y, valstep=1)
x_slider = Slider(fig.add_axes([0.13, 0.07, 0.75, 0.025]), "x", 0,
                  data.shape[0] - 1, valinit=x, valstep=1)


def update_slices(_):
    """Matplotlib calls this function whenever any slider changes."""
    x, y, z = int(x_slider.val), int(y_slider.val), int(z_slider.val)
    axial.set_data(data[:, :, z].T)
    coronal.set_data(data[:, y, :].T)
    sagittal.set_data(data[x, :, :].T)
    axes[0].set_title(f"Axial-like | z={z}")
    axes[1].set_title(f"Coronal-like | y={y}")
    axes[2].set_title(f"Sagittal-like | x={x}")
    fig.canvas.draw_idle()


x_slider.on_changed(update_slices)
y_slider.on_changed(update_slices)
z_slider.on_changed(update_slices)

(folder / "figures").mkdir(exist_ok=True)
fig.savefig(folder / "figures" / "view.png", dpi=150)
print("Saved figures/view.png. In a graphical backend, drag the sliders.")
plt.show()
