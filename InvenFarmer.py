from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
import requests
import time
import telegram
import re
import random

class InvenFarmer:
    def __init__(self):
        self.driver = None
        self.bot = None
        self.chat_id = None

    def driver_init(self, _mode='local', _headless=False, _host=None):
        if _mode == 'local':
            from selenium.webdriver.chrome.options import Options
            options = Options()
            if _headless:
                options.add_argument('headless')
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif _mode == 'remote':
            from selenium.webdriver.firefox.options import Options
            options = Options()
            options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                 "Chrome/107.0.0.0 Safari/537.36")
            options.set_preference("general.platform.override", "Win32")
            self.driver = webdriver.Remote(_host, options=options)

    def bot_init(self, _token, _chat_id):
        self.bot = telegram.Bot(token=_token)
        self.chat_id = _chat_id
    
    def login(self, _uid, _passwd):
        # 로그인 페이지 이동        
        self.driver.get('https://member.inven.co.kr/user/scorpio/mlogin')

        self.driver.find_element(By.XPATH, '//*[@id="user_id"]').send_keys(_uid)  # 아이디 입력
        self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(_passwd)  # 비밀번호 입력
        self.driver.find_element(By.XPATH, '//*[@id="loginBtn"]').click()  # 로그인 실행
        time.sleep(1)
                                                
        try:
            WebDriverWait(self.driver, 3).until(lambda driver: len(driver.window_handles) > 1)
            self.remove_popup()  # 팝업창 제거함수 호출
        except:
            pass  

    def check_point(self):
        # 마이페이지로 이동
        time.sleep(1)
        self.driver.get(url='https://www.inven.co.kr/')
        #time.sleep(1)
        # 인벤 팝업 포인트 열기
        self.driver.find_element(By.XPATH, '//*[@id="comHeadlink"]/div[2]/div[1]/button').click()
        _inni = self.driver.find_element(By.XPATH, '//*[@id="comHeadOutloginExpend"]/div/p[1]/span').text
        _veni = self.driver.find_element(By.XPATH, '//*[@id="comHeadOutloginExpend"]/div/p[2]/span').text
        _jeni = self.driver.find_element(By.XPATH, '//*[@id="comHeadOutloginExpend"]/div/p[3]/span').text        
        _msg = f'이니 : {_inni}, 베니 : {_veni}, 제니 : {_jeni}'
        #print(_msg)
        #self.send_telegram(_msg)
        return _msg

    def remove_popup(self):
        _driver = self.driver

        # 생성된 팝업창을 모두 닫음
        _tabs = _driver.window_handles
        while len(_tabs) != 1:
            _driver.switch_to.window(_tabs[1])
            _driver.close()
            _tabs = _driver.window_handles

        # 첫 창으로 돌아간다
        _driver.switch_to.window(_tabs[0])

    def send_telegram(self, _msg):
        self.bot.sendMessage(chat_id=self.chat_id, text=_msg)        

    def go_cc_inven(self):
        # 출첵 페이지로 이동
        _url = 'https://imart.inven.co.kr/attendance/'
        self.driver = self.driver
        self.driver.get(url=_url)
        time.sleep(1)

        # 팝업창 닫음
        try:
            WebDriverWait(self.driver, 3).until(lambda driver: len(driver.window_handles) > 1)
            self.remove_popup()  # 팝업창 제거함수 호출
        except:
            pass  

        # 출첵 클릭        
        self.driver.find_element(By.XPATH, '//*[@id="invenAttendCheck"]/div/div[2]/div/div[3]/div[1]/div[4]/a').click()
        time.sleep(1)
        try:
            result = Alert(self.driver)
            print(result.text)
            if (result.text=="이미 출석체크 하셨습니다. (0001)"):
                result.accept()
                return
            print('알림처리')

        except:
            print("알림없음")    
        print('출첵완료')

    def go_im_inven(self):
        # 출첵 페이지로 이동
        _url = 'https://imart.inven.co.kr/imarble/'
        self.driver = self.driver
        self.driver.get(url=_url)
        time.sleep(3)

        # 팝업창 닫음
        try:
            WebDriverWait(self.driver, 3).until(lambda driver: len(driver.window_handles) > 1)
            self.remove_popup()  # 팝업창 제거함수 호출
        except:
            pass  
        
        #무료체크        
        _dice = self.driver.find_element(By.XPATH, '//*[@id="imarbleBoard"]/div[5]/div[1]/span').text
        #pattern = 
        _dice2 = re.findall(r'\d+',_dice)
        #print(f'남은 무료 주사위 : {_dice2[0]}개')
        #print(f'남은 유료 주사위 : {_dice2[1]}개')

        temp_cnt = 1
        if int(_dice2[0]) > 0:
            print('무료 주사위 돌리자')  
            for i in range(1,int(_dice2[0])+1) :
                self.driver.find_element(By.XPATH, '//*[@id="imarbleBoard"]/div[4]/img').click()
                time.sleep(4)
                temp_cnt = temp_cnt +1                                                                 
                if self.driver.find_element(By.XPATH,'//*[@id="popreward"]/div[1]/div[1]'):                    
                    print("보상 팝업 발견")
                    self.driver.find_element(By.XPATH, '//*[@id="popreward"]/div[1]/div[1]').click()
                else :
                    print("보상 팝업 없음")     
        else:
            print('무료 주사위가 없음')     

if __name__ == '__main__':
    _host = 'http://127.71:4444/wd/hub'  # Selenium Remote 주소
    _uid = ''  # 인벤 아이디
    _passwd = ''  # 인벤 비밀번호
    _token = ''  # 텔레그램봇 토큰
    _chat_id = ''  # 텔레그램 전송받을 챗아이디
    
    driver_type = 'remote'
    #driver_type = 'local'
    delay = random.randint(1,120)
    print(f'{delay} 초 랜덤 딜레이')
    time.sleep(delay)
    farmer = InvenFarmer()
    farmer.driver_init(driver_type, False , _host)
    farmer.bot_init(_token, _chat_id)  
    farmer.login(_uid, _passwd)
    farmer.go_cc_inven() #출첵   
    farmer.go_im_inven() #아이마트 주사위 돌리기
    farmer.check_point()
    result = farmer.check_point()
    print(result)
    farmer.send_telegram(result)   # 텔레그램 불필요시 비활성화
    farmer.driver.quit()