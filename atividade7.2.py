#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox, filedialog
import os

class GeradorListaTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Lista de Tarefas")
        self.root.geometry("600x500")
        
        # Variável para armazenar o caminho do arquivo atual
        self.arquivo_atual = None
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Lista de Tarefas",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Frame para adicionar tarefas
        self.add_frame = tk.Frame(self.frame)
        self.add_frame.pack(fill=tk.X, pady=10)
        
        # Label e entrada para nova tarefa
        self.tarefa_label = tk.Label(
            self.add_frame,
            text="Nova Tarefa:",
            font=("Arial", 12)
        )
        self.tarefa_label.pack(side=tk.LEFT, padx=5)
        
        self.tarefa_var = tk.StringVar()
        self.tarefa_entry = tk.Entry(
            self.add_frame,
            textvariable=self.tarefa_var,
            font=("Arial", 12),
            width=40
        )
        self.tarefa_entry.pack(side=tk.LEFT, padx=5)
        
        # Botão para adicionar tarefa
        self.btn_adicionar = tk.Button(
            self.add_frame,
            text="Adicionar",
            font=("Arial", 12),
            command=self.adicionar_tarefa
        )
        self.btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        # Frame para a lista de tarefas
        self.lista_frame = tk.LabelFrame(
            self.frame,
            text="Tarefas",
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.lista_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Widget Text para exibir as tarefas
        self.lista_text = tk.Text(
            self.lista_frame,
            font=("Arial", 12),
            wrap=tk.WORD,
            selectbackground="#a6a6a6"
        )
        self.lista_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar para a lista
        self.scrollbar = tk.Scrollbar(self.lista_frame)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        
        # Configurar a scrollbar
        self.lista_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_text.yview)
        
        # Frame para os botões de arquivo
        self.arquivo_frame = tk.Frame(self.frame)
        self.arquivo_frame.pack(fill=tk.X, pady=10)
        
        # Botões para manipulação de arquivos
        self.btn_novo = tk.Button(
            self.arquivo_frame,
            text="Nova Lista",
            font=("Arial", 12),
            width=10,
            command=self.nova_lista
        )
        self.btn_novo.grid(row=0, column=0, padx=5)
        
        self.btn_abrir = tk.Button(
            self.arquivo_frame,
            text="Abrir",
            font=("Arial", 12),
            width=10,
            command=self.abrir_arquivo
        )
        self.btn_abrir.grid(row=0, column=1, padx=5)
        
        self.btn_salvar = tk.Button(
            self.arquivo_frame,
            text="Salvar",
            font=("Arial", 12),
            width=10,
            command=self.salvar_arquivo
        )
        self.btn_salvar.grid(row=0, column=2, padx=5)
        
        self.btn_salvar_como = tk.Button(
            self.arquivo_frame,
            text="Salvar Como",
            font=("Arial", 12),
            width=10,
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
        
        # Bind para adicionar tarefa ao pressionar Enter
        self.tarefa_entry.bind("<Return>", lambda event: self.adicionar_tarefa())
        
        # Foco inicial no campo de entrada
        self.tarefa_entry.focus_set()
        
    def adicionar_tarefa(self):
        tarefa = self.tarefa_var.get().strip()
        
        if not tarefa:
            messagebox.showwarning("Aviso", "Por favor, digite uma tarefa.")
            return
        
        # Adiciona a tarefa à lista
        self.lista_text.insert(tk.END, f"□ {tarefa}\n")
        
        # Limpa o campo de entrada
        self.tarefa_var.set("")
        self.tarefa_entry.focus_set()
    
    def nova_lista(self):
        # Verifica se há conteúdo não salvo
        if self.lista_text.get(1.0, tk.END).strip() and messagebox.askyesno(
            "Nova Lista", "Deseja criar uma nova lista? O conteúdo atual será perdido."
        ):
            self.lista_text.delete(1.0, tk.END)
            self.arquivo_atual = None
            self.atualizar_titulo()
    
    def abrir_arquivo(self):
        # Verifica se há conteúdo não salvo
        if self.lista_text.get(1.0, tk.END).strip() and not messagebox.askyesno(
            "Abrir Arquivo", "O conteúdo atual será perdido. Deseja continuar?"
        ):
            return
        
        # Abre o diálogo para selecionar o arquivo
        arquivo = filedialog.askopenfilename(
            title="Abrir Lista de Tarefas",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Abre o arquivo e carrega o conteúdo
                with open(arquivo, "r", encoding="utf-8") as f:
                    conteudo = f.read()
                
                # Limpa a lista atual e insere o conteúdo do arquivo
                self.lista_text.delete(1.0, tk.END)
                self.lista_text.insert(tk.END, conteudo)
                
                # Atualiza o arquivo atual
                self.arquivo_atual = arquivo
                self.atualizar_titulo()
                
                messagebox.showinfo("Sucesso", f"Arquivo '{os.path.basename(arquivo)}' aberto com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {str(e)}")
    
    def salvar_arquivo(self):
        # Se não houver arquivo atual, usa "Salvar Como"
        if not self.arquivo_atual:
            self.salvar_como()
        else:
            try:
                # Salva o conteúdo no arquivo atual
                with open(self.arquivo_atual, "w", encoding="utf-8") as f:
                    conteudo = self.lista_text.get(1.0, tk.END)
                    f.write(conteudo)
                
                messagebox.showinfo("Sucesso", f"Lista salva em '{os.path.basename(self.arquivo_atual)}'!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")
    
    def salvar_como(self):
        # Abre o diálogo para selecionar o arquivo
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Lista de Tarefas",
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Salva o conteúdo no arquivo selecionado
                with open(arquivo, "w", encoding="utf-8") as f:
                    conteudo = self.lista_text.get(1.0, tk.END)
                    f.write(conteudo)
                
                # Atualiza o arquivo atual
                self.arquivo_atual = arquivo
                self.atualizar_titulo()
                
                messagebox.showinfo("Sucesso", f"Lista salva em '{os.path.basename(arquivo)}'!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {str(e)}")
    
    def atualizar_titulo(self):
        # Atualiza o título da janela e o label de arquivo
        if self.arquivo_atual:
            nome_arquivo = os.path.basename(self.arquivo_atual)
            self.root.title(f"Lista de Tarefas - {nome_arquivo}")
            self.arquivo_label.config(text=f"Arquivo: {nome_arquivo}")
        else:
            self.root.title("Lista de Tarefas")
            self.arquivo_label.config(text="Nenhum arquivo aberto")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorListaTarefas(root)
    root.mainloop()

