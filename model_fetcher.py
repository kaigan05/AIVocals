import os
import requests
from tqdm import tqdm
# import subprocess
import shutil
# import platform
import logging
import os
import zipfile
import shutil
# import urllib.request
logger = logging.getLogger(__name__)

URL_BASE = "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main"
RVC_MODELS = "https://huggingface.co/kaigan05/FN/resolve/main"
models_download = [
    ("pretrained/", [
        "D32k.pth", "D40k.pth", "D48k.pth",
        "G32k.pth", "G40k.pth", "G48k.pth",
        "f0D32k.pth", "f0D40k.pth", "f0D48k.pth",
        "f0G32k.pth", "f0G40k.pth", "f0G48k.pth",
    ]),
    ("pretrained_v2/", [
        "D32k.pth", "D40k.pth", "D48k.pth",
        "G32k.pth", "G40k.pth", "G48k.pth",
        "f0D32k.pth", "f0D40k.pth", "f0D48k.pth",
        "f0G32k.pth", "f0G40k.pth", "f0G48k.pth",
    ]),
    ("", ["ffmpeg.exe", "ffprobe.exe"]),  # ffmpeg and ffprobe go to the main folder
]
models_vocals = [
    ("FN_1_split.zip", "assets/rvc_models/"),
]
# List of individual files with their respective local and remote paths
individual_files = [
    ("hubert_base.pt", "assets/hubert/"),
    ("rmvpe.pt", "assets/rmvpe/"),
    # ("rmvpe.onnx", "assets/rmvpe/"),
]

# Create a dictionary to map remote folders to local folders
folder_mapping = {
    "pretrained/": "assets/pretrained/",
    "pretrained_v2/": "assets/pretrained_v2/",
    "": "",  # Default folder for files without a remote folder
}

# Function to download a file with tqdm progress bar
def download_file_with_progress(url, destination_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 KB blocks

    with open(destination_path, 'wb') as file, tqdm(
            desc=os.path.basename(destination_path),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))

def extract_zip(extraction_folder, zip_name):
    os.makedirs(extraction_folder,exist_ok=True)
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(extraction_folder)
    os.remove(zip_name)

    index_filepath, model_filepath = None, None
    for root, dirs, files in os.walk(extraction_folder):
        for name in files:
            if name.endswith('.index') and os.stat(os.path.join(root, name)).st_size > 1024 * 100:
                index_filepath = os.path.join(root, name)

            if name.endswith('.pth') and os.stat(os.path.join(root, name)).st_size > 1024 * 1024 * 40:
                model_filepath = os.path.join(root, name)

    if not model_filepath:
        raise Exception(f'No .pth model file was found in the extracted zip. Please check {extraction_folder}.')

    # move model and index file to extraction folder
    os.rename(model_filepath, os.path.join(extraction_folder, os.path.basename(model_filepath)))
    if index_filepath:
        os.rename(index_filepath, os.path.join(extraction_folder, os.path.basename(index_filepath)))

    # remove any unnecessary nested folders
    for filepath in os.listdir(extraction_folder):
        if os.path.isdir(os.path.join(extraction_folder, filepath)):
            shutil.rmtree(os.path.join(extraction_folder, filepath))
# Download torch crepe if not exists
# if not os.path.exists("torchcrepe"):
#     os_name = platform.system()
#     # Cloning the GitHub repository into the temporary directory
#     print("Cloning the GitHub repository into the temporary directory...")
#     subprocess.run(["git", "clone", "https://github.com/maxrmorrison/torchcrepe.git", "temp_torchcrepe"])

#     # Copying the torchcrepe folder to a different location
#     print("Copying the torchcrepe folder...")
#     shutil.copytree("temp_torchcrepe/torchcrepe", "./torchcrepe")

#     # Removing the temporary directory
#     print("Removing the temporary directory...")
#     print(os_name)
#     if os_name == "Windows":
#         subprocess.run("rmdir /s /q temp_torchcrepe", shell=True)
#     if os_name == "Linux":
#         shutil.rmtree("temp_torchcrepe")

# # Download files that do not exist
# for remote_folder, file_list in models_download:
#     local_folder = folder_mapping.get(remote_folder, "")
#     for file in file_list:
#         destination_path = os.path.join(local_folder, file)
#         url = f"{URL_BASE}/{remote_folder}{file}"
#         if not os.path.exists(destination_path):
#             print(f"Downloading {url} to {destination_path}...")
#             download_file_with_progress(url, destination_path)  # Use the function tdqm

# Download individual files
for file_name, local_folder in individual_files:
    destination_path = os.path.join(local_folder, file_name)
    url = f"{URL_BASE}/{file_name}"
    if not os.path.exists(destination_path):
        print(f"Downloading {url} to {destination_path}...")
        download_file_with_progress(url, destination_path)  # Use the function tdqm

for file_name, local_folder in models_vocals:
    destination_path = os.path.join(local_folder, file_name)
    url = f"{RVC_MODELS}/{file_name}"
    if not os.path.exists(destination_path):
        print(f"Downloading {url} to {destination_path}...")
        download_file_with_progress(url, destination_path)  # Use the function tdqm
        extract_zip(local_folder, destination_path)

