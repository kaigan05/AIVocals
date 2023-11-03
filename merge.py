import sys

sys.path.append("..")
import os
# import shutil

now_dir = os.getcwd()
# import soundfile as sf
# import librosa
from lib.tools import audioEffects
from assets.i18n.i18n import I18nAuto

i18n = I18nAuto()
# import gradio as gr
# import tabs.resources as resources
# import numpy as np
def generate_output_path(output_folder, base_name, extension):
    index = 1
    while True:
        output_path = os.path.join(output_folder, f"{base_name}_{index}.{extension}")
        if not os.path.exists(output_path):
            return output_path
        index += 1
from pydub import AudioSegment
# from pydub.silence import detect_nonsilent
# import glob
# import re
def combine_and_save_audios(
    audio1_path, audio2_path, output_path, volume_factor_audio1, volume_factor_audio2
):
    audio1 = AudioSegment.from_file(audio1_path)
    audio2 = AudioSegment.from_file(audio2_path)
    
    # Verificar cuál audio tiene mayor longitud
    if len(audio1) > len(audio2):
        # Calcular la diferencia en duración en segundos
        diff_duration_seconds = (len(audio1) - len(audio2)) / 1000.0  # Convertir a segundos
        print(f"diff_duration_seconds: {diff_duration_seconds} seconds")
        # Crear el segmento de silencio en Pydub
        silence = AudioSegment.silent(duration=int(diff_duration_seconds))  # Convertir a milisegundos

        # Agregar el silencio al audio2 para igualar la duración
        audio2 = audio2 + silence
    else:
        # Calcular la diferencia en duración en segundos
        diff_duration_seconds = (len(audio2) - len(audio1)) / 1000.0  # Convertir a segundos
        print(f"diff_duration_seconds: {diff_duration_seconds} seconds")
        # Crear el segmento de silencio en Pydub
        silence = AudioSegment.silent(duration=int(diff_duration_seconds))  # Convertir a milisegundos

        # Agregar el silencio al audio1 para igualar la duración
        audio1 = audio1 + silence

    # Ajustar el volumen de los audios multiplicando por el factor de ganancia
    if volume_factor_audio1 != 1.0:
        audio1 *= volume_factor_audio1
    if volume_factor_audio2 != 1.0:
        audio2 *= volume_factor_audio2

    # Combinar los audios
    combined_audio = audio1.overlay(audio2)

    # Guardar el audio combinado en el archivo de salida
    combined_audio.export(output_path, format="wav")
            
def audio_combined(
    audio1_path,
    audio2_path,
    output_dir,
    volume_factor_audio1=1.0,
    volume_factor_audio2=1.0,
    reverb_enabled=False,
    compressor_enabled=False,
    noise_gate_enabled=False,
):
    output_folder = os.path.join(now_dir,output_dir)
    os.makedirs(output_folder, exist_ok=True)

    # Generar nombres únicos para los archivos de salida
    base_name = f"{os.path.splitext(os.path.basename(audio1_path))[0]}_combine"
    extension = "wav"
    output_path = generate_output_path(output_folder, base_name, extension)

    if reverb_enabled or compressor_enabled or noise_gate_enabled:
        # Procesa el primer audio con los efectos habilitados
        base_name = "effect_audio"
        output_path = generate_output_path(output_folder, base_name, extension)
        processed_audio_path = audioEffects.process_audio(
            audio2_path,
            output_path,
            reverb_enabled,
            compressor_enabled,
            noise_gate_enabled,
        )
        base_name = "combined_audio"
        output_path = generate_output_path(output_folder, base_name, extension)
        # Combina el audio procesado con el segundo audio usando audio_combined
        combine_and_save_audios(
            audio1_path,
            processed_audio_path,
            output_path,
            volume_factor_audio1,
            volume_factor_audio2,
        )

        return i18n("Conversion complete!"), output_path
    else:
        # base_name = "combined_audio"
        output_path = generate_output_path(output_folder, base_name, extension)
        # No hay efectos habilitados, combina directamente los audios sin procesar
        combine_and_save_audios(
            audio1_path,
            audio2_path,
            output_path,
            volume_factor_audio1,
            volume_factor_audio2,
        )

        return i18n("Conversion complete!"), output_path