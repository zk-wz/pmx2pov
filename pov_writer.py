
class PovWriter:
    def __init__() -> None:
        pass

    @staticmethod
    def write_camera(location, look_at):
        code = ""
        code += "camera {\n"
        code += f"  location <{location[0]}, {location[1]}, {location[2]}>\n"
        code += f"  look_at <{look_at[0]}, {look_at[1]}, {look_at[2]}>\n"
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
    def write_mesh(pmxvertices, faces):
        code = ""
        code += "mesh2 {\n"
        code += "  vertex_vectors {\n"
        code += f"    {len(pmxvertices)},\n"
        for v in pmxvertices:
            code += f"    <{v.Position[0]}, {v.Position[1]}, {v.Position[2]}>,\n"
        code += "  }\n"
        code += "  normal_vectors {\n"
        code += f"    {len(pmxvertices)},\n"
        for v in pmxvertices:
            code += f"    <{v.Normal[0]}, {v.Normal[1]}, {v.Normal[2]}>,\n"
        code += "  }\n"
        code += "  uv_vectors {\n"
        code += f"    {len(pmxvertices)},\n"
        for v in pmxvertices:
            code += f"    <{v.UV[0]}, {v.UV[1]}>,\n"
        code += "  }\n"
        code += "  face_indices {\n"
        code += f"    {len(faces)},\n"
        for f in faces:
            code += f"    <{f[0]}, {f[1]}, {f[2]}>,\n"
        code += "  }\n"
        code += "  pigment { rgb <1, 1, 1> }\n"
        code += "}\n"
        return code