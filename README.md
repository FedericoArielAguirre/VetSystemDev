# 🐾 VetSystem — Sistema de Gestión Veterinaria

**VetSystem** es una aplicación web ligera y elegante construida con Python y [Streamlit](https://streamlit.io/). Está diseñada para gestionar integralmente una clínica veterinaria y su tienda de mascotas (PetShop), combinando un historial clínico detallado con un punto de venta (POS) funcional.

El sistema destaca por su **diseño visual personalizado**, inyectado mediante CSS, que utiliza tipografías modernas (*Fraunces* y *DM Mono*) y una paleta de colores cuidada para ofrecer una experiencia de usuario (UX) limpia y profesional, alejándose del aspecto por defecto de Streamlit.

---

## ✨ Características Principales

La aplicación está dividida en 6 módulos principales accesibles desde la barra lateral:

*   **🏠 Dashboard:** Panel de control con métricas clave (total de pacientes, productos, facturación), alertas de stock bajo y previsualización de los últimos registros.
*   **🐶 Mascotas:** CRUD completo de pacientes. Permite registrar datos de la mascota, del dueño y visualizar su perfil completo junto con su historial médico.
*   **🩺 Consultas:** Módulo para registrar visitas clínicas (motivo, diagnóstico, tratamiento y actualización de peso). Todo queda guardado en el historial de la mascota.
*   **📦 Inventario:** Gestión de productos de la tienda y farmacia (Alimentos, Accesorios, Fármacos). Controla precios, stock, caducidad e indica si un fármaco requiere receta médica.
*   **💵 Punto de Venta (POS):** Sistema de caja para procesar ventas. Permite agregar servicios clínicos o productos del inventario. Si se vende un fármaco con receta, exige vincularlo a un paciente y actualiza automáticamente su historial médico.
*   **📊 Facturas:** Historial completo de ventas, cálculo de ticket promedio, ingresos totales y visualización detallada de los tickets/comprobantes de pago.

---

## 🛠️ Tecnologías

*   **Backend & Frontend:** [Python](https://www.python.org/) + [Streamlit](https://streamlit.io/)
*   **Almacenamiento:** Base de datos local basada en archivos `JSON` (ligera y sin dependencias externas).
*   **Estilos (UI):** CSS puro inyectado en Streamlit, con tipografías importadas de Google Fonts (*Fraunces* y *DM Mono*).

---

## 🚀 Instalación y Uso

### 1. Requisitos previos
Asegúrate de tener instalado **Python 3.8 o superior**.

### 2. Clonar o descargar el proyecto
Guarda el código fuente en un archivo, por ejemplo, `app.py`.

### 3. Instalar las dependencias
El único paquete externo requerido es Streamlit. Puedes instalarlo ejecutando en tu terminal:
```bash
pip install streamlit
```

### 4. Ejecutar la aplicación
Navega hasta la carpeta donde guardaste el archivo `app.py` y ejecuta:
```bash
streamlit run app.py
```
Esto abrirá automáticamente una pestaña en tu navegador web predeterminado (usualmente en `http://localhost:8501`).

---

## 🗄️ Gestión de Datos

El sistema no requiere configurar motores de bases de datos como MySQL o PostgreSQL. 
Toda la información (mascotas, inventario, historial y facturas) se guarda automáticamente en un archivo local llamado:

`datos_veterinaria.json`

*   **Nota:** Si el archivo no existe la primera vez que ejecutas la app, el sistema lo creará automáticamente con una estructura base vacía.
*   Para hacer un **respaldo (backup)** de tu sistema, simplemente copia y guarda este archivo `.json` en un lugar seguro.

---

## 🎨 Sobre el Diseño (UI/UX)
El código incluye un bloque de `<style>` exhaustivo que sobrescribe los componentes nativos de Streamlit:
*   Fondos con texturas sutiles (patrón de ruido en SVG).
*   Tarjetas con sombras dinámicas.
*   Botones estilizados y badges de colores para identificar categorías, especies y alertas.
*   Diseño responsivo y amigable para uso en monitores de escritorio (ideal para la recepción de una clínica).

---

## 📝 Licencia
Este proyecto es de código abierto. Siéntete libre de modificarlo, mejorarlo o adaptarlo a las necesidades específicas de tu clínica veterinaria.
