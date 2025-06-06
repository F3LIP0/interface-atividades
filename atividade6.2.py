#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

class FaixaNumerica:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de Faixa Numérica")
        self.root.geometry("400x350")
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Validador de Faixa Numérica",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Label de instrução
        self.instrucao = tk.Label(
            self.frame,
            text="Digite um número entre 1 e 100",
            font=("Arial", 12)
        )
        self.instrucao.pack(pady=5)
        
        # Frame para entrada e botão
        self.input_frame = tk.Frame(self.frame)
        self.input_frame.pack(pady=10, fill=tk.X)
        
        # Campo de entrada para o número
        self.numero_var = tk.StringVar()
        self.numero_entry = tk.Entry(
            self.input_frame,
            textvariable=self.numero_var,
            font=("Arial", 12),
            width=10
        )
        self.numero_entry.pack(side=tk.LEFT, padx=5)
        
        # Botão para validar
        self.btn_validar = tk.Button(
            self.input_frame,
            text="Validar",
            font=("Arial", 12),
            command=self.validar_numero
        )
        self.btn_validar.pack(side=tk.LEFT, padx=5)
        
        # Frame para o resultado
        self.resultado_frame = tk.Frame(self.frame, height=100)
        self.resultado_frame.pack(pady=10, fill=tk.X)
        self.resultado_frame.pack_propagate(False)
        
        # Label para mostrar o resultado da validação
        self.resultado_label = tk.Label(
            self.resultado_frame,
            text="Resultado da validação aparecerá aqui",
            font=("Arial", 12),
            wraplength=350
        )
        self.resultado_label.pack(pady=10)
        
        # Escala para visualizar a faixa
        self.escala_label = tk.Label(
            self.frame,
            text="Faixa válida (1-100):",
            font=("Arial", 10)
        )
        self.escala_label.pack(anchor=tk.W, pady=(10, 0))
        
        self.escala = tk.Scale(
            self.frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            length=350,
            showvalue=True,
            tickinterval=10
        )
        self.escala.pack(fill=tk.X, pady=5)
        self.escala.set(50)  # Valor inicial
        
        # Bind para validar ao pressionar Enter
        self.numero_entry.bind("<Return>", lambda event: self.validar_numero())
        
        # Bind para atualizar a escala quando o valor mudar
        self.numero_var.trace_add("write", self.atualizar_escala)
        
        # Foco inicial no campo de entrada
        self.numero_entry.focus_set()
        
    def validar_numero(self):
        entrada = self.numero_var.get().strip()
        
        if not entrada:
            self.mostrar_resultado("Por favor, digite um número.", "warning")
            return
        
        try:
            numero = float(entrada)
            
            # Verificar se é um número inteiro
            if numero != int(numero):
                self.mostrar_resultado(f"O valor '{entrada}' não é um número inteiro.", "error")
                return
                
            numero = int(numero)
            
            # Verificar se está na faixa válida
            if 1 <= numero <= 100:
                self.mostrar_resultado(f"O número {numero} está dentro da faixa válida (1-100)!", "success")
            else:
                self.mostrar_resultado(f"O número {numero} está fora da faixa válida. Digite um número entre 1 e 100.", "error")
        except ValueError:
            self.mostrar_resultado(f"'{entrada}' não é um número válido.", "error")
    
    def mostrar_resultado(self, mensagem, tipo):
        # Configura a cor do texto baseado no tipo de mensagem
        if tipo == "success":
            cor = "green"
        elif tipo == "error":
            cor = "red"
        else:  # warning
            cor = "orange"
            
        self.resultado_label.config(text=mensagem, fg=cor)
    
    def atualizar_escala(self, *args):
        # Tenta atualizar a escala com o valor digitado
        try:
            valor = float(self.numero_var.get())
            if 1 <= valor <= 100:
                self.escala.set(valor)
        except ValueError:
            pass  # Ignora se não for um número válido

if __name__ == "__main__":
    root = tk.Tk()
    app = FaixaNumerica(root)
    root.mainloop()

