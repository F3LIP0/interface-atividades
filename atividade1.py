import tkinter as tk

def calcular_dobro():
   try:
       numero = int(entrada.get())
       resultado = numero * 3
       label_resultado.config(text=f"O triplo de {numero} é {resultado}")
   except ValueError:
       label_resultado.config(text="Por favor, insira um número válido.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Calculadora de Triblo")


# Centralizar a janela
largura = 400
altura = 200
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
x = (largura_tela // 2) - (largura // 2)
y = (altura_tela // 2) - (altura // 2)
janela.geometry(f"{largura}x{altura}+{x}+{y}")


#texto pra instrucao
instrucao = tk.Label(janela, text="Digite um numero pra ser multiplicado ao triplo", font=("Arial", 10))
instrucao.pack(pady=(45, 0))


# Entrada de dados
entrada = tk.Entry(janela, font=("Arial", 14))
entrada.pack(pady=10)

# Botão para calcular
botao_calcular = tk.Button(janela, text="Calcular", command=calcular_dobro)
botao_calcular.pack(pady=10)

# Rótulo para exibir o resultado
label_resultado = tk.Label(janela, text="", font=("Arial", 14))
label_resultado.pack(pady=10)

# Iniciar a interface
janela.mainloop()
