import tkinter as tk

janela = tk.Tk()
janela.title("Botões com Rótulos")
janela.geometry("400x300")



tk.Label(janela, text="Botão 1").place(x=30, y=30)
tk.Button(janela, text="Clique").place(x=30, y=50)

tk.Label(janela, text="Botão 2").place(x=250, y=120)
tk.Button(janela, text="Clique").place(x=250, y=140)

tk.Label(janela, text="Botão 3").place(x=30, y=230)
tk.Button(janela, text="Clique").place(x=30, y=250)

janela.mainloop()