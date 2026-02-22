import json
import math

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib

STEP_PATH = r"D:\PROJECTS\CAD_ai\part.step"
OUTPUT_PATH = r"D:\PROJECTS\CAD_ai\geometry.json"

# ---------------- LOAD STEP ----------------

reader = STEPControl_Reader()
status = reader.ReadFile(STEP_PATH)

if status != IFSelect_RetDone:
    print("Failed to load STEP.")
    exit()

reader.TransferRoots()
shape = reader.OneShape()

print("STEP Loaded")

# ---------------- GLOBAL PROPERTIES ----------------

bbox = Bnd_Box()
brepbndlib.Add(shape, bbox)
xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()

bounding_box = {
    "x": round(xmax - xmin, 3),
    "y": round(ymax - ymin, 3),
    "z": round(zmax - zmin, 3)
}

mass_props = GProp_GProps()
brepgprop.VolumeProperties(shape, mass_props)

volume = mass_props.Mass()
com = mass_props.CentreOfMass()

global_data = {
    "bounding_box": bounding_box,
    "volume": round(volume, 3),
    "center_of_mass": [
        round(com.X(), 3),
        round(com.Y(), 3),
        round(com.Z(), 3)
    ]
}

# ---------------- FACE EXTRACTION ----------------

faces = []
planar_surfaces = []
cylindrical_surfaces = []

face_explorer = TopExp_Explorer(shape, TopAbs_FACE)
face_id = 0

while face_explorer.More():

    face = face_explorer.Current()
    surface = BRepAdaptor_Surface(face)
    surf_type = surface.GetType()

    props = GProp_GProps()
    brepgprop.SurfaceProperties(face, props)
    area = props.Mass()

    face_data = {
        "id": face_id,
        "area": round(area, 3)
    }

    if surf_type == GeomAbs_Plane:
        plane = surface.Plane()
        normal = plane.Axis().Direction()
        location = plane.Axis().Location()

        face_data["type"] = "plane"
        face_data["normal"] = [
            round(normal.X(), 3),
            round(normal.Y(), 3),
            round(normal.Z(), 3)
        ]
        face_data["point"] = [
            round(location.X(), 3),
            round(location.Y(), 3),
            round(location.Z(), 3)
        ]

        planar_surfaces.append(face_data)

    elif surf_type == GeomAbs_Cylinder:
        cylinder = surface.Cylinder()
        axis = cylinder.Axis()
        direction = axis.Direction()
        location = axis.Location()

        face_data["type"] = "cylinder"
        face_data["radius"] = round(cylinder.Radius(), 3)
        face_data["axis"] = [
            round(direction.X(), 3),
            round(direction.Y(), 3),
            round(direction.Z(), 3)
        ]
        face_data["center"] = [
            round(location.X(), 3),
            round(location.Y(), 3),
            round(location.Z(), 3)
        ]

        cylindrical_surfaces.append(face_data)

    else:
        face_data["type"] = "other"

    faces.append(face_data)

    face_id += 1
    face_explorer.Next()

# ---------------- WALL THICKNESS ESTIMATION ----------------

thickness_values = []

for i in range(len(planar_surfaces)):
    for j in range(i+1, len(planar_surfaces)):

        n1 = planar_surfaces[i]["normal"]
        n2 = planar_surfaces[j]["normal"]

        dot = n1[0]*n2[0] + n1[1]*n2[1] + n1[2]*n2[2]

        if abs(abs(dot) - 1) < 0.05:

            p1 = planar_surfaces[i]["point"]
            p2 = planar_surfaces[j]["point"]

            d = abs(
                (p2[0] - p1[0]) * n1[0] +
                (p2[1] - p1[1]) * n1[1] +
                (p2[2] - p1[2]) * n1[2]
            )

            thickness_values.append(round(d, 3))

wall_stats = {}

if thickness_values:
    wall_stats = {
        "min": min(thickness_values),
        "max": max(thickness_values),
        "mean": round(sum(thickness_values)/len(thickness_values), 3),
        "count": len(thickness_values)
    }

# ---------------- FINAL SCHEMA ----------------

geometry = {
    "global": global_data,
    "faces": faces,
    "planar_surfaces": planar_surfaces,
    "cylindrical_surfaces": cylindrical_surfaces,
    "wall_thickness_distribution": wall_stats
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(geometry, f, indent=4)

print("geometry.json generated successfully.")