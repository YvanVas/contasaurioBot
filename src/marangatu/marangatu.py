import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

PATH = os.environ['PATH']


class MarangatuBot:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path=PATH)

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
                #confirm_presentation_btn = bot.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/button[2]')

                # Click to cancel
                cancel_presentation_btn = bot.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/button[1]')
                cancel_presentation_btn.click()
                
                
            bot.implicitly_wait(3)
            bot.close()


    def logout(self) -> None:
        bot = self.bot
        bot.get('https://marangatu.set.gov.py/eset/logout')
        bot.close()


bot = MarangatuBot(username='', password='')
bot.login()
sleep(4)
bot.click_presentation()
sleep(4)
bot.add_fields_to_declatate(form_num='', year='', month='')
sleep(4)
bot.complete_form(sin_movimiento=True)
sleep(5)
bot.logout()
