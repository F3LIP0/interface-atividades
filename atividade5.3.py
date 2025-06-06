#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

class TecladoInterativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Teclado Interativo")
        self.root.geometry("400x300")
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True)
        
        # Label de instrução
        self.instrucao = tk.Label(
            self.frame,
            text="Pressione qualquer tecla para ver seu valor",
            font=("Arial", 14)
        )
        self.instrucao.pack(pady=20)
        
        # Label para mostrar a tecla pressionada
        self.label_titulo = tk.Label(
            self.frame,
            text="Última tecla pressionada:",
            font=("Arial", 12)
        )
        self.label_titulo.pack(pady=10)
        
        self.tecla_label = tk.Label(
            self.frame,
            text="Nenhuma tecla pressionada ainda",
            font=("Arial", 16, "bold"),
            width=20,
            height=2,
            relief=tk.RIDGE,
            bg="#f0f0f0"
        )
        self.tecla_label.pack(pady=10)
        
        # Label para mostrar o código da tecla
        self.codigo_label = tk.Label(
            self.frame,
            text="Código: -",
            font=("Arial", 12)
        )
        self.codigo_label.pack(pady=10)
        
        # Bind para capturar eventos de teclado
        self.root.bind("<Key>", self.mostrar_tecla)
        
        # Foco na janela para capturar eventos de teclado
        self.root.focus_set()
        
    def mostrar_tecla(self, event):
        # Obtém o nome da tecla e seu código
        tecla = event.keysym
        codigo = event.keycode
        
        # Atualiza os labels
        self.tecla_label.config(text=tecla)
        self.codigo_label.config(text=f"Código: {codigo}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TecladoInterativo(root)
    root.mainloop()

