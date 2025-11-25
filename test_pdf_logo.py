#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from generador_pdf import GeneradorPDF

# Datos de prueba
datos_prueba = pd.DataFrame({
    'CUSSP': ['244681JACET6'],
    'OPERACION': ['200903'],
    'FONDO_NOMINAL': [97.50],
    'COMISION_NOMINAL': [25.55],
    'SEGURO_NOMINAL': [0.00],
    'AFP_NOMINAL': [0.00],
    'TOTA_FONDO': [622.63],
    'DEUDA_CON_MORA': [622.63],
    'MORA': [499.58]
})

# Generar PDF
generador = GeneradorPDF()
pdf_bytes = generador.generar_liquidacion_pdf(
    ruc='20212246698',
    campana='REDIRECCIONAMIENTO',
    razon_social='ASOCIACION DEPORTIVA ALIANZA SULLANA',
    datos_ruc=datos_prueba,
    direccion=''
)

# Guardar
with open('LIQUIDACION_PRUEBA.pdf', 'wb') as f:
    f.write(pdf_bytes)

print('✓ PDF regenerado correctamente')
print('✓ Tamaño del logo ajustado a 1.5 x 0.9 pulgadas')
