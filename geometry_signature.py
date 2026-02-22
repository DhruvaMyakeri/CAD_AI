import json
from collections import Counter

GEOMETRY_PATH = "geometry.json"
FEATURES_PATH = "features.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)


def compute_face_distribution(geometry):
    faces = geometry.get("faces", [])
    total_faces = len(faces)

    if total_faces == 0:
        return {"total_faces": 0, "planar_ratio": 0, "cylindrical_ratio": 0}

    plane_count = sum(1 for f in faces if f.get("type") == "plane")
    cylinder_count = sum(1 for f in faces if f.get("type") == "cylinder")

    return {
        "total_faces": total_faces,
        "planar_ratio": round(plane_count / total_faces, 4),
        "cylindrical_ratio": round(cylinder_count / total_faces, 4)
    }


def compute_bbox_metrics(geometry):
    bbox = geometry["global"]["bounding_box"]
    dx, dy, dz = bbox["x"], bbox["y"], bbox["z"]

    dims = sorted([dx, dy, dz])
    aspect_ratio = round(dims[-1] / dims[0], 4) if dims[0] != 0 else 0

    bbox_volume = dx * dy * dz
    part_volume = geometry["global"]["volume"]
    volume_efficiency = round(part_volume / bbox_volume, 4) if bbox_volume else 0

    return {
        "dimensions_mm": [dx, dy, dz],
        "aspect_ratio": aspect_ratio,
        "bbox_volume_mm3": round(bbox_volume, 4),
        "part_volume_mm3": part_volume,
        "volume_efficiency": volume_efficiency
    }


def compute_axis_distribution(geometry):
    faces = geometry.get("faces", [])
    axes = [
        tuple(f["axis"])
        for f in faces
        if f.get("type") == "cylinder" and "axis" in f
    ]

    if not axes:
        return {"axis_count": 0, "dominant_axis_ratio": 0}

    axis_counts = Counter(axes)
    dominant_count = axis_counts.most_common(1)[0][1]
    total = len(axes)

    return {
        "axis_count": len(axis_counts),
        "dominant_axis_ratio": round(dominant_count / total, 4)
    }


def compute_feature_metrics(features, geometry):
    total_features = features.get("total_features", 0)
    volume = geometry["global"]["volume"]

    density = round(total_features / max(volume, 1), 8)

    return {
        "total_features": total_features,
        "feature_density": density
    }


def generate_geometry_signature():
    geometry = load_json(GEOMETRY_PATH)
    features = load_json(FEATURES_PATH)

    signature = {
        "face_distribution": compute_face_distribution(geometry),
        "bounding_box": compute_bbox_metrics(geometry),
        "axis_distribution": compute_axis_distribution(geometry),
        "feature_metrics": compute_feature_metrics(features, geometry)
    }

    with open("geometry_signature.json", "w") as f:
        json.dump(signature, f, indent=4)

    print(json.dumps(signature, indent=4))
    print("✅ geometry_signature.json saved.")


if __name__ == "__main__":
    generate_geometry_signature()