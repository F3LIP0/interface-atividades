#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv
import re

class CadastroUsuarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Usuários")
        self.root.geometry("700x600")
        
        # Variável para armazenar o caminho do arquivo CSV
        self.arquivo_csv = None
        
        # Lista para armazenar os usuários cadastrados
        self.usuarios = []
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Cadastro de Usuários",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Frame para o formulário
        self.form_frame = tk.LabelFrame(
            self.frame,
            text="Novo Usuário",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.form_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos do formulário
        self.form_grid = tk.Frame(self.form_frame)
        self.form_grid.pack(fill=tk.X, pady=10)
        
        # Campo Nome
        self.nome_label = tk.Label(
            self.form_grid,
            text="Nome:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.nome_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(
            self.form_grid,
            textvariable=self.nome_var,
            font=("Arial", 12),
            width=30
        )
        self.nome_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Idade
        self.idade_label = tk.Label(
            self.form_grid,
            text="Idade:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.idade_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.idade_var = tk.StringVar()
        self.idade_entry = tk.Entry(
            self.form_grid,
            textvariable=self.idade_var,
            font=("Arial", 12),
            width=10
        )
        self.idade_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo E-mail
        self.email_label = tk.Label(
            self.form_grid,
            text="E-mail:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.email_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            self.form_grid,
            textvariable=self.email_var,
            font=("Arial", 12),
            width=30
        )
        self.email_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Botões do formulário
        self.form_buttons = tk.Frame(self.form_frame)
        self.form_buttons.pack(pady=10)
        
        self.btn_limpar = tk.Button(
            self.form_buttons,
            text="Limpar",
            font=("Arial", 12),
            width=10,
            command=self.limpar_campos
        )
        self.btn_limpar.grid(row=0, column=0, padx=5)
        
        self.btn_cadastrar = tk.Button(
            self.form_buttons,
            text="Cadastrar",
            font=("Arial", 12),
            width=10,
            bg="#90EE90",
            command=self.cadastrar_usuario
        )
        self.btn_cadastrar.grid(row=0, column=1, padx=5)
        
        # Frame para mensagens de validação
        self.msg_frame = tk.Frame(self.frame, height=50)
        self.msg_frame.pack(fill=tk.X, pady=5)
        self.msg_frame.pack_propagate(False)
        
        self.msg_label = tk.Label(
            self.msg_frame,
            text="Preencha os campos acima e clique em Cadastrar",
            font=("Arial", 12),
            wraplength=650
        )
        self.msg_label.pack(pady=5)
        
        # Frame para a tabela de usuários
        self.tabela_frame = tk.LabelFrame(
            self.frame,
            text="Usuários Cadastrados",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.tabela_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabela de usuários (Treeview)
        self.colunas = ("nome", "idade", "email")
        self.tabela = ttk.Treeview(
            self.tabela_frame,
            columns=self.colunas,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar as colunas
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("email", text="E-mail")
        
        self.tabela.column("nome", width=200)
        self.tabela.column("idade", width=50)
        self.tabela.column("email", width=250)
        
        # Scrollbar para a tabela
        self.tabela_scroll = ttk.Scrollbar(
            self.tabela_frame,
            orient=tk.VERTICAL,
            command=self.tabela.yview
        )
        self.tabela.configure(yscrollcommand=self.tabela_scroll.set)
        
        # Posicionar a tabela e a scrollbar
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tabela_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para os botões de arquivo
        self.arquivo_frame = tk.Frame(self.frame)
        self.arquivo_frame.pack(fill=tk.X, pady=10)
        
        # Botões para manipulação de arquivos
        self.btn_novo = tk.Button(
            self.arquivo_frame,
            text="Novo Arquivo",
            font=("Arial", 12),
            width=12,
            command=self.novo_arquivo
        )
        self.btn_novo.grid(row=0, column=0, padx=5)
        
        self.btn_abrir = tk.Button(
            self.arquivo_frame,
            text="Abrir CSV",
            font=("Arial", 12),
            width=12,
            command=self.abrir_arquivo
        )
        self.btn_abrir.grid(row=0, column=1, padx=5)
        
        self.btn_salvar = tk.Button(
            self.arquivo_frame,
            text="Salvar",
            font=("Arial", 12),
            width=12,
            command=self.salvar_arquivo
        )
        self.btn_salvar.grid(row=0, column=2, padx=5)
        
        self.btn_salvar_como = tk.Button(
            self.arquivo_frame,
            text="Salvar Como",
            font=("Arial", 12),
            width=12,
            command=self.salvar_como
        )
        self.btn_salvar_como.grid(row=0, column=3, padx=5)
        
        # Label para mostrar o arquivo atual
        self.arquivo_label = tk.Label(
            self.frame,
            text="Nenhum arquivo aberto",
            font=("Arial", 10),
            fg="gray"
        )
        self.arquivo_label.pack(pady=5)
        
        # Foco inicial no campo de nome
        self.nome_entry.focus_set()
        
    def limpar_campos(self):
        self.nome_var.set("")
        self.idade_var.set("")
        self.email_var.set("")
        self.nome_entry.focus_set()
        self.mostrar_mensagem("Campos limpos. Preencha os dados para cadastrar.", "info")
        
    def cadastrar_usuario(self):
        nome = self.nome_var.get().strip()
        idade = self.idade_var.get().strip()
        email = self.email_var.get().strip()
        
        # Validação dos campos
        if not self.validar_campos(nome, idade, email):
            return
        
        # Adiciona o usuário à lista
        usuario = {"nome": nome, "idade": int(idade), "email": email}
        self.usuarios.append(usuario)
        
        # Adiciona o usuário à tabela
        self.tabela.insert("", tk.END, values=(nome, idade, email))
        
        # Limpa os campos para um novo cadastro
        self.limpar_campos()
        
        # Mostra mensagem de sucesso
        self.mostrar_mensagem(f"Usuário '{nome}' cadastrado com sucesso!", "success")
    
    def validar_campos(self, nome, idade, email):
        # Validação do nome
        if not nome:
            self.mostrar_mensagem("O campo Nome não pode estar vazio.", "error")
            self.nome_entry.focus_set()
            return False
        
        # Validação da idade
        if not idade:
            self.mostrar_mensagem("O campo Idade não pode estar vazio.", "error")
            self.idade_entry.focus_set()
            return False
        
        try:
            idade_num = int(idade)
            if idade_num <= 0:
                self.mostrar_mensagem("A idade deve ser um número positivo.", "error")
                self.idade_entry.focus_set()
                return False
        except ValueError:
            self.mostrar_mensagem("A idade deve ser um número inteiro.", "error")
            self.idade_entry.focus_set()
            return False
        
        # Validação do e-mail
        if not email:
            self.mostrar_mensagem("O campo E-mail não pode estar vazio.", "error")
            self.email_entry.focus_set()
            return False
        
        # Validação do formato do e-mail
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao_email, email):
            self.mostrar_mensagem("O e-mail informado não é válido.", "error")
            self.email_entry.focus_set()
            return False
        
        return True
    
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
    
    def novo_arquivo(self):
        # Verifica se há usuários cadastrados
        if self.usuarios and not messagebox.askyesno(
            "Novo Arquivo", "Deseja criar um novo arquivo? Os dados atuais serão perdidos."
        ):
            return
        
        # Limpa a lista de usuários e a tabela
        self.usuarios = []
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        # Reseta o arquivo atual
        self.arquivo_csv = None
        self.atualizar_titulo()
        
        self.mostrar_mensagem("Novo arquivo criado. Cadastre usuários e salve quando desejar.", "info")
    
    def abrir_arquivo(self):
        # Verifica se há usuários cadastrados
        if self.usuarios and not messagebox.askyesno(
            "Abrir Arquivo", "Os dados atuais serão perdidos. Deseja continuar?"
        ):
            return
        
        # Abre o diálogo para selecionar o arquivo
        arquivo = filedialog.askopenfilename(
            title="Abrir Arquivo CSV",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Limpa a lista de usuários e a tabela
                self.usuarios = []
                for item in self.tabela.get_children():
                    self.tabela.delete(item)
                
                # Abre o arquivo e carrega os usuários
                with open(arquivo, "r", encoding="utf-8", newline="") as f:
                    leitor = csv.DictReader(f)
                    for linha in leitor:
                        # Converte a idade para inteiro
                        linha["idade"] = int(linha["idade"])
                        
                        # Adiciona o usuário à lista
                        self.usuarios.append(linha)
                        
                        # Adiciona o usuário à tabela
                        self.tabela.insert("", tk.END, values=(linha["nome"], linha["idade"], linha["email"]))
                
                # Atualiza o arquivo atual
                self.arquivo_csv = arquivo
                self.atualizar_titulo()
                
                self.mostrar_mensagem(f"Arquivo '{os.path.basename(arquivo)}' aberto com sucesso! {len(self.usuarios)} usuários carregados.", "success")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {str(e)}")
    
    def salvar_arquivo(self):
        # Se não houver arquivo atual, usa "Salvar Como"
        if not self.arquivo_csv:
            self.salvar_como()
        else:
            self.salvar_csv(self.arquivo_csv)
    
    def salvar_como(self):
        # Abre o diálogo para selecionar o arquivo
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Arquivo CSV",
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*")]
        )
        
        if arquivo:
            self.salvar_csv(arquivo)
    
    def salvar_csv(self, arquivo):
        try:
            # Salva os usuários no arquivo CSV
            with open(arquivo, "w", encoding="utf-8", newline="") as f:
                # Define os campos do CSV
                campos = ["nome", "idade", "email"]
                
                # Cria o escritor CSV
                escritor = csv.DictWriter(f, fieldnames=campos)
                
                # Escreve o cabeçalho
                escritor.writeheader()
                
                # Escreve os usuários
                for usuario in self.usuarios:
                    escritor.writerow(usuario)
            
            # Atualiza o arquivo atual
            self.arquivo_csv = arquivo
            self.atualizar_titulo()
            
            self.mostrar_mensagem(f"Dados salvos com sucesso em '{os.path.basename(arquivo)}'!", "success")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")
    
    def atualizar_titulo(self):
        # Atualiza o título da janela e o label de arquivo
        if self.arquivo_csv:
            nome_arquivo = os.path.basename(self.arquivo_csv)
            self.root.title(f"Cadastro de Usuários - {nome_arquivo}")
            self.arquivo_label.config(text=f"Arquivo: {nome_arquivo}")
        else:
            self.root.title("Cadastro de Usuários")
            self.arquivo_label.config(text="Nenhum arquivo aberto")

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroUsuarios(root)
    root.mainloop()

