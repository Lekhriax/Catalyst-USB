from controllers.app_controller import AppController

def main():
    print("Iniciando entorno de despliegue MVC...")
    app = AppController()
    app.arrancar()

if __name__ == "__main__":
    main()