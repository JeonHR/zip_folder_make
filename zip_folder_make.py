import os
import datetime
import tarfile
import shutil
import sys

# 현재 실행 중인 위치를 기준으로 설정
if getattr(sys, 'frozen', False):  # .exe로 변환된 경우
    target_folder = os.path.dirname(sys.executable)  # 현재 실행된 exe 파일의 경로
else:
    target_folder = os.path.dirname(os.path.abspath(__file__))  # 일반 Python 스크립트 실행 시 경로

output_folder = target_folder  # 압축 파일 저장 위치도 동일
days = 7

# 특정 폴더를 압축할 때 사용할 cutoff_date 설정
cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)

# 폴더 압축 함수 (.tar.bz2 형식으로 압축)
def compress_folder_to_bz2(folder_path, output_path):
    with tarfile.open(output_path, "w:bz2") as tar:
        tar.add(folder_path, arcname=os.path.basename(folder_path))

# target_folder 내의 특정 기간 폴더를 확인하여 압축
for item in os.listdir(target_folder):
    item_path = os.path.join(target_folder, item)
    
    # 폴더인지 확인하고, 수정 날짜가 cutoff_date보다 최근인지 확인
    if os.path.isdir(item_path) and datetime.datetime.fromtimestamp(os.path.getmtime(item_path)) < cutoff_date:
        output_file_path = os.path.join(output_folder, f"{item}.tar.bz2")
        print(f"Compressing folder: {item_path} to {output_file_path}")
        
        # 폴더를 .tar.bz2로 압축
        compress_folder_to_bz2(item_path, output_file_path)
        
        # 압축 후 원본 폴더 삭제
        shutil.rmtree(item_path)
        print(f"Folder compressed and removed: {item_path}")
