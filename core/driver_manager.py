import os
import subprocess
import platform

class DriverManager:
    """Motor de extracción y respaldo de controladores del sistema host."""
    
    def exportar_drivers(self, ruta_destino):
        """Ejecuta DISM para clonar los drivers en la ruta especificada."""
        # Protección para pruebas en entornos no-Windows (como tu Linux Mint)
        if platform.system() != "Windows":
            return False, f"[SIMULACIÓN] Extracción omitida. Requiere entorno Windows para ejecutar DISM hacia: {ruta_destino}"
        
        try:
            os.makedirs(ruta_destino, exist_ok=True)
            
            # Comando nativo de Windows para clonar todos los drivers de terceros
            comando = ["dism", "/online", "/export-driver", f"/destination:{ruta_destino}"]
            
            # creationflags=0x08000000 oculta la ventana negra de CMD al usuario
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True, creationflags=0x08000000)
            
            return True, f"Respaldados exitosamente en {ruta_destino}"
            
        except subprocess.CalledProcessError as e:
            return False, f"Fallo en DISM: {e.stderr}"
        except Exception as e:
            return False, f"Error crítico: {str(e)}"