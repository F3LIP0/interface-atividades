#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

class CadastroSimples:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro Simples")
        self.root.geometry("450x400")
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Formulário de Cadastro",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Frame para o formulário
        self.form_frame = tk.Frame(self.frame)
        self.form_frame.pack(pady=10, fill=tk.X)
        
        # Campo Nome
        self.nome_label = tk.Label(
            self.form_frame,
            text="Nome:",
            font=("Arial", 12),
            anchor=tk.W,
            width=10
        )
        self.nome_label.grid(row=0, column=0, sticky=tk.W, pady=10)
        
        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(
            self.form_frame,
            textvariable=self.nome_var,
            font=("Arial", 12),
            width=30
        )
        self.nome_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Idade
        self.idade_label = tk.Label(
            self.form_frame,
            text="Idade:",
            font=("Arial", 12),
            anchor=tk.W,
            width=10
        )
        self.idade_label.grid(row=1, column=0, sticky=tk.W, pady=10)
        
        self.idade_var = tk.StringVar()
        self.idade_entry = tk.Entry(
            self.form_frame,
            textvariable=self.idade_var,
            font=("Arial", 12),
            width=10
        )
        self.idade_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Botões
        self.botoes_frame = tk.Frame(self.frame)
        self.botoes_frame.pack(pady=20)
        
        self.btn_limpar = tk.Button(
            self.botoes_frame,
            text="Limpar",
            font=("Arial", 12),
            width=10,
            command=self.limpar_campos
        )
        self.btn_limpar.grid(row=0, column=0, padx=10)
        
        self.btn_cadastrar = tk.Button(
            self.botoes_frame,
            text="Cadastrar",
            font=("Arial", 12),
            width=10,
            bg="#90EE90",
            command=self.cadastrar
        )
        self.btn_cadastrar.grid(row=0, column=1, padx=10)
        
        # Frame para mensagens de validação
        self.msg_frame = tk.Frame(self.frame, height=100)
        self.msg_frame.pack(pady=10, fill=tk.X)
        self.msg_frame.pack_propagate(False)
        
        # Label para mensagens de validação
        self.msg_label = tk.Label(
            self.msg_frame,
            text="Preencha os campos acima e clique em Cadastrar",
            font=("Arial", 12),
            wraplength=400
        )
        self.msg_label.pack(pady=10)
        
        # Frame para exibir os cadastros
        self.cadastros_frame = tk.LabelFrame(
            self.frame,
            text="Cadastros Realizados",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.cadastros_frame.pack(fill=tk.X, pady=10)
        
        self.cadastros_text = tk.Text(
            self.cadastros_frame,
            height=5,
            width=50,
            font=("Arial", 10),
            state=tk.DISABLED
        )
        self.cadastros_text.pack(fill=tk.X)
        
        # Lista para armazenar os cadastros
        self.cadastros = []
        
        # Foco inicial no campo de nome
        self.nome_entry.focus_set()
        
    def limpar_campos(self):
        self.nome_var.set("")
        self.idade_var.set("")
        self.nome_entry.focus_set()
        self.mostrar_mensagem("Campos limpos. Preencha os dados para cadastrar.", "info")
        
    def cadastrar(self):
        nome = self.nome_var.get().strip()
        idade = self.idade_var.get().strip()
        
        # Validação do nome
        if not nome:
            self.mostrar_mensagem("O campo Nome não pode estar vazio.", "error")
            self.nome_entry.focus_set()
            return
        
        # Validação da idade
        if not idade:
            self.mostrar_mensagem("O campo Idade não pode estar vazio.", "error")
            self.idade_entry.focus_set()
            return
        
        try:
            idade_num = int(idade)
            if idade_num <= 0:
                self.mostrar_mensagem("A idade deve ser um número positivo.", "error")
                self.idade_entry.focus_set()
                return
        except ValueError:
            self.mostrar_mensagem("A idade deve ser um número inteiro.", "error")
            self.idade_entry.focus_set()
            return
        
        # Cadastro válido
        self.cadastros.append({"nome": nome, "idade": idade_num})
        self.mostrar_mensagem(f"Cadastro realizado com sucesso! Nome: {nome}, Idade: {idade_num}", "success")
        
        # Atualiza a lista de cadastros
        self.atualizar_lista_cadastros()
        
        # Limpa os campos para um novo cadastro
        self.limpar_campos()
    
    def mostrar_mensagem(self, mensagem, tipo):
        # Configura a cor do texto baseado no tipo de mensagem
        if tipo == "success":
            cor = "green"
        elif tipo == "error":
            cor = "red"
        elif tipo == "warning":
            cor = "orange"
        else:  # info
            cor = "blue"
            
        self.msg_label.config(text=mensagem, fg=cor)
    
    def atualizar_lista_cadastros(self):
        # Habilita o widget Text para edição
        self.cadastros_text.config(state=tk.NORMAL)
        
        # Limpa o conteúdo atual
        self.cadastros_text.delete(1.0, tk.END)
        
        # Adiciona os cadastros
        if not self.cadastros:
            self.cadastros_text.insert(tk.END, "Nenhum cadastro realizado.")
        else:
            for i, cadastro in enumerate(self.cadastros, 1):
                self.cadastros_text.insert(tk.END, f"{i}. Nome: {cadastro['nome']}, Idade: {cadastro['idade']}\n")
        
        # Desabilita o widget Text novamente
        self.cadastros_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroSimples(root)
    root.mainloop()

