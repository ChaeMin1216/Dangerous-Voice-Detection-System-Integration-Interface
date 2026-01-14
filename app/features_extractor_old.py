import os
import numpy as np
import librosa
import tensorflow as tf
import pickle  # LabelEncoder 로드를 위해 필요

# Raw audio 데이터를 읽는 함수 정의
#def read_raw_audio(file_path, sample_rate=16000, dtype=np.int16):
#    audio_data = np.fromfile(file_path, dtype=dtype)
#    audio_data = audio_data.astype(np.float32)
#    audio_data /= np.max(np.abs(audio_data))  # 정규화
#    return audio_data

def read_raw_audio(file_path, sample_rate=16000, dtype=np.int16):
    audio_data = np.fromfile(file_path, dtype=dtype)
    audio_data = audio_data.astype(np.float32)
    
    # 최대 절대값 계산
    max_value = np.max(np.abs(audio_data))
    
    # 최대값이 0이 아닌 경우에만 정규화
    if max_value != 0:
        audio_data /= max_value  # 정규화
    else:
        print(f"Warning: {file_path} contains all zeros or is empty.")
    
    return audio_data



# MFCC 특징 추출 함수 정의
#def features_extractor(file, sample_rate=16000):
#    audio = read_raw_audio(file, sample_rate=sample_rate)
    
    # MFCC 추출
#    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
#    scaled_mfcc = np.mean(mfcc.T, axis=0)
#   return scaled_mfcc


def features_extractor(file, sample_rate=16000):
    audio = read_raw_audio(file, sample_rate=sample_rate)

    # 오디오 데이터가 유효한지 확인
    if not np.isfinite(audio).all():
        raise ValueError(f"Audio buffer is not finite everywhere in file: {file}")

    # MFCC 추출
    mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    scaled_mfcc = np.mean(mfcc.T, axis=0)
    return scaled_mfcc

