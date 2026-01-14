# app/audio_handler.py

import numpy as np
from datetime import datetime
from features_extractor import features_extractor
from model import risk_model

label_list = {
    0: 'firealarm',
    1: 'emergency_Vehicle',
    2: 'glass',
    3: 'help',
    4: 'normal',
    5: 'scream'
}
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
        #mfccs_scaled_features=mfccs_features.reshape(1,-1)
        x_predict=risk_model.predict(mfccs_features) 
        print(x_predict)
        #predicted_label=np.argmax(x_predict,axis=1)
        print(label_list[x_predict])
        if x_predict != 4:
            danger = 1
        else:
            danger = 0
        Audio_Id = get_device_index(file_path)

        response = {
            "Result": label_list[x_predict],
            "Audio_Id": Audio_Id,
            "Is_Danger": danger,
            "Time": datetime.now().isoformat(),
            "File_Name": file_path.split('/')[-1]
        }

        # 웹소켓을 통해 JSON 전송
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
