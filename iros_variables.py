import datetime
import os
import pathlib
from dataclasses import dataclass, field
from enum import Enum
from typing import List

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
PROJECT_PATH = pathlib.Path(__file__).parent
CURRENT_PATH = os.getcwd()
RESULT_PATH = f"{CURRENT_PATH}/result"
LOG_PATH = f"{CURRENT_PATH}/log"
SESSION_PATH = f"{CURRENT_PATH}/session"

PROGRAM_TITLE = "인터넷 등기소 데이터 수집+"
BASE_URL = "http://www.iros.go.kr"


@dataclass
class Cookie:
    name: str
    value: str
    domain: str

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'domain': self.domain,
        }


@dataclass
class Executive:
    position: str
    name: str
    reg_date: str
    reg_reason: str
    address: str = field(default="")

    def to_string(self):
        items = [self.position, self.name, self.address, self.reg_date, self.reg_reason]
        return "\t".join(items)


@dataclass
class Company:
    name: str
    reg_place: str
    reg_number: str
    reg_type: str
    address: str
    executives: List[Executive] = field(default_factory=list)

    def to_string(self):
        items = [self.name, self.reg_place, self.reg_number, self.reg_type, f'"{self.address}"',
                 str(len(self.executives))]
        base_str = "\t".join(items)
        targets = [base_str]
        for e in self.executives:
            targets.append(e.to_string())
        return "\t".join(targets) + "\n"


def string_to_company(string) -> Company:
    name, reg_place, reg_number, reg_type, address, length, *items = string.split("\t")
    address = address.replace('"', '')
    cmp = Company(
        name=name,
        reg_place=reg_place,
        reg_number=reg_number,
        reg_type=reg_type,
        address=address
    )
    for i in range(0, len(items), 5):
        e = Executive(
            position=items[i],
            name=items[i + 1],
            address=items[i + 2],
            reg_date=items[i + 3],
            reg_reason=items[i + 4],
        )
        cmp.executives.append(e)
    return cmp


@dataclass
class ProcessResult:
    current: int
    target: int
    companies: List[Company] = field(default_factory=list)


class ThreadState(Enum):
    RUNNING = 0
    COMPLETE = 1
    CANCELLED = 2
    ERROR = 3


class LogType(Enum):
    FILE = 0
    CONSOLE = 1


class ThreadkillException(Exception):
    pass


place_list = [
    '서울중앙지방법원  등기국',
    '인천지방법원  등기국',
    '인천지방법원 부천지원 등기과',
    '인천지방법원 부천지원 김포등기소',
    '수원지방법원 성남지원 등기과',
    '수원지방법원 여주지원 등기계',
    '수원지방법원 평택지원 등기과',
    '수원지방법원 안산지원 등기과',
    '수원지방법원 안양지원 안양등기소',
    '수원지방법원 성남지원 광주등기소',
    '수원지방법원  양평등기소',
    '수원지방법원  이천등기소',
    '수원지방법원  용인등기소',
    '수원지방법원  안성등기소',
    '수원지방법원  화성등기소',
    '수원지방법원 안산지원 광명등기소',
    '수원지방법원 안산지원 시흥등기소',
    '수원지방법원 성남지원 하남등기소',
    '수원지방법원  동수원등기소',
    '춘천지방법원  등기과',
    '춘천지방법원 강릉지원 등기과',
    '춘천지방법원 원주지원 등기과',
    '춘천지방법원 속초지원 등기계',
    '춘천지방법원 영월지원 등기계',
    '춘천지방법원  화천등기소',
    '춘천지방법원  양구등기소',
    '춘천지방법원  인제등기소',
    '춘천지방법원  고성등기소',
    '춘천지방법원  양양등기소',
    '춘천지방법원  삼척등기소',
    '춘천지방법원  동해등기소',
    '춘천지방법원  태백등기소',
    '춘천지방법원  정선등기소',
    '춘천지방법원  평창등기소',
    '춘천지방법원  횡성등기소',
    '춘천지방법원  홍천등기소',
    '청주지방법원  등기과',
    '청주지방법원 충주지원 등기계',
    '청주지방법원 제천지원 등기계',
    '청주지방법원 영동지원 등기계',
    '청주지방법원  보은등기소',
    '청주지방법원  옥천등기소',
    '청주지방법원  진천등기소',
    '청주지방법원  괴산등기소',
    '청주지방법원  음성등기소',
    '청주지방법원  단양등기소',
    '대전지방법원  등기국',
    '대전지방법원 홍성지원 등기계',
    '대전지방법원 공주지원 등기계',
    '대전지방법원 논산지원 등기계',
    '대전지방법원 서산지원 등기과',
    '대전지방법원 천안지원 등기과',
    '대전지방법원  금산등기소',
    '대전지방법원  부여등기소',
    '대전지방법원  장항등기소',
    '대전지방법원  보령등기소',
    '대전지방법원  청양등기소',
    '대전지방법원  세종등기소',
    '대전지방법원 천안지원 아산등기소',
    '대전지방법원  예산등기소',
    '대전지방법원  당진등기소',
    '대전지방법원  태안등기소',
    '대구지방법원  등기국',
    '대구지방법원 안동지원 등기계',
    '대구지방법원 경주지원 등기계',
    '대구지방법원 김천지원 등기계',
    '대구지방법원 상주지원 등기계',
    '대구지방법원 의성지원 등기계',
    '대구지방법원 영덕지원 등기계',
    '대구지방법원 포항지원 등기과',
    '대구지방법원  청송등기소',
    '대구지방법원  영양등기소',
    '대구지방법원  영천등기소',
    '대구지방법원  경산등기소',
    '대구지방법원  청도등기소',
    '대구지방법원 서부지원 고령등기소',
    '대구지방법원 서부지원 성주등기소',
    '대구지방법원  칠곡등기소',
    '대구지방법원  문경등기소',
    '대구지방법원  예천등기소',
    '대구지방법원  영주등기소',
    '대구지방법원  봉화등기소',
    '대구지방법원  울릉등기소',
    '대구지방법원  울진등기소',
    '대구지방법원  구미등기소',
    '부산지방법원  등기국',
    '창원지방법원 진주지원 등기과',
    '창원지방법원 통영지원 등기계',
    '창원지방법원 밀양지원 등기계',
    '창원지방법원 거창지원 등기계',
    '창원지방법원  등기과',
    '창원지방법원  함안등기소',
    '창원지방법원  의령등기소',
    '창원지방법원  남해등기소',
    '창원지방법원  하동등기소',
    '창원지방법원  산청등기소',
    '창원지방법원  거제등기소',
    '창원지방법원  고성등기소',
    '창원지방법원  창녕등기소',
    '창원지방법원  함양등기소',
    '창원지방법원  합천등기소',
    '창원지방법원  사천등기소',
    '창원지방법원  김해등기소',
    '광주지방법원  등기국',
    '광주지방법원 목포지원 등기과',
    '광주지방법원 장흥지원 등기계',
    '광주지방법원 순천지원 등기과',
    '광주지방법원 해남지원 등기계',
    '광주지방법원  담양등기소',
    '광주지방법원  곡성등기소',
    '광주지방법원 순천지원 구례등기소',
    '광주지방법원 순천지원 광양등기소',
    '광주지방법원 순천지원 고흥등기소',
    '광주지방법원 순천지원 보성등기소',
    '광주지방법원  화순등기소',
    '광주지방법원  강진등기소',
    '광주지방법원  영암등기소',
    '광주지방법원  나주등기소',
    '광주지방법원  함평등기소',
    '광주지방법원  무안등기소',
    '광주지방법원  영광등기소',
    '광주지방법원  장성등기소',
    '광주지방법원  완도등기소',
    '광주지방법원  진도등기소',
    '광주지방법원 순천지원 여천등기소',
    '전주지방법원  등기과',
    '전주지방법원 군산지원 등기과',
    '전주지방법원 정읍지원 등기계',
    '전주지방법원 남원지원 등기계',
    '전주지방법원  진안등기소',
    '전주지방법원  무주등기소',
    '전주지방법원  장수등기소',
    '전주지방법원  임실등기소',
    '전주지방법원  순창등기소',
    '전주지방법원  고창등기소',
    '전주지방법원  부안등기소',
    '전주지방법원  김제등기소',
    '전주지방법원  익산등기소',
    '제주지방법원  등기과',
    '제주지방법원  서귀포등기소',
    '울산지방법원  등기과',
    '울산지방법원  양산등기소',
    '의정부지방법원  의정부등기소',
    '의정부지방법원 남양주지원 등기과',
    '의정부지방법원  연천등기소',
    '의정부지방법원  포천등기소',
    '의정부지방법원 남양주지원 가평등기소',
    '의정부지방법원  동두천등기소',
    '의정부지방법원  철원등기소',
    '의정부지방법원 고양지원 파주등기소',
    '의정부지방법원 고양지원 고양등기소',
]
