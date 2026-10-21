from core.script_gen import ScriptGenerator
from core.config_parser import ProfileManager
from core.driver_manager import DriverManager
from gui.main_window import MainWindow

class AppController:
    def __init__(self):
        self.generador = ScriptGenerator()
        self.perfiles = ProfileManager()
        self.drivers = DriverManager()
        self.vista = MainWindow(controller=self)

    def iniciar_creacion(self, config_data):
        self.vista._log("Procesando estructura en el Controlador...")
        
        modo = config_data.get("modo")
        apps = config_data.get("apps")
        nombre_usb = config_data.get("nombre_usb")
        
        try:
            # 1. Generar scripts post-OS
            self.vista._log(f"Generando inyección para {len(apps)} programas en modo {modo}...")
            cmd_path = self.generador.generar_setup_complete(modo, apps)
            self.vista._log(f"[OK] Script de software creado en: {cmd_path}")
            
            # 2. Generar bypass de hardware
            self.vista._log("Inyectando directivas de evasión (TPM 2.0 y RAM)...")
            xml_path = self.generador.generar_autounattend(bypass_tpm=True, bypass_ram=True)
            self.vista._log(f"[OK] Archivo de respuesta creado en: {xml_path}")
            
            # 3. Respaldo de Controladores (AQUÍ ESTÁ LA SIMULACIÓN)
            self.vista._log("Verificando estado de los controladores locales...")
            exito, msj = self.drivers.exportar_drivers("X:\\Drivers")
            if exito:
                self.vista._log(f"[OK] {msj}")
            else:
                self.vista._log(f"[AVISO] {msj}")
            
            self.vista._log(f"Propiedades del volumen validadas. Etiqueta asignada: {nombre_usb}")
            self.vista._log("=== PREPARACIÓN LÓGICA FINALIZADA ===")
            
        except Exception as e:
            self.vista._log(f"[ERROR CRÍTICO] Fallo en la generación: {e}")

    def guardar_receta(self, config_data):
        self.vista._log("Serializando perfil de despliegue...")
        exito, resultado = self.perfiles.guardar_receta(config_data)
        
        if exito:
            self.vista._log(f"[OK] Receta JSON guardada exitosamente en: {resultado}")
        else:
            self.vista._log(f"[ERROR] No se pudo guardar el archivo: {resultado}")

    def arrancar(self):
        self.vista.mainloop()