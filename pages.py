import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # --- Localizadores de la Página ---
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")

    # Tarifas
    COMFORT_TARIFF = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    # Teléfono
    PHONE_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_VALUE_TEXT = (By.CLASS_NAME, "np-value")
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Siguiente')]")

    # Confirmación SMS
    CONFIRM_CODE_INPUT = (By.ID, "code")
    CONFIRM_CODE_BUTTON = (By.XPATH, "//button[text()='Confirmar']")
    CLOSE_PHONE_MODAL = (By.CSS_SELECTOR, "div.section.active button.close-button.section-close")
    CLOSE_PHONE_MODAL_BUTTON = (By.CSS_SELECTOR, ".number-picker.open .close-button")

    # --- Localizadores de Pago ---
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.XPATH, "//div[text()='Agregar tarjeta']")
    CARD_NUMBER_INPUT = (By.ID, "number")
    # Usamos este localizador para el CVV
    CARD_CVV_INPUT = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    CARD_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Agregar']")
    CLOSE_PAYMENT_MODAL_BUTTON = (By.CSS_SELECTOR, ".payment-picker .close-button")

    # --- Localizadores de Requisitos de Viaje ---
    COMMENT_INPUT = (By.ID, "comment")
    BLANKET_SWITCH = (By.CSS_SELECTOR, ".r-type-switch .slider.round, .slider.round")
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, ".div.counter-plus, .counter-plus")

    # Localizadores de pedido
    BOOK_TAXI_BUTTON = (By.CSS_SELECTOR, ".smart-button")
    SEARCH_MODAL = (By.CSS_SELECTOR, ".order-body")

    def __init__(self, driver):
        self.driver = driver

    # --- Métodos de Espera Auxiliares ---
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    # --- Acciones de la Página ---
    def set_addresses(self, from_address, to_address):
        from_field = self.wait_for_element(self.FROM_INPUT)
        from_field.send_keys(from_address)
        to_field = self.wait_for_element(self.TO_INPUT)
        to_field.send_keys(to_address)

    def click_call_taxi(self):
        call_taxi_btn = self.wait_for_element_clickable(self.CALL_TAXI_BUTTON)
        call_taxi_btn.click()

    def select_comfort_tariff(self):
        comfort_btn = self.wait_for_element_clickable(self.COMFORT_TARIFF)
        comfort_btn.click()

    def open_phone_modal(self):
        phone_btn = self.wait_for_element_clickable(self.PHONE_BUTTON)
        self.driver.execute_script("arguments[0].click();", phone_btn)

    def enter_phone_number(self, phone_number):
        phone_input = self.wait_for_element_visible(self.PHONE_INPUT)
        phone_input.send_keys(phone_number)
        next_btn = self.wait_for_element_clickable(self.NEXT_BUTTON)
        next_btn.click()

    def enter_confirmation_code(self, code):
        from selenium.webdriver.common.keys import Keys
        code_input = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.CONFIRM_CODE_INPUT)
        )
        code_input.clear()
        code_input.send_keys(code)
        code_input.send_keys(Keys.TAB)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONFIRM_CODE_BUTTON)
        )
        try:
            confirm_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", confirm_btn)

    def close_phone_modal(self):
        # 1. Esperamos a que el elemento esté presente en el DOM
        close_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CLOSE_PHONE_MODAL_BUTTON)
        )
        # 2. Hacemos clic usando JavaScript para garantizar que se ejecute de inmediato
        self.driver.execute_script("arguments[0].click();", close_btn)
    def open_payment_modal(self):
        payment_btn = self.wait_for_element_clickable(self.PAYMENT_METHOD_BUTTON)
        self.driver.execute_script("arguments[0].click();", payment_btn)

    def click_add_card(self):
        add_card_btn = self.wait_for_element_clickable(self.ADD_CARD_BUTTON)
        add_card_btn.click()

    def fill_card_details(self, card_number, card_cvv):
        from selenium.webdriver.common.keys import Keys
        card_num_field = self.wait_for_element_visible(self.CARD_NUMBER_INPUT)
        card_num_field.clear()
        card_num_field.send_keys(card_number)

        card_cvv_field = self.wait_for_element_visible(self.CARD_CVV_INPUT)
        card_cvv_field.clear()
        card_cvv_field.send_keys(card_cvv)

        # Pérdida de foco para activar el botón de confirmación
        card_cvv_field.send_keys(Keys.TAB)
        time.sleep(1)

    def confirm_card(self):
        card_confirm_btn = self.wait_for_element_clickable(self.CARD_CONFIRM_BUTTON)
        card_confirm_btn.click()
        time.sleep(1)

    def close_payment_method_modal(self):
        close_btn = self.wait_for_element_clickable(self.CLOSE_PAYMENT_MODAL_BUTTON)
        close_btn.click()

    def enter_driver_comment(self, comment_text):
        comment_field = self.wait_for_element(self.COMMENT_INPUT)
        comment_field.send_keys(comment_text)
        self.driver.execute_script("arguments[0].blur();", comment_field)
        time.sleep(0.5)

    def toggle_blanket_and_scarves(self):
        blanket_btn = self.wait_for_element(self.BLANKET_SWITCH)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", blanket_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", blanket_btn)
        time.sleep(1)

    def add_ice_cream(self, quantity):
        plus_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON) # Asegúrate de que este localizador apunte a .counter-plus
        )
        for _ in range(quantity):
            try:
                plus_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", plus_btn)

    def click_book_taxi(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.BOOK_TAXI_BUTTON)
        )
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def is_search_modal_visible(self):
        try:
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SEARCH_MODAL)
            )
            return modal.is_displayed()
        except Exception:
            return False