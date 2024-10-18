# Capstone_design
### 로봇 팔 운용(카메라 인식 + 툴패스 생성 + 로봇 제어)

### yolov8n-pose

- 빠른 성능을 위해서 사용
- yolov8n-pose.yaml 모델의 아키텍처, 네트워크 레이어, 하이퍼파라미터 등이 정의
- 사전 학습된 가중치 없이 모델 구조만 정의


### 전이 학습(Transfer Learning)
-   이미 학습된 모델을 사용하여 새로운 작업이나 데이터셋에 대해 학습하는 방법입니다.
- yaml 파일을 기반으로 원래 모델이 새로운 패턴을 학습하는것  
