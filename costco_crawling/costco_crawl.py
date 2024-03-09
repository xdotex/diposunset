from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
from selenium.webdriver.chrome.options import Options

# User-Agent와 Accept-Language를 설정하는 Chrome 옵션
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
options.add_argument("accept-language=en-US,en;q=0.9")

# WebDriver를 설정할 때 위에서 정의한 옵션을 사용합니다.
driver = webdriver.Chrome(options=options)

url = 'https://www.costco.co.kr/events'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)

# 무한 스크롤
old_height = driver.execute_script("return document.body.scrollHeight") #스크롤을 위한 높이 가져옴
while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #페이지 끝으로 스크롤 다운
        try:
            WebDriverWait(driver, 5).until(lambda d: d.execute_script("return document.body.scrollHeight;") > old_height) #컨텐츠 로드 10초 대기
            old_height = driver.execute_script("return document.body.scrollHeight") #페이지 높이 업데이트
        except TimeoutException: #10초 조건 만족 안 하면 루프 종료
            break


# CSV 파일
with open('costco_event_all_test1.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # CSV 파일의 헤더 작성
    writer.writerow(['판매자 상품코드', '카테고리 코드', '상품명', '상품상태', '판매가', '부가세', '재고수량', '옵션형태', '옵션명', '옵션값', '옵션가', '옵션 재고수량', '직접입력 옵션', '추가상품명', '추가상품값', '추가상품가', '추가상품 재고수량', '대표이미지', '추가이미지', '상세설명', '브랜드', '제조사', '제조일자', '유효일자', '원산지코드', '수입사', '복수원산지여부', '원산지 직접입력', '미성년자 구매', '배송비 템플릿코드', '배송방법', '택배사코드', '배송비유형', '기본배송비', '배송비 결제방식', '조건부무료-상품판매가 합계', '수량별부과-수량', '구간별-2구간수량', '구간별-3구간수량', '구간별-3구간배송비', '구간별-추가배송비', '반품배송비', '교환배송비', '지역별 차등 배송비', '별도설치비', '상품정보제공고시 템플릿코드', '상품정보제공고시 품명', '상품정보제공고시 모델명', '상품정보제공고시 인증허가사항', '상품정보제공고시 제조자', 'A/S 템플릿코드', 'A/S 전화번호', 'A/S 안내', '판매자특이사항', '즉시할인 값(기본할인)', '즉시할인 단위(기본할인)', '모바일 즉시할인 값', '모바일 즉시할인 단위', '복수구매할인 조건 값', '복수구매할인 조건 단위', '복수구매할인 값', '복수구매할인 단위', '상품구매시 포인트 지급 값', '상품구매시 포인트 지급 단위', '텍스트리뷰 작성시 지급 포인트', '포토/동영상 리뷰 작성시 지급 포인트'])
    # 제품들 링크
    products = driver.find_elements(By.CSS_SELECTOR, 'div.thumb a')

    # 제품별 정보 가져오기
    for product in products[:3]: # 3개만 가져오도록. 나중에 변경 필요.
        # 새 탭에서 링크 열기 // 상세보기 버튼+스펙
        link = product.get_attribute('href')
        driver.execute_script('window.open("{}");'.format(link))
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(3)

        # 정보 추출
        try:
            variant_select = driver.find_elements(By.CSS_SELECTOR, 'select.form-control.variant-select.costco-select')
            # 조건을 만족하는 요소가 있으면, 이 제품은 건너뛰고 탭을 닫습니다.
            if variant_select:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue  # 다음 제품으로 넘어갑니다.
            code = driver.find_element(By.CSS_SELECTOR, 'p.product-code span.notranslate').text
            sell_code = 'cc#'+code

            product_name = driver.find_element(By.CSS_SELECTOR, 'h1.product-name').text

            price = driver.find_element(By.CSS_SELECTOR, 'span.price-value span.notranslate.ng-star-inserted').text
            #최종판매가격(민성 추가)
            sell_price = int(round(1.95*float(price.replace('원','').replace(',','')) + 2175, -2))

            # 이미지
            images = driver.find_elements(By.CSS_SELECTOR, 'div.page-content.container.main-wrapper sip-product-details.ng-star-inserted div.primary-image-wrapper sip-media.zoomed-image.ng-star-inserted.is-initialized img.ng-star-inserted')
            main_img = images[0].get_attribute('src')
            img_urls = '\n'.join([img.get_attribute('src') for img in images[1:]])  # 이미지 URL을 개행문자로 연결
            
            
            # 상세이미지+정보 // 상세보기 버튼 클릭

            driver.find_element(By.CSS_SELECTOR, "button.view-more__button.ng-star-inserted").click()
            time.sleep(2)

            #배열에 추가
            file = driver.find_element(By.CSS_SELECTOR, "div.wrapper_itemDes")
            try: 
                detail = file.text
            except: 
                pass
            try:  
                detail = file.find_element(By.TAG_NAME, "img").get_attribute("src")
            except: 
                pass
            


            # 상품정보제공고시 품명 = product_name
            # 상품정보제공고시 모델명 = product_name

            # 스펙 오픈 후 정보 업로드까지 기다리기
            elements = driver.find_element(By.CSS_SELECTOR, 'i.costco-icons.costco-icon-plus-sign').click()
            time.sleep(2)

            # 리스트로 관리(하위 html 정보에 접근할 수 있는 방법이 있는지? ex: tr 정보를 따온 후 거기의 td에 접근하는 법)
            attrib = driver.find_elements(By.CSS_SELECTOR, 'td.attrib')
            attrib_val = driver.find_elements(By.CSS_SELECTOR, 'td.attrib-val')
            spec = []
            for idx in range(0,len(attrib)): 
                spec.append([attrib[idx].text, attrib_val[idx].text])
            manufacture = None
            made_in = None
            KC = None
            for spec_list in spec:
                 if spec_list[0] == '제조자/수입자':
                      manufacture = spec_list[1]
                 if spec_list[0] == '제조국 또는 원산지':
                      made_in = spec_list[1]
                 if spec_list[0] == 'KC 인증 정보' :
                      KC = spec_list[1]            
            # CSV 파일에 쓰기
            writer.writerow([
                #판매자 상품코드
                sell_code, 
                #카테고리
                '',
                #상품명
                product_name, 
                #상품상태
                "신상품", 
                #판매가
                sell_price, 
                #부가세
                "과세상품",
                #재고수량
                "9999", 
                #옵션형태
                "", 
                #옵션명
                "",
                #옵션값
                "",
                #옵션 재고수량
                "",
                #직접입력 옵션 
                "", 
                #추가상품명
                "", 
                #추가상품값
                "",
                #추가상품가
                "",
                #추가상품 재고수량
                "",
                #대표이미지 
                main_img, 
                #추가이미지
                img_urls, 
                #상세설명
                detail, 
                #브랜드
                "오버선셋",
                #제조사
                manufacture, 
                #제조일자
                "",
                #유효일자
                "",
                #원산지코드(제대로 들어가나?)
                "'04", 
                #수입사(직접입력의 경우도 필요한지 확인하기) 
                "", 
                #복수원산지여부
                "", 
                #원산지 직접입력
                made_in, 
                #미성년자 구매
                "Y", 
                #배송비템플릿코드 
                2913880, 
                #배송방법 
                "",
                #택배사코드
                "",
                #배송비유형 
                "", 
                #기본배송비 
                "", 
                #배송비 결제방식 
                "", 
                #조건부무료-상품판매가 합계
                "", 
                #수량별부과-수량 
                "", 
                #구간별-2구간수량
                "",
                #구간별-3구간수량
                "", 
                #구간별-3구간배송비
                "",
                #구간별-추가배송비
                "",
                #반품배송비
                "",
                #교환배송비
                "",
                #지역별 차등 배송비
                "", 
                #별도설치비
                "", 
                #상품정보제공고시 템플릿코드
                "",
                #상품정보제공고시 품명
                product_name, 
                #상품정보제공고시 모델명
                product_name, 
                #상품정보제공고시 인증허가사항
                KC,
                #상품정보제공고시 제조자
                manufacture,
                #A/S 템플릿코드
                2913881, 
                #A/S 전화번호 
                "", 
                #A/S 안내 
                "", 
                #판매자특이사항
                "", 
                #즉시할인값
                33, 
                #즉시할인 단위 
                "%", 
                #모바일 즉시할인 값 
                "", 
                #모바일 즉시할인 단위 
                "", 
                #복수구매할인 조건 값
                "", 
                #복수구매할인 조건 단위 
                "", 
                #복수구매할인 값 
                "", 
                #복수구매할인단위 
                "", 
                #상품구매시 포인트 지급 값 
                "", 
                #상품구매시 포인트 지급 단위 
                "", 
                #텍스트리뷰 작성시 지급 포인트 
                500, 
                #포토/동영상 리뷰 작성시 지급 포인트 
                1000
            ])

            #카테고리 코드는 이 파일이 끝난 후 실행해야 겹치지 않을 것이다.(만약 이 반복문에서 실행하게 된다면 코스트코와 네이버 쇼핑 브라우저를 동시에 실행해야 함.)
        except Exception as e:
            print(e)
        
        # 현재 탭 닫기 및 원래 탭으로 전환
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

driver.quit()