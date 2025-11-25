# SISTEMA DE GENERACIÓN DE LIQUIDACIONES - WORLDTEL

## 📋 Descripción General

Este sistema permite generar liquidaciones automáticas basadas en datos de deuda de empresas organizadas por **CAMPAÑAS**. Los datos se extraen de 4 archivos de detalle (DetalleEmpresas_Camp_70X.xlsx), cada uno representando una campaña diferente.

### Campañas Disponibles:
- **PRESUNTA** (Camp_717.xlsx) - 3,000 casos
- **DEUDA REAL TOTAL** (Camp_714.xlsx) - 793 casos
- **REDIRECCIONAMIENTO** (Camp_713.xlsx) - 4,000 casos
- **PREJUDICIAL FLUJO** (Camp_709.xlsx) - 1,344 casos
- **Total: 9,137 casos únicos (RUC x Campaña)**

### Características:
- ✅ Búsqueda rápida de RUCs con identifi cación de campañas
- ✅ Generación automática de liquidaciones en formato Excel por campaña
- ✅ Base de datos consolidada de 8,928 RUCs únicos
- ✅ Interfaz interactiva fácil de usar
- ✅ Exportación de reportes por campaña
- ✅ Cálculo automático de totales, intereses y gastos administrativos
- ✅ Identificación clara de campaña en cada liquidación

---

## 🚀 Guía Rápida

### OPCIÓN 1: Usar la Interfaz Interactiva (RECOMENDADO)

1. **Abra una terminal** en la carpeta `GENERACION DE LIQUIDACIONES`
2. **Ejecute el comando:**
   ```
   python interfaz_liquidaciones.py
   ```
3. **Seleccione una opción del menú:**
   - **Opción 1**: Buscar un RUC específico y ver sus campañas
   - **Opción 2**: Generar una liquidación individual (seleccionar RUC y campaña)
   - **Opción 3**: Generar liquidaciones múltiples (con opciones por campaña)
   - **Opción 4**: Listar todos los RUCs disponibles
   - **Opción 5**: Exportar base de datos de RUCs a Excel
   - **Opción 6**: Salir

### OPCIÓN 2: Usar el Generador Rápido

**Para generar una liquidación de forma instantánea:**

```bash
# Ingresará el RUC y seleccionará campaña interactivamente
python generar_rapido.py

# O especificar RUC directamente
python generar_rapido.py 20212246698

# O especificar RUC y campaña
python generar_rapido.py 20212246698 PRESUNTA
```

### OPCIÓN 3: Usar Python Directamente

```python
from generador_liquidaciones import GeneradorLiquidaciones

# Inicializar generador
gen = GeneradorLiquidaciones(r"C:\ruta\a\la\carpeta")

# Obtener RUCs disponibles
rucs = gen.obtener_rucs()

# Obtener campañas para un RUC específico
campanas = gen.obtener_campanas_ruc(ruc=10076631145)
print(campanas)  # ['PRESUNTA', 'DEUDA REAL TOTAL']

# Generar liquidación para RUC + Campaña
gen.generar_liquidacion(
    ruc=10076631145,
    campana="PRESUNTA",
    razon_social="MI EMPRESA S.A.",
    direccion="Calle Principal 123",
    fecha_pago="2025-11-24"
)

# Generar para todas las campañas de un RUC
gen.generar_liquidacion(ruc=10076631145)  # Genera para PRESUNTA y DEUDA REAL TOTAL
```

---

## 📁 Archivos del Sistema

### Archivos de Entrada (Fuentes de Datos)
- `DetalleEmpresas_Camp_717.xlsx` - Campaña: PRESUNTA (283,592 registros)
- `DetalleEmpresas_Camp_714.xlsx` - Campaña: DEUDA REAL TOTAL (12,347 registros)
- `DetalleEmpresas_Camp_713.xlsx` - Campaña: REDIRECCIONAMIENTO (157,588 registros)
- `DetalleEmpresas_Camp_709.xlsx` - Campaña: PREJUDICIAL FLUJO (7,316 registros)
- `formato.xlsx` - Plantilla de liquidación

### Archivos de Salida (Generados por el Sistema)
- `LIQUIDACIONES_GENERADAS/` - Carpeta con liquidaciones generadas
  - `LIQUIDACION_[RUC]_[CAMPANA]_[FECHA].xlsx` - Liquidación por RUC y Campaña
- `BASE_RUCS_DISPONIBLES.xlsx` - Base de datos de RUCs con información de campañas
- `BUSCADOR_LIQUIDACIONES.xlsx` - Herramienta de búsqueda (si se genera)

### Scripts Python
- `generador_liquidaciones.py` - Motor principal de generación (CORE)
- `interfaz_liquidaciones.py` - Interfaz interactiva (USAR ESTE)
- `generar_rapido.py` - Generador rápido por línea de comandos
- `crear_buscador.py` - Genera el archivo de búsqueda
- `analizar_estructura.py` - Análisis de estructura de datos

---

## 📊 Estructura de la Liquidación Generada

Cada liquidación contiene:

1. **Encabezado** (Filas 1-16)
   - Información de la empresa emisora (GI CORONADO)
   - Razón Social del deudor
   - RUC del deudor
   - Dirección
   - Fecha de pago
   - **Campaña** ← Nueva línea que identifica la campaña

2. **Tabla de Detalles** (Filas 18-71)
   - RUC del afiliado
   - Período de la obligación
   - Monto del fondo
   - Monto de administradora
   - Factor de interés
   - Interés del fondo
   - Interés de administradora
   - Total del fondo
   - Total de administradora
   - Total general
   - Nombre del afiliado

3. **Resumen de Totales** (Filas 72-78)
   - Deuda previsional con intereses
   - Gastos de cobranza (15% del total)
   - IGV sobre gastos (18%)
   - Total de gastos administrativos
   - TOTAL DEUDA

---

## 🔍 Búsqueda de RUCs con Campañas

### Ejemplo 1: RUC en una sola campaña
```
Ingrese RUC: 10002335935
Se encontró: 10002335935.0
Campañas: PREJUDICIAL FLUJO
```

### Ejemplo 2: RUC en múltiples campañas
```
Ingrese RUC: 10076631145
Se encontró: 10076631145.0
Campañas disponibles:
  1. PRESUNTA
  2. DEUDA REAL TOTAL

Seleccione la campaña:
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Generar una Liquidación para RUC Específico y Campaña

```bash
python interfaz_liquidaciones.py
# Selecciona: 2 (Generar liquidación por RUC)
# Ingresa RUC: 20212246698
# Selecciona campaña: PRESUNTA
# Presiona Enter en dirección y fecha para usar valores por defecto
```

Resultado: `LIQUIDACION_20212246698_PRESUNTA_20251124.xlsx`

### Ejemplo 2: Generar para todos los RUCs de una Campaña

```bash
python interfaz_liquidaciones.py
# Selecciona: 3 (Generar liquidaciones múltiples)
# Selecciona: 3 (Generar para una campaña específica)
# Selecciona campaña: PREJUDICIAL FLUJO
# Confirma generación de 1,344 liquidaciones
```

### Ejemplo 3: Exportar Base de RUCs por Campaña

```bash
python interfaz_liquidaciones.py
# Selecciona: 5 (Exportar base de datos)
```

Resultado: `BASE_RUCS_DISPONIBLES.xlsx` con columnas:
- RUC
- CAMPAÑA
- RAZÓN SOCIAL
- REGISTROS
- TOTAL DEUDA

---

## 📈 Estadísticas de la Base de Datos

| Métrica | Valor |
|---------|-------|
| Total de RUCs únicos | 8,928 |
| Total de registros | 460,843 |
| Total de casos (RUC x Campaña) | 9,137 |
| Período cubierto | 2008-2021 |

### Por Campaña:
| Campaña | RUCs | Casos | Registros |
|---------|------|-------|-----------|
| PRESUNTA | ~3,000 | 3,000 | 283,592 |
| DEUDA REAL TOTAL | ~793 | 793 | 12,347 |
| REDIRECCIONAMIENTO | ~4,000 | 4,000 | 157,588 |
| PREJUDICIAL FLUJO | ~1,344 | 1,344 | 7,316 |

---

## ⚙️ Configuración y Requisitos

### Requisitos Python
- Python 3.7+
- openpyxl 3.0+
- pandas 1.0+

### Instalación de Dependencias
```bash
pip install openpyxl pandas
```

### Carpeta de Trabajo
Todos los archivos deben estar en:
```
C:\Users\USUARIO\Desktop\REPORTE MENSUAL WORLDTEL\GENERACION DE LIQUIDACIONES\
```

---

## 🔧 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'openpyxl'"
**Solución:**
```bash
pip install openpyxl
```

### Problema: "RUC no encontrado"
**Verificar:**
- El RUC existe en los archivos de detalle
- No hay espacios en blanco al ingresar el RUC
- El RUC es válido (números solamente)

### Problema: "Campaña no encontrada"
**Verificar:**
- La campaña seleccionada existe para ese RUC
- Algunos RUCs solo aparecen en una o dos campañas

### Problema: "PermissionError" al guardar
**Verificar:**
- La carpeta `LIQUIDACIONES_GENERADAS` no está abierta en Excel
- Tiene permisos de escritura en la carpeta

---

## 📝 Notas Importantes

1. ⚠️ **RUCs Duplicados**: Un mismo RUC puede aparecer en múltiples campañas
   - Ejemplo: RUC 10076631145 aparece en PRESUNTA y DEUDA REAL TOTAL
   - Cada campaña genera una liquidación independiente

2. ⚠️ **Identificación de Campaña**: El nombre del archivo incluye la campaña
   - Formato: `LIQUIDACION_[RUC]_[CAMPANA_ABREV]_[FECHA].xlsx`
   - Ejemplo: `LIQUIDACION_10076631145_PRESUNTA_20251124.xlsx`

3. ⚠️ **Respaldo**: Asegúrese de hacer respaldo del archivo `formato.xlsx`

4. ⚠️ **Cálculos automáticos**: 
   - Gastos de cobranza: 15% de la deuda
   - IGV: 18% sobre gastos
   - Todos basados en datos de la campaña seleccionada

5. ⚠️ **Período de pago**: Por defecto usa la fecha actual

---

## ✅ Checklist de Uso

- [ ] Verificar que todos los 4 archivos de detalle estén en la carpeta
- [ ] Verificar que el archivo formato.xlsx esté presente
- [ ] Tener Python 3.7+ instalado
- [ ] Instalar dependencias: `pip install openpyxl pandas`
- [ ] Ejecutar: `python interfaz_liquidaciones.py`
- [ ] Seleccionar opción deseada
- [ ] Seleccionar RUC y Campaña
- [ ] Revisar liquidaciones en `LIQUIDACIONES_GENERADAS/`
- [ ] Guardar o enviar liquidaciones según sea necesario

---

## 🎯 Próximos Pasos

1. **Generar** una liquidación de prueba
2. **Verificar** que incluya información de la campaña
3. **Exportar** la base de RUCs por campaña si la necesita offline
4. **Automatizar** generación periódica por campaña si es necesario

---

## 📞 Información de Contacto

**Sistema de Liquidaciones WorldTel - Versión 2.0 (Multi-Campaña)**
- Versión: 2.0
- Última actualización: 24 de noviembre de 2025
- Desarrollado para: WORLDTEL

¡El sistema está listo para usar! 🚀
