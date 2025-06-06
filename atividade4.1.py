import tkinter as tk

def enviar():
    print(f"Nome: {entradaNome.get()}")
    print (f"Idade: {entradaIdade.get()}")
    print (f"Genero: {entradaGenero.get()}")

def limpar():
    entradaNome.delete(0, tk.END)
    entradaIdade.delete(0, tk.END)
    entradaGenero.set(None)

janela = tk.Tk()
janela.title("Mini-Formulário")
largura = 400
altura = 200
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{x}+{y}")


tk.Label(janela, text="Nome: ").grid(row=0, column=0)
entradaNome = tk.Entry(janela)
entradaNome.grid(row=0, column=1)

tk.Label(janela, text="Idade: ").grid(row=1,column=0)
entradaIdade = tk.Entry(janela)
entradaIdade.grid(row=1,column=1)

tk.Label(janela, text=" Genero: ").grid(row=2, column=0)
entradaGenero = tk.StringVar()
tk.Radiobutton(janela, text="Masculino", variable=entradaGenero, value="Masculino").grid(row=2, column=1)
tk.Radiobutton(janela, text="Feminino", variable=entradaGenero, value="Feminino").grid(row=3, column=1)

tk.Button(janela, text="Enviar", command=enviar).grid(row=4, column=0)
tk.Button(janela, text="Limpar", command=limpar).grid(row=4, column=1)

janela.mainloop()
