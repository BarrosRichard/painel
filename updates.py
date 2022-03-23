from bs4 import BeautifulSoup
import driver_config
from datetime import datetime
from infra.Models import StatusBI, StatusBILast
import time
import sendmail

def checkupdates(driver, infra, empresa, painel):
    try:
        hoje = datetime.today()
        hoje = datetime(hoje.year, hoje.month, hoje.day, 00, 00, 00)

        driver_config.driver_delay(driver)
        time.sleep(10)

        page = driver.find_element_by_xpath("/html").get_attribute("innerHTML")
        page = BeautifulSoup(page, "lxml")

        refreshHistory = page.find("button", {"class": "refreshHistory"})

        if refreshHistory == None:
            sendmail.sendmail(f"O Dataset do painel {painel.titulo} está incorreto, por favor alterar",
                            f"O Dataset do painel {painel.titulo} está incorreto, por favor alterar")
        else:
            driver.find_element_by_xpath(
                '//*[text()="Histórico de atualização"]').click()
            driver_config.driver_delay(driver)
            time.sleep(3)

            driver.find_element_by_xpath(
                '//*[text()="Agendado"]').click()
            driver_config.driver_delay(driver)
            time.sleep(3)

            # Init::Coleta Dados da Tabela
            table = driver.find_element_by_class_name(
                'historyTable').get_attribute('innerHTML')

            table = table.encode('utf-8')

            table = BeautifulSoup(table, 'lxml')

            tbody = table.find('tbody')

            agendado = True
            tr = tbody.find('tr')

            if tr == None:
                agendado = False
            else:
                data = tr.find_all('td')
                tipo = 'Agendada'
                iniciar = data[2].text
                iniciar = datetime.strptime(
                    iniciar, '%d/%m/%Y %H:%M:%S')
                terminar = data[3].text
                if terminar != '':
                    terminar = datetime.strptime(
                        terminar, '%d/%m/%Y %H:%M:%S')
                else:
                    terminar = datetime.now()

                status = data[4].text
                mensagem = data[5].text

            driver.find_element_by_xpath(
                '//*[text()="OneDrive"]').click()
            driver_config.driver_delay(driver)
            time.sleep(3)

            table = driver.find_element_by_class_name(
                'historyTable').get_attribute('innerHTML')
            table = table.encode('utf-8')

            table = BeautifulSoup(table, 'lxml')

            tbody = table.find('tbody')

            tr = tbody.find('tr')

            data = tr.find_all('td')
            manual_tipo = 'Manual'
            manual_iniciar = data[2].text
            manual_iniciar = datetime.strptime(
                manual_iniciar, '%d/%m/%Y %H:%M:%S')
            manual_terminar = data[3].text
            manual_terminar = datetime.strptime(
                manual_terminar, '%d/%m/%Y %H:%M:%S')
            manual_status = data[4].text
            manual_mensagem = data[5].text

            # End::Coleta Dados Tabela


            if agendado == True:
                if manual_terminar < hoje:
                    manual_status = 'Falhou'

                if iniciar > manual_iniciar:
                    iniciar = datetime.strftime(
                        iniciar, '%Y-%m-%d %H:%M:%S')
                    if terminar != '':
                        terminar = datetime.strftime(
                            terminar, '%Y-%m-%d %H:%M:%S')

                    new_log = StatusBILast(id_empresa=empresa.id,
                                            nome_conjunto=empresa.name,
                                            nome_painel=painel.titulo,
                                            dataset_id=painel.dataset_id,
                                            tipo=tipo,
                                            iniciar=iniciar,
                                            terminar=terminar if terminar != '' else "0000-00-00 00:00:00",
                                            status=status,
                                            mensagem=mensagem)

                    infra.add(new_log)
                    infra.commit()

                    new_log = StatusBI(id_empresa=empresa.id,
                                        nome_conjunto=empresa.name,
                                        nome_painel=painel.titulo,
                                        dataset_id=painel.dataset_id,
                                        tipo=tipo,
                                        iniciar=iniciar,
                                        terminar=terminar if terminar != '' else "0000-00-00 00:00:00",
                                        status=status,
                                        mensagem=mensagem)

                    infra.add(new_log)
                    infra.commit()
                    print("Commitei")

                elif manual_iniciar > iniciar:
                    manual_iniciar = datetime.strftime(
                        manual_iniciar, '%Y-%m-%d %H:%M:%S')
                    manual_terminar = datetime.strftime(
                        manual_terminar, '%Y-%m-%d %H:%M:%S')

                    new_log = StatusBILast(id_empresa=empresa.id,
                                            nome_conjunto=empresa.name,
                                            nome_painel=painel.titulo,
                                            dataset_id=painel.dataset_id,
                                            tipo=manual_tipo,
                                            iniciar=manual_iniciar,
                                            terminar=manual_terminar,
                                            status=manual_status,
                                            mensagem=manual_mensagem)

                    infra.add(new_log)
                    infra.commit()
                    print("Commitei")

                    new_log = StatusBI(id_empresa=empresa.id,
                                        nome_conjunto=empresa.name,
                                        nome_painel=painel.titulo,
                                        dataset_id=painel.dataset_id,
                                        tipo=manual_tipo,
                                        iniciar=manual_iniciar,
                                        terminar=manual_terminar,
                                        status=manual_status,
                                        mensagem=manual_mensagem)

                    infra.add(new_log)
                    infra.commit()
                    print("Commitei")

            else:
                manual_iniciar = datetime.strftime(
                        manual_iniciar, '%Y-%m-%d %H:%M:%S')
                manual_terminar = datetime.strftime(
                    manual_terminar, '%Y-%m-%d %H:%M:%S')

                new_log = StatusBILast(id_empresa=empresa.id,
                                        nome_conjunto=empresa.name,
                                        nome_painel=painel.titulo,
                                        dataset_id=painel.dataset_id,
                                        tipo=manual_tipo,
                                        iniciar=manual_iniciar,
                                        terminar=manual_terminar,
                                        status=manual_status,
                                        mensagem=manual_mensagem)

                infra.add(new_log)
                infra.commit()
                print("Commitei")

                new_log = StatusBI(id_empresa=empresa.id,
                                    nome_conjunto=empresa.name,
                                    nome_painel=painel.titulo,
                                    dataset_id=painel.dataset_id,
                                    tipo=manual_tipo,
                                    iniciar=manual_iniciar,
                                    terminar=manual_terminar,
                                    status=manual_status,
                                    mensagem=manual_mensagem)

                infra.add(new_log)
                infra.commit()
                print("Commitei")
    except:
        pass

