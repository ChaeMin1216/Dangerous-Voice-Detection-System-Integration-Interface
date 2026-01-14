import librosa
import numpy as np

def features_extractor(file):
    with open(file, 'rb') as f:
        raw_audio = np.frombuffer(f.read(), dtype=np.int16)
    
    sample_rate = 16000
    
    audio = raw_audio.astype(np.float32) / 32768.0  # 16-bit PCM을 float으로 변환 (정규화)
    
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    return mfccs_scaled_features
