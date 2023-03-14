# *****************************************************************************************
# FileName     : SmartPot_Basic
# Description  : 스마트 팩토리 코딩 키트 (기본)
# Author       : 손정인
# CopyRight    : (주)한국공학기술연구원(www.ketri.re.kr)
# Created Date : 2022.02.08
# Reference    :
# Modified     : 2022.11.23 : YSY : 소스 크린징, distance범위지정 
# Modified     : 2022.12.19 : YSY : 주석수정
# Modified     : 2022.12.21 : YSY : 변수 명명법 통일
# Modified     : 2022.12.21 : YSY : 2 < distance < 8
# Modified     : 2023.03.14 : PEJ : 주석 및 코드 길이, 헤더 주석 수정
# *****************************************************************************************

# import
import time                                        # 시간 관련 모듈
from machine import Pin, time_pulse_us             # 핀 및 시간 관련 모듈
from ETboard.lib.pin_define import *               # ETboard 핀 관련 모듈
from ETboard.lib.OLED_U8G2 import *                # ETboard OLED 관련 모듈

#------------------------------------------------------------------------------------------
# ETBoard 핀번호 설정
#------------------------------------------------------------------------------------------
# global variable
oled = oled_u8g2()                                 

reset_pin = Pin(D6)                                # 카운트 리셋핀 ( D6 = 빨강 버튼 )

echo_pin = Pin(D8)                                 # 초음파 센서 수신부
trig_pin = Pin(D9)                                 # 초음파 센서 송신부

count = 0                                          # 카운터용 변수
pre_time = 0                                       # 이전에 물건이 지나간 시간


#==========================================================================================
# setup
#==========================================================================================
def setup():
    reset_pin.init(Pin.IN)                         # 리셋 버튼 입력 모드 설정
    
    trig_pin.init(Pin.OUT)                         # 초음파 센서 송신부 출력 모드 설정
    echo_pin.init(Pin.IN)                          # 초음파 센서 수신부 입력 모드 설정


#==========================================================================================
# main loop
#==========================================================================================
    #--------------------------------------------------------------------------------------
    # 물체가 초음파 센서를 지나면 카운트 하기
    #--------------------------------------------------------------------------------------
    global pre_time, count                         
    trig_pin.value(LOW)                            # 초음파 센서 거리 센싱 시작
    echo_pin.value(LOW)
    time.sleep_ms(2)
    trig_pin.value(HIGH)
    time.sleep_ms(10)
    trig_pin.value(LOW)                            # 초음파 센서 거리 센싱 종료

    duration = time_pulse_us(echo_pin, HIGH)       # 반사되어 돌아온 초음파의 시간을 저장
    distance  = ((34 * duration) / 1000) / 2       # 측정된 값을 cm로 변환하는 공식 

    print("distance : ", distance, "cm")           

    if( distance > 2 and distance < 8 ) :          # 물체와의 거리가 2cm초과 10cm 미만이면
        now_time = int(round(time.time() * 1000))  
        if(now_time - pre_time > 500) :            # 중복 카운트를 방지하기 위해 0.5초 초과면
            count += 1                             # 한 번 카운트
            pre_time = now_time;                   # 이전 시각에 현재 시각 저장
            
    #--------------------------------------------------------------------------------------
    # 리셋 버튼을 누르면 카운트 초기화 하기
    #--------------------------------------------------------------------------------------
    if(reset_pin.value() == LOW) :                 # 리셋 버튼을 누르면
        print("count reset")                       
        count = 0                                  # 카운트 초기화

    print("count : ", count)               
    print("---------------------")
    
    #--------------------------------------------------------------------------------------
    # OLED 텍스트 표시
    #--------------------------------------------------------------------------------------
    text1 = "count: %d" %(count)                   # text1 count 값 표시
    
    oled.setLine(1, "* Smart Factory *")           # OLED 첫 번째 줄 : 시스템 이름
    oled.setLine(2, text1)                         # OLED 두 번째 줄 : count 값
    oled.setLine(3, "---------------------")       # OLED 세 번째 줄
    oled.display()
    
    time.sleep(0.3)                                


if __name__ == "__main__":
    setup()
    while True:
        loop()

#==========================================================================================
#
#  (주)한국공학기술연구원 http://et.ketri.re.kr
#
#==========================================================================================