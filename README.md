# 📄 Sistema de Liquidaciones WorldTel

Aplicación web Streamlit para generación rápida de liquidaciones en PDF.

## 🚀 Características

- **Búsqueda rápida de RUCs**: Encuentra clientes al instante
- **Generación instantánea de PDFs**: Descarga liquidaciones formateadas
- **Multi-campaña**: Soporta múltiples campañas de cobranza
- **Tabla de detalles**: Visualiza todos los registros y totales
- **Interfaz intuitiva**: Diseño limpio y fácil de usar

## 📋 Requisitos

- Python 3.8+
- pandas >= 2.0.0
- streamlit >= 1.28.0
- reportlab >= 4.0.0
- openpyxl >= 3.0.0

## 📦 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/liquidaciones-worldtel.git
cd liquidaciones-worldtel
```

### 2. Crear entorno virtual

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación abrirá en tu navegador en `http://localhost:8501`

## ☁️ Desplegar en Streamlit Cloud

### 1. Crear cuenta en Streamlit Cloud

- Ve a [streamlit.io/cloud](https://streamlit.io/cloud)
- Crea una cuenta o inicia sesión con GitHub

### 2. Conectar tu repositorio GitHub

- Fork este repositorio en tu cuenta de GitHub
- En Streamlit Cloud, selecciona "New app"
- Elige el repositorio y la rama (main)
- Selecciona `app.py` como punto de entrada

### 3. Configurar secretos (si es necesario)

- En la sección "Advanced settings" de tu app en Streamlit Cloud
- Agrega las variables de entorno necesarias

## 📁 Estructura de archivos

```
streamlit-deploy/
├── app.py                      # Aplicación principal
├── generador_cache.py          # Sistema de caché
├── generador_pdf.py            # Generador de PDFs
├── generador_liquidaciones.py  # Lógica principal
├── calculador_intereses.py     # Cálculos de intereses
├── logo_coronado.png           # Logo
├── requirements.txt            # Dependencias
├── factor_interes.xlsx         # Tabla de factores
├── DetalleEmpresas_Camp_*.xlsx # Datos de empresas
└── .streamlit/
    └── config.toml             # Configuración Streamlit
```

## 🔧 Uso

1. **Ingrese un RUC**: Busque por número de RUC
2. **Seleccione campaña**: Elija entre las campañas disponibles
3. **Genere PDF**: Haga clic en "Generar PDF" para descargar
4. **Ver detalles**: Use "Ver Datos" para visualizar tabla completa

## 💡 Funciones principales

- **Cálculo automático de mora**: Calcula intereses según fecha
- **Totales por línea**: Suma automática de todas las columnas
- **PDF profesional**: Formato de liquidación lista para enviar
- **Caché rápido**: Primera carga ~10s, siguiente <100ms

## 🐛 Solución de problemas

### Error: "RUC no encontrado"
- Verifique que el RUC sea correcto
- Asegúrese que exista en la base de datos

### Error: "No se puede generar PDF"
- Verifique que tengas los permisos de escritura
- Comprueba que reportlab esté instalado correctamente

### Lentitud en primera carga
- Es normal, se está generando el caché
- Las cargas posteriores serán <100ms

## 📞 Soporte

Para reportar problemas, abre un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 👤 Autor

**Isaac WorldTel**
- GitHub: [@isaac24012000-oss](https://github.com/isaac24012000-oss)

---

**Versión**: 2.0  
**Actualizado**: 25 de noviembre de 2025
