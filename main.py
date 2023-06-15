import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

parrot_code = ":conga_parrot:"
# parrot_code = ":이빨을_보이며_웃고_있는_얼굴:"
blank_code = ":white_square:"

width, height = 500, 300
image = Image.new("RGB", (width, height), color=(255, 255, 255))  # 흰색 이미지 생성
draw = ImageDraw.Draw(image)

text = input("텍스트를 입력하세요 (2글자 권장) : ")

# 한글 텍스트 추가
font_path = "C:\Windows\Fonts\malgunsl.ttf"  # 한글 폰트 파일 경로
font_size = 50
font_color = (0, 0, 0)  # 검은색

font = ImageFont.truetype(font_path, font_size)

# 글씨 크기 계산
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]

text_x = int((width - text_width) / 2)
text_y = int((height - text_height) / 2)

draw.text((text_x, text_y), text, font=font, fill=font_color, stroke_width=2, stroke_fill=font_color)

# 이미지를 numpy 배열로 변환
image_np = np.array(image)

# 결과 이미지 출력
# cv2.imshow("Image with Text", image_np)
# cv2.waitKey(0)

'''이진화'''
threshold_value = 100  # 임계값 설정
_, binary_image = cv2.threshold(image_np, threshold_value, 255, cv2.THRESH_BINARY)

# cv2.imshow("Binary Image", binary_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

black_pixels = np.where(binary_image == 0)

# 시작 범위와 끝 범위 계산
start_x = np.min(black_pixels[1]) - 1
start_y = np.min(black_pixels[0]) - 1
end_x = np.max(black_pixels[1])
end_y = np.max(black_pixels[0])

# 결과 출력
print("Start Position: ({}, {})".format(start_x, start_y))
print("End Position: ({}, {})".format(end_x, end_y))

roi_image = binary_image[start_y:end_y, start_x:end_x]

# 결과 이미지 출력
# cv2.imshow("Region of Interest", roi_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 세로 크기 설정
desired_width = 16

# 비율 계산
current_width = end_x - start_x
scale_ratio = desired_width / current_width

# 이미지 크기 조정
roi_image_resized = cv2.resize(roi_image, None, fx=scale_ratio, fy=2*scale_ratio)

# 결과 이미지 출력
# cv2.imshow("Resized ROI Image", roi_image_resized)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

roi_text = ""
roi_text2 = ""
for row in roi_image_resized:
    for pixel in row.flatten():  # 2차원 배열을 1차원으로 평탄화하여 각 픽셀 값을 확인
        if pixel == 0:
            roi_text2 += "#"
            roi_text += parrot_code
        else:
            roi_text2 += " "
            roi_text += blank_code

    roi_text += "\n"
    roi_text2 += "\n"

# 결과 출력
print(roi_text)

print(roi_text2)
