# Proyecto Urban Routes - Automatización de Pruebas QA

## Descripción del Proyecto
Este proyecto consiste en la automatización del flujo completo de reserva de taxis en la aplicación web **Urban Routes**. La suite de pruebas cubre desde la configuración inicial de las direcciones de origen y destino hasta la confirmación final del pedido, garantizando que todos los componentes de la interfaz de usuario interactúen de manera fluida y correcta bajo condiciones reales de uso.

## Tecnologías y Técnicas Utilizadas
Para el desarrollo y ejecución de este framework de automatización se implementaron las siguientes tecnologías y mejores prácticas de ingeniería de software:

*   **Python (v3.13):** Lenguaje de programación principal para la lógica de las pruebas.
*   **Selenium WebDriver:** Herramienta para la automatización del navegador web e interacción con los elementos del DOM.
*   **Pytest:** Framework de pruebas encargado de la gestión, ejecución y reporte de los casos de prueba.
*   **Patrón de Diseño Page Object Model (POM):** Técnica utilizada para separar la lógica de las pruebas de los elementos de la interfaz de usuario, distribuidos en `main.py` (clase de página y pruebas) y `data.py` (datos de configuración), facilitando el mantenimiento del código.
*   **Esperas Explícitas (WebDriverWait):** Sincronización avanzada para manejar de manera óptima los tiempos de carga y transiciones de la interfaz.
*   **Inyección de scripts mediante JavaScript:** Técnica avanzada para controlar el enfoque de la aplicación (`blur()`) y el desplazamiento visual (`scrollIntoView`), asegurando estabilidad en elementos dinámicos u ocultos.

## Requisitos y Cobertura de Pruebas
La suite de pruebas automatiza y valida el escenario completo de un usuario pidiendo un taxi:
1. Configuración de las direcciones (Origen y Destino).
2. Selección de la tarifa Comfort.
3. Validación del número de teléfono a través de código SMS.
4. Vinculación de un método de pago (Tarjeta de Crédito).
5. Configuración de los requisitos del viaje (Escribir mensaje al conductor, activar manta/pañuelos y pedir 2 helados).
6. Confirmación final de la solicitud del taxi.

### Tipos de Localizadores Utilizados
Para cumplir con los estándares de robustez y diversidad, se implementaron más de 4 tipos distintos de selectores en Selenium:
*   `By.ID`: Para campos únicos del sistema como el cuadro de comentarios (`comment`).
*   `By.CSS_SELECTOR`: Para botones específicos como la selección de la tarifa o el botón de confirmación.
*   `By.XPATH`: Para localizar elementos mediante relaciones jerárquicas o textos dinámicos en la interfaz.
*   `By.CLASS_NAME` (o selectores combinados): Para el control preciso de modales y cierres de sección.

## Instrucciones de Ejecución

### 1. Clonar el repositorio y acceder al proyecto
```bash
cd qa-project-Urban-Routes-es