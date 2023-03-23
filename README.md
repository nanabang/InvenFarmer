# InvenFarmer
사용자 변경 부분

코드 하단에 보면 아래와같이 있는데 

셀레니움remote 이 따로 있으면 주소를 넣고 driver_type 을 remote 로 하고  local에서 진행시 local로 변경한다.

인벤 아이디,비번, 텔레그램토큰,아이디 를 넣고 1~120초 의 딜레이를 넣었으니 변경이 필요하다면 변경하면 된다.


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
