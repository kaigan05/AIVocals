import os, sys
now_dir = os.getcwd()
sys.path.append(now_dir)
import sys
import torch
# import tqdm as tq
from multiprocessing import cpu_count
from config import Config


from lib.infer.modules.vc.modules import VC
hubert_model = None
from dotenv import load_dotenv


# current_script_path = os.path.abspath(__file__)
# now_dir = os.path.dirname(current_script_path)
output_dir = f"{now_dir}/assets/audios/outputs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
import mdx as mdx
_,results = mdx.uvr(
    model_name="UVR-MDX-NET-Voc_FT.onnx",
    input_dir="./",
    output_dir=f"{now_dir}/assets/audios/outputs",
    agg=1,
    format0="wav",
    architecture="MDX",
)
f0up_key = 0
input_path = "./assets/audios/origin_linhsan.mp3"
f0method = "rmvpe"

index_path = "./assets/rvc_models/added_IVF1291_Flat_nprobe_1_Fonos_1_split_v2.index"
model_path = "./assets/rvc_models/Fonos_1_split.pth"
index_rate = 0.5
device = "cuda:0"
is_half = False
filter_radius = 3
resample_sr = 0
rms_mix_rate = 1
protect = 0.33
load_dotenv()
config = Config(device)
vc = VC(config)
vc.get_vc(model_path)
from merge import audio_combined
for result in results:
    vocals_save_path, instrumental_save_path = result
    print ("RVC")
    conver_vocal = vc.vc_single(
            0, vocals_save_path,output_dir, f0up_key, None, f0method, index_path, None, index_rate , 3, 0, 0.25, 0.33, "wav", False, 120, 50, "" , 1100, "", False
        )
    print ("COMBINE")
    audio_combined(conver_vocal,instrumental_save_path,output_dir)
