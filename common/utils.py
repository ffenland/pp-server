import requests
from bs4 import BeautifulSoup


def getSidoList():
    """시,도 List를 받아온다."""
    sidoList = []
    try:
        url = "https://www.code.go.kr/stdcode/regCodeL.do"
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        sido_select = soup.find("select", id="Type1")

        if sido_select:
            for option in sido_select.find_all("option"):
                code = option.get("value")
                sido = option.get_text(strip=True)
                if code and len(code) > 1:
                    sidoList.append({"code": code, "sido": sido})

            sidoList.sort(key=lambda x: x["code"])
            return sidoList
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False


def getSggList(sido_code):
    """sido Code를 인자로 받아서 SGG 리스트 받긔"""
    sggList = []
    try:
        url = "https://www.code.go.kr/stdcode/sggCodeIL.do"
        payload = {"disuseAt": "0", "sidoCd": sido_code}
        response = requests.post(url, data=payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        script_text = soup.find("script").text

        SggNmStartIndex = script_text.find('strSggNm = "') + 12
        SggNmEndIndex = script_text.find('.split(",");') - 2
        SggNm = script_text[SggNmStartIndex:SggNmEndIndex].split(",")

        SggCdStartIndex = script_text.find('strSggCd = "') + 12
        SggCdEndIndex = script_text.find('.split(",");', SggNmEndIndex + 10) - 2
        SggCd = script_text[SggCdStartIndex:SggCdEndIndex].split(",")

        if len(SggNm) == len(SggCd):
            for i in range(len(SggNm)):
                sggList.append({"code": SggCd[i], "sgg": SggNm[i]})
            return sggList
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False
