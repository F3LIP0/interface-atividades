#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class CadastroProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Produtos")
        self.root.geometry("900x700")
        
        # Configurações de conexão com o banco de dados
        self.config_db = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "estoque"
        }
        
        # Variável para armazenar a conexão com o banco
        self.conexao = None
        
        # Lista para armazenar as categorias disponíveis
        self.categorias = []
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Cadastro de Produtos",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Frame para conexão com o banco
        self.conexao_frame = tk.LabelFrame(
            self.frame,
            text="Conexão com o Banco de Dados",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.conexao_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos de conexão
        self.conexao_grid = tk.Frame(self.conexao_frame)
        self.conexao_grid.pack(fill=tk.X, pady=5)
        
        # Campo Host
        self.host_label = tk.Label(
            self.conexao_grid,
            text="Host:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.host_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.host_var = tk.StringVar(value=self.config_db["host"])
        self.host_entry = tk.Entry(
            self.conexao_grid,
            textvariable=self.host_var,
            font=("Arial", 12),
            width=20
        )
        self.host_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Usuário
        self.user_label = tk.Label(
            self.conexao_grid,
            text="Usuário:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.user_label.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.user_var = tk.StringVar(value=self.config_db["user"])
        self.user_entry = tk.Entry(
            self.conexao_grid,
            textvariable=self.user_var,
            font=("Arial", 12),
            width=20
        )
        self.user_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Campo Senha
        self.password_label = tk.Label(
            self.conexao_grid,
            text="Senha:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_var = tk.StringVar(value=self.config_db["password"])
        self.password_entry = tk.Entry(
            self.conexao_grid,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=20,
            show="*"
        )
        self.password_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo Banco de Dados
        self.database_label = tk.Label(
            self.conexao_grid,
            text="Banco:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.database_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.database_var = tk.StringVar(value=self.config_db["database"])
        self.database_entry = tk.Entry(
            self.conexao_grid,
            textvariable=self.database_var,
            font=("Arial", 12),
            width=20
        )
        self.database_entry.grid(row=1, column=3, sticky=tk.W)
        
        # Botão para conectar
        self.btn_conectar = tk.Button(
            self.conexao_frame,
            text="Conectar",
            font=("Arial", 12),
            width=15,
            command=self.conectar_bd
        )
        self.btn_conectar.pack(pady=10)
        
        # Frame para mensagens
        self.msg_frame = tk.Frame(self.frame, height=50)
        self.msg_frame.pack(fill=tk.X, pady=5)
        self.msg_frame.pack_propagate(False)
        
        self.msg_label = tk.Label(
            self.msg_frame,
            text="Configure a conexão com o banco de dados e clique em Conectar",
            font=("Arial", 12),
            wraplength=850
        )
        self.msg_label.pack(pady=5)
        
        # Frame para o formulário de cadastro
        self.cadastro_frame = tk.LabelFrame(
            self.frame,
            text="Cadastro de Produto",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.cadastro_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos do formulário
        self.cadastro_grid = tk.Frame(self.cadastro_frame)
        self.cadastro_grid.pack(fill=tk.X, pady=5)
        
        # Campo Nome
        self.nome_label = tk.Label(
            self.cadastro_grid,
            text="Nome:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.nome_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(
            self.cadastro_grid,
            textvariable=self.nome_var,
            font=("Arial", 12),
            width=30
        )
        self.nome_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Categoria
        self.categoria_label = tk.Label(
            self.cadastro_grid,
            text="Categoria:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.categoria_label.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(
            self.cadastro_grid,
            textvariable=self.categoria_var,
            font=("Arial", 12),
            width=20,
            state="readonly"
        )
        self.categoria_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Campo Quantidade
        self.qtd_label = tk.Label(
            self.cadastro_grid,
            text="Quantidade:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.qtd_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.qtd_var = tk.StringVar()
        self.qtd_entry = tk.Entry(
            self.cadastro_grid,
            textvariable=self.qtd_var,
            font=("Arial", 12),
            width=10
        )
        self.qtd_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo Preço
        self.preco_label = tk.Label(
            self.cadastro_grid,
            text="Preço:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.preco_label.grid(row=1, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.preco_var = tk.StringVar()
        self.preco_entry = tk.Entry(
            self.cadastro_grid,
            textvariable=self.preco_var,
            font=("Arial", 12),
            width=10
        )
        self.preco_entry.grid(row=1, column=3, sticky=tk.W)
        
        # Campo Descrição
        self.descricao_label = tk.Label(
            self.cadastro_grid,
            text="Descrição:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.descricao_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.descricao_text = tk.Text(
            self.cadastro_grid,
            font=("Arial", 12),
            width=50,
            height=3
        )
        self.descricao_text.grid(row=2, column=1, columnspan=3, sticky=tk.W)
        
        # Botões do formulário
        self.cadastro_botoes = tk.Frame(self.cadastro_frame)
        self.cadastro_botoes.pack(pady=10)
        
        self.btn_limpar = tk.Button(
            self.cadastro_botoes,
            text="Limpar",
            font=("Arial", 12),
            width=10,
            command=self.limpar_cadastro
        )
        self.btn_limpar.grid(row=0, column=0, padx=5)
        
        self.btn_cadastrar = tk.Button(
            self.cadastro_botoes,
            text="Cadastrar",
            font=("Arial", 12),
            width=10,
            bg="#90EE90",
            command=self.cadastrar_produto
        )
        self.btn_cadastrar.grid(row=0, column=1, padx=5)
        
        # Frame para exibir os produtos cadastrados
        self.produtos_frame = tk.LabelFrame(
            self.frame,
            text="Produtos Cadastrados",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.produtos_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabela para exibir os produtos
        self.colunas_produtos = ("id", "nome", "categoria", "quantidade", "preco", "descricao")
        self.tabela_produtos = ttk.Treeview(
            self.produtos_frame,
            columns=self.colunas_produtos,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar as colunas
        self.tabela_produtos.heading("id", text="ID")
        self.tabela_produtos.heading("nome", text="Nome")
        self.tabela_produtos.heading("categoria", text="Categoria")
        self.tabela_produtos.heading("quantidade", text="Quantidade")
        self.tabela_produtos.heading("preco", text="Preço")
        self.tabela_produtos.heading("descricao", text="Descrição")
        
        self.tabela_produtos.column("id", width=50)
        self.tabela_produtos.column("nome", width=200)
        self.tabela_produtos.column("categoria", width=100)
        self.tabela_produtos.column("quantidade", width=80)
        self.tabela_produtos.column("preco", width=80)
        self.tabela_produtos.column("descricao", width=300)
        
        # Scrollbar para a tabela
        self.produtos_scroll = ttk.Scrollbar(
            self.produtos_frame,
            orient=tk.VERTICAL,
            command=self.tabela_produtos.yview
        )
        self.tabela_produtos.configure(yscrollcommand=self.produtos_scroll.set)
        
        # Posicionar a tabela e a scrollbar
        self.tabela_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.produtos_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_frame = tk.Frame(self.frame)
        self.status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Desconectado",
            font=("Arial", 10),
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)
        
        # Desabilita os campos de cadastro até que a conexão seja estabelecida
        self.desabilitar_campos()
    
    def desabilitar_campos(self):
        # Desabilita os campos de cadastro
        self.nome_entry.config(state=tk.DISABLED)
        self.categoria_combo.config(state=tk.DISABLED)
        self.qtd_entry.config(state=tk.DISABLED)
        self.preco_entry.config(state=tk.DISABLED)
        self.descricao_text.config(state=tk.DISABLED)
        self.btn_limpar.config(state=tk.DISABLED)
        self.btn_cadastrar.config(state=tk.DISABLED)
    
    def habilitar_campos(self):
        # Habilita os campos de cadastro
        self.nome_entry.config(state=tk.NORMAL)
        self.categoria_combo.config(state="readonly")
        self.qtd_entry.config(state=tk.NORMAL)
        self.preco_entry.config(state=tk.NORMAL)
        self.descricao_text.config(state=tk.NORMAL)
        self.btn_limpar.config(state=tk.NORMAL)
        self.btn_cadastrar.config(state=tk.NORMAL)
    
    def conectar_bd(self):
        # Atualiza as configurações de conexão
        self.config_db["host"] = self.host_var.get()
        self.config_db["user"] = self.user_var.get()
        self.config_db["password"] = self.password_var.get()
        self.config_db["database"] = self.database_var.get()
        
        try:
            # Tenta estabelecer a conexão
            self.conexao = mysql.connector.connect(
                host=self.config_db["host"],
                user=self.config_db["user"],
                password=self.config_db["password"],
                database=self.config_db["database"]
            )
            
            # Verifica se a conexão foi bem-sucedida
            if self.conexao.is_connected():
                # Cria as tabelas necessárias
                self.criar_tabelas()
                
                # Carrega as categorias
                self.carregar_categorias()
                
                # Habilita os campos de cadastro
                self.habilitar_campos()
                
                # Atualiza a interface
                self.mostrar_mensagem("Conexão estabelecida com sucesso!", "success")
                self.status_label.config(text=f"Conectado a {self.config_db['database']} em {self.config_db['host']}")
                
                # Carrega os produtos na tabela
                self.carregar_produtos()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao conectar ao banco de dados: {str(e)}", "error")
    
    def criar_tabelas(self):
        try:
            cursor = self.conexao.cursor()
            
            # SQL para criar a tabela de categorias
            sql_criar_categorias = """
            CREATE TABLE IF NOT EXISTS categorias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE
            )
            """
            
            # SQL para criar a tabela de produtos
            sql_criar_produtos = """
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                categoria_id INT,
                quantidade INT NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                descricao TEXT,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
            """
            
            cursor.execute(sql_criar_categorias)
            cursor.execute(sql_criar_produtos)
            
            # Insere algumas categorias padrão se não existirem
            categorias_padrao = ["Eletrônicos", "Alimentos", "Vestuário", "Livros", "Outros"]
            
            for categoria in categorias_padrao:
                try:
                    sql_inserir_categoria = "INSERT IGNORE INTO categorias (nome) VALUES (%s)"
                    cursor.execute(sql_inserir_categoria, (categoria,))
                except:
                    pass  # Ignora se a categoria já existir
            
            self.conexao.commit()
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao criar tabelas: {str(e)}", "error")
    
    def carregar_categorias(self):
        try:
            cursor = self.conexao.cursor()
            
            # SQL para selecionar todas as categorias
            sql_selecionar = "SELECT id, nome FROM categorias ORDER BY nome"
            
            cursor.execute(sql_selecionar)
            categorias = cursor.fetchall()
            
            # Limpa a lista de categorias
            self.categorias = []
            
            # Adiciona as categorias à lista
            for categoria in categorias:
                self.categorias.append({"id": categoria[0], "nome": categoria[1]})
            
            # Atualiza o combobox
            self.categoria_combo["values"] = [categoria["nome"] for categoria in self.categorias]
            
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao carregar categorias: {str(e)}", "error")
    
    def carregar_produtos(self):
        try:
            cursor = self.conexao.cursor()
            
            # SQL para selecionar todos os produtos com suas categorias
            sql_selecionar = """
            SELECT p.id, p.nome, c.nome, p.quantidade, p.preco, p.descricao
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            ORDER BY p.id DESC
            """
            
            cursor.execute(sql_selecionar)
            produtos = cursor.fetchall()
            
            # Limpa a tabela
            for item in self.tabela_produtos.get_children():
                self.tabela_produtos.delete(item)
            
            # Adiciona os produtos à tabela
            for produto in produtos:
                # Destaca produtos com quantidade abaixo de 5
                if produto[3] < 5:
                    self.tabela_produtos.insert("", tk.END, values=produto, tags=("pouco_estoque",))
                else:
                    self.tabela_produtos.insert("", tk.END, values=produto)
            
            # Configura a tag para destacar produtos com pouco estoque
            self.tabela_produtos.tag_configure("pouco_estoque", foreground="red")
            
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao carregar produtos: {str(e)}", "error")
    
    def limpar_cadastro(self):
        self.nome_var.set("")
        self.categoria_var.set("")
        self.qtd_var.set("")
        self.preco_var.set("")
        self.descricao_text.delete(1.0, tk.END)
        self.nome_entry.focus_set()
    
    def cadastrar_produto(self):
        # Obtém os valores dos campos
        nome = self.nome_var.get().strip()
        categoria = self.categoria_var.get()
        quantidade = self.qtd_var.get().strip()
        preco = self.preco_var.get().strip()
        descricao = self.descricao_text.get(1.0, tk.END).strip()
        
        # Validação dos campos
        if not self.validar_campos_produto(nome, categoria, quantidade, preco):
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # Obtém o ID da categoria selecionada
            categoria_id = None
            for cat in self.categorias:
                if cat["nome"] == categoria:
                    categoria_id = cat["id"]
                    break
            
            # SQL para inserir um produto
            sql_inserir = """
            INSERT INTO produtos (nome, categoria_id, quantidade, preco, descricao)
            VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nome, categoria_id, int(quantidade), float(preco), descricao)
            
            cursor.execute(sql_inserir, valores)
            self.conexao.commit()
            
            # Obtém o ID do produto inserido
            produto_id = cursor.lastrowid
            
            cursor.close()
            
            # Limpa os campos
            self.limpar_cadastro()
            
            # Recarrega os produtos
            self.carregar_produtos()
            
            self.mostrar_mensagem(f"Produto '{nome}' cadastrado com sucesso!", "success")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao cadastrar produto: {str(e)}", "error")
    
    def validar_campos_produto(self, nome, categoria, quantidade, preco):
        # Validação do nome
        if not nome:
            self.mostrar_mensagem("O campo Nome não pode estar vazio.", "error")
            self.nome_entry.focus_set()
            return False
        
        # Validação da categoria
        if not categoria:
            self.mostrar_mensagem("Selecione uma categoria.", "error")
            self.categoria_combo.focus_set()
            return False
        
        # Validação da quantidade
        if not quantidade:
            self.mostrar_mensagem("O campo Quantidade não pode estar vazio.", "error")
            self.qtd_entry.focus_set()
            return False
        
        try:
            qtd = int(quantidade)
            if qtd <= 0:
                self.mostrar_mensagem("A quantidade deve ser um número inteiro positivo.", "error")
                self.qtd_entry.focus_set()
                return False
        except ValueError:
            self.mostrar_mensagem("A quantidade deve ser um número inteiro.", "error")
            self.qtd_entry.focus_set()
            return False
        
        # Validação do preço
        if not preco:
            self.mostrar_mensagem("O campo Preço não pode estar vazio.", "error")
            self.preco_entry.focus_set()
            return False
        
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                self.mostrar_mensagem("O preço deve ser um número positivo.", "error")
                self.preco_entry.focus_set()
                return False
        except ValueError:
            self.mostrar_mensagem("O preço deve ser um número válido.", "error")
            self.preco_entry.focus_set()
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroProdutos(root)
    root.mainloop()

