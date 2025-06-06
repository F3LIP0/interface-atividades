import tkinter as tk

janela = tk.Tk()
janela.title("Layout com Pack")
janela.geometry("400x300")


# Botões empacotados verticalmente
tk.Button(janela, text="Botão 1", width=15).pack(pady=(80, 5))
tk.Button(janela, text="Botão 2", width=15).pack(pady=5)
tk.Button(janela, text="Botão 3", width=15).pack(pady=5)

janela.mainloop()