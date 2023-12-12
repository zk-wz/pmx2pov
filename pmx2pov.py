import pmx_read
import pov_writer
import os

code = ""
code += pov_writer.PovWriter.write_init()
code += pov_writer.PovWriter.write_camera([0, 10, -30], [0, 10, 0])
code += pov_writer.PovWriter.write_light([0, 20, -10], [1, 1, 1])
code += pov_writer.PovWriter.write_light([0, 20, -10], [1, 1, 1])

filepath = r"E:\projects\programming\py\pmx2pov\pmx\YYB Hatsune Miku_10th\test.pmx"
folderpath = r"."
pmx = pmx_read.PmxImporter.load(filepath)
code += pov_writer.PovWriter.write_texture(pmx, folderpath, 'miku')
code += pov_writer.PovWriter.write_mesh(pmx, 'miku')

filepath = r"E:\projects\programming\py\pmx2pov\pmx\RedialC_EpRoomDS\EPDS.pmx"
folderpath = r"."
pmx = pmx_read.PmxImporter.load(filepath)
code += pov_writer.PovWriter.write_texture(pmx, folderpath, 'room')
code += pov_writer.PovWriter.write_mesh(pmx, 'room')

file_name = "test.pov"
povfilepath = f"pmx2pov\pov\{file_name}"
with open(povfilepath, mode="w") as f:
    f.write(code)
print(f"Saved to {povfilepath}")

