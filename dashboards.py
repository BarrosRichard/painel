from infra.config import Database
from infra.Models import Empresas, LinksBI
from selenium import webdriver
import login
import updates
import driver_config
import refresh

def dashboards():
    infra = Database().infra
    infra.execute('TRUNCATE TABLE sit_status_bi_last')
    infra.commit()

    # coleta as empresas all empresas
    empresas = infra.query(Empresas).where(
        Empresas.deleted == None, Empresas.bi_user != None)

    # para cada empresa dentro da empresas
    for empresa in empresas:
        # coleta todos os painels
        paineis = infra.query(LinksBI).where(
            LinksBI.empresa_id == empresa.id, LinksBI.deleted == None, LinksBI.dataset_id != None)
        
        options = driver_config.driver_options()

        driver = webdriver.Chrome("./drivers/chromedriver.exe" ,chrome_options=options)
        driver = login.login(driver, empresa.name,
                             empresa.bi_user, empresa.bi_pass)

        if driver == None:
            pass
        else:
            for painel in paineis:
                print(f"{empresa.name}, {painel.titulo}")
                if painel.workspace_id == None:
                    driver.get(
                        f'https://app.powerbi.com/groups/me/settings/datasets/{painel.dataset_id}')
                else:
                    driver.get(
                        f'https://app.powerbi.com/groups/{painel.workspace_id}/settings/datasets/{painel.dataset_id}')

                updates.checkupdates(driver, infra, empresa, painel)
                driver_config.driver_delay(driver)

    gaspar = infra.query(Empresas).filter_by(id=37).first()
    
    driver = webdriver.Chrome("./drivers/chromedriver.exe" ,chrome_options=options)
    driver = login.login(driver, gaspar.name,
                         gaspar.bi_user, gaspar.bi_pass)

    refresh.refresh(
        driver, '624ccada-7f68-44a1-8ef3-9e747dde6710', gaspar.bi_user, gaspar.bi_pass)

dashboards()
