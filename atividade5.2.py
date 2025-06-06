#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

class JogoContador:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo do Contador")
        self.root.geometry("400x300")
        
        # Variável para armazenar o valor do contador
        self.contador = 0
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Jogo do Contador",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Label para mostrar o valor do contador
        self.valor_label = tk.Label(
            self.frame,
            text="0",
            font=("Arial", 36, "bold"),
            width=5,
            height=1,
            relief=tk.RIDGE,
            bg="#f0f0f0"
        )
        self.valor_label.pack(pady=20)
        
        # Frame para os botões
        self.botoes_frame = tk.Frame(self.frame)
        self.botoes_frame.pack(pady=10)
        
        # Botão para decrementar
        self.btn_decrementar = tk.Button(
            self.botoes_frame,
            text="-",
            font=("Arial", 14, "bold"),
            width=5,
            command=self.decrementar
        )
        self.btn_decrementar.grid(row=0, column=0, padx=5)
        
        # Botão para resetar
        self.btn_resetar = tk.Button(
            self.botoes_frame,
            text="Reset",
            font=("Arial", 14),
            width=5,
            command=self.resetar,
            bg="#ff9999"
        )
        self.btn_resetar.grid(row=0, column=1, padx=5)
        
        # Botão para incrementar
        self.btn_incrementar = tk.Button(
            self.botoes_frame,
            text="+",
            font=("Arial", 14, "bold"),
            width=5,
            command=self.incrementar
        )
        self.btn_incrementar.grid(row=0, column=2, padx=5)
        
        # Label de informação
        self.info_label = tk.Label(
            self.frame,
            text="Clique nos botões para alterar o contador",
            font=("Arial", 10)
        )
        self.info_label.pack(pady=10)
        
    def incrementar(self):
        self.contador += 1
        self.atualizar_contador()
        
    def decrementar(self):
        self.contador -= 1
        self.atualizar_contador()
        
    def resetar(self):
        # Confirma se o usuário realmente quer resetar
        if self.contador != 0:
            resposta = messagebox.askyesno("Resetar Contador", "Tem certeza que deseja resetar o contador para zero?")
            if resposta:
                self.contador = 0
                self.atualizar_contador()
        else:
            messagebox.showinfo("Informação", "O contador já está em zero!")
        
    def atualizar_contador(self):
        self.valor_label.config(text=str(self.contador))
        
        # Muda a cor do texto baseado no valor
        if self.contador > 0:
            self.valor_label.config(fg="green")
        elif self.contador < 0:
            self.valor_label.config(fg="red")
        else:
            self.valor_label.config(fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = JogoContador(root)
    root.mainloop()

