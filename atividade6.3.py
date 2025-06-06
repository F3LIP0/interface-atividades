#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import re

class ValidadorEmail:
    def __init__(self, root):
        self.root = root
        self.root.title("Validador de E-mail")
        self.root.geometry("450x300")
        
        # Frame principal
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Label de título
        self.titulo = tk.Label(
            self.frame,
            text="Validador de E-mail",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Label de instrução
        self.instrucao = tk.Label(
            self.frame,
            text="Digite um endereço de e-mail para validar",
            font=("Arial", 12)
        )
        self.instrucao.pack(pady=5)
        
        # Frame para entrada e botão
        self.input_frame = tk.Frame(self.frame)
        self.input_frame.pack(pady=10, fill=tk.X)
        
        # Campo de entrada para o e-mail
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            self.input_frame,
            textvariable=self.email_var,
            font=("Arial", 12),
            width=30
        )
        self.email_entry.pack(side=tk.LEFT, padx=5)
        
        # Botão para validar
        self.btn_validar = tk.Button(
            self.input_frame,
            text="Validar",
            font=("Arial", 12),
            command=self.validar_email
        )
        self.btn_validar.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar o resultado da validação
        self.resultado_frame = tk.Frame(self.frame, height=80)
        self.resultado_frame.pack(pady=10, fill=tk.X)
        self.resultado_frame.pack_propagate(False)
        
        self.resultado_label = tk.Label(
            self.resultado_frame,
            text="Resultado da validação aparecerá aqui",
            font=("Arial", 12),
            wraplength=400
        )
        self.resultado_label.pack(pady=10)
        
        # Bind para validar ao pressionar Enter
        self.email_entry.bind("<Return>", lambda event: self.validar_email())
        
        # Foco inicial no campo de entrada
        self.email_entry.focus_set()
        
    def validar_email(self):
        email = self.email_var.get().strip()
        
        if not email:
            self.mostrar_resultado("Por favor, digite um endereço de e-mail.", "warning")
            return
        
        # Validação básica: verificar se contém @ e pelo menos um ponto após o @
        if self.validar_formato_email(email):
            self.mostrar_resultado(f"O e-mail '{email}' é válido!", "success")
        else:
            self.mostrar_resultado(f"O e-mail '{email}' é inválido! Deve conter '@' e pelo menos um '.' após o '@'.", "error")
    
    def validar_formato_email(self, email):
        # Validação simples: verificar se contém @ e pelo menos um ponto após o @
        if "@" not in email:
            return False
        
        # Verificar se há pelo menos um ponto após o @
        partes = email.split("@")
        if len(partes) != 2:
            return False
        
        if "." not in partes[1]:
            return False
            
        # Verificação adicional usando expressão regular
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))
    
    def mostrar_resultado(self, mensagem, tipo):
        # Configura a cor do texto baseado no tipo de mensagem
        if tipo == "success":
            cor = "green"
        elif tipo == "error":
            cor = "red"
        else:  # warning
            cor = "orange"
            
        self.resultado_label.config(text=mensagem, fg=cor)

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidadorEmail(root)
    root.mainloop()

