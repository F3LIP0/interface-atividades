import tkinter as tk

def calcular_soma():
   try:
       # Obtém os valores digitados
       numero1 = float(entrada1.get())
       numero2 = float(entrada2.get())
       
       # Calcula a soma
       media = numero1 + numero2 / 2
       
       # Exibe o resultado
       label_resultado.config(text=f"A soma de {numero1} e {numero2} é {media}")
   except ValueError:
       # Exibe mensagem de erro
       label_resultado.config(text="Por favor, insira números válidos.")

def limpar_campos():
    # Limpa as entradas
    entrada1.delete(0, tk.END)
    entrada2.delete(0, tk.END)
    
    # Limpa o rótulo de resultado
    label_resultado.config(text="")

# Cria a janela principal
janela = tk.Tk()
janela.title("Calculadora de media")
janela.geometry("400x300")

# Rótulo e entrada para o primeiro número
label1 = tk.Label(janela, text="Digite o primeiro número:")
label1.pack(pady=5)
entrada1 = tk.Entry(janela)
entrada1.pack(pady=5)

# Rótulo e entrada para o segundo número
label2 = tk.Label(janela, text="Digite o segundo número:")
label2.pack(pady=5)
entrada2 = tk.Entry(janela)
entrada2.pack(pady=5)

# Botão para calcular
botao_calcular = tk.Button(janela, text="Calcular media", command=calcular_soma)
botao_calcular.pack(pady=10)

# Botão para limpar
botao_limpar = tk.Button(janela, text="Limpar", command=limpar_campos)
botao_limpar.pack(pady=10)

# Rótulo para exibir o resultado
label_resultado = tk.Label(janela, text="", font=("Arial", 14))
label_resultado.pack(pady=10)

# Mantém a janela aberta
janela.mainloop()