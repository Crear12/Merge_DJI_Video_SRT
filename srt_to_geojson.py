import re
import json

def extract_coordinates_from_srt(srt_file):
    with open(srt_file, 'r') as f:
        srt_data = f.read()

    pattern = r'\[latitude: ([-+]?\d+\.\d+)\] \[longitude: ([-+]?\d+\.\d+)\]'
    coordinates = re.findall(pattern, srt_data)
    
    return coordinates

def generate_geojson(coordinates):
    features = []
    for i, (lat, lon) in enumerate(coordinates, start=1):
        feature = {
            "type": "Feature",
            "properties": {
                "id": i
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(lon), float(lat)]
            }
        }
        features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson_data

def save_geojson(geojson_data, output_file):
    with open(output_file, 'w') as f:
        json.dump(geojson_data, f, indent=4)

if __name__ == "__main__":
    srt_file = "merged_videos.srt"
    output_file = "merged_videos.geojson"
    
    coordinates = extract_coordinates_from_srt(srt_file)
    geojson_data = generate_geojson(coordinates)
    save_geojson(geojson_data, output_file)
    
    print("GeoJSON file generated successfully.")