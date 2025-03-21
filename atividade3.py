import tkinter as tk
from tkinter import messagebox

# Função para exibir os dados na interface
def exibir_dados():
    nome = entrada_nome.get()
    email = entrada_email.get()
    preferencia = var_preferencia.get()

    # Verifica se todos os campos foram preenchidos
    if not nome or not email or not preferencia:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
    else:
        # Exibe os dados no rótulo de resultado
        resultado = f"Nome: {nome}\nE-mail: {email}\nPreferência de Contato: {preferencia}"
        label_resultado.config(text=resultado)

        # Limpa os campos após exibir os dados
        entrada_nome.delete(0, tk.END)
        entrada_email.delete(0, tk.END)
        var_preferencia.set("")  # Reseta a seleção do RadioButton

# Cria a janela principal
janela = tk.Tk()
janela.title("Mini-Formulário")
janela.geometry("400x350")

# Rótulo e entrada para o nome
label_nome = tk.Label(janela, text="Nome:")
label_nome.pack(pady=5)
entrada_nome = tk.Entry(janela, width=30)
entrada_nome.pack(pady=5)

# Rótulo e entrada para o e-mail
label_email = tk.Label(janela, text="E-mail:")
label_email.pack(pady=5)
entrada_email = tk.Entry(janela, width=30)
entrada_email.pack(pady=5)

# Rótulo e RadioButtons para a preferência de contato
label_preferencia = tk.Label(janela, text="Preferência de Contato:")
label_preferencia.pack(pady=5)

# Variável para armazenar a preferência de contato
var_preferencia = tk.StringVar()

# RadioButton para E-mail
rb_email = tk.Radiobutton(janela, text="E-mail", variable=var_preferencia, value="E-mail")
rb_email.pack(pady=5)

# RadioButton para Telefone
rb_telefone = tk.Radiobutton(janela, text="Telefone", variable=var_preferencia, value="Telefone")
rb_telefone.pack(pady=5)

# Botão para exibir os dados
botao_exibir = tk.Button(janela, text="Exibir Dados", command=exibir_dados)
botao_exibir.pack(pady=20)

# Rótulo para exibir o resultado
label_resultado = tk.Label(janela, text="", font=("Arial", 12), justify="left")
label_resultado.pack(pady=10)

# Mantém a janela aberta
janela.mainloop()