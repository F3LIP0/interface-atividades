#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import math

class ConsultaProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Consulta de Produtos")
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
        
        # Variáveis para paginação
        self.pagina_atual = 1
        self.itens_por_pagina = 10
        self.total_paginas = 1
        self.total_produtos = 0
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Consulta de Produtos",
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
        
        # Frame para os filtros de busca
        self.filtro_frame = tk.LabelFrame(
            self.frame,
            text="Filtros de Busca",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.filtro_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos de filtro
        self.filtro_grid = tk.Frame(self.filtro_frame)
        self.filtro_grid.pack(fill=tk.X, pady=5)
        
        # Campo de busca
        self.busca_label = tk.Label(
            self.filtro_grid,
            text="Buscar:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.busca_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.busca_var = tk.StringVar()
        self.busca_entry = tk.Entry(
            self.filtro_grid,
            textvariable=self.busca_var,
            font=("Arial", 12),
            width=30
        )
        self.busca_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Campo Categoria
        self.filtro_categoria_label = tk.Label(
            self.filtro_grid,
            text="Categoria:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.filtro_categoria_label.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.filtro_categoria_var = tk.StringVar()
        self.filtro_categoria_combo = ttk.Combobox(
            self.filtro_grid,
            textvariable=self.filtro_categoria_var,
            font=("Arial", 12),
            width=20,
            state="readonly"
        )
        self.filtro_categoria_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Botão para buscar
        self.btn_buscar = tk.Button(
            self.filtro_frame,
            text="Buscar",
            font=("Arial", 12),
            width=15,
            command=self.buscar_produtos
        )
        self.btn_buscar.pack(pady=10)
        
        # Frame para exibir os produtos
        self.produtos_frame = tk.LabelFrame(
            self.frame,
            text="Produtos",
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
        
        # Frame para paginação
        self.paginacao_frame = tk.Frame(self.frame)
        self.paginacao_frame.pack(fill=tk.X, pady=10)
        
        # Botão para página anterior
        self.btn_anterior = tk.Button(
            self.paginacao_frame,
            text="< Anterior",
            font=("Arial", 12),
            width=10,
            command=self.pagina_anterior
        )
        self.btn_anterior.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar a página atual
        self.pagina_label = tk.Label(
            self.paginacao_frame,
            text="Página 1 de 1",
            font=("Arial", 12)
        )
        self.pagina_label.pack(side=tk.LEFT, padx=5)
        
        # Botão para próxima página
        self.btn_proxima = tk.Button(
            self.paginacao_frame,
            text="Próxima >",
            font=("Arial", 12),
            width=10,
            command=self.proxima_pagina
        )
        self.btn_proxima.pack(side=tk.LEFT, padx=5)
        
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
        
        # Desabilita os campos de busca até que a conexão seja estabelecida
        self.desabilitar_campos()
    
    def desabilitar_campos(self):
        # Desabilita os campos de busca
        self.busca_entry.config(state=tk.DISABLED)
        self.filtro_categoria_combo.config(state=tk.DISABLED)
        self.btn_buscar.config(state=tk.DISABLED)
        self.btn_anterior.config(state=tk.DISABLED)
        self.btn_proxima.config(state=tk.DISABLED)
    
    def habilitar_campos(self):
        # Habilita os campos de busca
        self.busca_entry.config(state=tk.NORMAL)
        self.filtro_categoria_combo.config(state="readonly")
        self.btn_buscar.config(state=tk.NORMAL)
        self.atualizar_botoes_paginacao()
    
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
                # Carrega as categorias
                self.carregar_categorias()
                
                # Habilita os campos de busca
                self.habilitar_campos()
                
                # Atualiza a interface
                self.mostrar_mensagem("Conexão estabelecida com sucesso!", "success")
                self.status_label.config(text=f"Conectado a {self.config_db['database']} em {self.config_db['host']}")
                
                # Carrega os produtos na tabela
                self.buscar_produtos()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao conectar ao banco de dados: {str(e)}", "error")
    
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
            
            # Adiciona a opção "Todas" no início
            valores_combo = ["Todas"]
            valores_combo.extend([categoria["nome"] for categoria in self.categorias])
            
            # Atualiza o combobox
            self.filtro_categoria_combo["values"] = valores_combo
            self.filtro_categoria_combo.current(0)  # Seleciona "Todas" por padrão
            
            cursor.close()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao carregar categorias: {str(e)}", "error")
    
    def buscar_produtos(self):
        # Reseta a paginação
        self.pagina_atual = 1
        
        # Obtém os valores dos filtros
        busca = self.busca_var.get().strip()
        categoria = self.filtro_categoria_var.get()
        
        try:
            cursor = self.conexao.cursor()
            
            # Constrói a consulta SQL base
            sql_base = """
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
            """
            
            # Adiciona condições de filtro
            params = []
            
            if busca:
                sql_base += " AND p.nome LIKE %s"
                params.append(f"%{busca}%")
            
            if categoria and categoria != "Todas":
                sql_base += " AND c.nome = %s"
                params.append(categoria)
            
            # Consulta para contar o total de produtos
            sql_contar = f"SELECT COUNT(*) {sql_base}"
            
            cursor.execute(sql_contar, params)
            self.total_produtos = cursor.fetchone()[0]
            
            # Calcula o total de páginas
            self.total_paginas = math.ceil(self.total_produtos / self.itens_por_pagina)
            if self.total_paginas < 1:
                self.total_paginas = 1
            
            # Atualiza o label de paginação
            self.atualizar_label_paginacao()
            
            # Consulta para buscar os produtos da página atual
            offset = (self.pagina_atual - 1) * self.itens_por_pagina
            
            sql_buscar = f"""
            SELECT p.id, p.nome, c.nome, p.quantidade, p.preco, p.descricao
            {sql_base}
            ORDER BY p.id DESC
            LIMIT {self.itens_por_pagina} OFFSET {offset}
            """
            
            cursor.execute(sql_buscar, params)
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
            
            # Atualiza os botões de paginação
            self.atualizar_botoes_paginacao()
            
            # Mostra mensagem com o número de resultados
            if self.total_produtos > 0:
                self.mostrar_mensagem(f"{self.total_produtos} produto(s) encontrado(s).", "success")
            else:
                self.mostrar_mensagem("Nenhum produto encontrado.", "warning")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao buscar produtos: {str(e)}", "error")
    
    def pagina_anterior(self):
        if self.pagina_atual > 1:
            self.pagina_atual -= 1
            self.carregar_pagina()
    
    def proxima_pagina(self):
        if self.pagina_atual < self.total_paginas:
            self.pagina_atual += 1
            self.carregar_pagina()
    
    def carregar_pagina(self):
        # Obtém os valores dos filtros
        busca = self.busca_var.get().strip()
        categoria = self.filtro_categoria_var.get()
        
        try:
            cursor = self.conexao.cursor()
            
            # Constrói a consulta SQL base
            sql_base = """
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
            """
            
            # Adiciona condições de filtro
            params = []
            
            if busca:
                sql_base += " AND p.nome LIKE %s"
                params.append(f"%{busca}%")
            
            if categoria and categoria != "Todas":
                sql_base += " AND c.nome = %s"
                params.append(categoria)
            
            # Consulta para buscar os produtos da página atual
            offset = (self.pagina_atual - 1) * self.itens_por_pagina
            
            sql_buscar = f"""
            SELECT p.id, p.nome, c.nome, p.quantidade, p.preco, p.descricao
            {sql_base}
            ORDER BY p.id DESC
            LIMIT {self.itens_por_pagina} OFFSET {offset}
            """
            
            cursor.execute(sql_buscar, params)
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
            
            cursor.close()
            
            # Atualiza o label de paginação
            self.atualizar_label_paginacao()
            
            # Atualiza os botões de paginação
            self.atualizar_botoes_paginacao()
        except Error as e:
            self.mostrar_mensagem(f"Erro ao carregar página: {str(e)}", "error")
    
    def atualizar_label_paginacao(self):
        self.pagina_label.config(text=f"Página {self.pagina_atual} de {self.total_paginas}")
    
    def atualizar_botoes_paginacao(self):
        # Habilita/desabilita os botões de paginação conforme necessário
        if self.pagina_atual <= 1:
            self.btn_anterior.config(state=tk.DISABLED)
        else:
            self.btn_anterior.config(state=tk.NORMAL)
        
        if self.pagina_atual >= self.total_paginas:
            self.btn_proxima.config(state=tk.DISABLED)
        else:
            self.btn_proxima.config(state=tk.NORMAL)
    
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
    app = ConsultaProdutos(root)
    root.mainloop()

