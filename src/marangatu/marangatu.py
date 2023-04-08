import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from marangatu.baja_timbrado import document_util
from utils import export_files

MOTIVO = 'ANULACION'


class MarangatuBot:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()

    def login(self) -> None:
        bot = self.bot
        bot.get('https://marangatu.set.gov.py/eset/login')
        sleep(3)

        try:
            user = bot.find_element(By.ID, 'usuario')
            user.clear()
            user.send_keys(self.username)

            password = bot.find_element(By.ID, 'clave')
            password.clear()
            password.send_keys(self.password)
            password.send_keys(Keys.RETURN)
        except:
            bot.close()

    def click_presentation(self) -> None:
        bot = self.bot
        btn_presentation = bot.find_element(
            By.XPATH, '/html/body/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/section[1]/div/div[1]/a[1]')
        btn_presentation.click()

    def add_fields_to_declatate(self, form_num: str, year: str, month: str) -> None:
        bot = self.bot

        # Find obligation select

        bot.switch_to.window(bot.window_handles[1])

        try:
            obligation_place = bot.find_element(By.NAME, 'obligacion')
            # # Click to deploy options
            # obligation_select.click()
            # obligation_select.send_keys(form_num)
            # obligation_select.send_keys(Keys.RETURN)

            obligation_select = Select(obligation_place)
            obligation_select.select_by_value(form_num)

            bot.implicitly_wait(3)

            # Find year and month
            year_place = bot.find_element(
                By.XPATH, '//*[@id="periodo"]/div/div[1]/select')
            month_place = bot.find_element(
                By.XPATH, '//*[@id="periodo"]/div/div[2]/select')

            # Select the options for year
            year_select = Select(year_place)
            year_select.select_by_value(year)

            bot.implicitly_wait(3)

            # Select the options for month
            month_select = Select(month_place)
            month_select.select_by_value(month)

            bot.implicitly_wait(4)

            # Verify to charge the form data
            form_data = bot.find_element(
                By.XPATH, '/html/body/div/div/div[2]/div/div/div[2]/div/div/div/div/div/form/section[2]/div/div/div/div/input')
            if form_data:
                open_declaration_btn = bot.find_element(
                    By.XPATH, '/html/body/div/div/div[2]/div/div/div[2]/div/div/div/div/div/form/div[4]/div/button')
                open_declaration_btn.click()
        except:
            self.logout()

    def complete_form(self, sin_movimiento: False) -> None:
        bot = self.bot
        if sin_movimiento:
            field_data = bot.find_element(By.XPATH, '//*[@id="C10"]')
            field_data.send_keys('0')
            field_data.send_keys(Keys.TAB)

            sleep(5)

            verify_enter_data = bot.find_element(By.XPATH, '//*[@id="C150"]')
            data = verify_enter_data.get_attribute('value')

            if data == '0':
                present_declaration_btn = bot.find_element(
                    By.XPATH, '//*[@id="Formu"]/section/div/div/div[2]/button')
                present_declaration_btn.click()

                bot.implicitly_wait(3)

                # Click to presentate
                # confirm_presentation_btn = bot.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/button[2]')

                # Click to cancel
                cancel_presentation_btn = bot.find_element(
                    By.XPATH, '/html/body/div[2]/div/div/div/div[3]/button[1]')
                cancel_presentation_btn.click()

            bot.implicitly_wait(3)
            bot.close()

    def logout(self) -> None:
        bot = self.bot
        bot.switch_to.window(bot.window_handles[0])
        bot.get('https://marangatu.set.gov.py/eset/logout')
        bot.quit()


class SendAnulados(MarangatuBot):

    def open_page_anulados(self) -> None:
        bot = self.bot
        try:

            try:
                btn_facturacion = WebDriverWait(bot, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[15]/div')
                    )
                )

                btn_facturacion = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[15]/div'
                )
                btn_facturacion.click()

            except TimeoutException:
                print('No hay elemento')

            solicitudes_xpath = '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[1]'
            solicitudes_xpath = bot.find_element(By.XPATH, solicitudes_xpath)
            if solicitudes_xpath:
                solicitudes_xpath.click()
                preimpresos = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[3]/div')

                if preimpresos:
                    preimpresos.click()
                    baja_pre = bot.find_element(
                        By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div[1]/div/div/div/div/section/div/div/div[2]/div/div/div[4]/div/div')

                    if baja_pre:
                        baja_pre.click()
                        bot.switch_to.window(bot.window_handles[1])
        except:
            self.logout()

    def timbrado_input(self, numero_timbrado: str) -> None:
        bot = self.bot
        try:
            timbrado_input = bot.find_element(
                By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section[1]/div[2]/div[1]/input')

            if timbrado_input:
                timbrado_input.clear()
                timbrado_input.send_keys(numero_timbrado)
                timbrado_input.send_keys(Keys.TAB)

                sleep(2)

                # search the next btn
                nex_button = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section[2]/div/div[2]/button')
                if nex_button:
                    nex_button.click()
        except:
            self.logout()

    def input_reason_and_date(self, date: str) -> None:
        bot = self.bot
        try:
            reason_select_element = bot.find_element(
                By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div[2]/div[1]/select')

            if reason_select_element:
                reason_select = Select(reason_select_element)
                reason_select.select_by_value(MOTIVO)

                date_element = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div[2]/div[2]/div/input')
                if date_element:
                    date_element.clear()
                    date_element.send_keys(date)
                    date_element.send_keys(Keys.TAB)

                    # search the next btn
                    nex_button = bot.find_element(
                        By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/section/div/div[2]/button')
                    if nex_button:
                        nex_button.click()

        except:
            self.logout()

    def document_data_input(self, document_number_range: str) -> None:
        bot = self.bot
        try:
            range_number_element_one = bot.find_element(
                By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div/div[1]/input')

            if range_number_element_one:
                range_number_element_one.clear()
                range_number_element_one.send_keys(document_number_range)
                # range_number_element_one.send_keys(Keys.TAB)

                range_number_element_two = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div/div[2]/input')
                if range_number_element_two:
                    range_number_element_two.clear()
                    range_number_element_two.send_keys(document_number_range)
                    range_number_element_two.send_keys(Keys.TAB)

                    # second_input = bot.find_element(
                    #     By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div[2]')

                    try:
                        second_input = WebDriverWait(bot, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/div/div/div/div/div[2]/table/tbody/tr/td[3]/div[2]')
                            )
                        )

                        # search the next btn
                        nex_button = bot.find_element(
                            By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/section/form/section/div/div[2]/button')

                        if nex_button:
                            nex_button.click()

                    except TimeoutException:
                        print('No hay elemento')

        except TimeoutException:
            print('No hay elemento')
            self.logout()

    def send_request(self):
        bot = self.bot
        try:
            # Verify document_anulado
            setlogo_img_reference = bot.find_element(
                By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/div/div/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/p[1]/font/img')

            if setlogo_img_reference:
                # Click the finalizar button
                finally_button = bot.find_element(
                    By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/form/section/div/div[2]/button')

                if finally_button:
                    finally_button.click()

                    alert_modal = bot.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/div/div[1]')
                    if alert_modal:
                        send_button = bot.find_element(
                            By.XPATH, '/html/body/div[2]/div/div/div/div[3]/button[2]')
                        if send_button:
                            send_button.click()

                            try:
                                setlogo_img_finally_reference = WebDriverWait(bot, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/div/div/div/div[2]/div/div/div/div[2]/div/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td[1]/p[1]/font/img')
                                    )
                                )
                            except TimeoutException:
                                print('No hay elemento')
        except:
            self.logout()

    def screen_anulado(self, ruc: str, document_number: str) -> None:
        bot = self.bot
        # Localizar el elemento que quieres capturar
        elemento = bot.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div[2]/div/div')

        # Hacer una captura de pantalla del elemento y guardarla en un archivo
        elemento.screenshot(
            f'archives/anulados/baja_{ruc}_{document_number}.png')


# bot = MarangatuBot(username='5255645', password='135910Vrela')
# bot.login()
# sleep(4)
# bot.click_presentation()
# sleep(4)
# bot.add_fields_to_declatate(form_num='211', year='2023', month='2')
# sleep(4)
# bot.complete_form(sin_movimiento=True)
# bot.logout()

# bot = SendAnulados(username='1192752', password='Yamil522')
# bot.login()
# sleep(3)
# bot.open_page_anulados()
# sleep(3)
# bot.timbrado_input('15550962')
# sleep(3)
# bot.input_reason_and_date('09/02/23')
# sleep(3)
# bot.document_data_input('29929')
# sleep(3)
# bot.send_request()
# sleep(3)
# bot.logout()


# anulados_path = document_util.separate_anulados()
# print(anulados_path)


# anulados = []

# for file_path in files_path:
#     anulados_data = document_util.get_anulados_data(path=file_path)
#     anulados.append(anulados_data)

# print(anulados)

# for documents in anulados:
#     for document in documents:
#         if 'no' not in document['client_name']:
#             print(document)
#             bot = SendAnulados(username='2634451', password='nicolas10')
#             bot.login()
#             sleep(3)
#             bot.open_page_anulados()
#             sleep(3)
#             bot.timbrado_input(document['timbrado'])
#             sleep(3)
#             bot.input_reason_and_date(document['date'])
#             sleep(3)
#             bot.document_data_input(
#                 document_number_range=document['document_number']['number'])
#             sleep(3)
#             bot.send_request()
#             sleep(3)
#             bot.screen_anulado(
#                 ruc='2634451', document_number=document['document_number']['total_number'])
#             bot.logout()
