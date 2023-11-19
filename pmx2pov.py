from pmx_read import *
from pov_writer import *

filepath = r"pmx2pov\pmx\YYB Hatsune Miku_10th\YYB Hatsune Miku_10th_v1.02.pmx"

pmx = PmxImporter.load(filepath)

code = ""
code += PovWriter.write_camera([0, 10, -25], [0, 10, 0])
code += PovWriter.write_light([0, 20, -10], [1, 1, 1])
code += PovWriter.write_mesh(pmx.Vertices, pmx.Faces)

file_name = "test.pov"
povfilepath = f"pmx2pov\pov\{file_name}"
with open(povfilepath, mode="w") as f:
    f.write(code)
print(f"Saved to {povfilepath}")

