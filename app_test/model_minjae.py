import tensorflow as tf
import numpy as np
import pickle  # joblib 대신 pickle을 사용
import os

class RiskModel:
    def __init__(self, model_path: str, label_encoder_path: str):
        # 모델 파일과 레이블 인코더 파일이 존재하는지 확인
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        if not os.path.isfile(label_encoder_path):
            raise FileNotFoundError(f"Label encoder file not found at {label_encoder_path}")

        # 모델과 레이블 인코더 로드
        self.model = tf.keras.models.load_model(model_path)
        
        # pickle을 사용하여 레이블 인코더 로드
        with open(label_encoder_path, 'rb') as file:
            self.label_encoder = pickle.load(file)

    def predict(self, features: np.ndarray) -> str:
        # 예측 수행
        prediction = self.model.predict(features)
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        predicted_label = self.label_encoder.inverse_transform([predicted_class_index])[0]
        return predicted_label

# 모델 인스턴스 생성
risk_model = RiskModel('../model/test4.keras', '../model/labelencoder(test4).pkl')

