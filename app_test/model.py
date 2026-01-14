# app/model.py
import tensorflow as tf
import numpy as np

# 모델 불러오기
class RiskModel:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
    
    def predict(self, features: np.ndarray) -> str:
        prediction = self.model.predict(features)
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        # 예측 결과를 해석하여 문자열로 반환
        # 예시: 위험상황(1) 또는 안전(0)으로 간주
        return predicted_class_index

# 모델 인스턴스 생성
risk_model = RiskModel('../model/test2.keras')
