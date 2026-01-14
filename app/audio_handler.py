import numpy as np
from datetime import datetime
from features_extractor import features_extractor
from model import risk_model
import pickle

# label_encoder.pkl 파일 로드
#with open('../model/label_encoder.pkl', 'rb') as f: #정확한 label 코드 위치 기입
#    labelencoder = pickle.load(f)

device_list = []

def get_device_index(file_path):
    global device_list

    file_name = file_path.split('/')[-1]
    device_name = file_name.split('-')[0]

    if device_name in device_list:
        print(device_list)
        return device_list.index(device_name)
    else:
        device_list.append(device_name)
        print(device_list)
        return len(device_list) - 1

async def process_audio_file(file_path: str, Audio_Id: int, websocket_manager):
    try:
        # 오디오 파일에서 특징 추출
        mfccs_features = features_extractor(file_path)
        #mfccs_scaled_features = mfccs_features.reshape(1, -1)
        # 예측 수행
        #x_predict = risk_model.predict(mfccs_features) 
        #print(x_predict)

        # 예측 결과의 인덱스를 라벨로 변환
        #predicted_label_index = np.argmax(x_predict, axis=1)[0]
        #predicted_label = labelencoder.classes_[predicted_label_index]
        #print(predicted_label)
        predicted_label = risk_model.predict(mfccs_features)
        print(f"Predicted Label: {predicted_label}")
        # 위험 판단 (normal이 아닌 경우 danger = 1)
        if predicted_label != 'normal':
            danger = 1
        else:
            danger = 0

        Audio_Id = get_device_index(file_path)

        # 응답 생성
        response = {
            "Result": predicted_label,
            "Audio_Id": Audio_Id,
            "Is_Danger": danger,
            "Time": datetime.now().isoformat(),
            "File_Name": file_path.split('/')[-1]
        }

        # 웹소켓을 통해 JSON 전송
        await websocket_manager.send_json(response)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

