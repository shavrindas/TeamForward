import os
from PIL import Image

# 입력 폴더와 출력 폴더 설정
입력_폴더 = r"E:\Data\008.의류 통합 데이터(착용 이미지, 치수 및 원단 정보)\01-1.정식개방데이터\Training\01.원천데이터\TS_상품_하의_onepiece(jumpsuite)"
출력_폴더 = r"E:\Data\Hazy\onepiece(jumpsuite)"

# 입력 폴더 내 파일들을 순회하며 조건에 맞는 파일을 찾고, 사이즈를 조정하여 저장
for 파일명 in os.listdir(입력_폴더):
    if 파일명.endswith(".jpg"):  # jpg 파일인지 확인
        파일_경로 = os.path.join(입력_폴더, 파일명)
        if "wear" not in 파일명:  # 파일명에 "wear" 문자열이 없는지 확인
            try:
                with Image.open(파일_경로) as img:
                    img.thumbnail((50, 50))  # 이미지 크기 조정
                    저장_파일명 = f"onepiece(jumpsuite)_{파일명}"
                    저장_파일_경로 = os.path.join(출력_폴더, 저장_파일명)
                    img.save(저장_파일_경로)
                    print(f"{파일명}을(를) 50x50 크기로 조정하여 {저장_파일_경로}에 저장했습니다.")
            except Exception as e:
                print(f"{파일명} 처리 중 오류가 발생했습니다: {e}")
