import os

class ScriptGenerator:
    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def generar_setup_complete(self, modo, programas, programas_custom=None):
        """Genera el script batch que Windows ejecutará en el primer inicio."""
        ruta_archivo = os.path.join(self.output_dir, "SetupComplete.cmd")
        
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write("@echo off\n")
            f.write("echo === Iniciando instalacion desatendida ===\n\n")
            
            if modo == "Online":
                f.write(":: Instalacion mediante Winget\n")
                # Diccionario interno de IDs de Winget
                winget_ids = {
                    "Google Chrome": "Google.Chrome",
                    "Visual Studio Code": "Microsoft.VisualStudioCode",
                    "Spotify": "Spotify.Spotify",
                    "Steam": "Valve.Steam"
                }
                
                for prog in programas:
                    app_id = winget_ids.get(prog)
                    if app_id:
                        f.write(f"winget install --id {app_id} -e --accept-package-agreements --accept-source-agreements --silent\n")
            
            elif modo == "Offline":
                f.write(":: Instalacion desde ruta local del USB (X:\\Apps\\)\n")
                for prog in programas:
                    nombre_exe = f"{prog.replace(' ', '')}Setup.exe"
                    f.write(f'start /wait %~dp0Apps\\{nombre_exe} /silent /install\n')

            if programas_custom:
                f.write("\n:: Instaladores personalizados\n")
                for custom in programas_custom:
                    f.write(f'start /wait %~dp0Apps\\Custom\\{custom} /S /quiet\n')
                    
            f.write("\necho === Finalizado ===\n")
            
        return ruta_archivo

    def generar_autounattend(self, nombre_usuario="Lekhriax", bypass_tpm=True, bypass_ram=True):
        """Genera el archivo XML con opciones de bypass personalizables."""
        ruta_xml = os.path.join(self.output_dir, "autounattend.xml")
        
        comandos_bypass = ""
        orden = 1
        
        if bypass_tpm:
            comandos_bypass += f"""
            <RunSynchronousCommand wcm:action="add">
                <Order>{orden}</Order>
                <Path>cmd /c reg add "HKLM\\SYSTEM\\Setup\\LabConfig" /v BypassTPMCheck /t REG_DWORD /d 1 /f</Path>
            </RunSynchronousCommand>
            <RunSynchronousCommand wcm:action="add">
                <Order>{orden+1}</Order>
                <Path>cmd /c reg add "HKLM\\SYSTEM\\Setup\\LabConfig" /v BypassSecureBootCheck /t REG_DWORD /d 1 /f</Path>
            </RunSynchronousCommand>"""
            orden += 2
            
        if bypass_ram:
            comandos_bypass += f"""
            <RunSynchronousCommand wcm:action="add">
                <Order>{orden}</Order>
                <Path>cmd /c reg add "HKLM\\SYSTEM\\Setup\\LabConfig" /v BypassRAMCheck /t REG_DWORD /d 1 /f</Path>
            </RunSynchronousCommand>"""

        plantilla_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<unattend xmlns="urn:schemas-microsoft-com:unattend">
    <settings pass="windowsPE">
        <component name="Microsoft-Windows-Setup" processorArchitecture="amd64" publicKeyToken="31bf3856ad364e35" language="neutral" versionScope="nonSxS">
            <RunSynchronous>{comandos_bypass}
            </RunSynchronous>
            <UserData>
                <AcceptEula>true</AcceptEula>
            </UserData>
        </component>
    </settings>
</unattend>"""

        with open(ruta_xml, "w", encoding="utf-8") as f:
            f.write(plantilla_xml)
            
        return ruta_xml