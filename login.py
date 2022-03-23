from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import driver_config
import time
import sendmail

def login(driver, empresa, user, password):
    try:
        # Acessa o site inicial do PowerBI para verificar existencia da conta
        driver.get('https://app.powerbi.com/')
        driver_config.driver_delay(driver)

        # Adiciona o email na caixa de verificação
        driver.find_element_by_id('email').send_keys(user)
        time.sleep(0.5)

        driver.find_element_by_id('submitBtn').click() # Envia as informações
        
        driver_config.driver_delay(driver) # Aguarda carregamento para login
        time.sleep(3)

        # insere as senha e envia a senha
        driver.find_element_by_id("i0118").send_keys(password, Keys.ENTER)
        
        # verificação de senha
        page = driver.find_element_by_xpath("/html").get_attribute("innerHTML") # pega o código da página
        page = BeautifulSoup(page, "lxml") # converte em xml
        errorPassowrd = page.find("div", {"id": "passwordError"}) # verifica se existe mensagem de erro

        # Se a senha for incorreta é enviado um email para alteração
        if errorPassowrd != None:
            subject = f"A senha de {empresa} está incorreta, por favor alterar"
            message = f"A senha de {empresa} está incorreta, por favor alterar"
            sendmail.sendmail(subject, message)
            return None
        else:
            # caso contrário é confirmado o logon e pronto, você está logado ^^
            driver.find_element_by_id("idSIButton9").click()
            return driver # retorna o driver logado
    except:
        return None
