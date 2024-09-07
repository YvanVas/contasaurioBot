from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ConsultarCi:
    def __init__(self) -> None:
        options = Options()

        #options.add_argument("--headless")
        self.bot = Firefox(options=options)

    def search_ci(self, ci: str) -> str:
        bot = self.bot
        bot.get(
            'https://servicios.set.gov.py/eset-publico/constanciaNoSerContribuyenteIService.do')
        wait = WebDriverWait(bot, 10)

        try:
            # Wait the input element
            input_identificacion = wait.until(
                EC.presence_of_element_located(
                    (By.NAME, 'numeroIdentificacion')
                )
            )

            # Send the identification value
            input_identificacion = bot.find_element(
                By.NAME, 'numeroIdentificacion')
            input_identificacion.clear()
            input_identificacion.send_keys(ci)

            # TAB to search the identification name
            input_identificacion.send_keys(Keys.TAB)

            while (True):
                input_fullname = bot.find_element(By.NAME, 'nombreRazonSocial')
                fullname = input_fullname.get_attribute('value')
                if fullname != '':
                    break

            bot.close()

            data = {
                'ci': ci,
                'fullname': fullname,
            }

            return data

        except:
            bot.close()
