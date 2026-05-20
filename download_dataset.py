import os
import zipfile
import subprocess
import shutil

print(f"Current Working Directory: {os.getcwd()}")
print("Ensure you have placed your 'kaggle.json' inside 'C:\\Users\\<Username>\\.kaggle\\kaggle.json' before running this script.")
print("This will download the HAM10000 dataset into the 'data' directory.\n")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Ensure kaggle command is available (relies on requirements.txt being installed)
try:
    print("Downloading HAM10000 Dataset...")
    # Using python subprocess to execute kaggle API command
    # URL for HAM10000: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
    subprocess.run(["kaggle", "datasets", "download", "-d", "kmader/skin-cancer-mnist-ham10000", "-p", DATA_DIR], check=True)
except subprocess.CalledProcessError as e:
    print(f"Failed to download dataset. Ensure kaggle API key is configured. Error: {e}")
    exit(1)
except FileNotFoundError:
    print("'kaggle' command not found. Have you installed the requirements.txt with `pip install -r requirements.txt`?")
    exit(1)

# Extract ZIP file
zip_path = os.path.join(DATA_DIR, "skin-cancer-mnist-ham10000.zip")
extract_path = os.path.join(DATA_DIR, "HAM10000")

if os.path.exists(zip_path):
    print(f"Extracting {zip_path}...")
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print("Extraction Complete.")
    print(f"Dataset is ready at '{extract_path}'.")
else:
    print(f"Warning: downloaded zip file not found at {zip_path}")

print("Note: The images will be spread across HAM10000_images_part_1 and HAM10000_images_part_2 folders within the extracted path.")
print("You can run 'python train_model.py' once done.")
