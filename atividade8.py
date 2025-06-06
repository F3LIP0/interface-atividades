#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class IntegracaoMySQL:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gerenciamento de Produtos")
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
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Sistema de Gerenciamento de Produtos",
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
        
        # Notebook para as operações
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tab para cadastrar produtos
        self.tab_cadastrar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cadastrar, text="Cadastrar Produto")
        
        # Tab para buscar produtos
        self.tab_buscar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_buscar, text="Buscar Produtos")
        
        # Tab para atualizar produtos
        self.tab_atualizar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_atualizar, text="Atualizar Produto")
        
        # Tab para excluir produtos
        self.tab_excluir = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_excluir, text="Excluir Produto")
        
        # Inicializa as tabs
        self.inicializar_tab_cadastrar()
        self.inicializar_tab_buscar()
        self.inicializar_tab_atualizar()
        self.inicializar_tab_excluir()
        
        # Desabilita as tabs até que a conexão seja estabelecida
        self.notebook.tab(0, state="disabled")
        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")
        self.notebook.tab(3, state="disabled")
        
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
    
    def inicializar_tab_cadastrar(self):
        # Frame para o formulário de cadastro
        self.cadastro_frame = tk.Frame(self.tab_cadastrar, padx=20, pady=20)
        self.cadastro_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de título
        self.cadastro_titulo = tk.Label(
            self.cadastro_frame,
            text="Cadastrar Novo Produto",
            font=("Arial", 14, "bold")
        )
        self.cadastro_titulo.pack(pady=10)
        
        # Frame para os campos do formulário
        self.cadastro_form = tk.Frame(self.cadastro_frame)
        self.cadastro_form.pack(fill=tk.X, pady=10)
        
        # Campo Nome
        self.nome_label = tk.Label(
            self.cadastro_form,
            text="Nome:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.nome_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(
            self.cadastro_form,
            textvariable=self.nome_var,
            font=("Arial", 12),
            width=30
        )
        self.nome_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Quantidade
        self.qtd_label = tk.Label(
            self.cadastro_form,
            text="Quantidade:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.qtd_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.qtd_var = tk.StringVar()
        self.qtd_entry = tk.Entry(
            self.cadastro_form,
            textvariable=self.qtd_var,
            font=("Arial", 12),
            width=10
        )
        self.qtd_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo Preço
        self.preco_label = tk.Label(
            self.cadastro_form,
            text="Preço:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.preco_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.preco_var = tk.StringVar()
        self.preco_entry = tk.Entry(
            self.cadastro_form,
            textvariable=self.preco_var,
            font=("Arial", 12),
            width=10
        )
        self.preco_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Botões
        self.cadastro_botoes = tk.Frame(self.cadastro_frame)
        self.cadastro_botoes.pack(pady=10)
        
        self.btn_limpar_cadastro = tk.Button(
            self.cadastro_botoes,
            text="Limpar",
            font=("Arial", 12),
            width=10,
            command=self.limpar_cadastro
        )
        self.btn_limpar_cadastro.grid(row=0, column=0, padx=5)
        
        self.btn_cadastrar_produto = tk.Button(
            self.cadastro_botoes,
            text="Cadastrar",
            font=("Arial", 12),
            width=10,
            bg="#90EE90",
            command=self.cadastrar_produto
        )
        self.btn_cadastrar_produto.grid(row=0, column=1, padx=5)
        
        # Frame para exibir os produtos cadastrados
        self.produtos_frame = tk.LabelFrame(
            self.cadastro_frame,
            text="Produtos Cadastrados",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.produtos_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabela para exibir os produtos
        self.colunas_produtos = ("id", "nome", "quantidade", "preco")
        self.tabela_produtos = ttk.Treeview(
            self.produtos_frame,
            columns=self.colunas_produtos,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar as colunas
        self.tabela_produtos.heading("id", text="ID")
        self.tabela_produtos.heading("nome", text="Nome")
        self.tabela_produtos.heading("quantidade", text="Quantidade")
        self.tabela_produtos.heading("preco", text="Preço")
        
        self.tabela_produtos.column("id", width=50)
        self.tabela_produtos.column("nome", width=250)
        self.tabela_produtos.column("quantidade", width=100)
        self.tabela_produtos.column("preco", width=100)
        
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
    
    def inicializar_tab_buscar(self):
        # Frame para a busca de produtos
        self.busca_frame = tk.Frame(self.tab_buscar, padx=20, pady=20)
        self.busca_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de título
        self.busca_titulo = tk.Label(
            self.busca_frame,
            text="Buscar Produtos",
            font=("Arial", 14, "bold")
        )
        self.busca_titulo.pack(pady=10)
        
        # Frame para os campos de busca
        self.busca_form = tk.Frame(self.busca_frame)
        self.busca_form.pack(fill=tk.X, pady=10)
        
        # Campo de busca
        self.busca_label = tk.Label(
            self.busca_form,
            text="Buscar por:",
            font=("Arial", 12)
        )
        self.busca_label.grid(row=0, column=0, padx=5)
        
        self.busca_var = tk.StringVar()
        self.busca_entry = tk.Entry(
            self.busca_form,
            textvariable=self.busca_var,
            font=("Arial", 12),
            width=30
        )
        self.busca_entry.grid(row=0, column=1, padx=5)
        
        # Combobox para o tipo de busca
        self.tipo_busca_label = tk.Label(
            self.busca_form,
            text="Tipo:",
            font=("Arial", 12)
        )
        self.tipo_busca_label.grid(row=0, column=2, padx=5)
        
        self.tipo_busca_var = tk.StringVar()
        self.tipo_busca_combo = ttk.Combobox(
            self.busca_form,
            textvariable=self.tipo_busca_var,
            font=("Arial", 12),
            width=15,
            state="readonly"
        )
        self.tipo_busca_combo["values"] = ("ID", "Nome", "Todos")
        self.tipo_busca_combo.current(1)  # Seleciona "Nome" por padrão
        self.tipo_busca_combo.grid(row=0, column=3, padx=5)
        
        # Botão de busca
        self.btn_buscar = tk.Button(
            self.busca_form,
            text="Buscar",
            font=("Arial", 12),
            width=10,
            command=self.buscar_produtos
        )
        self.btn_buscar.grid(row=0, column=4, padx=5)
        
        # Frame para exibir os resultados da busca
        self.resultados_frame = tk.LabelFrame(
            self.busca_frame,
            text="Resultados da Busca",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabela para exibir os resultados
        self.colunas_resultados = ("id", "nome", "quantidade", "preco")
        self.tabela_resultados = ttk.Treeview(
            self.resultados_frame,
            columns=self.colunas_resultados,
            show="headings",
            selectmode="browse"
        )
        
        # Configurar as colunas
        self.tabela_resultados.heading("id", text="ID")
        self.tabela_resultados.heading("nome", text="Nome")
        self.tabela_resultados.heading("quantidade", text="Quantidade")
        self.tabela_resultados.heading("preco", text="Preço")
        
        self.tabela_resultados.column("id", width=50)
        self.tabela_resultados.column("nome", width=250)
        self.tabela_resultados.column("quantidade", width=100)
        self.tabela_resultados.column("preco", width=100)
        
        # Scrollbar para a tabela
        self.resultados_scroll = ttk.Scrollbar(
            self.resultados_frame,
            orient=tk.VERTICAL,
            command=self.tabela_resultados.yview
        )
        self.tabela_resultados.configure(yscrollcommand=self.resultados_scroll.set)
        
        # Posicionar a tabela e a scrollbar
        self.tabela_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.resultados_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def inicializar_tab_atualizar(self):
        # Frame para atualização de produtos
        self.atualizar_frame = tk.Frame(self.tab_atualizar, padx=20, pady=20)
        self.atualizar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de título
        self.atualizar_titulo = tk.Label(
            self.atualizar_frame,
            text="Atualizar Produto",
            font=("Arial", 14, "bold")
        )
        self.atualizar_titulo.pack(pady=10)
        
        # Frame para busca do produto a ser atualizado
        self.atualizar_busca_frame = tk.Frame(self.atualizar_frame)
        self.atualizar_busca_frame.pack(fill=tk.X, pady=10)
        
        # Campo ID do produto
        self.atualizar_id_label = tk.Label(
            self.atualizar_busca_frame,
            text="ID do Produto:",
            font=("Arial", 12)
        )
        self.atualizar_id_label.grid(row=0, column=0, padx=5)
        
        self.atualizar_id_var = tk.StringVar()
        self.atualizar_id_entry = tk.Entry(
            self.atualizar_busca_frame,
            textvariable=self.atualizar_id_var,
            font=("Arial", 12),
            width=10
        )
        self.atualizar_id_entry.grid(row=0, column=1, padx=5)
        
        # Botão para buscar o produto
        self.btn_buscar_atualizar = tk.Button(
            self.atualizar_busca_frame,
            text="Buscar",
            font=("Arial", 12),
            width=10,
            command=self.buscar_produto_atualizar
        )
        self.btn_buscar_atualizar.grid(row=0, column=2, padx=5)
        
        # Frame para o formulário de atualização
        self.atualizar_form = tk.LabelFrame(
            self.atualizar_frame,
            text="Dados do Produto",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.atualizar_form.pack(fill=tk.X, pady=10)
        
        # Campo Nome (somente leitura)
        self.atualizar_nome_label = tk.Label(
            self.atualizar_form,
            text="Nome:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.atualizar_nome_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.atualizar_nome_var = tk.StringVar()
        self.atualizar_nome_entry = tk.Entry(
            self.atualizar_form,
            textvariable=self.atualizar_nome_var,
            font=("Arial", 12),
            width=30,
            state="readonly"
        )
        self.atualizar_nome_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Quantidade
        self.atualizar_qtd_label = tk.Label(
            self.atualizar_form,
            text="Quantidade:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.atualizar_qtd_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.atualizar_qtd_var = tk.StringVar()
        self.atualizar_qtd_entry = tk.Entry(
            self.atualizar_form,
            textvariable=self.atualizar_qtd_var,
            font=("Arial", 12),
            width=10
        )
        self.atualizar_qtd_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo Preço
        self.atualizar_preco_label = tk.Label(
            self.atualizar_form,
            text="Preço:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.atualizar_preco_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.atualizar_preco_var = tk.StringVar()
        self.atualizar_preco_entry = tk.Entry(
            self.atualizar_form,
            textvariable=self.atualizar_preco_var,
            font=("Arial", 12),
            width=10
        )
        self.atualizar_preco_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Botão para atualizar o produto
        self.btn_atualizar_produto = tk.Button(
            self.atualizar_form,
            text="Atualizar",
            font=("Arial", 12),
            width=10,
            bg="#90EE90",
            command=self.atualizar_produto,
            state=tk.DISABLED
        )
        self.btn_atualizar_produto.grid(row=3, column=1, sticky=tk.W, pady=10)
    
    def inicializar_tab_excluir(self):
        # Frame para exclusão de produtos
        self.excluir_frame = tk.Frame(self.tab_excluir, padx=20, pady=20)
        self.excluir_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de título
        self.excluir_titulo = tk.Label(
            self.excluir_frame,
            text="Excluir Produto",
            font=("Arial", 14, "bold")
        )
        self.excluir_titulo.pack(pady=10)
        
        # Frame para busca do produto a ser excluído
        self.excluir_busca_frame = tk.Frame(self.excluir_frame)
        self.excluir_busca_frame.pack(fill=tk.X, pady=10)
        
        # Campo ID do produto
        self.excluir_id_label = tk.Label(
            self.excluir_busca_frame,
            text="ID do Produto:",
            font=("Arial", 12)
        )
        self.excluir_id_label.grid(row=0, column=0, padx=5)
        
        self.excluir_id_var = tk.StringVar()
        self.excluir_id_entry = tk.Entry(
            self.excluir_busca_frame,
            textvariable=self.excluir_id_var,
            font=("Arial", 12),
            width=10
        )
        self.excluir_id_entry.grid(row=0, column=1, padx=5)
        
        # Botão para buscar o produto
        self.btn_buscar_excluir = tk.Button(
            self.excluir_busca_frame,
            text="Buscar",
            font=("Arial", 12),
            width=10,
            command=self.buscar_produto_excluir
        )
        self.btn_buscar_excluir.grid(row=0, column=2, padx=5)
        
        # Frame para exibir os detalhes do produto
        self.excluir_detalhes_frame = tk.LabelFrame(
            self.excluir_frame,
            text="Detalhes do Produto",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.excluir_detalhes_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os detalhes
        self.excluir_detalhes_grid = tk.Frame(self.excluir_detalhes_frame)
        self.excluir_detalhes_grid.pack(fill=tk.X, pady=5)
        
        # Campo ID (somente leitura)
        self.excluir_id_info_label = tk.Label(
            self.excluir_detalhes_grid,
            text="ID:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.excluir_id_info_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.excluir_id_info_var = tk.StringVar()
        self.excluir_id_info_entry = tk.Entry(
            self.excluir_detalhes_grid,
            textvariable=self.excluir_id_info_var,
            font=("Arial", 12),
            width=10,
            state="readonly"
        )
        self.excluir_id_info_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Nome (somente leitura)
        self.excluir_nome_label = tk.Label(
            self.excluir_detalhes_grid,
            text="Nome:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.excluir_nome_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.excluir_nome_var = tk.StringVar()
        self.excluir_nome_entry = tk.Entry(
            self.excluir_detalhes_grid,
            textvariable=self.excluir_nome_var,
            font=("Arial", 12),
            width=30,
            state="readonly"
        )
        self.excluir_nome_entry.grid(row=1, column=1, sticky=tk.W)
        
        # Campo Quantidade (somente leitura)
        self.excluir_qtd_label = tk.Label(
            self.excluir_detalhes_grid,
            text="Quantidade:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.excluir_qtd_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.excluir_qtd_var = tk.StringVar()
        self.excluir_qtd_entry = tk.Entry(
            self.excluir_detalhes_grid,
            textvariable=self.excluir_qtd_var,
            font=("Arial", 12),
            width=10,
            state="readonly"
        )
        self.excluir_qtd_entry.grid(row=2, column=1, sticky=tk.W)
        
        # Campo Preço (somente leitura)
        self.excluir_preco_label = tk.Label(
            self.excluir_detalhes_grid,
            text="Preço:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.excluir_preco_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.excluir_preco_var = tk.StringVar()
        self.excluir_preco_entry = tk.Entry(
            self.excluir_detalhes_grid,
            textvariable=self.excluir_preco_var,
            font=("Arial", 12),
            width=10,
            state="readonly"
        )
        self.excluir_preco_entry.grid(row=3, column=1, sticky=tk.W)
        
        # Botão para excluir o produto
        self.btn_excluir_produto = tk.Button(
            self.excluir_detalhes_frame,
            text="Excluir",
            font=("Arial", 12),
            width=10,
            bg="#FF6B6B",
            command=self.excluir_produto,
            state=tk.DISABLED
        )
        self.btn_excluir_produto.pack(pady=10)
    
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
                # Cria a tabela de produtos se não existir
                self.criar_tabela_produtos()
                
                # Habilita as tabs
                self.notebook.tab(0, state="normal")
                self.notebook.tab(1, state="normal")
                self.notebook.tab(2, state="normal")
                self.notebook.tab(3, state="normal")
                
                # Atualiza a interface
                self.mostrar_mensagem("Conexão estabelecida com sucesso!", "success")
                self.status_label.config(text=f"Conectado a {self.config_db['database']} em {self.config_db['host']}")
                
                # Carrega os produtos na tabela
                self.carregar_produtos()
                
                # Seleciona a primeira tab
                self.notebook.select(0)
        except Error as e:
            self.mostrar_mensagem(f"Erro ao conectar ao banco de dados: {str(e)}", "error")
    
    def criar_tabela_produtos(self):
        try:
            cursor = self.conexao.cursor()
            
            # SQL para criar a tabela de produtos
            sql_criar_tabela = """
            CREATE TABLE IF NOT EXISTS produtos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                quantidade INT NOT NULL,
                preco DECIMAL(10, 2) NOT NULL
            )
            """
            
            cursor.execute(sql_criar_tabela)
            self.conexao.commit()
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao criar tabela: {str(e)}", "error")
    
    def carregar_produtos(self):
        try:
            cursor = self.conexao.cursor()
            
            # SQL para selecionar todos os produtos
            sql_selecionar = "SELECT id, nome, quantidade, preco FROM produtos"
            
            cursor.execute(sql_selecionar)
            produtos = cursor.fetchall()
            
            # Limpa a tabela
            for item in self.tabela_produtos.get_children():
                self.tabela_produtos.delete(item)
            
            # Adiciona os produtos à tabela
            for produto in produtos:
                self.tabela_produtos.insert("", tk.END, values=produto)
            
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao carregar produtos: {str(e)}", "error")
    
    def limpar_cadastro(self):
        self.nome_var.set("")
        self.qtd_var.set("")
        self.preco_var.set("")
        self.nome_entry.focus_set()
    
    def cadastrar_produto(self):
        # Obtém os valores dos campos
        nome = self.nome_var.get().strip()
        quantidade = self.qtd_var.get().strip()
        preco = self.preco_var.get().strip()
        
        # Validação dos campos
        if not self.validar_campos_produto(nome, quantidade, preco):
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para inserir um produto
            sql_inserir = "INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s)"
            valores = (nome, int(quantidade), float(preco))
            
            cursor.execute(sql_inserir, valores)
            self.conexao.commit()
            
            # Obtém o ID do produto inserido
            produto_id = cursor.lastrowid
            
            cursor.close()
            
            # Adiciona o produto à tabela
            self.tabela_produtos.insert("", tk.END, values=(produto_id, nome, quantidade, preco))
            
            # Limpa os campos
            self.limpar_cadastro()
            
            self.mostrar_mensagem(f"Produto '{nome}' cadastrado com sucesso!", "success")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao cadastrar produto: {str(e)}", "error")
    
    def validar_campos_produto(self, nome, quantidade, preco):
        # Validação do nome
        if not nome:
            self.mostrar_mensagem("O campo Nome não pode estar vazio.", "error")
            self.nome_entry.focus_set()
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
    
    def buscar_produtos(self):
        # Obtém os valores dos campos
        busca = self.busca_var.get().strip()
        tipo_busca = self.tipo_busca_var.get()
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para buscar produtos
            if tipo_busca == "ID":
                if not busca:
                    self.mostrar_mensagem("Digite um ID para buscar.", "error")
                    return
                
                try:
                    id_busca = int(busca)
                    sql_buscar = "SELECT id, nome, quantidade, preco FROM produtos WHERE id = %s"
                    valores = (id_busca,)
                except ValueError:
                    self.mostrar_mensagem("O ID deve ser um número inteiro.", "error")
                    return
            elif tipo_busca == "Nome":
                if not busca:
                    self.mostrar_mensagem("Digite um nome para buscar.", "error")
                    return
                
                sql_buscar = "SELECT id, nome, quantidade, preco FROM produtos WHERE nome LIKE %s"
                valores = (f"%{busca}%",)
            else:  # Todos
                sql_buscar = "SELECT id, nome, quantidade, preco FROM produtos"
                valores = ()
            
            cursor.execute(sql_buscar, valores)
            produtos = cursor.fetchall()
            
            # Limpa a tabela de resultados
            for item in self.tabela_resultados.get_children():
                self.tabela_resultados.delete(item)
            
            # Adiciona os produtos à tabela de resultados
            for produto in produtos:
                self.tabela_resultados.insert("", tk.END, values=produto)
            
            cursor.close()
            
            # Mostra mensagem com o número de resultados
            if produtos:
                self.mostrar_mensagem(f"{len(produtos)} produto(s) encontrado(s).", "success")
            else:
                self.mostrar_mensagem("Nenhum produto encontrado.", "warning")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao buscar produtos: {str(e)}", "error")
    
    def buscar_produto_atualizar(self):
        # Obtém o ID do produto
        id_produto = self.atualizar_id_var.get().strip()
        
        if not id_produto:
            self.mostrar_mensagem("Digite o ID do produto para buscar.", "error")
            return
        
        try:
            id_produto = int(id_produto)
        except ValueError:
            self.mostrar_mensagem("O ID deve ser um número inteiro.", "error")
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para buscar o produto pelo ID
            sql_buscar = "SELECT id, nome, quantidade, preco FROM produtos WHERE id = %s"
            valores = (id_produto,)
            
            cursor.execute(sql_buscar, valores)
            produto = cursor.fetchone()
            
            cursor.close()
            
            if produto:
                # Preenche os campos com os dados do produto
                self.atualizar_nome_var.set(produto[1])
                self.atualizar_qtd_var.set(produto[2])
                self.atualizar_preco_var.set(produto[3])
                
                # Habilita o botão de atualizar
                self.btn_atualizar_produto.config(state=tk.NORMAL)
                
                self.mostrar_mensagem(f"Produto encontrado: {produto[1]}", "success")
            else:
                # Limpa os campos
                self.atualizar_nome_var.set("")
                self.atualizar_qtd_var.set("")
                self.atualizar_preco_var.set("")
                
                # Desabilita o botão de atualizar
                self.btn_atualizar_produto.config(state=tk.DISABLED)
                
                self.mostrar_mensagem(f"Produto com ID {id_produto} não encontrado.", "warning")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao buscar produto: {str(e)}", "error")
    
    def atualizar_produto(self):
        # Obtém os valores dos campos
        id_produto = self.atualizar_id_var.get().strip()
        quantidade = self.atualizar_qtd_var.get().strip()
        preco = self.atualizar_preco_var.get().strip()
        
        # Validação dos campos
        if not self.validar_campos_atualizacao(quantidade, preco):
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para atualizar o produto
            sql_atualizar = "UPDATE produtos SET quantidade = %s, preco = %s WHERE id = %s"
            valores = (int(quantidade), float(preco), int(id_produto))
            
            cursor.execute(sql_atualizar, valores)
            self.conexao.commit()
            
            cursor.close()
            
            # Limpa os campos
            self.atualizar_id_var.set("")
            self.atualizar_nome_var.set("")
            self.atualizar_qtd_var.set("")
            self.atualizar_preco_var.set("")
            
            # Desabilita o botão de atualizar
            self.btn_atualizar_produto.config(state=tk.DISABLED)
            
            # Recarrega os produtos
            self.carregar_produtos()
            
            self.mostrar_mensagem(f"Produto com ID {id_produto} atualizado com sucesso!", "success")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao atualizar produto: {str(e)}", "error")
    
    def validar_campos_atualizacao(self, quantidade, preco):
        # Validação da quantidade
        if not quantidade:
            self.mostrar_mensagem("O campo Quantidade não pode estar vazio.", "error")
            self.atualizar_qtd_entry.focus_set()
            return False
        
        try:
            qtd = int(quantidade)
            if qtd <= 0:
                self.mostrar_mensagem("A quantidade deve ser um número inteiro positivo.", "error")
                self.atualizar_qtd_entry.focus_set()
                return False
        except ValueError:
            self.mostrar_mensagem("A quantidade deve ser um número inteiro.", "error")
            self.atualizar_qtd_entry.focus_set()
            return False
        
        # Validação do preço
        if not preco:
            self.mostrar_mensagem("O campo Preço não pode estar vazio.", "error")
            self.atualizar_preco_entry.focus_set()
            return False
        
        try:
            preco_float = float(preco)
            if preco_float <= 0:
                self.mostrar_mensagem("O preço deve ser um número positivo.", "error")
                self.atualizar_preco_entry.focus_set()
                return False
        except ValueError:
            self.mostrar_mensagem("O preço deve ser um número válido.", "error")
            self.atualizar_preco_entry.focus_set()
            return False
        
        return True
    
    def buscar_produto_excluir(self):
        # Obtém o ID do produto
        id_produto = self.excluir_id_var.get().strip()
        
        if not id_produto:
            self.mostrar_mensagem("Digite o ID do produto para buscar.", "error")
            return
        
        try:
            id_produto = int(id_produto)
        except ValueError:
            self.mostrar_mensagem("O ID deve ser um número inteiro.", "error")
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para buscar o produto pelo ID
            sql_buscar = "SELECT id, nome, quantidade, preco FROM produtos WHERE id = %s"
            valores = (id_produto,)
            
            cursor.execute(sql_buscar, valores)
            produto = cursor.fetchone()
            
            cursor.close()
            
            if produto:
                # Preenche os campos com os dados do produto
                self.excluir_id_info_var.set(produto[0])
                self.excluir_nome_var.set(produto[1])
                self.excluir_qtd_var.set(produto[2])
                self.excluir_preco_var.set(produto[3])
                
                # Habilita o botão de excluir
                self.btn_excluir_produto.config(state=tk.NORMAL)
                
                self.mostrar_mensagem(f"Produto encontrado: {produto[1]}", "success")
            else:
                # Limpa os campos
                self.excluir_id_info_var.set("")
                self.excluir_nome_var.set("")
                self.excluir_qtd_var.set("")
                self.excluir_preco_var.set("")
                
                # Desabilita o botão de excluir
                self.btn_excluir_produto.config(state=tk.DISABLED)
                
                self.mostrar_mensagem(f"Produto com ID {id_produto} não encontrado.", "warning")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao buscar produto: {str(e)}", "error")
    
    def excluir_produto(self):
        # Obtém o ID do produto
        id_produto = self.excluir_id_info_var.get().strip()
        nome_produto = self.excluir_nome_var.get()
        
        # Confirmação de exclusão
        if not messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto '{nome_produto}'?"):
            return
        
        try:
            cursor = self.conexao.cursor()
            
            # SQL para excluir o produto
            sql_excluir = "DELETE FROM produtos WHERE id = %s"
            valores = (id_produto,)
            
            cursor.execute(sql_excluir, valores)
            self.conexao.commit()
            
            cursor.close()
            
            # Limpa os campos
            self.excluir_id_var.set("")
            self.excluir_id_info_var.set("")
            self.excluir_nome_var.set("")
            self.excluir_qtd_var.set("")
            self.excluir_preco_var.set("")
            
            # Desabilita o botão de excluir
            self.btn_excluir_produto.config(state=tk.DISABLED)
            
            # Recarrega os produtos
            self.carregar_produtos()
            
            self.mostrar_mensagem(f"Produto '{nome_produto}' excluído com sucesso!", "success")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao excluir produto: {str(e)}", "error")
    
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
    app = IntegracaoMySQL(root)
    root.mainloop()

