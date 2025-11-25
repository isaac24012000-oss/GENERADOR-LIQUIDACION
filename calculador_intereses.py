"""
CALCULADOR DE INTERESES Y MORA
===============================

Módulo para calcular deuda actual incluida mora/intereses.
Utiliza el archivo factor_interes.xlsx para aplicar multiplicadores.

Estructura:
- factor_interes.xlsx contiene: día, período, factor_interes
- DetalleEmpresas contiene OPERACION con formato: RUC_PERIODO (ej: 20123456789_201808)
- Se multiplica: deuda_base * factor_interes = deuda_con_mora
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, Optional, Tuple
import time


class CalculadorIntereses:
    """Calcula la deuda actual incluida mora/intereses por período."""
    
    def __init__(self, ruta_base: str = None):
        """
        Inicializar calculador de intereses.
        
        Args:
            ruta_base: Ruta base del proyecto (para ubicar factor_interes.xlsx)
        """
        if ruta_base is None:
            ruta_base = os.getcwd()
        
        self.ruta_base = ruta_base
        self.df_factor = None
        self.cache_factores = {}  # Cache para búsquedas rápidas
        self.dia_actual = None
        
        self._cargar_factores()
    
    def _cargar_factores(self):
        """Cargar tabla de factores de interés."""
        ruta_factor = os.path.join(self.ruta_base, 'factor_interes.xlsx')
        
        if not os.path.exists(ruta_factor):
            print(f"[ADVERTENCIA] Archivo de factores no encontrado: {ruta_factor}")
            print("  Las deudas se mostrarán sin intereses/mora")
            self.df_factor = None
            return
        
        try:
            print(f"[CARGANDO] Factores de interes desde: factor_interes.xlsx")
            self.df_factor = pd.read_excel(ruta_factor)
            
            # Convertir periodo a formato numerico
            self.df_factor['periodo'] = self.df_factor['periodo'].astype(int)
            self.df_factor['dia'] = self.df_factor['dia'].astype(int)
            
            # Crear indice para busqueda rapida: (dia, periodo) -> factor
            for _, row in self.df_factor.iterrows():
                key = (row['dia'], row['periodo'])
                self.cache_factores[key] = row['factor_interes']
            
            print(f"  OK {len(self.df_factor)} registros de factores cargados")
            print(f"  OK Dias disponibles: {sorted(self.df_factor['dia'].unique())}")
            print(f"  OK Periodos: {self.df_factor['periodo'].min()} a {self.df_factor['periodo'].max()}")
            
        except Exception as e:
            print(f"[ERROR] No se pudo cargar factores: {e}")
            self.df_factor = None
    
    def establecer_dia(self, dia: int = None):
        """
        Establecer el día actual para buscar factores.
        
        Args:
            dia: Día del mes (1-31). Si es None, usa el día de hoy.
        """
        if dia is None:
            dia = datetime.now().day
        
        self.dia_actual = dia
        print(f"[OK] Día de cálculo establecido: {dia}")
    
    def obtener_periodo_de_operacion(self, operacion: str) -> Optional[int]:
        """
        Extraer período de la columna OPERACION.
        
        Formato esperado: RUC_YYYYMM (ej: 20123456789_201808)
        
        Args:
            operacion: String con formato RUC_YYYYMM
            
        Returns:
            Período en formato YYYYMM (ej: 201808) o None si no se puede extraer
        """
        if not isinstance(operacion, str):
            return None
        
        try:
            # Formato esperado: RUC_PERIODO
            partes = str(operacion).split('_')
            if len(partes) >= 2:
                periodo_str = partes[-1]  # Tomar última parte
                periodo = int(periodo_str)
                
                # Validar que sea un período válido (YYYYMM)
                if 190000 <= periodo <= 209912:  # 1900 a 2099, mes 01 a 12
                    return periodo
        except (ValueError, IndexError):
            pass
        
        return None
    
    def obtener_factor_interes(self, dia: int, periodo: int) -> Optional[float]:
        """
        Obtener el factor de interés para un día y período.
        
        Args:
            dia: Día del mes (1-31)
            periodo: Período en formato YYYYMM
            
        Returns:
            Factor de interés (multiplicador) o None si no existe
        """
        if self.df_factor is None:
            return None
        
        # Buscar en cache primero (muy rápido)
        key = (dia, periodo)
        if key in self.cache_factores:
            return self.cache_factores[key]
        
        # Búsqueda fallida = período no tiene mora aplicable
        return None
    
    def calcular_deuda_con_mora(self, deuda_base: float, operacion: str, 
                               dia: int = None) -> Tuple[float, float, Optional[int]]:
        """
        Calcular deuda actual incluyendo mora/intereses.
        
        Args:
            deuda_base: Deuda nominal sin intereses
            operacion: String con formato RUC_YYYYMM
            dia: Día del mes. Si es None, usa el día establecido o el de hoy.
            
        Returns:
            Tupla: (deuda_con_mora, mora, período)
            - deuda_con_mora: Deuda base * factor (o deuda_base si no hay factor)
            - mora: Monto adicional por intereses (deuda_con_mora - deuda_base)
            - período: Período extraído de OPERACION
        """
        # Usar día establecido o el actual
        if dia is None:
            dia = self.dia_actual or datetime.now().day
        
        # Extraer período de OPERACION
        periodo = self.obtener_periodo_de_operacion(operacion)
        
        if periodo is None:
            # No se pudo extraer período válido
            return (deuda_base, 0, None)
        
        # Obtener factor de interés
        factor = self.obtener_factor_interes(dia, periodo)
        
        if factor is None:
            # No hay factor para este período (fuera de rango o periodo nuevo)
            return (deuda_base, 0, periodo)
        
        # Calcular deuda con mora
        deuda_con_mora = deuda_base * factor
        mora = deuda_con_mora - deuda_base
        
        return (round(deuda_con_mora, 2), round(mora, 2), periodo)
    
    def enriquecer_detalle_con_mora(self, df: pd.DataFrame, 
                                   columna_deuda: str = 'TOTA_FONDO',
                                   columna_operacion: str = 'OPERACION',
                                   dia: int = None) -> pd.DataFrame:
        """
        Agregar columnas de mora y deuda con mora a un DataFrame de detalles.
        
        Args:
            df: DataFrame con detalles (debe tener columna de deuda y OPERACION)
            columna_deuda: Nombre de la columna con deuda base
            columna_operacion: Nombre de la columna con OPERACION
            dia: Día del mes para cálculo
            
        Returns:
            DataFrame con columnas adicionales:
            - PERIODO: Período extraído de OPERACION
            - FACTOR_INTERES: Factor aplicado (si existe)
            - MORA: Monto adicional por intereses
            - DEUDA_CON_MORA: Deuda base * factor
        """
        print(f"\n[CALCULANDO] Mora e intereses para {len(df)} registros...")
        inicio = time.time()
        
        # Usar día establecido o el actual
        if dia is None:
            dia = self.dia_actual or datetime.now().day
        
        df_result = df.copy()
        df_result['PERIODO'] = None
        df_result['FACTOR_INTERES'] = None
        df_result['MORA'] = 0.0
        df_result['DEUDA_CON_MORA'] = df_result[columna_deuda]
        
        # Procesar cada fila
        for idx, row in df_result.iterrows():
            deuda_base = row[columna_deuda]
            operacion = row[columna_operacion]
            
            deuda_mora, mora, periodo = self.calcular_deuda_con_mora(
                deuda_base, operacion, dia
            )
            
            df_result.at[idx, 'PERIODO'] = periodo
            df_result.at[idx, 'MORA'] = mora
            df_result.at[idx, 'DEUDA_CON_MORA'] = deuda_mora
            
            # Obtener factor para mostrar
            if periodo:
                factor = self.obtener_factor_interes(dia, periodo)
                if factor:
                    df_result.at[idx, 'FACTOR_INTERES'] = round(factor, 4)
        
        tiempo = time.time() - inicio
        print(f"  ✓ Cálculo completado en {tiempo:.2f} segundos")
        print(f"  ✓ Deuda total base: ${df_result[columna_deuda].sum():,.2f}")
        print(f"  ✓ Mora total: ${df_result['MORA'].sum():,.2f}")
        print(f"  ✓ Deuda con mora: ${df_result['DEUDA_CON_MORA'].sum():,.2f}")
        
        return df_result
    
    def estadisticas(self) -> Dict:
        """Obtener estadísticas del calculador."""
        if self.df_factor is None:
            return {
                'estado': 'sin_factores',
                'mensaje': 'Archivo de factores no encontrado'
            }
        
        return {
            'total_registros': len(self.df_factor),
            'dias_disponibles': sorted(self.df_factor['dia'].unique().tolist()),
            'periodo_minimo': int(self.df_factor['periodo'].min()),
            'periodo_maximo': int(self.df_factor['periodo'].max()),
            'factor_minimo': float(self.df_factor['factor_interes'].min()),
            'factor_maximo': float(self.df_factor['factor_interes'].max()),
            'cache_size': len(self.cache_factores)
        }


# Prueba rápida si se ejecuta directamente
if __name__ == "__main__":
    print("\n" + "="*80)
    print("PRUEBA DEL CALCULADOR DE INTERESES")
    print("="*80 + "\n")
    
    # Inicializar
    calc = CalculadorIntereses()
    calc.establecer_dia(24)  # Usando día 24 (hoy)
    
    # Pruebas
    print("\n[PRUEBA 1] Extraer período de OPERACION")
    operaciones = [
        "10060998642_201805",
        "20123456789_202509",
        "12345678901_199308"
    ]
    for op in operaciones:
        periodo = calc.obtener_periodo_de_operacion(op)
        print(f"  {op} -> Período: {periodo}")
    
    print("\n[PRUEBA 2] Obtener factor de interés")
    print(f"  Día: 24, Período 201805 -> Factor: {calc.obtener_factor_interes(24, 201805)}")
    print(f"  Día: 24, Período 199308 -> Factor: {calc.obtener_factor_interes(24, 199308)}")
    print(f"  Día: 24, Período 202599 -> Factor: {calc.obtener_factor_interes(24, 202599)} (no existe)")
    
    print("\n[PRUEBA 3] Calcular deuda con mora")
    deuda_con_mora, mora, periodo = calc.calcular_deuda_con_mora(1000.0, "10060998642_201805")
    print(f"  Deuda base: $1000.00")
    print(f"  Factor: {1000 * 1.0 if mora == 0 else 'aplicado'}")
    print(f"  Mora: ${mora:,.2f}")
    print(f"  Deuda con mora: ${deuda_con_mora:,.2f}")
    
    print("\n[ESTADÍSTICAS]")
    stats = calc.estadisticas()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
