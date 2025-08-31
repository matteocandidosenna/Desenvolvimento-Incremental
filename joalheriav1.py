# joalheria_v1.py - COM PERSISTÊNCIA
import tkinter as tk
from tkinter import messagebox
import json
import os

class JoalheriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joalheria Luxo - V1.0")
        self.root.geometry("500x400")
        
        self.joias = []
        self.carregar_joias()  # Carrega joias do arquivo ao iniciar
        
        self.criar_interface()
    
    def carregar_joias(self):
        """Carrega as joias do arquivo JSON se existir"""
        try:
            if os.path.exists("joias.json"):
                with open("joias.json", "r") as f:
                    self.joias = json.load(f)
                print(f"✅ {len(self.joias)} joias carregadas do arquivo!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")
            self.joias = []
    
    def salvar_joias(self):
        """Salva as joias no arquivo JSON"""
        try:
            with open("joias.json", "w") as f:
                json.dump(self.joias, f, indent=4)
            print("💾 Joias salvas no arquivo!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")
    
    def criar_interface(self):
        # Frame principal
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        tk.Label(frame, text="💎 Joalheria Luxo", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(frame, text="V1.0 - Com persistência em arquivo", font=("Arial", 10)).pack(pady=5)
        
        # Botões
        tk.Button(frame, text="Cadastrar Joia", command=self.cadastrar_joia, 
                 height=2, width=20, bg="#4CAF50", fg="white").pack(pady=5)
        
        tk.Button(frame, text="Listar Joias", command=self.listar_joias,
                 height=2, width=20, bg="#2196F3", fg="white").pack(pady=5)
        
        tk.Button(frame, text="Salvar no Arquivo", command=self.salvar_joias,
                 height=2, width=20, bg="#FF9800", fg="white").pack(pady=5)
        
        tk.Button(frame, text="Sair", command=self.sair,
                 height=2, width=20, bg="#f44336", fg="white").pack(pady=5)
    
    def cadastrar_joia(self):
        # Janela de cadastro
        janela = tk.Toplevel(self.root)
        janela.title("Cadastrar Joia")
        janela.geometry("300x300")
        
        tk.Label(janela, text="Nome:").pack(pady=5)
        nome_entry = tk.Entry(janela, width=30)
        nome_entry.pack(pady=5)
        
        tk.Label(janela, text="Material:").pack(pady=5)
        material_entry = tk.Entry(janela, width=30)
        material_entry.pack(pady=5)
        
        tk.Label(janela, text="Preço R$:").pack(pady=5)
        preco_entry = tk.Entry(janela, width=30)
        preco_entry.pack(pady=5)
        
        def confirmar_cadastro():
            nome = nome_entry.get().strip()
            material = material_entry.get().strip()
            preco = preco_entry.get().strip()
            
            if not nome or not material or not preco:
                messagebox.showerror("Erro", "Preencha todos os campos!")
                return
            
            try:
                preco_float = float(preco)
                if preco_float <= 0:
                    messagebox.showerror("Erro", "O preço deve ser maior que zero!")
                    return
                
                # Adiciona joia
                self.joias.append({
                    "nome": nome, 
                    "material": material, 
                    "preço": preco_float
                })
                
                # Salva automaticamente no arquivo
                self.salvar_joias()
                
                messagebox.showinfo("Sucesso", f"Joia '{nome}' cadastrada e salva!")
                janela.destroy()
                
            except ValueError:
                messagebox.showerror("Erro", "Digite um preço válido!")
        
        # BOTÃO CONFIRMAR
        btn_confirmar = tk.Button(janela, text="Confirmar Cadastro", 
                                 command=confirmar_cadastro,
                                 bg="#4CAF50", fg="white", width=20)
        btn_confirmar.pack(pady=10)
        
        # Botão cancelar
        def cancelar():
            janela.destroy()
        
        btn_cancelar = tk.Button(janela, text="Cancelar", 
                                command=cancelar,
                                bg="#f44336", fg="white", width=20)
        btn_cancelar.pack(pady=5)
    
    def listar_joias(self):
        janela = tk.Toplevel(self.root)
        janela.title("Lista de Joias")
        janela.geometry("600x500")
        
        if not self.joias:
            tk.Label(janela, text="Nenhuma joia cadastrada!").pack(pady=20)
            return
        
        # Frame com scrollbar
        frame_principal = tk.Frame(janela)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas e scrollbar
        canvas = tk.Canvas(frame_principal)
        scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cabeçalho
        tk.Label(scrollable_frame, text="Nome", font=("Arial", 10, "bold"), width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(scrollable_frame, text="Material", font=("Arial", 10, "bold"), width=15).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(scrollable_frame, text="Preço", font=("Arial", 10, "bold"), width=15).grid(row=0, column=2, padx=5, pady=5)
        
        # Lista de joias
        for i, joia in enumerate(self.joias, 1):
            tk.Label(scrollable_frame, text=joia["nome"], width=20, anchor="w").grid(row=i, column=0, padx=5, pady=2)
            tk.Label(scrollable_frame, text=joia["material"], width=15, anchor="w").grid(row=i, column=1, padx=5, pady=2)
            tk.Label(scrollable_frame, text=f"R$ {joia['preço']:.2f}", width=15, anchor="w").grid(row=i, column=2, padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def sair(self):
        """Salva automaticamente antes de sair"""
        self.salvar_joias()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = JoalheriaApp(root)
    root.mainloop()