"""
Generador de liquidaciones en PDF de alta velocidad
Optimizado para uso web con Streamlit
"""

from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os
from PIL import Image as PILImage

class GeneradorPDF:
    """Genera liquidaciones en PDF de forma rápida"""
    
    def __init__(self):
        self.fecha_actual = datetime.now().strftime('%d/%m/%Y')
    
    def generar_liquidacion_pdf(self, ruc, campana, razon_social, datos_ruc, 
                                 direccion="", fecha_pago=None):
        """
        Genera liquidación en PDF
        
        Args:
            ruc: RUC del deudor
            campana: Nombre de la campaña
            razon_social: Razón social
            datos_ruc: DataFrame con datos del RUC
            direccion: Dirección (opcional)
            fecha_pago: Fecha de pago (opcional)
        
        Returns:
            bytes: PDF generado en bytes
        """
        
        if fecha_pago is None:
            fecha_pago = self.fecha_actual
        
        # Crear PDF en memoria con orientación horizontal (landscape)
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                               rightMargin=0.1*inch, leftMargin=0.1*inch,
                               topMargin=0.5*inch, bottomMargin=0.1*inch)
        
        # Contenedor de elementos
        elements = []
        
        # Agregar espacio superior estándar
        elements.append(Spacer(1, 0.25*inch))
        
        # Crear tabla para logo y información en primera fila
        logo_path = os.path.join(os.path.dirname(__file__), 'logo_coronado.png')
        
        # Preparar logo
        logo_img = None
        if os.path.exists(logo_path):
            try:
                # Logo grande: 2.5 x 2.5 pulgadas
                logo_img = Image(logo_path, width=2.5*inch, height=2.5*inch)
            except:
                pass
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        titulo_style = ParagraphStyle(
            'TituloCustom',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=colors.HexColor('#203864'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'HeadingCustom',
            parent=styles['Heading2'],
            fontSize=10,
            textColor=colors.HexColor('#203864'),
            spaceAfter=4,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'NormalCustom',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=2
        )
        
        # Información de la empresa
        # Formatear RUC sin .0
        ruc_formateado = str(int(float(ruc))) if '.' in str(ruc) else str(ruc)
        
        # Obtener CUSSP del primer registro si está disponible
        cussp_display = datos_ruc.iloc[0]['CUSSP'] if len(datos_ruc) > 0 else ruc_formateado
        
        info_data = [
            ["Razón Social:", razon_social],
            ["CUSSP:", cussp_display],
            ["RUC:", ruc_formateado],
            ["Campaña:", campana],
            ["Fecha de pago:", fecha_pago],
        ]
        
        # Agregar dirección solo si tiene contenido
        if direccion and direccion.strip() and direccion != "No especificada":
            info_data.insert(2, ["Dirección:", direccion])
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#203864')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        # Crear tabla con logo e información al costado
        if logo_img:
            header_data = [[logo_img, info_table]]
            header_table = Table(header_data, colWidths=[2.8*inch, 8.4*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('BORDER', (0, 0), (-1, -1), 0, colors.white),
            ]))
            elements.append(header_table)
        
        elements.append(Spacer(1, 0.1*inch))
        
        # TABLA DE DETALLES
        elements.append(Paragraph("DETALLE DE DEUDA", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Preparar datos de la tabla
        table_data = [
            ['CUSSP', 'Afiliado', 'Período', 'Fondo', 'Mora', 'Total Admin.', 'Total Fondo'],
        ]
        
        total_fondo = 0
        total_mora = 0
        total_administradora = 0
        
        for idx, row in datos_ruc.iterrows():
            # Usar DEUDA_CON_MORA si está disponible, sino usar TOTA_FONDO
            deuda_con_mora = row.get('DEUDA_CON_MORA', row['TOTA_FONDO'])
            mora = row.get('MORA', 0)
            
            # Cálculos
            fondo = row['FONDO_NOMINAL']
            admin = row['COMISION_NOMINAL']
            interes_admin = row['SEGURO_NOMINAL'] + row['AFP_NOMINAL']
            total_admin_row = admin + interes_admin
            
            # Saltar si admin es 0
            if total_admin_row == 0:
                continue
            
            # Usar CUSSP completo
            cussp_str = str(row['CUSSP'])
            
            # Obtener AFILIADO (si existe) - mostrar nombre completo
            afiliado_str = str(row.get('AFILIADO', '')) if 'AFILIADO' in row else ''
            
            # Extraer solo YYYYMM del período
            periodo_str = str(row['OPERACION'])[-6:] if len(str(row['OPERACION'])) >= 6 else str(row['OPERACION'])
            
            table_data.append([
                cussp_str,
                afiliado_str,
                periodo_str,
                f"S/. {fondo:.2f}",
                f"S/. {mora:.2f}",
                f"S/. {total_admin_row:.2f}",
                f"S/. {deuda_con_mora:.2f}",
            ])
            
            total_fondo += deuda_con_mora
            total_mora += mora
            total_administradora += total_admin_row
        
        # Agregar fila de TOTAL
        table_data.append([
            'TOTAL',
            '',
            '',
            '',
            f"S/. {total_mora:.2f}",
            f"S/. {total_administradora:.2f}",
            f"S/. {total_fondo:.2f}",
        ])
        
        # Crear tabla con columnas más anchas para landscape - maximizar espacio
        table = Table(table_data, colWidths=[1.2*inch, 2.6*inch, 1.0*inch, 1.05*inch, 1.05*inch, 
                                             1.35*inch, 1.35*inch])
        
        table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Datos - sin grilla, más espacioso
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#4472C4')),
            ('ROWPADDING', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            
            # Fila de totales
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E7E6E6')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('TOPPADDING', (0, -1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, -1), (-1, -1), 10),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#4472C4')),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
        
        # RESUMEN DE TOTALES
        elements.append(Paragraph("RESUMEN DE TOTALES", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Cálculos de gastos
        gastos_cobranza = total_fondo * 0.15
        igv = gastos_cobranza * 0.18
        total_gastos = gastos_cobranza + igv
        total_final = total_fondo + total_gastos
        
        resumen_data = [
            ['Deuda previsional con intereses:', f"S/. {total_fondo:.2f}"],
            ['Gastos de cobranza (15%):', f"S/. {gastos_cobranza:.2f}"],
            ['IGV (18%):', f"S/. {igv:.2f}"],
            ['Total gastos administrativos:', f"S/. {total_gastos:.2f}"],
            ['TOTAL DEUDA:', f"S/. {total_final:.2f}"],
        ]
        
        resumen_table = Table(resumen_data, colWidths=[5.5*inch, 2.5*inch])
        resumen_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            
            # Fila "Deuda previsional con intereses" - amarilla y negrita
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FFC000')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            
            # Fila "Total gastos administrativos" - amarilla y negrita
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#FFC000')),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            
            # Fila final "TOTAL DEUDA" - sin color de fondo, solo negrita normal
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
        ]))
        
        elements.append(resumen_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Construir PDF
        doc.build(elements)
        
        # Obtener bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
