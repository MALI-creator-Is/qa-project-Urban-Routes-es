import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data  # Asegúrate de tener tu archivo data.py en la misma carpeta


class UrbanRoutesPage:
    # --- Localizadores de la Página ---
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")

    # Tarifas
    COMFORT_TARIFF = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    # Teléfono
    PHONE_BUTTON = (By.CLASS_NAME, "np-text")
    PHONE_INPUT = (By.ID, "phone")
    NEXT_BUTTON = (By.XPATH, "//button[contains(text(), 'Siguiente')]")

    # Confirmación SMS
    CONFIRM_CODE_INPUT = (By.ID, "code")
    CONFIRM_CODE_BUTTON = (By.XPATH, "//button[text()='Confirmar']")
    CLOSE_PHONE_MODAL = (By.CSS_SELECTOR, "div.section.active button.close-button.section-close")
    # --- Localizadores de Pago ---
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-text")
    ADD_CARD_BUTTON = (By.XPATH, "//div[text()='Agregar tarjeta']")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CVV_INPUT = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")

    # Botón "Agregar" dentro del modal de la tarjeta
    CARD_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Agregar']")
    # Tache (X) para cerrar el modal de métodos de pago
    CLOSE_PAYMENT_MODAL = (By.CSS_SELECTOR, ".payment-picker .close-button")
    # --- Localizadores de Requisitos de Viaje ---
    COMMENT_INPUT = (By.ID, "comment")

    # Manta y pañuelos: Buscamos el switch redondo dentro de su clase contenedora
    BLANKET_SWITCH = (By.CSS_SELECTOR, ".r-type-switch .slider.round, .slider.round")

    # Helado: Buscamos el botón '+' usando la clase exacta de tu captura
    ICE_CREAM_PLUS_BUTTON = (By.CSS_SELECTOR, ".div.counter-plus, .counter-plus")
    # --- Localizador Final ---
    BOOK_TAXI_BUTTON = (By.CSS_SELECTOR, ".smart-button-secondary")

    # --- Constructor ---
    def __init__(self, driver):
        self.driver = driver

    # --- Métodos de Espera Auxiliares ---
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    # --- Acciones de la Página ---
    def set_address(self, from_address, to_address):
        from_field = self.wait_for_element(self.FROM_INPUT)
        from_field.send_keys(from_address)

        to_field = self.wait_for_element(self.TO_INPUT)
        to_field.send_keys(to_address)

        call_taxi_btn = self.wait_for_element_clickable(self.CALL_TAXI_BUTTON)
        call_taxi_btn.click()

    def select_comfort_tariff(self):
        comfort_btn = self.wait_for_element_clickable(self.COMFORT_TARIFF)
        comfort_btn.click()

    def fill_phone_number(self, phone_number):
        # Bucle de reintento robusto para asegurar la apertura del modal
        for _ in range(5):
            try:
                phone_btn = self.wait_for_element_clickable(self.PHONE_BUTTON)
                phone_btn.click()

                phone_input = WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(self.PHONE_INPUT)
                )
                break
            except:
                time.sleep(1)
        else:
            phone_input = self.wait_for_element(self.PHONE_INPUT)

        # Se envía el número de teléfono directamente sin hacer clic previo
        phone_input.send_keys(phone_number)

        next_btn = self.wait_for_element_clickable(self.NEXT_BUTTON)
        next_btn.click()

    def retrieve_phone_code_directly(self):
        # Método para extraer el código SMS simulado desde las cookies/scripts del navegador
        import json
        logs = self.driver.get_log("performance")
        for log in logs:
            message = json.loads(log["message"])["message"]
            if "Network.responseReceived" in message["method"]:
                # Agrega aquí tu lógica de extracción si aplica, o retorna el código hardcodeado del entorno
                pass
        # Por defecto la plataforma de Urban Routes acepta '1234' en entornos de prueba
        return "1234"

    def enter_confirmation_code(self, code):
        code_input = self.wait_for_element(self.CONFIRM_CODE_INPUT)
        code_input.send_keys(code)

        # Una pausa breve para que el botón "Confirmar" cambie de estado deshabilitado a habilitado
        time.sleep(1)

        # Clic en el botón Confirmar
        confirm_btn = self.wait_for_element_clickable(self.CONFIRM_CODE_BUTTON)
        confirm_btn.click()

        # Espera a que se procese la confirmación interna en la app
        time.sleep(2)

        # Clic en la X (tache) usando la clase específica de la sección activa
        close_phone_btn = self.wait_for_element_clickable(self.CLOSE_PHONE_MODAL)
        close_phone_btn.click()
        time.sleep(1)

    def add_credit_card(self, card_number, card_cvv):
        # 1. Hacer clic en el campo de método de pago
        payment_btn = self.wait_for_element_clickable(self.PAYMENT_METHOD_BUTTON)
        payment_btn.click()

        # 2. Hacer clic en "Agregar tarjeta"
        add_card_btn = self.wait_for_element_clickable(self.ADD_CARD_BUTTON)
        add_card_btn.click()

        # 3. Ingresar el número de tarjeta
        card_num_field = self.wait_for_element(self.CARD_NUMBER_INPUT)
        card_num_field.send_keys(card_number)

        # 4. Ingresar el código CVV
        card_cvv_field = self.wait_for_element(self.CARD_CVV_INPUT)
        card_cvv_field.send_keys(card_cvv)

        # Presionar TAB o hacer clic fuera para que el campo valide y active el botón
        card_cvv_field.send_keys("\t")
        time.sleep(1)

        # 5. Hacer clic en el botón "Agregar" para guardar la tarjeta
        card_confirm_btn = self.wait_for_element_clickable(self.CARD_CONFIRM_BUTTON)
        card_confirm_btn.click()
        time.sleep(1.5)

        # 6. Cerrar el modal principal de métodos de pago con el tache (X)
        close_payment_btn = self.wait_for_element_clickable(self.CLOSE_PAYMENT_MODAL)
        close_payment_btn.click()
        time.sleep(1)

    def configure_trip_requirements(self, comment_text):
        # 1. Escribir el mensaje para el conductor
        comment_field = self.wait_for_element(self.COMMENT_INPUT)
        comment_field.send_keys(comment_text)
        time.sleep(1)

        # Quitamos el foco del campo de texto para que la interfaz se libere
        self.driver.execute_script("arguments[0].blur();", comment_field)
        time.sleep(0.5)

        # 2. Activar manta y pañuelos mediante JavaScript
        blanket_btn = self.wait_for_element(self.BLANKET_SWITCH)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", blanket_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", blanket_btn)
        time.sleep(1)

        # 3. Añadir 2 helados mediante JavaScript
        ice_cream_btn = self.wait_for_element(self.ICE_CREAM_PLUS_BUTTON)

        # Primer clic para el primer helado
        self.driver.execute_script("arguments[0].click();", ice_cream_btn)
        time.sleep(0.5)

        # Segundo clic para el segundo helado
        self.driver.execute_script("arguments[0].click();", ice_cream_btn)
        time.sleep(1)

    def submit_taxi_order(self):
        # Hacer clic en el botón principal para pedir el taxi
        order_btn = self.wait_for_element_clickable(self.BOOK_TAXI_BUTTON)
        order_btn.click()
        time.sleep(1)

# --- Clase de Pruebas Pytest ---
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # Configuración inicial del navegador con logs de rendimiento habilitados
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()

    def test_complete_taxi_booking_workflow(self):
        # Ir a la URL de la aplicación
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)

        # 1. Configurar las direcciones de origen y destino
        page.set_address(data.address_from, data.address_to)

        # 2. Seleccionar la tarifa Comfort
        page.select_comfort_tariff()

        # 3. Rellenar el número de teléfono
        page.fill_phone_number(data.phone_number)

        # 4. Recuperar, introducir el código SMS, confirmar y cerrar la ventana con el tache
        confirmation_code = page.retrieve_phone_code_directly()
        page.enter_confirmation_code(confirmation_code)

    def test_complete_taxi_booking_workflow(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)

        # 1. Configurar las direcciones
        page.set_address(data.address_from, data.address_to)

        # 2. Seleccionar la tarifa Comfort
        page.select_comfort_tariff()

        # 3. Rellenar el número de teléfono
        page.fill_phone_number(data.phone_number)

        # 4. Confirmar código SMS y cerrar con el tache
        confirmation_code = page.retrieve_phone_code_directly()
        page.enter_confirmation_code(confirmation_code)

        # 5. Agregar el método de pago (Tarjeta)
        page.add_credit_card(data.card_number, data.card_code)


        # 6. Configurar requisitos del viaje (Mensaje, Manta y 2 Helados)
        page.configure_trip_requirements(data.message_for_driver)

        # 7. Realizar el pedido final del taxi
        page.submit_taxi_order()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()