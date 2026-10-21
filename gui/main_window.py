import customtkinter as ctk
from tkinter import filedialog
import threading
import time
import sys

BG_COLOR = "#0B0B0F"
PANEL_BG = "#16161E"
ACCENT_COLOR = "#6366F1"
TEXT_MAIN = "#F8F9FA"
TEXT_MUTED = "#8B949E"
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_MAIN = ("Helvetica", 13)

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Catalyst USB - Consola de Despliegue")
        self.geometry("900x850")
        self.configure(fg_color=BG_COLOR)
        
        # Variables de estado
        self.iso_path_var = ctk.StringVar()
        self.modo_var = ctk.StringVar(value="Online")
        self.esquema_var = ctk.StringVar(value="GPT")
        self.target_var = ctk.StringVar(value="UEFI (no CSM)")
        self.formato_var = ctk.StringVar(value="NTFS")
        self.nombre_usb_var = ctk.StringVar(value="CATALYST_OS")
        self.apps_vars = {}
        
        self._construir_ui()

    def _construir_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # 1. Panel de ISO y Configuración de Unidad
        frame_top = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=12)
        frame_top.grid(row=0, column=0, pady=(20, 10), padx=30, sticky="ew")
        
        ctk.CTkLabel(frame_top, text="1. Origen y Propiedades de la Unidad", font=FONT_MAIN, text_color=TEXT_MUTED).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 5))
        
        ctk.CTkEntry(frame_top, textvariable=self.iso_path_var, width=550, state="disabled", fg_color=BG_COLOR).grid(row=1, column=0, padx=(20, 10), pady=10)
        ctk.CTkButton(frame_top, text="Explorar ISO", font=FONT_MAIN, fg_color="#2D2D3B", command=self._pedir_iso).grid(row=1, column=1, padx=(0, 20))

        # Selectores de formato y partición
        opciones_frame = ctk.CTkFrame(frame_top, fg_color="transparent")
        opciones_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        
        ctk.CTkComboBox(opciones_frame, variable=self.esquema_var, values=["GPT", "MBR"], width=100).pack(side="left", padx=(0, 10))
        ctk.CTkComboBox(opciones_frame, variable=self.target_var, values=["UEFI (no CSM)", "BIOS o UEFI"], width=150).pack(side="left", padx=(0, 10))
        ctk.CTkComboBox(opciones_frame, variable=self.formato_var, values=["NTFS", "FAT32", "exFAT"], width=100).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(opciones_frame, text="Etiqueta:", font=FONT_MAIN, text_color=TEXT_MAIN).pack(side="left", padx=(10, 5))
        ctk.CTkEntry(opciones_frame, textvariable=self.nombre_usb_var, width=150, fg_color=BG_COLOR).pack(side="left")

        # 2. Panel de Software
        frame_apps = ctk.CTkFrame(self, fg_color=PANEL_BG, corner_radius=12)
        frame_apps.grid(row=1, column=0, pady=10, padx=30, sticky="ew")
        
        ctk.CTkLabel(frame_apps, text="2. Carga Útil y Bypass", font=FONT_MAIN, text_color=TEXT_MUTED).pack(anchor="w", padx=20, pady=(15, 5))
        
        grid_frame = ctk.CTkFrame(frame_apps, fg_color="transparent")
        grid_frame.pack(pady=5, padx=20, fill="x")

        apps_lista = ["Google Chrome", "Visual Studio Code", "Spotify", "Steam"]
        for i, app in enumerate(apps_lista):
            var = ctk.BooleanVar()
            self.apps_vars[app] = var
            chk = ctk.CTkCheckBox(
                grid_frame, 
                text=app, 
                variable=var, 
                fg_color=ACCENT_COLOR,
                text_color=TEXT_MAIN,  # Fuerza el color blanco/plata
                font=FONT_MAIN         # Aplica la tipografía correcta
            )
            chk.grid(row=i//2, column=i%2, padx=(0, 40), pady=10, sticky="w")
            
        # 3. Consola de Logs en Tiempo Real
        self.terminal = ctk.CTkTextbox(self, height=150, fg_color="#000000", text_color="#00FF00", font=("Consolas", 12))
        self.terminal.grid(row=2, column=0, pady=10, padx=30, sticky="ew")
        self.terminal.insert("0.0", "CATALYST_OS v0.1 // SISTEMA LISTO...\n")
        self.terminal.configure(state="disabled")

        # Botones Principales
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(10, 20), padx=30, sticky="ew")
        
        ctk.CTkButton(btn_frame, text="GUARDAR RECETA", fg_color="#2D2D3B", command=self._guardar_perfil).pack(side="left", padx=(0, 10))
        self.btn_generar = ctk.CTkButton(btn_frame, text="INICIAR DESPLIEGUE", font=("Helvetica", 14, "bold"), fg_color=ACCENT_COLOR, width=300, command=self._iniciar_animacion)
        self.btn_generar.pack(side="right")

    def _log(self, mensaje):
        """Escribe en la terminal integrada."""
        self.terminal.configure(state="normal")
        self.terminal.insert("end", f"> {mensaje}\n")
        self.terminal.see("end")
        self.terminal.configure(state="disabled")

    def _pedir_iso(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos ISO", "*.iso")])
        if ruta:
            self.iso_path_var.set(ruta)
            self._log(f"ISO Seleccionada: {ruta}")

    def _guardar_perfil(self):
        config_data = {
            "modo": self.modo_var.get(),
            "esquema": self.esquema_var.get(),
            "target": self.target_var.get(),
            "formato": self.formato_var.get(),
            "nombre_usb": self.nombre_usb_var.get(),
            "apps": [app for app, var in self.apps_vars.items() if var.get()]
        }
        self.controller.guardar_receta(config_data)

    def _iniciar_animacion(self):
        self.btn_generar.configure(state="disabled", text="PROCESANDO...", fg_color="#2D2D3B")
        self._log("Iniciando secuencia de despliegue Catalyst...")
        threading.Thread(target=self._tarea_background, daemon=True).start()

    def _tarea_background(self):
        import time
        time.sleep(1.5) # Simulación de carga visual
        
        config_data = {
            "modo": self.modo_var.get(),
            "esquema": self.esquema_var.get(),
            "target": self.target_var.get(),
            "formato": self.formato_var.get(),
            "nombre_usb": self.nombre_usb_var.get(),
            "apps": [app for app, var in self.apps_vars.items() if var.get()]
        }
        
        self.controller.iniciar_creacion(config_data)
        self.after(0, self._restaurar_ui)

    def _restaurar_ui(self):
        self.btn_generar.configure(state="normal", text="INICIAR DESPLIEGUE", fg_color=ACCENT_COLOR)
        self._log("Proceso finalizado. Esperando nuevas órdenes.")