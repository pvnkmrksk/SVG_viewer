#!/usr/bin/env python3
import pandas as pd  # Import pandas for data handling
import json
import os
import re
import glob  # Import glob for file pattern matching


STOPS_FILE = "stops.txt"
SCHEMATICS_DIR = "schematics"
OUTPUT_JSON = "markers.json"

def main():
    # 1) Read stops.txt into a DataFrame
    stops_df = pd.read_csv(STOPS_FILE, encoding="utf-8")
    stops_dict = pd.Series(zip(stops_df['stop_name'], stops_df['stop_lat'], stops_df['stop_lon']), index=stops_df['stop_id']).to_dict()

    # 2) Use glob to find all .svg files in the schematics directory
    svg_files = glob.glob(os.path.join(SCHEMATICS_DIR, "*.svg"))
    
    # Create a list of markers using a vectorized approach
    marker_list = []

    # Add a check to ensure all SVG files are processed
    if not svg_files:
        print("No SVG files found in the schematics directory.")
        return

    for filepath in svg_files:
        filename = os.path.basename(filepath)
        base = os.path.splitext(filename)[0]  # remove the ".svg"
        
        # Extract IDs using split method
        parts = base.split('_')
        if len(parts) > 2:
            id_part = parts[2].split('-')[0]
            ids = [id_part]  # Wrap in a list to keep the loop structure
        else:
            ids = []  # No valid ID found
        
        for stop_id in ids:
            if stop_id in stops_dict:
                stop_name, lat, lon = stops_dict[stop_id]
                # Add an entry
                marker_list.append({
                    "stopID": stop_id,
                    "name": stop_name,
                    "lat": lat,
                    "lng": lon,
                    "svgFile": filepath  # Use the full path to the .svg
                })
            else:
                print(f"Warning: ID '{stop_id}' not found in stops.txt (filename: {filename})")

    # 3) Write out markers.json
    with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
        json.dump(marker_list, out, indent=2)
    print(f"Wrote {len(marker_list)} marker entries to '{OUTPUT_JSON}'")

if __name__ == "__main__":
    main()
