import tkinter as tk
from model.modelo import Modelo
from view.main_view import MainView
from controller.controller import Controller
from model.dbConnetion import initialize_database

def main():
    initialize_database()
    root = tk.Tk()
    modelo = Modelo()
    vista_principal = MainView(root)
    controller = Controller(root, modelo, vista_principal)
    vista_principal.set_controller(controller)
    vista_principal.mostrar()
    root.mainloop()

if __name__ == "__main__":
    main()