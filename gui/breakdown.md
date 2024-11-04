# qt designer 변환 방법 (ui > py)

1. 폴더 만들어서 안에 ui를 둔다

2. 그 폴더로 가서 python -m PyQt5.uic.pyuic -x main.ui -o main_cmd.py 를 작성

3. 마찬 가지로 이미지 파일 들어있는 resource.qrc 또한
pyrcc5 resource.qrc -o resource_rc.py 작성하기
