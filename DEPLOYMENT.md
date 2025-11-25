# 🚀 Guía de Despliegue en Streamlit Cloud

## Opción 1: Desplegar desde este repositorio

### Pasos:

1. **Fork el repositorio** a tu cuenta de GitHub
   - Ve a: https://github.com/isaac24012000-oss/GENERADOR-LIQUIDACIONES
   - Haz clic en "Fork" (esquina superior derecha)

2. **Ve a Streamlit Cloud**
   - Dirígete a: https://streamlit.io/cloud
   - Inicia sesión con tu cuenta de GitHub

3. **Crea una nueva app**
   - Haz clic en "New app"
   - Selecciona tu repositorio forkeado
   - Rama: `main`
   - Archivo: `streamlit-deploy/app.py`
   - Haz clic en "Deploy"

4. **¡Listo!**
   - Tu app estará en línea en pocos minutos
   - Streamlit te proporcionará una URL pública

## Opción 2: Crear nuevo repositorio

Si prefieres crear tu propio repositorio:

1. **Crea un nuevo repositorio en GitHub**

2. **Clona este proyecto a tu máquina**
   ```bash
   git clone https://github.com/isaac24012000-oss/GENERADOR-LIQUIDACIONES.git
   cd GENERADOR-LIQUIDACIONES
   ```

3. **Copia la carpeta `streamlit-deploy`**
   ```bash
   cp -r streamlit-deploy ..
   cd streamlit-deploy
   ```

4. **Configura tu nuevo repositorio**
   ```bash
   git init
   git remote add origin https://github.com/tu-usuario/liquidaciones-deploy.git
   git add .
   git commit -m "Initial commit: Sistema de Liquidaciones WorldTel"
   git push -u origin main
   ```

5. **Despliega en Streamlit Cloud**
   - Sigue los mismos pasos que en la Opción 1

## ⚙️ Configuración en Streamlit Cloud

Una vez que hayas iniciado el despliegue:

### Variables de entorno (si es necesario)

En la sección **Secrets** de tu app en Streamlit Cloud:

1. Haz clic en **"Advanced settings"**
2. Ve a **"Secrets"**
3. Agrega variables en formato TOML si las necesitas

### Ejemplo:
```toml
database_url = "tu_url_aqui"
api_key = "tu_clave_aqui"
```

## 📊 Requisitos del servidor

Streamlit Cloud requiere:
- **RAM**: Mínimo 1GB (recomendado 2GB)
- **CPU**: 1-2 cores
- **Almacenamiento**: 500MB - 1GB

Esta aplicación debería funcionar sin problemas en el plan gratuito de Streamlit Cloud.

## 🔄 Actualizar tu app

Después de cualquier cambio en tu repositorio:

1. Sube los cambios a GitHub
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push
   ```

2. Streamlit Cloud se actualizará automáticamente

## ⏱️ Tiempos de inicio

- **Primera carga**: ~10-15 segundos (genera caché)
- **Cargas posteriores**: <100ms
- **Timeout**: Si tarda >60 segundos, Streamlit puede cancelarlo

## 🔒 Seguridad

**IMPORTANTE**: No commitees credenciales o información sensible

1. Nunca subas archivos con información privada
2. Usa Secrets en lugar de archivos `.env`
3. Revisa tu `.gitignore` antes de hacer push

## 🐛 Solución de problemas

### "Deploy failed"
- Verifica que `requirements.txt` tenga todas las dependencias
- Comprueba que el archivo principal se llama `app.py`
- Revisa los logs en Streamlit Cloud

### "Module not found"
- Asegúrate que `requirements.txt` incluya todas las librerías
- Reinstala con: `pip install -r requirements.txt`

### Aplicación muy lenta
- Aumenta memoria en Advanced Settings
- Optimiza el caché
- Considera archivos más pequeños de datos

## 📞 Soporte

- Documentación: https://docs.streamlit.io
- Community: https://discuss.streamlit.io
- Issues: Reporta en el repositorio GitHub

---

**Versión**: 2.0  
**Última actualización**: 25 de noviembre de 2025
