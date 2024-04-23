import data
from urban_routes_page import UrbanRoutesPage #Importar el archivo que contiene la clase UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException


#Se creo otro archivo para la clase de  UrbanRoutesPage y se importa en el archivo main
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Se elimino el uso de "time.sleep()" y se agrego el método "assert" en todas las pruebas
    #Se elimino time.sleep()
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "from")))
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

#Se agrego assert
    def test_order_blanket_scarves(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        routes_page.click_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_blanket_scarves()
        slider_locator = (By.XPATH, "//*[@class='slider round']")
        slider_field = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(slider_locator))
        actual_slider = slider_field.get_attribute('class')
        assert 'data-slider-select-id' in actual_slider, "El slider no se seleccionó correctamente"

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
        counter_element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, "//*[@class='counter-value']")))
        counter = counter_element.text
        counter_number = int(counter)
        assert counter_number == data.ice_cream, f"La cantidad no coincide"

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
        button_order = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(UrbanRoutesPage.button_order_locator))
        routes_page.click_order_taxi()
        is_clicked = button_order.is_enabled()
        assert is_clicked, "No se seleccionó el botón Ordenar Taxi."

#Se agrego el método assert y se elimino time.sleep()
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
        timer_finished = routes_page.wait_until_timer_finish()
        assert timer_finished, "El temporizador no ha finalizado correctamente"


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
