import cv2
from ultralytics import YOLO
import time
from calculating import matrix,tool_path,write_csv

# YOLO 모델 로드
model = YOLO('best_pose.pt')

# OpenCV를 사용하여 카메라 열기
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()  # 카메라에서 프레임 읽기
    if not ret:
        print("프레임을 가져오는 데 실패했습니다.")
        break

    # YOLO 모델 실행 (show=False로 설정하여 모델이 자동으로 창을 띄우지 않게 함)
    results = model(frame, show=False, conf=0.3, save=True)

    # YOLO 모델이 반환한 이미지 가져오기
    img = results[0].plot()  # 모델의 결과 이미지를 가져옴
    
    first_result = results[0]  # 첫 번째 이미지의 결과 객체 가져오기

    # keypoints 객체 가져오기
    keypoints = first_result.keypoints

    flag=True

    if keypoints is not None:
        # keypoints 배열로 변환 (각 keypoint에 대한 x, y 좌표와 confidence)
        keypoints_array = keypoints.data.cpu().numpy()  # tensor에서 numpy 배열로 변환
        print(keypoints_array)
        # keypoints 정보 출력
        for i in range(keypoints_array.shape[1]):  # 각 keypoint에 대해 반복
            x, y, conf = keypoints_array[0][i]  # 첫 번째 탐지의 keypoint 정보
            if conf > 0.5:  # confidence 값이 0.5 이상일 때
                print(f"Keypoint {i}: x={x}, y={y}, confidence={conf}")

            # 왼쪽 팔꿈치(관절 6)와 왼쪽 손목(관절 7) 좌표 사용
            elbow = keypoints_array[0][1][:2]  # 왼쪽 팔꿈치
            wrist = keypoints_array[0][0][:2]  # 왼쪽 손목

            # 좌표 출력
            print(f"팔꿈치 좌표: ({int(elbow[0])}, {int(elbow[1])})")
            print(f"손목 좌표: ({int(wrist[0])}, {int(wrist[1])})")

            if flag:
                path=tool_path(elbow,wrist)

                robot_point_transformed=matrix(point)

                write_csv(robot_point_transformed)

                flag=False

            # YOLO가 반환한 이미지에 선 그리기 (녹색 선)
            cv2.line(img, (int(elbow[0]), int(elbow[1])), (int(wrist[0]), int(wrist[1])), (0, 255, 0), 2)

    # OpenCV 창에서 수정된 이미지를 표시 (모델 결과에 직접 선을 그린 것)
    cv2.imshow('YOLO Pose Detection', img)

    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 처리 속도를 조절하기 위한 시간 지연
    time.sleep(0.8)

# 카메라 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()


