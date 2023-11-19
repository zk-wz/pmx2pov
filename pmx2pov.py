from pmx_importer import *
pmx = PmxImporter.load(r"CGassignment\登门喜鹊泠鸢yousa-ver2.0\泠鸢yousa登门喜鹊153cm-Apose2.1完整版.pmx")

vertices = []
normals = []
faces = [0,1,2,3]
uvs = []
for i in range(4):
    vertices.append(pmx.Vertices[i].Position)
    normals.append(pmx.Vertices[i].Normal)
    uvs.append(pmx.Vertices[i].UV)

print("Vertices:", vertices)
print("Normals:", normals)
print("Faces:", faces)
print("UVs:", uvs)
