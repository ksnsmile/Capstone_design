import numpy as np
import csv
import math

class Node:
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y
        self.z = z

def calculate_matrix(pixel_point):
    # y축을 기준으로 x만 반전시킨것 
    rotation_matrix = np.array([[-1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    # 스케일링 행렬 (x에 1.25, y에 1.4 적용)
    scaling_matrix = np.array([[1.25, 0, 0],
                           [0, 1.4, 0],
                           [0, 0, 1]])

    # 이동 행렬 (카메라 좌표계의 이동 위치)
    translation_matrix = np.array([[1, 0, 510],
                               [0, 1, -170.4],
                               [0, 0, 1]])

    # 전체 변환 행렬 계산 (스케일링 → 회전 → 이동)
    transformation_matrix = translation_matrix @ rotation_matrix @ scaling_matrix

    # pixel_point를 변환 (node 대신 pixel_point 사용)
    pixel_point_array = np.array([pixel_point.x, pixel_point.y, pixel_point.z])
    robot_point_transformed = transformation_matrix @ pixel_point_array

    return Node(robot_point_transformed[0], robot_point_transformed[1], robot_point_transformed[2])

def calculate_tool_path(elbow,wrist):

    path = []

    current_position = np.array([(wrist[0]+elbow[0])/2, (wrist[1]+elbow[1])/2, 1], dtype=float)
    path.append(Node(current_position[0], current_position[1], current_position[2]))
    path.append(Node(current_position[0], current_position[1], current_position[2]))
    path.append(Node(current_position[0], current_position[1], current_position[2]))

    for i in range(3):

        current_position[0]=wrist[0]
        current_position[1]=wrist[1]
        path.append(Node(current_position[0], current_position[1], current_position[2]))

        current_position[0]=elbow[0]
        current_position[1]=elbow[1]
        path.append(Node(current_position[0], current_position[1], current_position[2]))

    current_position = np.array([(wrist[0]+elbow[0])/2, (wrist[1]+elbow[1])/2, 1], dtype=float)
    path.append(Node(current_position[0], current_position[1], current_position[2]))
    path.append(Node(current_position[0], current_position[1], current_position[2]))
    path.append(Node(current_position[0], current_position[1], current_position[2]))


    # 픽셀 좌표계를 로봇 좌표계로 변환
    transformed_path = [calculate_matrix(node) for node in path]

    return transformed_path


def calculate_angle(elbow,wrist):

    x_delta=elbow[0]-wrist[0]
    y_delta=elbow[1]-wrist[1]

    x_d_scaled=x_delta*1.25
    y_d_scaled=y_delta*1.4

    # 각도 계산 (라디안 단위)
    angle_radians = math.atan2(y_d_scaled, x_d_scaled)

    # 각도를 도(degree) 단위로 변환
    angle_degrees = math.degrees(angle_radians) 

    return angle_degrees

def write_csv(transformed_path, elbow, wrist):
    # CSV 파일을 쓰기 모드로 열기
    f = open('C:/Users/ksn71/OneDrive/바탕 화면/git/Capstone_design/yolov8_pose/Var_P.csv', 'w', newline='')  
    csv_writer = csv.writer(f)  # CSV 작성기 객체 생성

    

    # 메타데이터 작성
    csv_writer.writerow(['===== Export Data Var P ====='])  
    csv_writer.writerow(['RobotTypeName :', 'VP-5243'])
    csv_writer.writerow(['RobotTypeID :', '65', '0'])
    csv_writer.writerow(['File Version :', '2'])
    csv_writer.writerow(['[No.]', '[X]', '[Y]', '[Z]', '[RX]', '[RY]', '[RZ]', '[FIG]', '[using]', '[macro name]'])

    # robot_path의 각 점에 대해 CSV 파일에 작성
    for k, robotPt in enumerate(transformed_path):
        # robotPt는 Node 객체이므로 속성을 사용하여 값을 추출

        angle = calculate_angle(elbow, wrist)
        
        if k==0 or k==len(transformed_path)-1:
            csv_writer.writerow([k, robotPt.x, robotPt.y, 400, 180, 0, 0, '13 - Lefty | Above | NonFlip | J6Double | J4Single | J1Single'])

        elif k==1 or k==len(transformed_path)-2:

            csv_writer.writerow([k, robotPt.x, robotPt.y, 400, 180, 0, angle, '13 - Lefty | Above | NonFlip | J6Double | J4Single | J1Single'])
            
        else:
            csv_writer.writerow([k, robotPt.x, robotPt.y, 180, 180, 0, angle, '13 - Lefty | Above | NonFlip | J6Double | J4Single | J1Single'])
    
    # 파일 닫기
    f.close()