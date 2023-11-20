import struct

class PmxHeader:
    def __init__(self) -> None:
        __slots__ = [
            "Signature",
            "Version",
            "GlobalsCount",
            "Globals",
            "ModelNameLocal",
            "ModelNameUniversal",
            "CommentsLocal",
            "CommentsUniversal"
        ]
        self.Signature = ""
        self.Version = 0.0
        self.GlobalsCount = 0
        self.Globals = []
        self.ModelNameLocal = ""
        self.ModelNameUniversal = ""
        self.CommentsLocal = ""
        self.CommentsUniversal = ""

class PmxVertex:
    def __init__(self) -> None:
        __slots__ = [
            "Position",
            "Normal",
            "UV",
            "AdditionalVec4",
            "WeightDeformType",
            "WeightDeform",
            "EdgeScale"
        ]
        self.Position = [0.0, 0.0, 0.0]
        self.Normal = [0.0, 0.0, 0.0]
        self.UV = [0.0, 0.0]
        self.AdditionalVec4 = []
        self.WeightDeformType = 0
        self.WeightDeform = []
        self.EdgeScale = 0.0

class PmxMaterial:
    def __init__(self) -> None:
        __slots__ = [
            "NameLocal",
            "NameUniversal",
            "DiffuseColor",
            "SpecularColor",
            "SpecularStrength",
            "AmbientColor",
            "DrawingFlags",
            "EdgeColor",
            "EdgeScale",
            "TextureIndex",
            "EnvironmentIndex",
            "EnvironmentBlendMode",
            "ToonReference",
            "ToonValue",
            "MetaData",
            "SurfaceCount"
        ]
        self.NameLocal = ""
        self.NameUniversal = ""
        self.DiffuseColor = [0.0, 0.0, 0.0, 0.0]
        self.SpecularColor = [0.0, 0.0, 0.0]
        self.SpecularStrength = 0.0
        self.AmbientColor = [0.0, 0.0, 0.0]
        self.DrawingFlags = 0
        self.EdgeColor = [0.0, 0.0, 0.0, 0.0]
        self.EdgeScale = 0.0
        self.TextureIndex = 0
        self.EnvironmentIndex = 0
        self.EnvironmentBlendMode = 0
        self.ToonReference = 0
        self.ToonValue = 0
        self.MetaData = ""
        self.SurfaceCount = 0
        

class Pmx:
    def __init__(self) -> None:
        self.GlobalInfo = {
            "Text encoding": "",
            "Additional vec4 count": 0,
            "Vertex index size": 0,
            "Texture index size": 0,
            "Material index size": 0,
            "Bone index size": 0,
            "Morph index size": 0,
            "Rigid body index size": 0
        }
        self.Header = PmxHeader()
        self.Vertices = []
        self.Faces = []
        self.Textures = []
        self.Materials = []

class PmxImporter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def print_text_info(text, info):
        if info == "":
            print("No " + text + " info!")
        else:
            print(text + ": " + info)

    @staticmethod
    def load(filepath: str):
        pmx = Pmx()
        # read pmx file
        with open(filepath, 'rb') as pmx_file:
            #----------------------------------------
            # load header
            pmx.Header.Signature = pmx_file.read(4).decode('utf-8')
            if pmx.Header.Signature != "PMX ":
                raise Exception("Not a pmx file!")
            else:
                print("Loading pmx...")

            pmx.Header.Version = struct.unpack('<f', pmx_file.read(4))[0]
            print("Pmx version: " + str(pmx.Header.Version))

            pmx.Header.GlobalsCount = struct.unpack('<B', pmx_file.read(1))[0]
            pmx.Header.Globals = list(pmx_file.read(pmx.Header.GlobalsCount))
            pmx.GlobalInfo["Text encoding"] = "utf-8" if pmx.Header.Globals[0] else "utf-16"
            pmx.GlobalInfo["Additional vec4 count"] = pmx.Header.Globals[1]
            pmx.GlobalInfo["Vertex index size"] = pmx.Header.Globals[2]
            pmx.GlobalInfo["Texture index size"] = pmx.Header.Globals[3]
            pmx.GlobalInfo["Material index size"] = pmx.Header.Globals[4]
            pmx.GlobalInfo["Bone index size"] = pmx.Header.Globals[5]
            pmx.GlobalInfo["Morph index size"] = pmx.Header.Globals[6]
            pmx.GlobalInfo["Rigid body index size"] = pmx.Header.Globals[7]

            pmx.Header.ModelNameLocal = pmx_file.read(struct.unpack('<I', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
            pmx.Header.ModelNameUniversal = pmx_file.read(struct.unpack('<I', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
            pmx.Header.CommentsLocal = pmx_file.read(struct.unpack('<I', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
            pmx.Header.CommentsUniversal = pmx_file.read(struct.unpack('<I', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])


            # change the type of index to struct.unpack format
            vertex_index_type = {1: 'B', 2: 'H', 4: 'I'}[pmx.GlobalInfo["Vertex index size"]]
            bone_index_type = {1: 'b', 2: 'h', 4: 'i'}[pmx.GlobalInfo["Bone index size"]]
            texture_index_type = {1: 'b', 2: 'h', 4: 'i'}[pmx.GlobalInfo["Texture index size"]]
            material_index_type = {1: 'b', 2: 'h', 4: 'i'}[pmx.GlobalInfo["Material index size"]]
            morph_index_type = {1: 'b', 2: 'h', 4: 'i'}[pmx.GlobalInfo["Morph index size"]]
            rigidbody_index_type = {1: 'b', 2: 'h', 4: 'i'}[pmx.GlobalInfo["Rigid body index size"]]
            
            #----------------------------------------
            # load vertices
            vertex_count = struct.unpack('<i', pmx_file.read(4))[0]
            print("Vertex count: " + str(vertex_count))
            for i in range(vertex_count):
                vertex = PmxVertex()
                
                vertex.Position = struct.unpack('<3f', pmx_file.read(12))
                vertex.Normal = struct.unpack('<3f', pmx_file.read(12))
                vertex.UV = struct.unpack('<2f', pmx_file.read(8))
                for _ in range(pmx.GlobalInfo["Additional vec4 count"]):
                    vertex.AdditionalVec4.append(struct.unpack('<4f', pmx_file.read(16)))

                vertex.WeightDeformType = struct.unpack('<b', pmx_file.read(1))[0]
                # struct: [(bone, weight),...]
                if vertex.WeightDeformType == 0:
                    BDEF1 = struct.unpack('<'+bone_index_type, pmx_file.read(pmx.GlobalInfo["Bone index size"]))[0]
                    vertex.WeightDeform.append((BDEF1, 1.0))
                elif vertex.WeightDeformType == 1:
                    BDEF2 = struct.unpack('<'+bone_index_type*2+'f', pmx_file.read(pmx.GlobalInfo["Bone index size"]*2+4))
                    vertex.WeightDeform.extend([(BDEF2[0], BDEF2[2]),
                                                (BDEF2[1], 1-BDEF2[2])])
                elif vertex.WeightDeformType == 2:
                    BDEF4 = struct.unpack('<'+bone_index_type*4+'f'*4, pmx_file.read(pmx.GlobalInfo["Bone index size"]*4+16))
                    vertex.WeightDeform.extend([(BDEF4[0], BDEF4[4]),
                                                (BDEF4[1], BDEF4[5]),
                                                (BDEF4[2], BDEF4[6]),
                                                (BDEF4[3], BDEF4[7])])
                elif vertex.WeightDeformType == 3:
                    SDEF = struct.unpack('<'+bone_index_type*2+'f'*10, pmx_file.read(pmx.GlobalInfo["Bone index size"]*2+40))
                    vertex.WeightDeform.extend([(SDEF[0], SDEF[2]),
                                                (SDEF[1], 1-SDEF[2]),
                                                {'C': SDEF[3:6], 'R0': SDEF[6:9], 'R1': SDEF[9:12]}])
                elif vertex.WeightDeformType == 4:
                    QDEF = struct.unpack('<'+bone_index_type*4+'f'*4, pmx_file.read(pmx.GlobalInfo["Bone index size"]*4+16))
                    vertex.WeightDeform.extend([(QDEF[0], QDEF[4]),
                                                (QDEF[1], QDEF[5]),
                                                (QDEF[2], QDEF[6]),
                                                (QDEF[3], QDEF[7])])
                elif vertex.WeightDeformType == -1:
                    pass
                else:
                    raise Exception(f'Weight Type {vertex.WeightDeformType} not found!')
                
                vertex.EdgeScale = struct.unpack('<f', pmx_file.read(4))[0]
                pmx.Vertices.append(vertex)
                
            #----------------------------------------
            # load faces
            face_count = struct.unpack('<i', pmx_file.read(4))[0]//3
            print("Face count: " + str(face_count))
            for i in range(face_count):
                pmx.Faces.append(struct.unpack('<'+vertex_index_type*3, pmx_file.read(pmx.GlobalInfo["Vertex index size"]*3)))

            #----------------------------------------
            # load textures
            texture_count = struct.unpack('<i', pmx_file.read(4))[0]
            print("Texture count: " + str(texture_count))
            for i in range(texture_count):
                pmx.Textures.append(pmx_file.read(struct.unpack('<i', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"]))

            #----------------------------------------
            # load materials
            material_count = struct.unpack('<i', pmx_file.read(4))[0]
            print("Material count: " + str(material_count))
            for i in range(material_count):
                material = PmxMaterial()
                material.NameLocal = pmx_file.read(struct.unpack('<i', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
                material.NameUniversal = pmx_file.read(struct.unpack('<i', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
                material.DiffuseColor = struct.unpack('<4f', pmx_file.read(16))
                material.SpecularColor = struct.unpack('<3f', pmx_file.read(12))
                material.SpecularStrength = struct.unpack('<f', pmx_file.read(4))[0]
                material.AmbientColor = struct.unpack('<3f', pmx_file.read(12))
                DrawingFlags = struct.unpack('<b', pmx_file.read(1))[0]
                material.DrawingFlags = {
                    "Both faces": DrawingFlags & 0b00000001,
                    "Ground shadow": DrawingFlags & 0b00000010,
                    "Self shadow map": DrawingFlags & 0b00000100,
                    "Self shadow": DrawingFlags & 0b00001000,
                    "Edge": DrawingFlags & 0b00010000,
                    "Vertex color": DrawingFlags & 0b00100000,
                    "Point drawing": DrawingFlags & 0b01000000,
                    "Line drawing": DrawingFlags & 0b10000000
                }
                material.EdgeColor = struct.unpack('<4f', pmx_file.read(16))
                material.EdgeScale = struct.unpack('<f', pmx_file.read(4))[0]
                material.TextureIndex = struct.unpack('<'+texture_index_type, pmx_file.read(pmx.GlobalInfo["Texture index size"]))[0]
                material.EnvironmentIndex = struct.unpack('<'+texture_index_type, pmx_file.read(pmx.GlobalInfo["Texture index size"]))[0]
                material.EnvironmentBlendMode = struct.unpack('<b', pmx_file.read(1))[0]
                material.ToonReference = struct.unpack('<b', pmx_file.read(1))[0]
                if material.ToonReference == 0: # texture
                    material.ToonValue = struct.unpack('<'+texture_index_type, pmx_file.read(pmx.GlobalInfo["Texture index size"]))[0]
                elif material.ToonReference == 1: # toon
                    material.ToonValue = struct.unpack('<b', pmx_file.read(1))[0]
                else:
                    raise Exception(f'Toon Reference {material.ToonReference} not found!')
                material.MetaData = pmx_file.read(struct.unpack('<i', pmx_file.read(4))[0]).decode(pmx.GlobalInfo["Text encoding"])
                material.SurfaceCount = struct.unpack('<i', pmx_file.read(4))[0]
                pmx.Materials.append(material)

            #----------------------------------------
            # load bones


        return pmx



if __name__ == '__main__':
    pmx = PmxImporter.load(r"pmx2pov\pmx\YYB Hatsune Miku_10th\YYB Hatsune Miku_10th_v1.02.pmx")
    PmxImporter.print_text_info("Model name(local)", pmx.Header.ModelNameLocal)
    PmxImporter.print_text_info("Model name(universal)", pmx.Header.ModelNameUniversal)
    PmxImporter.print_text_info("Comments(local)", pmx.Header.CommentsLocal)
    PmxImporter.print_text_info("Comments(universal)", pmx.Header.CommentsUniversal)
    sum = 0
    for mat in pmx.Materials:
        sum += mat.SurfaceCount
    print(sum)
    print(len(pmx.Faces*3))



