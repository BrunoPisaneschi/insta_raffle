import random
import string
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class instagram():
    def __init__(self, username, password, url_vote, user_perfil):
        self._driver = self._instance_driver()
        self._username = username
        self._password = password
        self._url_instagram = 'https://www.instagram.com/'
        self._url_vote = url_vote
        self._user_perfil = user_perfil
        self._list_friends=[]

    def _instance_driver(self):
        return webdriver.Chrome()

    def _wait_loadpage(self, _delay, _name):
        try:
            WebDriverWait(self._driver, _delay).until(EC.presence_of_element_located((By.NAME, _name)))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

    def login(self):
        self._driver.get(self._url_instagram)
        self._wait_loadpage(5,"username")
        input_search_box = self._driver.find_element_by_name('username')
        input_password = self._driver.find_element_by_name('password')
        input_search_box.send_keys(self._username)
        input_password.send_keys(self._password)
        input_password.submit()
        _url=""
        while _url == '' or _url == self._url_instagram:
            sleep(1)
            _url = self._driver.current_url
        if('onetap' in _url):
            self._driver.execute_script("document.getElementsByTagName('button')[1].click();")
            while _url != self._url_instagram:
                sleep(1)
                _url = self._driver.current_url

    def _follow_friends(self):
        self._driver.get("https://www.instagram.com/"+self._user_perfil+"/")
        _url = ""
        while _url == '' or _url == self._url_instagram:
            sleep(1)
            _url = self._driver.current_url

        _list_tags_a = self._driver.find_elements_by_tag_name("a")
        _tag_a= None
        for _tag_a in _list_tags_a:
            if(("/"+self._user_perfil+"/following/").lower() in _tag_a.get_attribute("href")):
                break
        _body = self._driver.find_element_by_tag_name("body")
        _quantidade_seguindo = int(_tag_a.find_elements_by_tag_name("span")[0].text)
        while 'overflow: hidden;' not in _body.get_attribute('style'):
            _tag_a.click()
            sleep(2)
            _body = self._driver.find_element_by_tag_name("body")

        _list_divs = self._driver.find_elements_by_tag_name("div")
        _div = self._capture_divs()

        _list_tags_button = _div.find_elements_by_tag_name("button")
        _contagem_botao_seguir = 0
        _quantidade_seguir_por_paginacao = 0
        while _contagem_botao_seguir != _quantidade_seguindo:
            _contagem_botao_seguir = 0
            for _button in _list_tags_button:
                if (_button.text == 'Seguir') or (_button.text == 'Seguindo')\
                        or (_button.text == 'Follow') or (_button.text == 'Following'):
                    _contagem_botao_seguir+=1
            if(_quantidade_seguir_por_paginacao == 0):
                _quantidade_seguir_por_paginacao = _contagem_botao_seguir
            _list_tags_button[-1].send_keys(Keys.END)
            _div = self._capture_divs()
            _list_tags_button = _div.find_elements_by_tag_name("button")

        _div = self._capture_divs()
        _list_tags_button[-1].send_keys(Keys.HOME)
        _div = self._capture_divs()
        _contagem =0
        for _button in _list_tags_button:
            if(_button.text == 'Seguir') or (_button.text == 'Follow'):
                _button.click()
                sleep(0.7)
                _contagem+=1
            if(_contagem==_quantidade_seguir_por_paginacao):
                _contagem=0
                _list_tags_button[-1].send_keys(Keys.PAGE_DOWN)

    def _capture_divs(self):
        _list_divs = self._driver.find_elements_by_tag_name("div")
        _div = None
        for _div in _list_divs:
            try:
                if ('dialog' in _div.get_attribute("role")):
                    break
            except:
                continue
        return _div

    def vote_post(self):
        self._follow_friends()
        self._driver.get(self._url_vote)
        _url = ""
        while _url == '' or _url == self._url_instagram:
            sleep(1)
            _url = self._driver.current_url
        while True:
            try:
                self._driver.execute_script("document.getElementsByTagName('textarea')[0].value='';document.getElementsByTagName('textarea')[0].click();")
                sleep(random.randint(1, 4))
                _list_textarea = self._driver.find_elements_by_tag_name("textarea")
                _list_textarea[0].click()
                _list_textarea = self._driver.find_elements_by_tag_name("textarea")
                _mensagem = self._text_random()
                print("Comentario sendo publicado: {}\nHorario: {}\n".format(_mensagem, datetime.now()))
                _list_textarea[0].send_keys(_mensagem)
                sleep(random.randint(1, 3))
                _list_tags_button = self._driver.find_elements_by_tag_name("button")
                for _button in _list_tags_button:
                    if (_button.text == 'Publicar') or (_button.text == 'Publish'):
                        _button.click()
                        sleep(random.randint(1, 3))
                        break
            except Exception as erro:
                if('element click intercepted' in str(erro).lower()):
                    self._driver.refresh()

    def _text_random(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(random.randint(1, 30)))
        return result_str

if __name__ == '__main__':
    username = input("Enter your USERNAME. Ex: pisaneschibruno\n")
    password = input("Enter your password\n")
    url_vote = input("Enter URL from specific publish\n")
    user_perfil = input("Enter specific username to be followed\n")
    insta = instagram(username, password, url_vote, user_perfil)
    insta.login()
    insta.vote_post()