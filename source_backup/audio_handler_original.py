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



async def process_audio_file(file_path: str, device_id: str, websocket_manager):
    try:
        # 오디오 파일에서 특징 추출
        mfccs_features = features_extractor(file_path)
        # mfccs_scaled_features=mfccs_features.reshape(1,-1)
        x_predict=risk_model.predict(mfccs_features)
        print(x_predict)
        # predicted_label=np.argmax(x_predict,axis=0)
        print(label_list[x_predict])
        if x_predict != 4:
            danger = 1
        else:
            danger = 0

        response = {
            "result": label_list[x_predict],
            "device_id": device_id,
            "Is Danger": danger,
            "file name": file_path.split('/')[-1],
            "time": datetime.now().isoformat()
        }

        # 웹소켓을 통해 JSON 전송
        await websocket_manager.send_json(response)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
