import os

def print_progressbar(progress, max_progress, bar_length=20):
    progress = min(progress, max_progress)
    percent = progress / max_progress
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    print(f"\rProgress: [{hashes + spaces}] {percent*100:.2f}%", end='\r')

class PovWriter:
    def __init__() -> None:
        pass

    @staticmethod
    def write_init():
        code = ""
        code += "#include \"colors.inc\"\n"
        code += "sky_sphere {\n"
        code += "  pigment {\n"
        code += "    gradient y\n"
        code += "    color_map {\n"
        code += "      [0, 1 color Gray50 color Gray80]\n"
        code += "    }\n"
        code += "  }\n"
        code += "}\n"
        return code

    @staticmethod
    def write_texture(pmx, folderpath, s):
        texture_list = pmx.Textures
        material_list = pmx.Materials
        code = ""
        for i in range(len(material_list)):
            tex = os.path.join(folderpath, texture_list[material_list[i].TextureIndex])
            ext_name = os.path.splitext(tex)[1][1:]
            code += "#declare tex"+s+str(i)+" = texture {\n"
            code += "  uv_mapping\n"
            code += "  pigment {\n"
            code += "    image_map {\n"
            code += f"      {ext_name} \"{tex}\"\n"
            code += "      map_type 0\n"
            code += "      interpolate 2\n"
            code += "    }\n"
            code += "  }\n"
            code += "}\n"
        return code
        

    @staticmethod
    def write_camera(location, look_at):
        code = ""
        code += "camera {\n"
        code += f"  location <{location[0]}, {location[1]}, {location[2]}>\n"
        code += f"  look_at <{look_at[0]}, {look_at[1]}, {look_at[2]}>\n"
        code += "   right x*image_width/image_height\n"
        code += "}\n"
        return code
    
    @staticmethod
    def write_light(location, color):
        code = ""
        code += "light_source {\n"
        code += f"  <{location[0]}, {location[1]}, {location[2]}>\n"
        code += f"  color rgb <{color[0]}, {color[1]}, {color[2]}>\n"
        code += "}\n"
        return code
    
    @staticmethod
    def write_mesh(pmx,s):
        pmxvertices = pmx.Vertices
        faces = pmx.Faces
        material_list = pmx.Materials

        code = ""
        face_count = 0
        # for mat_index in range(1):
        for mat_index in range(len(material_list)):
            print_progressbar(face_count, len(faces))
            mat = material_list[mat_index]
            code += "#declare pmx"+s+str(mat_index)+" = mesh2 {\n"
            code += "  vertex_vectors {\n"
            code += f"    {mat.SurfaceCount},\n"
            for i in range(int(mat.SurfaceCount/3)):
                for j in range(3):
                    v = pmxvertices[faces[face_count+i][j]]
                    code += f"    <{v.Position[0]}, {v.Position[1]}, {v.Position[2]}>,\n"
            code += "  }\n"
            code += "  normal_vectors {\n"
            code += f"    {mat.SurfaceCount},\n"
            for i in range(int(mat.SurfaceCount/3)):
                for j in range(3):
                    v = pmxvertices[faces[face_count+i][j]]
                    code += f"    <{v.Normal[0]}, {v.Normal[1]}, {v.Normal[2]}>,\n"
            code += "  }\n"
            code += "  uv_vectors {\n"
            code += f"    {mat.SurfaceCount},\n"
            for i in range(int(mat.SurfaceCount/3)):
                for j in range(3):
                    v = pmxvertices[faces[face_count+i][j]]
                    code += f"    <{v.UV[0]}, {1-v.UV[1]}>,\n"
            code += "  }\n"
            code += "  face_indices {\n"
            code += f"    {int(mat.SurfaceCount/3)},\n"
            for i in range(int(mat.SurfaceCount/3)):
                code += f"    <{i*3}, {i*3+1}, {i*3+2}>,\n"
            code += "  }\n"
            # code += "  uv_mapping\n"
            code += "  texture {\n"
            code += f"    tex{s}{mat_index}\n"
            code += "  }\n"
            code += "}\n"
            face_count += int(mat.SurfaceCount/3)
        code += "union {\n"
        # for i in range(1):
        for i in range(len(material_list)):
            code += f"  object {{ pmx{s}{i} }}\n"
        code += "}\n"
                    
            
        # code = ""
        # code += "mesh2 {\n"
        # code += "  vertex_vectors {\n"
        # code += f"    {len(pmxvertices)},\n"
        # for v in pmxvertices:
        #     code += f"    <{v.Position[0]}, {v.Position[1]}, {v.Position[2]}>,\n"
        # code += "  }\n"
        # code += "  normal_vectors {\n"
        # code += f"    {len(pmxvertices)},\n"
        # for v in pmxvertices:
        #     code += f"    <{v.Normal[0]}, {v.Normal[1]}, {v.Normal[2]}>,\n"
        # code += "  }\n"
        # code += "  uv_vectors {\n"
        # code += f"    {len(pmxvertices)},\n"
        # for v in pmxvertices:
        #     code += f"    <{v.UV[0]}, {v.UV[1]}>,\n"
        # code += "  }\n"
        # code += "  face_indices {\n"
        # code += f"    {len(faces)},\n"
        # for f in faces:
        #     code += f"    <{f[0]}, {f[1]}, {f[2]}>,\n"
        # code += "  }\n"
        # # for i in range(len(texture_list)):
        # #     code += f"  texture {{ tex{i} }}\n"
        # code += "  pigment { rgb <1, 1, 1> }\n"
        # code += "}\n"
        return code