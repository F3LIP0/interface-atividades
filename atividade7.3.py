#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import csv
import re
import json

class ValidacaoDados:
    def __init__(self, root):
        self.root = root
        self.root.title("Validação de Dados em Arquivos")
        self.root.geometry("700x600")
        
        # Variáveis para armazenar os caminhos dos arquivos
        self.arquivo_entrada = None
        self.arquivo_saida = None
        
        # Lista para armazenar os dados
        self.dados = []
        self.dados_validos = []
        self.dados_invalidos = []
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Validação de Dados em Arquivos",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Frame para seleção de arquivos
        self.arquivo_frame = tk.LabelFrame(
            self.frame,
            text="Arquivos",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.arquivo_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos de arquivo
        self.arquivo_grid = tk.Frame(self.arquivo_frame)
        self.arquivo_grid.pack(fill=tk.X, pady=5)
        
        # Campo para arquivo de entrada
        self.entrada_label = tk.Label(
            self.arquivo_grid,
            text="Arquivo de Entrada:",
            font=("Arial", 12),
            width=15,
            anchor=tk.W
        )
        self.entrada_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.entrada_var = tk.StringVar()
        self.entrada_entry = tk.Entry(
            self.arquivo_grid,
            textvariable=self.entrada_var,
            font=("Arial", 12),
            width=40,
            state="readonly"
        )
        self.entrada_entry.grid(row=0, column=1, sticky=tk.W)
        
        self.btn_entrada = tk.Button(
            self.arquivo_grid,
            text="Selecionar",
            font=("Arial", 12),
            command=self.selecionar_entrada
        )
        self.btn_entrada.grid(row=0, column=2, padx=5)
        
        # Campo para arquivo de saída
        self.saida_label = tk.Label(
            self.arquivo_grid,
            text="Arquivo de Saída:",
            font=("Arial", 12),
            width=15,
            anchor=tk.W
        )
        self.saida_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.saida_var = tk.StringVar()
        self.saida_entry = tk.Entry(
            self.arquivo_grid,
            textvariable=self.saida_var,
            font=("Arial", 12),
            width=40,
            state="readonly"
        )
        self.saida_entry.grid(row=1, column=1, sticky=tk.W)
        
        self.btn_saida = tk.Button(
            self.arquivo_grid,
            text="Selecionar",
            font=("Arial", 12),
            command=self.selecionar_saida
        )
        self.btn_saida.grid(row=1, column=2, padx=5)
        
        # Botões de ação
        self.acoes_frame = tk.Frame(self.arquivo_frame)
        self.acoes_frame.pack(pady=10)
        
        self.btn_carregar = tk.Button(
            self.acoes_frame,
            text="Carregar Dados",
            font=("Arial", 12),
            width=15,
            command=self.carregar_dados
        )
        self.btn_carregar.grid(row=0, column=0, padx=5)
        
        self.btn_validar = tk.Button(
            self.acoes_frame,
            text="Validar Dados",
            font=("Arial", 12),
            width=15,
            command=self.validar_dados,
            state=tk.DISABLED
        )
        self.btn_validar.grid(row=0, column=1, padx=5)
        
        self.btn_salvar = tk.Button(
            self.acoes_frame,
            text="Salvar Válidos",
            font=("Arial", 12),
            width=15,
            command=self.salvar_dados_validos,
            state=tk.DISABLED
        )
        self.btn_salvar.grid(row=0, column=2, padx=5)
        
        # Frame para mensagens
        self.msg_frame = tk.Frame(self.frame, height=50)
        self.msg_frame.pack(fill=tk.X, pady=5)
        self.msg_frame.pack_propagate(False)
        
        self.msg_label = tk.Label(
            self.msg_frame,
            text="Selecione um arquivo de entrada para começar",
            font=("Arial", 12),
            wraplength=650
        )
        self.msg_label.pack(pady=5)
        
        # Notebook para exibir os dados
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab para todos os dados
        self.tab_todos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_todos, text="Todos os Dados")
        
        # Tab para dados válidos
        self.tab_validos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_validos, text="Dados Válidos")
        
        # Tab para dados inválidos
        self.tab_invalidos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_invalidos, text="Dados Inválidos")
        
        # Tabela para todos os dados
        self.colunas = ("nome", "idade", "email", "status")
        self.tabela_todos = self.criar_tabela(self.tab_todos)
        
        # Tabela para dados válidos
        self.tabela_validos = self.criar_tabela(self.tab_validos)
        
        # Tabela para dados inválidos
        self.tabela_invalidos = self.criar_tabela(self.tab_invalidos)
        
        # Status bar
        self.status_frame = tk.Frame(self.frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Pronto",
            font=("Arial", 10),
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)
    
    def criar_tabela(self, parent):
        # Cria uma tabela (Treeview) para exibir os dados
        tabela = ttk.Treeview(
            parent,
            columns=self.colunas,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar as colunas
        tabela.heading("nome", text="Nome")
        tabela.heading("idade", text="Idade")
        tabela.heading("email", text="E-mail")
        tabela.heading("status", text="Status")
        
        tabela.column("nome", width=200)
        tabela.column("idade", width=50)
        tabela.column("email", width=250)
        tabela.column("status", width=100)
        
        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(
            parent,
            orient=tk.VERTICAL,
            command=tabela.yview
        )
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar a tabela e a scrollbar
        tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return tabela
    
    def selecionar_entrada(self):
        # Abre o diálogo para selecionar o arquivo de entrada
        arquivo = filedialog.askopenfilename(
            title="Selecionar Arquivo de Entrada",
            filetypes=[
                ("Arquivos CSV", "*.csv"),
                ("Arquivos JSON", "*.json"),
                ("Arquivos de Texto", "*.txt"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.arquivo_entrada = arquivo
            self.entrada_var.set(arquivo)
            self.mostrar_mensagem(f"Arquivo de entrada selecionado: {os.path.basename(arquivo)}", "info")
            
            # Sugere um nome para o arquivo de saída
            nome_base, extensao = os.path.splitext(arquivo)
            self.arquivo_saida = f"{nome_base}_validos{extensao}"
            self.saida_var.set(self.arquivo_saida)
    
    def selecionar_saida(self):
        # Abre o diálogo para selecionar o arquivo de saída
        arquivo = filedialog.asksaveasfilename(
            title="Selecionar Arquivo de Saída",
            defaultextension=".csv",
            filetypes=[
                ("Arquivos CSV", "*.csv"),
                ("Arquivos JSON", "*.json"),
                ("Arquivos de Texto", "*.txt"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        
        if arquivo:
            self.arquivo_saida = arquivo
            self.saida_var.set(arquivo)
            self.mostrar_mensagem(f"Arquivo de saída selecionado: {os.path.basename(arquivo)}", "info")
    
    def carregar_dados(self):
        # Verifica se um arquivo de entrada foi selecionado
        if not self.arquivo_entrada:
            self.mostrar_mensagem("Selecione um arquivo de entrada primeiro.", "error")
            return
        
        try:
            # Limpa os dados e as tabelas
            self.dados = []
            self.dados_validos = []
            self.dados_invalidos = []
            
            for tabela in [self.tabela_todos, self.tabela_validos, self.tabela_invalidos]:
                for item in tabela.get_children():
                    tabela.delete(item)
            
            # Determina o tipo de arquivo pela extensão
            _, extensao = os.path.splitext(self.arquivo_entrada)
            
            if extensao.lower() == ".csv":
                self.carregar_csv()
            elif extensao.lower() == ".json":
                self.carregar_json()
            else:
                self.mostrar_mensagem("Formato de arquivo não suportado. Use CSV ou JSON.", "error")
                return
            
            # Atualiza a interface
            self.btn_validar.config(state=tk.NORMAL)
            self.mostrar_mensagem(f"{len(self.dados)} registros carregados do arquivo.", "success")
            self.atualizar_status(f"Carregados: {len(self.dados)}, Válidos: 0, Inválidos: 0")
            
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao carregar o arquivo: {str(e)}", "error")
    
    def carregar_csv(self):
        # Carrega os dados de um arquivo CSV
        with open(self.arquivo_entrada, "r", encoding="utf-8", newline="") as f:
            leitor = csv.DictReader(f)
            for linha in leitor:
                # Verifica se o arquivo tem os campos necessários
                if not all(campo in linha for campo in ["nome", "idade", "email"]):
                    self.mostrar_mensagem("O arquivo CSV não contém os campos necessários (nome, idade, email).", "error")
                    return
                
                # Adiciona o registro aos dados
                registro = {
                    "nome": linha["nome"],
                    "idade": linha["idade"],
                    "email": linha["email"],
                    "status": "Não validado"
                }
                self.dados.append(registro)
                
                # Adiciona o registro à tabela
                self.tabela_todos.insert("", tk.END, values=(
                    registro["nome"],
                    registro["idade"],
                    registro["email"],
                    registro["status"]
                ))
    
    def carregar_json(self):
        # Carrega os dados de um arquivo JSON
        with open(self.arquivo_entrada, "r", encoding="utf-8") as f:
            dados_json = json.load(f)
            
            # Verifica se o arquivo contém uma lista
            if not isinstance(dados_json, list):
                self.mostrar_mensagem("O arquivo JSON não contém uma lista de registros.", "error")
                return
            
            for item in dados_json:
                # Verifica se o item tem os campos necessários
                if not all(campo in item for campo in ["nome", "idade", "email"]):
                    self.mostrar_mensagem("O arquivo JSON não contém os campos necessários (nome, idade, email).", "error")
                    return
                
                # Adiciona o registro aos dados
                registro = {
                    "nome": item["nome"],
                    "idade": item["idade"],
                    "email": item["email"],
                    "status": "Não validado"
                }
                self.dados.append(registro)
                
                # Adiciona o registro à tabela
                self.tabela_todos.insert("", tk.END, values=(
                    registro["nome"],
                    registro["idade"],
                    registro["email"],
                    registro["status"]
                ))
    
    def validar_dados(self):
        # Verifica se há dados para validar
        if not self.dados:
            self.mostrar_mensagem("Não há dados para validar.", "error")
            return
        
        # Limpa os dados válidos e inválidos
        self.dados_validos = []
        self.dados_invalidos = []
        
        # Limpa as tabelas de dados válidos e inválidos
        for tabela in [self.tabela_validos, self.tabela_invalidos]:
            for item in tabela.get_children():
                tabela.delete(item)
        
        # Valida cada registro
        for i, registro in enumerate(self.dados):
            nome = registro["nome"]
            idade = registro["idade"]
            email = registro["email"]
            
            # Validação do nome
            if not nome or not isinstance(nome, str) or len(nome) < 2:
                registro["status"] = "Nome inválido"
                self.dados_invalidos.append(registro)
                self.tabela_invalidos.insert("", tk.END, values=(nome, idade, email, registro["status"]))
                continue
            
            # Validação da idade
            try:
                idade_num = int(idade)
                if idade_num <= 0 or idade_num > 120:
                    registro["status"] = "Idade inválida"
                    self.dados_invalidos.append(registro)
                    self.tabela_invalidos.insert("", tk.END, values=(nome, idade, email, registro["status"]))
                    continue
            except (ValueError, TypeError):
                registro["status"] = "Idade não numérica"
                self.dados_invalidos.append(registro)
                self.tabela_invalidos.insert("", tk.END, values=(nome, idade, email, registro["status"]))
                continue
            
            # Validação do e-mail
            padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not isinstance(email, str) or not re.match(padrao_email, email):
                registro["status"] = "E-mail inválido"
                self.dados_invalidos.append(registro)
                self.tabela_invalidos.insert("", tk.END, values=(nome, idade, email, registro["status"]))
                continue
            
            # Se chegou aqui, o registro é válido
            registro["status"] = "Válido"
            self.dados_validos.append(registro)
            self.tabela_validos.insert("", tk.END, values=(nome, idade, email, registro["status"]))
            
            # Atualiza o status na tabela de todos os dados
            item_id = self.tabela_todos.get_children()[i]
            self.tabela_todos.item(item_id, values=(nome, idade, email, registro["status"]))
        
        # Atualiza a interface
        self.btn_salvar.config(state=tk.NORMAL if self.dados_validos else tk.DISABLED)
        self.mostrar_mensagem(f"Validação concluída. {len(self.dados_validos)} registros válidos, {len(self.dados_invalidos)} inválidos.", "success")
        self.atualizar_status(f"Carregados: {len(self.dados)}, Válidos: {len(self.dados_validos)}, Inválidos: {len(self.dados_invalidos)}")
        
        # Seleciona a aba apropriada
        if self.dados_invalidos:
            self.notebook.select(2)  # Seleciona a aba de dados inválidos
        else:
            self.notebook.select(1)  # Seleciona a aba de dados válidos
    
    def salvar_dados_validos(self):
        # Verifica se há dados válidos para salvar
        if not self.dados_validos:
            self.mostrar_mensagem("Não há dados válidos para salvar.", "error")
            return
        
        # Verifica se um arquivo de saída foi selecionado
        if not self.arquivo_saida:
            self.mostrar_mensagem("Selecione um arquivo de saída primeiro.", "error")
            return
        
        try:
            # Determina o tipo de arquivo pela extensão
            _, extensao = os.path.splitext(self.arquivo_saida)
            
            if extensao.lower() == ".csv":
                self.salvar_csv()
            elif extensao.lower() == ".json":
                self.salvar_json()
            else:
                self.mostrar_mensagem("Formato de arquivo não suportado para saída. Use CSV ou JSON.", "error")
                return
            
            self.mostrar_mensagem(f"{len(self.dados_validos)} registros válidos salvos em '{os.path.basename(self.arquivo_saida)}'.", "success")
            
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao salvar o arquivo: {str(e)}", "error")
    
    def salvar_csv(self):
        # Salva os dados válidos em um arquivo CSV
        with open(self.arquivo_saida, "w", encoding="utf-8", newline="") as f:
            # Define os campos do CSV
            campos = ["nome", "idade", "email"]
            
            # Cria o escritor CSV
            escritor = csv.DictWriter(f, fieldnames=campos)
            
            # Escreve o cabeçalho
            escritor.writeheader()
            
            # Escreve os registros válidos
            for registro in self.dados_validos:
                # Cria um novo dicionário apenas com os campos necessários
                dados_saida = {campo: registro[campo] for campo in campos}
                escritor.writerow(dados_saida)
    
    def salvar_json(self):
        # Salva os dados válidos em um arquivo JSON
        with open(self.arquivo_saida, "w", encoding="utf-8") as f:
            # Cria uma lista com os registros válidos, excluindo o campo "status"
            dados_saida = []
            for registro in self.dados_validos:
                dados_saida.append({
                    "nome": registro["nome"],
                    "idade": int(registro["idade"]),
                    "email": registro["email"]
                })
            
            # Escreve os dados no arquivo JSON
            json.dump(dados_saida, f, ensure_ascii=False, indent=4)
    
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
    
    def atualizar_status(self, mensagem):
        self.status_label.config(text=mensagem)

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidacaoDados(root)
    root.mainloop()

