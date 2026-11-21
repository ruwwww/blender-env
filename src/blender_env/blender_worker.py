"""Executed only by Blender's embedded Python interpreter."""
import json, sys
from pathlib import Path
import bpy


def main():
    req_path, res_path = [Path(x) for x in sys.argv[sys.argv.index("--") + 1:]]
    req = json.loads(req_path.read_text(encoding="utf-8"))
    op = req["op"]
    if op == "reset":
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)
    elif op == "create_cube":
        if any(o.type == "MESH" for o in bpy.context.scene.objects):
            raise ValueError("Only one mesh object is allowed")
        bpy.ops.mesh.primitive_cube_add(size=2.0)
    elif op == "set_dimensions":
        obj = next((o for o in bpy.context.scene.objects if o.type == "MESH"), None)
        if obj is None:
            raise ValueError("Create the cube before setting dimensions")
        dims = req["dimensions"]
        if len(dims) != 3 or any(float(x) <= 0 or float(x) > 100 for x in dims):
            raise ValueError("Dimensions must be three positive values <= 100")
        obj.dimensions = [float(x) for x in dims]
        bpy.context.view_layer.update()
    elif op == "bevel":
        obj = next((o for o in bpy.context.scene.objects if o.type == "MESH"), None)
        if obj is None:
            raise ValueError("Create the cube before beveling")
        width = float(req.get("width", 0.05))
        if not 0 < width <= 0.25:
            raise ValueError("Bevel width must be in (0, 0.25]")
        mod = obj.modifiers.new(name="AgentBevel", type="BEVEL")
        mod.width, mod.segments = width, 2
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    elif op != "finish":
        raise ValueError("Unsupported operation")
    scene_path = Path(req["scene_path"])
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path))
    bpy.context.view_layer.update()
    objects = []
    for obj in bpy.context.scene.objects:
        if obj.type == "MESH":
            objects.append({"name": obj.name, "dimensions": [float(x) for x in obj.dimensions],
                            "vertex_count": len(obj.data.vertices),
                            "polygon_count": len(obj.data.polygons),
                            "location": [float(x) for x in obj.location]})
    res_path.write_text(json.dumps({"execution_ok": True, "objects": objects}), encoding="utf-8")


if __name__ == "__main__":
    main()
