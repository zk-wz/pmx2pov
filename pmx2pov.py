import pmx_read
import pov_writer
import os

filepath = r"pmx2pov\pmx\YYB Hatsune Miku_10th\YYB Hatsune Miku_10th_v1.02.pmx"
folderpath = r"E:\projects\programming\py\pmx2pov\pmx\YYB Hatsune Miku_10th"

pmx = pmx_read.PmxImporter.load(filepath)

code = ""
code += pov_writer.PovWriter.write_texture(pmx.Textures, folderpath)
code += pov_writer.PovWriter.write_camera([0, 10, -25], [0, 10, 0])
code += pov_writer.PovWriter.write_light([0, 20, -10], [1, 1, 1])
code += pov_writer.PovWriter.write_mesh(pmx)

file_name = "test.pov"
povfilepath = f"pmx2pov\pov\{file_name}"
with open(povfilepath, mode="w") as f:
    f.write(code)
print(f"Saved to {povfilepath}")

