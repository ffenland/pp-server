import requests
from django.conf import settings

send_url = "https://apis.aligo.in/send/"
api_key = settings.ALIGO_API_KEY
user_id = settings.ALIGO_USER_ID


def send_verification(phone_number, verification_code):
    sms_data = {
        "key": api_key,  # api key
        "userid": user_id,  # 알리고 사이트 아이디
        "sender": "01084931032",  # 발신번호
        "receiver": phone_number,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": f"PalmPharm 인증번호는 {verification_code} 입니다.",  # 문자 내용
        "msg_type": "SMS",  # 메세지 타입 (SMS, LMS)
        # 메세지 제목 (장문에 적용)
        # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        # "testmode_yn": "Y",  # 테스트모드 적용 여부 Y/N
    }
    response = requests.post(send_url, data=sms_data)
    if response.json().get("result_code") == "1":
        return True
    else:
        return False
