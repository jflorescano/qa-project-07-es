#Archivo con la clase "UrbanRoutesPage"

import data
import helpers ##Importar el archivo con los métodos de apoyo
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException



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

    def wait_until_timer_finish(self):
        timer_locator = (By.CLASS_NAME, 'order-header-time')
        try:
            WebDriverWait(self.driver, 10).until(ec.text_to_be_present_in_element(timer_locator, "00:00"))
            return True
        except TimeoutException:
            return False
