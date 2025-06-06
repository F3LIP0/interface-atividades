#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import csv
import datetime
import os

class RelatoriosProdutos:
    def __init__(self, root):
        self.root = root
        self.root.title("Relatórios e Exportação de Dados")
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
        
        # Lista para armazenar os produtos filtrados
        self.produtos_filtrados = []
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Relatórios e Exportação de Dados",
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
        
        # Frame para os filtros de relatório
        self.filtro_frame = tk.LabelFrame(
            self.frame,
            text="Filtros de Relatório",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.filtro_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos de filtro
        self.filtro_grid = tk.Frame(self.filtro_frame)
        self.filtro_grid.pack(fill=tk.X, pady=5)
        
        # Campo Categoria
        self.filtro_categoria_label = tk.Label(
            self.filtro_grid,
            text="Categoria:",
            font=("Arial", 12),
            width=10,
            anchor=tk.W
        )
        self.filtro_categoria_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.filtro_categoria_var = tk.StringVar()
        self.filtro_categoria_combo = ttk.Combobox(
            self.filtro_grid,
            textvariable=self.filtro_categoria_var,
            font=("Arial", 12),
            width=20,
            state="readonly"
        )
        self.filtro_categoria_combo.grid(row=0, column=1, sticky=tk.W)
        
        # Botão para gerar relatório
        self.btn_gerar = tk.Button(
            self.filtro_frame,
            text="Gerar Relatório",
            font=("Arial", 12),
            width=15,
            command=self.gerar_relatorio
        )
        self.btn_gerar.grid(row=0, column=2, padx=20)
        
        # Botão para exportar dados
        self.btn_exportar = tk.Button(
            self.filtro_frame,
            text="Exportar CSV",
            font=("Arial", 12),
            width=15,
            command=self.exportar_csv
        )
        self.btn_exportar.grid(row=0, column=3, padx=20)
        
        # Frame para exibir os produtos
        self.produtos_frame = tk.LabelFrame(
            self.frame,
            text="Relatório de Produtos",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.produtos_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Tabela para exibir os produtos
        self.colunas_produtos = ("id", "nome", "categoria", "quantidade", "preco", "valor_total")
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
        self.tabela_produtos.heading("preco", text="Preço Unit.")
        self.tabela_produtos.heading("valor_total", text="Valor Total")
        
        self.tabela_produtos.column("id", width=50)
        self.tabela_produtos.column("nome", width=200)
        self.tabela_produtos.column("categoria", width=100)
        self.tabela_produtos.column("quantidade", width=80)
        self.tabela_produtos.column("preco", width=80)
        self.tabela_produtos.column("valor_total", width=100)
        
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
        
        # Frame para o resumo do relatório
        self.resumo_frame = tk.LabelFrame(
            self.frame,
            text="Resumo do Relatório",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.resumo_frame.pack(fill=tk.X, pady=10)
        
        # Grid para os campos de resumo
        self.resumo_grid = tk.Frame(self.resumo_frame)
        self.resumo_grid.pack(fill=tk.X, pady=5)
        
        # Total de produtos
        self.total_produtos_label = tk.Label(
            self.resumo_grid,
            text="Total de Produtos:",
            font=("Arial", 12),
            width=15,
            anchor=tk.W
        )
        self.total_produtos_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.total_produtos_var = tk.StringVar(value="0")
        self.total_produtos_entry = tk.Entry(
            self.resumo_grid,
            textvariable=self.total_produtos_var,
            font=("Arial", 12),
            width=10,
            state="readonly"
        )
        self.total_produtos_entry.grid(row=0, column=1, sticky=tk.W)
        
        # Total de itens
        self.total_itens_label = tk.Label(
            self.resumo_grid,
            text="Total de Itens:",
            font=("Arial", 12),
            width=15,
            anchor=tk.W
        )
        self.total_itens_label.grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        
        self.total_itens_var = tk.StringVar(value="0")
        self.total_itens_entry = tk.Entry(
            self.resumo_grid,
            textvariable=self.total_itens_var,
            font=("Arial", 12),
            width=10,
            state="readonly"
        )
        self.total_itens_entry.grid(row=0, column=3, sticky=tk.W)
        
        # Valor total do estoque
        self.valor_total_label = tk.Label(
            self.resumo_grid,
            text="Valor Total (R$):",
            font=("Arial", 12),
            width=15,
            anchor=tk.W
        )
        self.valor_total_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.valor_total_var = tk.StringVar(value="0.00")
        self.valor_total_entry = tk.Entry(
            self.resumo_grid,
            textvariable=self.valor_total_var,
            font=("Arial", 12, "bold"),
            width=10,
            state="readonly"
        )
        self.valor_total_entry.grid(row=1, column=1, sticky=tk.W)
        
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
        
        # Desabilita os campos de relatório até que a conexão seja estabelecida
        self.desabilitar_campos()
    
    def desabilitar_campos(self):
        # Desabilita os campos de relatório
        self.filtro_categoria_combo.config(state=tk.DISABLED)
        self.btn_gerar.config(state=tk.DISABLED)
        self.btn_exportar.config(state=tk.DISABLED)
    
    def habilitar_campos(self):
        # Habilita os campos de relatório
        self.filtro_categoria_combo.config(state="readonly")
        self.btn_gerar.config(state=tk.NORMAL)
        self.btn_exportar.config(state=tk.DISABLED)  # Será habilitado após gerar o relatório
    
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
                
                # Habilita os campos de relatório
                self.habilitar_campos()
                
                # Atualiza a interface
                self.mostrar_mensagem("Conexão estabelecida com sucesso!", "success")
                self.status_label.config(text=f"Conectado a {self.config_db['database']} em {self.config_db['host']}")
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
    
    def gerar_relatorio(self):
        # Obtém a categoria selecionada
        categoria = self.filtro_categoria_var.get()
        
        try:
            cursor = self.conexao.cursor()
            
            # Constrói a consulta SQL base
            sql_base = """
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
            """
            
            # Adiciona condição de filtro por categoria
            params = []
            
            if categoria and categoria != "Todas":
                sql_base += " AND c.nome = %s"
                params.append(categoria)
            
            # Consulta para buscar os produtos
            sql_buscar = f"""
            SELECT p.id, p.nome, c.nome, p.quantidade, p.preco, (p.quantidade * p.preco) as valor_total
            {sql_base}
            ORDER BY p.id
            """
            
            cursor.execute(sql_buscar, params)
            produtos = cursor.fetchall()
            
            # Armazena os produtos filtrados
            self.produtos_filtrados = produtos
            
            # Limpa a tabela
            for item in self.tabela_produtos.get_children():
                self.tabela_produtos.delete(item)
            
            # Adiciona os produtos à tabela
            total_produtos = 0
            total_itens = 0
            valor_total = 0.0
            
            for produto in produtos:
                # Adiciona o produto à tabela
                self.tabela_produtos.insert("", tk.END, values=produto)
                
                # Atualiza os totais
                total_produtos += 1
                total_itens += produto[3]  # quantidade
                valor_total += produto[5]  # valor_total
            
            # Atualiza os campos de resumo
            self.total_produtos_var.set(str(total_produtos))
            self.total_itens_var.set(str(total_itens))
            self.valor_total_var.set(f"{valor_total:.2f}")
            
            cursor.close()
            
            # Habilita o botão de exportar
            self.btn_exportar.config(state=tk.NORMAL)
            
            # Mostra mensagem com o número de resultados
            if total_produtos > 0:
                self.mostrar_mensagem(f"Relatório gerado com sucesso! {total_produtos} produto(s) encontrado(s).", "success")
            else:
                self.mostrar_mensagem("Nenhum produto encontrado para os filtros selecionados.", "warning")
        except Error as e:
            self.mostrar_mensagem(f"Erro ao gerar relatório: {str(e)}", "error")
    
    def exportar_csv(self):
        # Verifica se há produtos para exportar
        if not self.produtos_filtrados:
            self.mostrar_mensagem("Não há dados para exportar. Gere um relatório primeiro.", "warning")
            return
        
        try:
            # Gera o nome do arquivo com data e hora
            agora = datetime.datetime.now()
            nome_arquivo = f"relatorio_{agora.strftime('%Y-%m-%d_%H-%M')}.csv"
            
            # Abre o diálogo para selecionar o local de salvamento
            arquivo = filedialog.asksaveasfilename(
                title="Salvar Relatório",
                initialfile=nome_arquivo,
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os Arquivos", "*.*")]
            )
            
            if not arquivo:
                return
            
            # Escreve os dados no arquivo CSV
            with open(arquivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                
                # Escreve o cabeçalho
                escritor.writerow(["ID", "Nome", "Categoria", "Quantidade", "Preço Unitário", "Valor Total"])
                
                # Escreve os dados dos produtos
                for produto in self.produtos_filtrados:
                    escritor.writerow(produto)
                
                # Escreve uma linha em branco
                escritor.writerow([])
                
                # Escreve o resumo
                escritor.writerow(["Resumo do Relatório"])
                escritor.writerow(["Total de Produtos", self.total_produtos_var.get()])
                escritor.writerow(["Total de Itens", self.total_itens_var.get()])
                escritor.writerow(["Valor Total (R$)", self.valor_total_var.get()])
            
            self.mostrar_mensagem(f"Relatório exportado com sucesso para '{os.path.basename(arquivo)}'!", "success")
        except Exception as e:
            self.mostrar_mensagem(f"Erro ao exportar relatório: {str(e)}", "error")
    
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
    app = RelatoriosProdutos(root)
    root.mainloop()

