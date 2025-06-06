#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import random

class CoresDinamicas:
    def __init__(self, root):
        self.root = root
        self.root.title("Cores Dinâmicas")
        self.root.geometry("400x300")
        
        # Cores possíveis para o lado esquerdo e direito
        self.cores_esquerda = ["#FF5733", "#C70039", "#900C3F", "#581845", "#2471A3", "#148F77"]
        self.cores_direita = ["#F1C40F", "#27AE60", "#3498DB", "#8E44AD", "#E74C3C", "#D35400"]
        
        # Configuração inicial
        self.root.configure(bg="#FFFFFF")
        
        # Label com instruções
        self.label = tk.Label(
            root, 
            text="Clique no lado esquerdo ou direito da janela para mudar a cor de fundo",
            font=("Arial", 12),
            wraplength=380,
            bg="#FFFFFF"
        )
        self.label.pack(pady=20)
        
        # Bind para capturar cliques do mouse
        self.root.bind("<Button-1>", self.mudar_cor)
        
    def mudar_cor(self, event):
        # Obtém a largura da janela
        largura = self.root.winfo_width()
        
        # Verifica se o clique foi no lado esquerdo ou direito
        if event.x < largura / 2:
            # Lado esquerdo
            nova_cor = random.choice(self.cores_esquerda)
            self.root.configure(bg=nova_cor)
            self.label.configure(bg=nova_cor)
        else:
            # Lado direito
            nova_cor = random.choice(self.cores_direita)
            self.root.configure(bg=nova_cor)
            self.label.configure(bg=nova_cor)

if __name__ == "__main__":
    root = tk.Tk()
    app = CoresDinamicas(root)
    root.mainloop()

