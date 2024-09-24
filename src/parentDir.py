import os
def get_parent_dir():
    # 현재 파일의 디렉토리 경로를 얻습니다.
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    return parent_dir