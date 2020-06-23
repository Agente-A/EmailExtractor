
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import os
import requests
import json
import re


class WebBot():
    def __init__(self):
        self.driver = Firefox()

    def login(self):
        
        self.driver.get("https://adfs.inacap.cl/adfs/ls/?wtrealm=https://siga.inacap.cl/sts/&wa=wsignin1.0&wreply=https://siga.inacap.cl/sts/&wctx=https%3a%2f%2fadfs.inacap.cl%2fadfs%2fls%2f%3fwreply%3dhttps%3a%2f%2fwww.inacap.cl%2ftportalvp%2fintranet-alumno%26wtrealm%3dhttps%3a%2f%2fwww.inacap.cl%2f")
        
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('//*[@id="userNameInput"]'))
        inputUsr = self.driver.find_element_by_xpath('//*[@id="userNameInput"]')
        inputUsr.send_keys(username)

        inputPass = self.driver.find_element_by_xpath('//*[@id="passwordInput"]')
        inputPass.send_keys(password)

        inputLogin = self.driver.find_element_by_xpath('//*[@id="submitButton"]') 
        inputLogin.click()
        sleep(10)

    def getSede(self):

        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('/html/body/div[1]/div/section[3]/div[1]/ul/li[3]/a'))
        self.driver.find_element_by_xpath('/html/body/div[1]/div/section[3]/div[1]/ul/li[3]/a').click()
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])

        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/section/div/div/aside/aside[2]/div/div/div[1]/ul/li[2]/a'))
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/section/div/div/aside/aside[2]/div/div/div[1]/ul/li[2]/a').click()
        
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_elements_by_css_selector('div.media'))
        clases = self.driver.find_elements_by_css_selector('div.media')
        for x in clases:
            sede = x.find_element_by_tag_name('a').text
            match = re.search('Santiago Centro', sede)
            if match:
                print('Sede: ' + match.group())
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return
        print('La sede no es la especificad')
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.close()
        input('Pulse una tecla para finalizar')
        raise SystemExit

    def getCarrera(self):
        
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('//*[@id="t1_contenido"]'))
        cont = self.driver.find_element_by_xpath('//*[@id="t1_contenido"]')
        carrera = cont.find_element_by_tag_name('h3')
        print('La carrera es: ' + carrera.text)
        if carrera.text == 'Ingeniería en Informática' or carrera.text == 'Analista Programador':
            print('Usted es de la carrera c:')
            return
        print('Usted no es de la carrera :c')
        self.driver.close()
        input('Pulse una tecla para finalizar')
        raise SystemExit

    def getRamos(self):
        
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_link_text('Mi Malla'))
        self.driver.find_element_by_link_text('Mi Malla').click()
        sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        pattern = re.compile('^TI[a-zA-Z0-9]*')
        ti = []

        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_elements_by_css_selector('div.card'))
        clases = self.driver.find_elements_by_css_selector('div.card')
        for x in clases:
            match = pattern.match(x.find_element_by_tag_name('p').text)
            if match:
                name = x.find_element_by_tag_name('h5').text
                print(name)
                ti.append(name)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return ti

    def goToEmail(self, ti):

        lista = {}

        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('/html/body/div/div/section[3]/div[1]/div[1]/div[1]/h5'))
        self.driver.find_element_by_xpath('/html/body/div/div/section[3]/div[1]/div[1]/div[1]/h5').click()
        sleep(1)
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('/html/body/div/div/section[3]/div[1]/div[1]/div[1]/ul/li[4]/a'))
        self.driver.find_element_by_xpath('/html/body/div/div/section[3]/div[1]/div[1]/div[1]/ul/li[4]/a').click()
        
        sleep(3)

        self.driver.switch_to.window(self.driver.window_handles[1]) 
        
        # entrar a curso
        el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_elements_by_class_name('curso'))
        cursos = self.driver.find_elements_by_class_name('curso') 
        for curso in cursos:
            if curso.text in ti:
                print('\n' + curso.text)
                el = WebDriverWait(self.driver, timeout=30).until(lambda d: curso.find_element_by_tag_name('a'))
                curso.find_element_by_tag_name('a').click()
                
                el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_element_by_xpath('/html/body/form/div[4]/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/label/select'))
                cb = Select(self.driver.find_element_by_xpath('/html/body/form/div[4]/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/label/select'))
                cb.select_by_visible_text('100')

                # sacar lista de alumnos
                sleep(2)
                el = WebDriverWait(self.driver, timeout=30).until(lambda d: d.find_elements_by_css_selector('td.sorting_1'))
                nom = self.driver.find_elements_by_css_selector('td.sorting_1')
                mails = self.driver.find_elements_by_css_selector('td.curso')
                
                # limpiar basura
                aux = mails.copy()
                for x in aux:
                    if len(x.text) < 1 : mails.remove(x)

                # Llenar lista de estudiantes a mandar
                for x in range(len(nom)): 
                    lista[x] = {'name' : nom[x].text, 'email' : mails[x].text}
                    print('nombre: ' + nom[x].text + '\tCorreo: '+ mails[x].text + '\n') #cambiar por output de correos
                self.driver.find_element_by_xpath('//*[@id="btnVolver"]').click()
                sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        return lista

def sendData(alumnos, url):
    payload = {}
    for x , y in alumnos.items():
        payload[x] = json.dumps(y)

    x = requests.post(url, data = payload)
    print(x.text)


username = input('Introduce tu rut:\n(Recuerda que deben ser igual que en la intranet, sin puntos y con guión)\n EJ: 12345678-9\n')
password = input('Introduce tu contraseña:\n')
url = ''
os.system('cls')
bot = WebBot()
bot.driver.set_window_size(1303,784)
bot.login()
bot.getSede()
bot.getCarrera()
ti = bot.getRamos()
alumnos = bot.goToEmail(ti)
sendData(alumnos, url)
bot.driver.close()
input('Presione una tecla para finalizar o cierra la ventana si no quiere terminar')
raise SystemExit