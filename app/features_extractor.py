import os
import numpy as np
import librosa
import tensorflow as tf
import soundfile as sf
from tensorflow.keras.models import load_model
import pickle  # LabelEncoder 로드를 위해 필요



def read_raw_audio(file_path, sample_rate=16000, dtype=np.float16):
    #audio_data = np.fromfile(file_path, dtype=dtype)
    audio_data, sr = sf.read(file_path, channels=1, samplerate=sample_rate, format="RAW", subtype="PCM_16" )
    audio_data = audio_data.astype(np.float32)
    audio_data /= np.max(np.abs(audio_data))# 정규화

    #audio_data /= 32768.0  # 정규화
    return audio_data

# MFCC 특징 추출 함수 정의
def features_extractor(file, sample_rate=16000):
    audio = read_raw_audio(file, sample_rate=sample_rate)
    
    # MFCC 추출
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40) #, n_fft=2048)
    scaled_mfcc = np.mean(mfcc.T, axis=0)
    return scaled_mfcc
