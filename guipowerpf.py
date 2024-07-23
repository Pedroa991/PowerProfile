"""GUI para do APP PowerProfile"""

import webbrowser
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo
import customtkinter as ctk
import powerpf


MAIN_WINDOW_TITLE = f"Study Tools - PowerProfile {powerpf.SCRIPT_VERSION}"
MIN_SIZE_WINDOW_WIDTH = 370
MIN_SIZE_WINDOW_HEIGHT = 150


class ButtomFuntions:
    """Classe para funções dos botões"""

    def __init__(self) -> None:
        self.path_db = ""
        self.path_engref = ""

    def getbd(self):
        """Pega o caminho do banco de dados"""
        dirname = filedialog.askdirectory(title="Selecione a pasta do BD do Cliente")
        if dirname:
            print("Pasta de Destino: " + str(dirname) + "\n")
            self.path_db = dirname

    def getengref(self):
        """Pega caminho do arquivo de referências de performance dos motores"""
        pathfile = filedialog.askopenfilename(
            title="Selecione o arquivo de Referência do Motor",
            filetypes=[("Excel file", "*.xlsx")],
        )
        if pathfile:
            print("Arquivo de Referência do Motor:" + str(pathfile) + "\n")
            self.path_engref = pathfile

    def run_powerpf(self) -> None:
        """Executa a rotina do PowerProfile"""
        if not self.path_db:
            tx_error = "Erro: Caminho do BD Cliente inválido!"
            print(tx_error)
            showerror("Erro", tx_error)
            return

        if not self.path_engref:
            tx_error = "Erro: Caminho do arquivo de referência de motor inválido!"
            print(tx_error)
            showerror("Erro", tx_error)
            return

        powerpf.main(self.path_db, self.path_engref)
        showinfo("Sucesso!", "Resultados obitidos com sucesso!")

    def run_interpolation(self):
        """Interpola dados do TMI"""
        if not self.path_engref:
            tx_error = "Erro: Caminho do arquivo de referência de motor inválido!"
            print(tx_error)
            showerror("Erro", tx_error)
            return

        powerpf.interpolation_eng_ref(self.path_engref)
        showinfo("Sucesso!", "Resultados obitidos com sucesso!")


def put_gadgets_main(app: ctk.CTk) -> None:
    """Coloca gadgets da janela principal"""

    runbt = ButtomFuntions()

    tx_title = "Study Tools - PowerProfile"
    lb_title = ctk.CTkLabel(app, text=tx_title)
    lb_title.pack(side="top")

    bt_engref = ctk.CTkButton(
        master=app, text="Referência Motor ", command=runbt.getengref
    )
    bt_db = ctk.CTkButton(master=app, text="BD Cliente", command=runbt.getbd)
    bt_run = ctk.CTkButton(
        master=app, text="Executar", fg_color="Red", command=runbt.run_powerpf
    )
    bt_interpol = ctk.CTkButton(
        master=app,
        text="Somente Interpolar",
        fg_color="Red",
        command=runbt.run_interpolation,
    )

    bt_engref.place(relx=0.30, rely=0.30, anchor=ctk.CENTER)
    bt_db.place(relx=0.70, rely=0.30, anchor=ctk.CENTER)
    bt_run.place(relx=0.30, rely=0.6, anchor=ctk.CENTER)
    bt_interpol.place(relx=0.70, rely=0.6, anchor=ctk.CENTER)

    text_about = powerpf.SCRIPT_VERSION + " - By Pedro Venancio - Sobre / Ajuda"
    lb_about = ctk.CTkLabel(app, text=text_about, text_color="blue")
    lb_about.pack(side="bottom")
    lb_about.bind(
        "<Button-1>",
        lambda x: webbrowser.open_new("https://www.linkedin.com/in/pedrobvenancio/"),
    )


def main() -> None:
    """Cria a janela principal"""

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.minsize(width=MIN_SIZE_WINDOW_WIDTH, height=MIN_SIZE_WINDOW_HEIGHT)
    app.title(MAIN_WINDOW_TITLE)
    app.geometry(f"{MIN_SIZE_WINDOW_WIDTH} X {MIN_SIZE_WINDOW_HEIGHT}")
    app.resizable(False, False)

    put_gadgets_main(app)

    app.mainloop()


if __name__ == "__main__":

    print(
        "Bem-vindo ao PowerProfile! \n",
        "Versão: ",
        powerpf.SCRIPT_VERSION,
        "\n",
    )

    main()
