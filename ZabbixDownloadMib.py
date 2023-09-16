import os
import json
import requests

def download_mib(mib_name, mib_dir_path):
    url = f"https://bestmonitoringtools.com/mibdb/mibs/{mib_name}.mib"
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(mib_dir_path, f"{mib_name}.txt"), "wb") as f:
            f.write(response.content)
        print(f"Downloaded {mib_name}.txt successfully.")
    else:
        print(f"Failed to download {mib_name}.txt.")

def main(mib_name, mib_dir_path):
    # Download the main MIB
    download_mib(mib_name, mib_dir_path)

    # Load the JSON data
    url = f"https://bestmonitoringtools.com/mibdb/mibs_json/{mib_name}.json"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        dependencies = [mib for mib in json_data.get("imports", {}) if mib != "class"]
        for dependency in dependencies:
            download_mib(dependency, mib_dir_path)
    else:
        print(f"Failed to fetch JSON data for {mib_name}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 mib_downloader.py <MIB_name> <MIB_DIR_PATH>")
    else:
        mib_name = sys.argv[1]
        mib_dir_path = sys.argv[2]
        main(mib_name, mib_dir_path)
