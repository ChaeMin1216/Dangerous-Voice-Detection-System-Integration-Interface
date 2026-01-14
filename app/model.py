import tensorflow as tf
import numpy as np
import pickle

# 모델 불러오기
#class RiskModel:

#def __init__(self, model_path: str, label_encoder_path: str):
#        self.model = tf.keras.models.load_model(model_path)
#        with open(label_encoder_path, 'rb') as f:
#            self.label_encoder = pickle.load(f)

#    def predict(self, features: np.ndarray) -> str:
#        prediction = self.model.predict(features)
#        predicted_class_index = np.argmax(prediction, axis=1)[0]
#        predicted_label = self.label_encoder.inverse_transform([predicted_class_index])[0]
#        return predicted_label

class RiskModel:
    def __init__(self, model_path: str, label_encoder_path: str):
        self.model = tf.keras.models.load_model(model_path)
        with open(label_encoder_path, 'rb') as f:
            self.label_encoder = pickle.load(f)
    
#    def predict(file_path):
#        mfcc_features = extract_mfcc_from_raw(file_path)
#        mfcc_features = np.expand_dims(mfcc_features, axis=0)
#        predictions = model.predict(mfcc_features)
#        predicted_class = np.argmax(predictions, axis=1)
#        class_label = labelencoder.inverse_transform(predicted_class)[0]
#        return class_label

    def predict(self, features: np.ndarray) -> str:
        # 입력 차원 확인

        # 모델이 형태가 (None, 40)
        if features.ndim == 1:  
            features = features.reshape(1, -1)  # (1, 40) 형태로 변환
        prediction = self.model.predict(features)
        predicted_class_index = np.argmax(prediction, axis=1)[0]
        predicted_label = self.label_encoder.inverse_transform([predicted_class_index])[0]
        return predicted_label



# 모델 인스턴스 생성
risk_model = RiskModel('../model/classification(mfcc_no_fft_1sec).keras', '../model/label_encoder.pkl')
# 정확한 모델 위치 기입
