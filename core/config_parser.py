import json
import os

class ProfileManager:
    def guardar_receta(self, configuracion, ruta_archivo="receta_despliegue.json"):
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(configuracion, f, indent=4)
            return True, ruta_archivo
        except Exception as e:
            return False, str(e)

    def cargar_receta(self, ruta_archivo):
        if not os.path.exists(ruta_archivo):
            return False, "Archivo no encontrado."
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                return True, json.load(f)
        except Exception as e:
            return False, str(e)
