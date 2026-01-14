import numpy as np
from datetime import datetime
from features_extractor import features_extractor
from model_minjae import risk_model
import os
import json

cctv_mapping_file = "../cctv_mapping.json"

# 식별자 카운터 관리
identifier_counter = {}
next_id = 0

def extract_identifier_from_filename(filename: str) -> str:
    try:
        # 파일 이름에서 '-' 앞부분을 식별자로 사용
        identifier = filename.split('-')[0]
        return identifier
    except IndexError as e:
        print(f"Error extracting identifier from filename {filename}: {e}")
        return None

def get_or_create_id(identifier: str) -> int:
    global next_id
    if identifier not in identifier_counter:
        identifier_counter[identifier] = next_id
        next_id += 1
    return identifier_counter[identifier]

def update_cctv_counter(identifier: str):
#    """식별자를 기반으로 CCTV 카운트를 업데이트하고 JSON 파일에 저장합니다."""
    global identifier_counter
    if identifier not in identifier_counter:
        identifier_counter[identifier] = 0  # 새 식별자가 발견되면 카운트를 0으로 설정
    else:
        identifier_counter[identifier] += 1  # 기존 식별자는 카운트를 1 증가

    # 매핑 파일 저장
    save_cctv_mapping()

def save_cctv_mapping():
#    """식별자 카운트를 JSON 파일에 저장합니다."""
    with open(cctv_mapping_file, 'w') as file:
        json.dump(identifier_counter, file)

async def process_audio_file(file_path: str, websocket_manager):
    try:
        filename = os.path.basename(file_path)
        identifier = extract_identifier_from_filename(filename)

        mfccs_features = features_extractor(file_path)
        predicted_label = risk_model.predict(np.array(mfccs_features).reshape(1, -1))

        print(f"Predicted Label: {predicted_label}")

        danger = 1 if predicted_label != 'normal' else 0

        if identifier:
            audio_id = get_or_create_id(identifier)
            update_cctv_counter(identifier)
        else:
            audio_id = "unknown"

        response = {
            "Result": predicted_label,
            "Audio_Id": audio_id,
            "Is_Danger": danger,
            "Time": datetime.now().isoformat(),
            "File_Name": file_path.split('/')[-1]
        }

        await websocket_manager.send_json(response)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")





















# # app/audio_handler.py

# import os
# from datetime import datetime
# from features_extractor import features_extractor
# from model import risk_model
# import numpy as np

# label_list={
#     0 : 'firealarm',
#     1 : 'emergency_Vehicle',
#     2 : 'glass',
#     3 : 'help',
#     4 : 'normal',
#     5 : 'scream'
#            }

# async def process_audio_file(file_path: str, device_id: str, websocket_manager):
#     # mfccs_features = features_extractor(file_path)
#     # mfccs_scaled_features=mfccs_features.reshape(1,-1)
#     # x_predict=risk_model.predict(mfccs_scaled_features) 
#     # print(x_predict)
#     # result=np.argmax(x_predict,axis=1)
    
#     mfccs_features = features_extractor(file_path)
#     mfccs_scaled_features=mfccs_features.reshape(1,-1)
#     x_predict=risk_model.predict(mfccs_scaled_features) 
#     predicted_label=np.argmax(x_predict,axis=1)
#     # 1. 오디오 파일 전처리
#     # features = features_extractor(file_path)
#     # features=np.argmax(features,axis=1)
#     # # 2. 모델 예측
#     # result = risk_model.predict(features)
    
#     # # 3. JSON 파일 생성
#     response = {
#         "result": label_list[predicted_label[0]],
#         "device_id": device_id,
#         "time": datetime.now().isoformat()
#     }
    
#     # 4. 웹소켓을 통해 JSON 전송
#     await websocket_manager.send_json(response)
    
#     # 5. 파일 삭제
#     # os.remove(file_path)
