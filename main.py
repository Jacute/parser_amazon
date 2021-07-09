import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pyexcel
from pyexcel._compact import OrderedDict
from webdriver_manager.firefox import GeckoDriverManager
import time
import os
from random import randint
import traceback
import csv


def main(urls):
    product_urls = list()
    result = list()
    for url in urls:
        driver.get(url)
        while True:
            document_height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.execute_script(f"window.scrollTo(0, {document_height - 1533});")
            time.sleep(randint(1, 2))
            if check_xpath('//button[@class="style__button__1MgdH default style__beacon__2ECwE style__button__1KJD9 style__secondary__39EKa style__disableInternalPointerEvents__1ECVO"]'):
                driver.find_element_by_xpath('//button[@class="style__button__1MgdH default style__beacon__2ECwE style__button__1KJD9 style__secondary__39EKa style__disableInternalPointerEvents__1ECVO"]').click()
                time.sleep(randint(3, 4))
            else:
                break
        product_urls.extend([i.get_attribute('href') for i in driver.find_elements_by_xpath('//a[@class="style__overlay__2qYgu ProductGridItem__overlay__1ncmn"]')])
        print(len(product_urls))
    product_urls.extend(['https://www.amazon.co.uk/SUPCASE-Protector-Full-Body-Kickstand-Protective-Black/dp/B086V4DLRM?ref_=ast_sto_dp&th=1&psc=1',
                         'https://www.amazon.co.uk/i-Blason-Release-Trifold-Protective-Pencil-Marble/dp/B087JDJ1BY?ref_=ast_sto_dp&th=1&psc=1',
                         'https://www.amazon.co.uk/SUPCASE-Protector-Full-Body-Kickstand-Protective-Black/dp/B086P74WSY?ref_=ast_sto_dp&th=1&psc=1',
                         'https://www.amazon.co.uk/i-Blason-Trifold-Protective-Pencil-Release-Marble/dp/B086YPWK3J?ref_=ast_sto_dp&th=1&psc=1'])
    # product_urls.append('https://www.amazon.co.uk/SUPCASE-Unicorn-Full-body-Protective-Protector/dp/B072C9CL4N?ref_=ast_sto_dp')
    time.sleep(randint(2, 4))
    for url in product_urls:
        print(f'{product_urls.index(url) + 1} из {len(product_urls)}')
        driver.get(url)
        print(driver.current_url)
        driver.execute_script(f"window.scrollTo(0, {455});")
        try:
            driver.find_element_by_xpath('//button[@class="a-button-text"]').click()
            driver.execute_script(f"window.scrollTo(0, {455});")
            time.sleep(2.75)
        except Exception:
            pass
        tips = driver.find_elements_by_xpath('//button[@class="a-button-text"]')
        if tips == []:
            result.append(get_info())
        else:
            for tip in tips:
                if tips.index(tip) != 0:
                    driver.execute_script(f"window.scrollTo(0, {455});")
                    try:
                        tip.click()
                    except ElementClickInterceptedException:
                        driver.execute_script(f"window.scrollTo(0, {-123});")
                        tip.click()
                driver.implicitly_wait(5)
                time.sleep(2.6)
                result.append(get_info())
    return result


def get_info():
    name = driver.find_element_by_xpath('//span[@id="productTitle"]').text
    try:
        price = driver.find_element_by_xpath('//span[@id="priceblock_ourprice"]').text
    except Exception:
        try:
            price = driver.find_element_by_xpath('//span[@id="priceblock_saleprice"]').text
        except Exception:
            price = ''
    about = driver.find_element_by_xpath('//ul[@class="a-unordered-list a-vertical a-spacing-mini"]').get_attribute(
        'innerHTML').split('\n\n\n')[-1].strip()
    try:
        description = driver.find_element_by_xpath('//div[@id="productDescription"]/p').get_attribute("innerHTML").strip()
    except Exception:
        description = ''
    try:
        details = driver.find_element_by_xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]').get_attribute(
            'innerHTML').strip()
    except NoSuchElementException:
        details = ''
    flag = False
    try:
        tmp = driver.find_element_by_xpath(
            '//ul[@class="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list"]').text.split('\n')
        for i in tmp:
            if 'ASIN' in i:
                flag = True
                asin = i.split(' : ')[1]
    except NoSuchElementException:
        tmp = driver.find_element_by_xpath('//table[@id="productDetails_detailBullets_sections1"]').text.split('\n')
        for i in tmp:
            if 'ASIN' in i:
                flag = True
                asin = i.split()[1]
    if not flag:
        tmp = driver.find_element_by_xpath('//table[@id="productDetails_techSpec_section_1"]').text.split('\n')
        for i in tmp:
            if 'ASIN' in i:
                asin = i.split()[1]
    photos = list()
    fname = search_file_name(asin)
    if name not in ['SUPCASE [Unicorn Beetle Pro] Series Case for Galaxy Watch Active 2, Rugged Protective Case with Strap Bands for Galaxy Watch Active 2 [44mm] 2019 Release',
                    ]:
        try:
            driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
        except Exception:
            driver.execute_script(f"window.scrollTo(0, {666});")
            time.sleep(1)
            try:
                driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
            except Exception:
                driver.execute_script(f"window.scrollTo(0, {-155});")
                time.sleep(1)
                try:
                    driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
                except Exception:
                    driver.execute_script(f"window.scrollTo(0, {356});")
                    time.sleep(1)
                    try:
                        driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
                    except Exception:
                        driver.execute_script(f"window.scrollTo(0, {-450});")
                        time.sleep(1)
                        try:
                            driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
                        except Exception:
                            driver.execute_script(f"window.scrollTo(0, {-111});")
                            time.sleep(1)
                            try:
                                driver.find_elements_by_xpath('//div[@class="imgTagWrapper" and @style]')[-1].click()
                            except Exception:
                                driver.find_element_by_xpath('//div[@class="sp-cc-text"]').click()
    time.sleep(3)
    try:
        photo_url = driver.find_element_by_xpath('//img[@class="fullscreen"]').get_attribute('src')
        photo = get_photo(fname, '1', photo_url)
        photos.append(photo)
        thumbs = driver.find_elements_by_xpath('//div[@class="ivThumb"]')
        for thumb in thumbs:
            thumb.click()
            time.sleep(0.5)
            photo_url = driver.find_element_by_xpath('//img[@class="fullscreen"]').get_attribute('src')
            photo = get_photo(fname, thumbs.index(thumb) + 2, photo_url)
            photos.append(photo)
        try:
            driver.find_element_by_xpath('//button[@data-action="a-popover-close"]').click()
        except Exception:
            pass
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
    time.sleep(1.5)
    driver.implicitly_wait(6)
    return [name.replace('"', "'"), price, ','.join(photos), about.replace('"', "'").replace(';', ''), details.replace('"', "'").replace(';', ''), description.replace('"', "'").replace(';', '')]


def check_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except Exception:
        return False


def get_photo(fname, count, photo_url):
    global c
    p = requests.get(photo_url)
    try:
        photo = f"photos/{fname.replace('/', '_')}{count}.jpg"
    except AttributeError:
        c += 1
        photo = f"photos/NotFound-{c}-{count}.jpg"
    with open(photo, "wb") as f:
        f.write(p.content)
    return photo


def search_file_name(asin):
    my_array = pyexcel.get_array(file_name="data.xlsx")
    print(my_array)
    for i in my_array:
        if asin in i:
            return i[2]


def get_csv(data):
    with open('result.csv', encoding='utf-8', mode='w', newline='') as f:
        writer = csv.writer(
            f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(('item-name', 'item-price', 'item-photos', 'about-item', 'item-details', 'item-description'))
        for i in data:
            print(i)
            writer.writerow(i)


if __name__ == '__main__':
    c = 0
    urls = [
        'https://www.amazon.co.uk/stores/page/886467DD-E127-40BF-A1FE-1005BB8AB61D?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/3F9BCA48-F922-46AF-A45F-9706DC7AD5EC?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/80FF9183-303C-4596-9823-A0C7486CF277?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/AD1D4985-246C-4614-B164-9D9D70564ACA?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/7FCEDEAC-5320-4CD1-883D-7A4F90D77BA9?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/9D5FFEA3-EB19-4131-B230-3C49AC48FB18?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/4F0E5402-56FD-4009-A069-A2FF6A6FCE58?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/DD5493B9-185E-4071-9AC4-CC2362A36BF2?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/A1B00389-3203-4A3E-90C8-0D8DE95EE6CF?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln',
        'https://www.amazon.co.uk/stores/page/57DC53B2-F1E4-44D2-A546-392EE80FAD6A?ingress=2&visitId=ec615058-dbde-4fc5-8b83-d39059984c20&ref_=ast_bln'
        ]
    options = webdriver.FirefoxOptions()

    # change useragent
    options.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0")
    options.set_preference("dom.webdriver.enabled", False)
    # options.headless = True
    driver = webdriver.Firefox(
        executable_path=GeckoDriverManager().install(),
        options=options
    )
    driver.set_window_size(1280, 1080)
    actions = webdriver.ActionChains(driver)
    try:
        result = main(urls)
        get_csv(result)
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
    finally:
        driver.close()
        driver.quit()
        input('Press ENTER to close this program')