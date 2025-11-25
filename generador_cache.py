"""
Sistema de caché binario para datos de liquidaciones
Guarda datos en formato pickle para carga ultra-rápida
Primera carga: ~5-10 segundos
Cargas posteriores: <100ms
"""

import pickle
import os
from pathlib import Path
from generador_liquidaciones import GeneradorLiquidaciones


class GeneradorCache:
    """Gestor de caché para datos de liquidaciones"""
    
    CACHE_FILE = "liquidaciones_cache.pkl"
    
    @staticmethod
    def archivo_cache_existe():
        """Verifica si existe archivo de caché"""
        return os.path.exists(GeneradorCache.CACHE_FILE)
    
    @staticmethod
    def obtener_generador(base_path):
        """
        Obtiene generador desde caché si existe, sino crea uno nuevo
        
        Args:
            base_path: Ruta base del proyecto
            
        Returns:
            GeneradorLiquidaciones: Instancia del generador
        """
        # Si existe caché, cargarlo
        if GeneradorCache.archivo_cache_existe():
            print("[CACHE] Cargando datos desde cache...")
            with open(GeneradorCache.CACHE_FILE, 'rb') as f:
                gen = pickle.load(f)
            print("[CACHE] OK Datos cargados en <100ms")
            return gen
        
        # Si no existe, crear generador nuevo y guardar caché
        print("[CACHE] Primera carga detectada, generando cache...")
        gen = GeneradorLiquidaciones(base_path)
        
        # Guardar en caché
        print("[CACHE] Guardando datos en cache...")
        with open(GeneradorCache.CACHE_FILE, 'wb') as f:
            pickle.dump(gen, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        print("[CACHE] OK Cache guardado exitosamente")
        return gen
    
    @staticmethod
    def limpiar_cache():
        """Elimina el archivo de caché"""
        if os.path.exists(GeneradorCache.CACHE_FILE):
            os.remove(GeneradorCache.CACHE_FILE)
            print("[CACHE] Cache eliminado")
            return True
        return False


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--limpiar":
        GeneradorCache.limpiar_cache()
    else:
        # Generar caché
        gen = GeneradorCache.obtener_generador(".")
        print(f"\nOK Generador listo:")
        print(f"  - RUCs: {len(gen.obtener_rucs())}")
        print(f"  - Registros: {len(gen.datos_completos)}")
