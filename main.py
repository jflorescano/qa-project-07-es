import data
import helpers ##Importar el archivo con los métodos de apoyo
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

#Todos los selectores se movieron al inicio de las pruebas y se cambio el tipo de selector
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button_locator = (By.XPATH, "//*[@class='button round' and text()='Pedir un taxi']")  #Selector único para el botón
    comfort_tariff_locator = (By.XPATH, "//*[@class='tcard-title' and text()='Comfort']")
    glam_tariff_locator = (By.XPATH, "//*[@class='tcard-title' and text()='Glamuroso']")
    phone_button_locator = (By.XPATH, "//*[@class='np-text' and text()='Número de teléfono']")
    phone_number_field_locator = (By.XPATH, "//*[@id='phone']")
    next_button_locator = (By.XPATH, "//*[@class='button full' and text()='Siguiente']") #Selector único para el botón
    code_locator = (By.XPATH, "//*[@id='code']")
    button_confirm_locator = (By.XPATH, "//*[@class='button full' and text()='Confirmar']") #Selector único para el botón
    payment_method_button_locator = (By.XPATH, "//*[@class='pp-text' and text()='Método de pago']")
    credit_card_locator = (By.XPATH, "//*[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_field_locator = (By.XPATH, "//*[@id='number']")
    cvv_number_field_locator = (By.XPATH, "//*[@id='code']")
    message_field_locator = (By.XPATH, "//*[@id='comment']")
    slider_locator = (By.XPATH, "//*[@class='slider round']") #Selector único para el slider
    increment_button_locator = (By.XPATH, "//*[@class='counter-plus']") #Selector único para el contador
    button_order_locator = (By.XPATH, "//*[@class='smart-button']") #Selector único para el botón

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
        comfort_tariff = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.comfort_tariff_locator))
        comfort_tariff.click()

    def click_glam_tariff(self):
        comfort_tariff = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.glam_tariff_locator))
        comfort_tariff.click()

    def click_phone(self):
        phone_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.phone_button_locator))
        phone_button.click()

    def fill_phone_number(self, phone_number):
        wait = WebDriverWait(self.driver, 10)
        phone_number_field = wait.until(ec.visibility_of_element_located(self.phone_number_field_locator))
        phone_number_field.clear()
        phone_number_field.send_keys(phone_number)
        next_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.next_button_locator))
        next_button.click()
        code = helpers.retrieve_phone_code(self.driver)
        code_field = wait.until(ec.visibility_of_element_located(self.code_locator))
        code_field.clear()
        code_field.send_keys(code)
        button_confirm = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.button_confirm_locator))
        button_confirm.click()

    def get_phone_number(self):
        phone_number_field_locator = (By.XPATH, "//*[@id='phone']")
        phone_number_field = self.driver.find_element(*phone_number_field_locator)
        return phone_number_field.get_attribute('value')

    def click_payment_method_card_button(self):
        payment_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.payment_method_button_locator))
        payment_button.click()
        card_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.credit_card_locator))
        card_button.click()

    def fill_credit_number_card(self, card):
        wait = WebDriverWait(self.driver, 10)
        card_number_field = wait.until(ec.visibility_of_element_located(self.card_number_field_locator))
        card_number_field.clear()
        card_number_field.send_keys(card)
        card_number_field.send_keys(Keys.TAB)

    def fill_credit_cvv_card(self, cvv):
        wait = WebDriverWait(self.driver, 10)
        cvv_number_field = wait.until(ec.visibility_of_element_located(self.cvv_number_field_locator))
        cvv_number_field.clear()
        cvv_number_field.send_keys(cvv)
        cvv_number_field.send_keys(Keys.TAB)

    def send_message(self, message):
        wait = WebDriverWait(self.driver, 10)
        message_field = wait.until(ec.visibility_of_element_located(self.message_field_locator))
        message_field.clear()
        message_field.send_keys(message)

    def click_blanket_scarves(self):
        slider = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(self.slider_locator))
        slider.click()

    def click_order_icecream(self):
        increment_button = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.increment_button_locator))
        for _ in range(data.ice_cream):
            increment_button.click()

    def click_order_taxi(self):
        button_order = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(self.button_order_locator))
        button_order.click()


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options=Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Se elimino el uso de "time.sleep()" y se agrego el método "assert" en todas las pruebas
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(1)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_set_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
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
    
    def test_phone_number(self):
        self.driver.get(data.urban_routes_url)
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

#Se agrego assert
    def test_credit_card(self):
        self.driver.get(data.urban_routes_url)
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

        card_number_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(routes_page.card_number_field_locator))
        assert card_number_field.get_attribute('value') == card_numer_test, "El número de tarjeta no coincide."
        cvv_number_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(routes_page.cvv_number_field_locator))
        assert cvv_number_field.get_attribute('value') == cvv_test, "El CVV no coincide."

    def test_message_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        message_test = data.message_for_driver
        routes_page.send_message(message_test)
        comment_field_locator = (By.XPATH, "//*[@id='comment']")
        comment_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(comment_field_locator))
        actual_message = comment_field.get_attribute('value')
        assert actual_message == message_test, f"El mensaje no se escribió correctamente."

    def test_order_blanket_scarves(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_blanket_scarves()

#Se agrego assert
    def test_order_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_order_icecream()
        counter_element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "counter-value")))
        counter = counter_element.text
        assert counter == data.ice_cream, f"La cantidad no coincide"

#Se agrego assert
    def test_order_taxi(self):
        self.driver.get(data.urban_routes_url)
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
        routes_page.click_order_taxi()
        try:
            # Verifica si el botón sigue siendo clickeable después de hacer clic
            is_clicked = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(UrbanRoutesPage.button_order_locator)).is_enabled()
        except StaleElementReferenceException:
            # Si el elemento ya no está presente en el DOM, se produce una excepción
            is_clicked = False

            # Utiliza un assert para verificar si el botón fue clickeado correctamente
        assert is_clicked, "No se pudo confirmar que se hizo clic en el botón Order Taxi."


    def test_order_taxi_info(self):
        self.driver.get(data.urban_routes_url)
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
        routes_page.click_order_taxi()
        time.sleep(60)



    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
