import imageio
import os

def save_as_gif(frames, filename):
    if frames:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{filename}.gif")
        imageio.mimsave(output_path, frames, fps=10, loop=0)
        print(f"GIF guardado en: {output_path}")
    else:
        print("No se capturaron frames para generar el GIF.")
