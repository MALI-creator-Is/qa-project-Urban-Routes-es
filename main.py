import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import data
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code
import time


class TestUrbanRoutes:
    driver = None
    page = None

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # 1️⃣ Configuración de dirección inicial
    def test_1_set_address(self):
        self.page.set_addresses(data.address_from, data.address_to)
        self.page.click_call_taxi()

        # Validar que los campos de dirección tengan los valores correctos
        from_val = self.driver.find_element(*self.page.FROM_INPUT).get_attribute("value")
        to_val = self.driver.find_element(*self.page.TO_INPUT).get_attribute("value")
        assert from_val == data.address_from
        assert to_val == data.address_to

    # 2️⃣ Selección de la tarifa Comfort
    def test_2_select_comfort_tariff(self):
        self.page.select_comfort_tariff()
        tariff_element = self.page.wait_for_element(self.page.COMFORT_TARIFF)
        assert tariff_element.is_displayed()

    # 3️⃣ Registro del número telefónico
    def test_3_register_phone_number(self):
        self.page.open_phone_modal()
        self.page.enter_phone_number(data.phone_number)

    # 4️⃣ Agregar tarjeta bancaria
    def test_4_add_payment_method_card(self):
        # 1. Abre el modal de métodos de pago
        self.page.open_payment_modal()

        # 2. Haz clic en agregar tarjeta
        self.page.click_add_card()

        # 3. Rellena los detalles de la tarjeta (usa el método limpio fill_card_details)
        self.page.fill_card_details("1234 5678 9101 1121", "111")

    # 5️⃣ Confirmación de la tarjeta y cierre de modal
    def test_5_confirm_card_and_close(self):
        # 1. Haz clic en el botón verde "Agregar" de la tarjeta
        self.page.confirm_card()

        # 2. Haz clic en la "X" para cerrar el modal de métodos de pago
        self.page.close_payment_method_modal()

        # 3. Valida que volvió a la pantalla principal y muestra "Tarjeta"
        payment_val = self.driver.find_element(*self.page.PAYMENT_METHOD_BUTTON).text
        assert "Tarjeta" in payment_val or "Card" in payment_val

    # 6️⃣ Confirmación de código SMS
        # 6️⃣ Confirmación de código SMS
        # 6️⃣ Confirmación de código SMS
        # 6️⃣ Confirmación de código SMS
        def test_6_confirm_sms_code(self):
            # 1. Recuperamos el código SMS generado por la base de datos
            sms_code = retrieve_phone_code(self.driver)

            # 2. Introducimos el código en el input y se confirma
            self.page.enter_confirmation_code(sms_code)

            # Pequeña pausa para que la app procese la validación del código antes de cerrar
            time.sleep(1)

            # 3. Cerramos el modal de teléfono usando la cruz "X"
            self.page.close_phone_modal()

            # 4. Esperamos a que el modal del número de teléfono desaparezca por completo de la pantalla
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".number-picker.open"))
            )

            # 5. Esperamos a que el número de teléfono aparezca guardado en la pantalla principal
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(
                    *self.page.PHONE_VALUE_TEXT).text != "Introducir un número de teléfono y reservar"
            )

            # 6. Aserción final de validación del número telefónico
            phone_val_element = self.driver.find_element(*self.page.PHONE_VALUE_TEXT)
            assert data.phone_number in phone_val_element.text
    # 7️⃣ Envío de mensaje al conductor
    def test_7_send_driver_comment(self):
        self.page.enter_driver_comment(data.message_for_driver)
        comment_val = self.driver.find_element(*self.page.COMMENT_INPUT).get_attribute("value")
        assert comment_val == data.message_for_driver

    # 8️⃣ Solicitud de manta, pañuelos y 2 helados
    def test_8_configure_extras(self):
        # 1. Activar manta y pañuelos
        self.page.toggle_blanket_and_scarves()

        # 2. Pedir exactamente 2 helados
        self.page.add_ice_cream(2)

        # 3. Validar que el checkbox de la manta esté seleccionado
        checkbox = self.driver.find_element(By.CSS_SELECTOR, ".r-type-switch .switch-input")
        assert checkbox.is_selected() or checkbox.get_property("checked") is True

        # 4. Validar que el contador de helados muestre "2"
        ice_cream_value = self.driver.find_element(By.CSS_SELECTOR, ".counter-value").text
        assert ice_cream_value == "2"

    # 9️⃣ Validación de aparición del modal de búsqueda de taxi
    def test_9_submit_and_verify_search_modal(self):
        # 1. Hacemos clic en el botón definitivo para pedir el taxi
        self.page.click_book_taxi()

        # 2. Validamos que el modal de búsqueda de taxi aparezca en pantalla
        assert self.page.is_search_modal_visible() is True