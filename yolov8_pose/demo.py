import cv2
from ultralytics import YOLO

# 모델 로드
model = YOLO('yolov8n-pose.pt')

# 웹캠 실행
cap = cv2.VideoCapture(0)  # 0은 기본 웹캠, 다른 숫자는 추가된 카메라

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모델 예측
    results = model(frame)

    # 첫 번째 이미지의 결과 객체 가져오기
    first_result = results[0]

    # keypoints 객체 가져오기
    keypoints = first_result.keypoints

    if keypoints is not None:
        # keypoints 배열로 변환 (각 keypoint에 대한 x, y 좌표와 confidence)
        keypoints_array = keypoints.data.cpu().numpy()  # tensor에서 numpy 배열로 변환

        # 첫 번째 사람의 keypoints만 사용
        person_keypoints = keypoints_array[0]  # 첫 번째 사람의 keypoints

        # 표시할 관절 인덱스 (왼쪽 어깨, 오른쪽 어깨, 왼쪽 팔꿈치, 오른쪽 팔꿈치 등)
        target_indices = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

        # 각 target keypoint에 대해 빨간색 원 표시
        for i in target_indices:
            x, y= person_keypoints[i][:2]  # 해당 관절의 x, y 좌표와 신뢰도
            
            cv2.circle(frame, (int(x), int(y)), radius=5, color=(0, 0, 255), thickness=-1)  # 빨간색 원

    # 결과 화면 출력
    cv2.imshow('YOLOv8 Pose', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 종료
        break

cap.release()
cv2.destroyAllWindows()
