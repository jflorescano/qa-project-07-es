import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as ec



# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button_locator = (By.CSS_SELECTOR, "#root > div > div.workflow > div.workflow-subcontainer > div.type-picker.shown > div.results-container > div.results-text > button")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_taxi_button(self):
        taxi_button = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.taxi_button_locator))
        taxi_button.click()

    def click_comfort_tariff(self):
        comfort_tariff_locator = (By.XPATH, "//*[@class='tcard-title' and text()='Comfort']")
        comfort_tariff = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(comfort_tariff_locator))
        comfort_tariff.click()

    def click_glam_tariff(self):
        comfort_tariff_locator = (By.XPATH, "//*[@class='tcard-title' and text()='Glamuroso']")
        comfort_tariff = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(comfort_tariff_locator))
        comfort_tariff.click()

    def click_phone(self):
        phone_button_locator = (By.XPATH, "//*[@class='np-text' and text()='Número de teléfono']")
        phone_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(phone_button_locator))
        phone_button.click()

    def fill_phone_number(self, phone_number):
        wait = WebDriverWait(self.driver, 10)
        phone_number_field_locator = (By.XPATH, "//*[@id='phone']")
        phone_number_field = wait.until(ec.visibility_of_element_located(phone_number_field_locator))
        phone_number_field.clear()
        phone_number_field.send_keys(phone_number)
        next_button_locator = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
        next_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(next_button_locator))
        next_button.click()
        code = retrieve_phone_code(self.driver)
        code_locator = (By.XPATH, "//*[@id='code']")
        code_field = wait.until(ec.visibility_of_element_located(code_locator))
        code_field.clear()
        code_field.send_keys(code)
        button_confirm_locator = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
        button_confirm = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(button_confirm_locator))
        button_confirm.click()

    def get_phone_number(self):
        phone_number_field_locator = (By.XPATH, "//*[@id='phone']")
        phone_number_field = self.driver.find_element(*phone_number_field_locator)
        return phone_number_field.get_attribute('value')

    def click_payment_method_card_button(self):
        payment_method_button_locator = (By.XPATH, "//*[@class='pp-text' and text()='Método de pago']")
        payment_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(payment_method_button_locator))
        payment_button.click()
        credit_card_locator = (By.XPATH, "//*[@class='pp-title' and text()='Agregar tarjeta']")
        card_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(credit_card_locator))
        card_button.click()

    def fill_credit_number_card(self, card):
        wait = WebDriverWait(self.driver, 10)
        card_number_field_locator = (By.XPATH, "//*[@id='number']")
        card_number_field = wait.until(ec.visibility_of_element_located(card_number_field_locator))
        card_number_field.clear()
        card_number_field.send_keys(card)
        card_number_field.send_keys(Keys.TAB)
        time.sleep(1)

    def fill_credit_cvv_card(self, cvv):
        wait = WebDriverWait(self.driver, 10)
        cvv_number_field_locator = (By.XPATH, "//*[@id='code']")
        cvv_number_field = wait.until(ec.visibility_of_element_located(cvv_number_field_locator))
        cvv_number_field.clear()
        cvv_number_field.send_keys(cvv)
        cvv_number_field.send_keys(Keys.TAB)
        time.sleep(1)

    def send_message(self, message):
        wait = WebDriverWait(self.driver, 10)
        message_field_locator = (By.XPATH, "//*[@id='comment']")
        message_field = wait.until(ec.visibility_of_element_located(message_field_locator))
        message_field.clear()
        message_field.send_keys(message)

    def click_blanket_scarves(self):
        slider_locator = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
        slider = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(slider_locator))
        slider.click()

    def click_order_icecream(self):
        increment_button_locator = (By.XPATH,"//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
        increment_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(increment_button_locator))
        for _ in range(data.ice_cream):
            increment_button.click()
            time.sleep(1)

    def click_order_taxi(self):
        button_order_locator = (By.XPATH, "//*[@id='root']/div/div[3]/div[4]/button/span[1]")
        button_order = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(button_order_locator))
        button_order.click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options=Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        comfort_tariff_element = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, "#root > div > div.workflow > div.workflow-subcontainer > div.tariff-picker.shown > div.tariff-cards > div.tcard.active > div.tcard-title")))
        assert "Comfort" in comfort_tariff_element.text, "La tarifa de comfort no se ha seleccionado"
        time.sleep(2)
    
    def test_phone_number(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_phone()
        phone_number_test = data.phone_number
        routes_page.fill_phone_number(phone_number_test)
        actual_phone_number = routes_page.get_phone_number()
        assert actual_phone_number == phone_number_test, f"Número actual: {actual_phone_number}"
        time.sleep(2)

    def test_credit_card(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_phone()
        phone_number_test = data.phone_number
        routes_page.fill_phone_number(phone_number_test)
        routes_page.click_payment_method_card_button()
        card_numer_test = data.card_number
        cvv_test = data.card_code
        routes_page.fill_credit_number_card(card_numer_test)
        routes_page.fill_credit_cvv_card(cvv_test)
        time.sleep(2)

    def test_message_driver(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        message_test = data.message_for_driver
        routes_page.send_message(message_test)
        time.sleep(2)
        comment_field_locator = (By.XPATH, "//*[@id='comment']")
        comment_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(comment_field_locator))
        actual_message = comment_field.get_attribute('value')
        assert actual_message == message_test, f"El mensaje no se escribió correctamente."

    def test_order_blanket_scarves(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_blanket_scarves()
        time.sleep(2)

    def test_order_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_order_icecream()
        time.sleep(2)
    
    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_glam_tariff()
        routes_page.click_phone()
        phone_number_test = data.phone_number
        routes_page.fill_phone_number(phone_number_test)
        actual_phone_number = routes_page.get_phone_number()
        assert actual_phone_number == phone_number_test, f"Número actual: {actual_phone_number}"
        routes_page.click_order_taxi()
        time.sleep(5)
   
    def test_order_taxi_info(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(2)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_glam_tariff()
        routes_page.click_phone()
        phone_number_test = data.phone_number
        routes_page.fill_phone_number(phone_number_test)
        actual_phone_number = routes_page.get_phone_number()
        assert actual_phone_number == phone_number_test, f"Número actual: {actual_phone_number}"
        routes_page.click_order_taxi()
        time.sleep(60)



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
