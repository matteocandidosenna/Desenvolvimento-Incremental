# joalheria_v1.py - COM PERSISTÊNCIA + LISTAGEM POR CATEGORIA + ALTERAR PRODUTO
import tkinter as tk
from tkinter import messagebox
import json
import os

class JoalheriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joalheria Luxo - V1.0")
        self.root.geometry("500x500")
        
        self.joias = []
        self.carregar_joias()
        
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
    
    def determinar_categoria(self, preco):
        """Determina a categoria baseada no preço"""
        if preco > 10000:
            return "LUXO"
        elif preco > 5000:
            return "PREMIUM"
        elif preco > 1000:
            return "STANDARD"
        else:
            return "BÁSICA"
    
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
        
        tk.Button(frame, text="Listar Todas as Joias", command=self.listar_joias,
                 height=2, width=20, bg="#2196F3", fg="white").pack(pady=5)
        
        tk.Button(frame, text="Listar por Categoria", command=self.listar_por_categoria,
                 height=2, width=20, bg="#FF9800", fg="white").pack(pady=5)
        
        # NOVO BOTÃO: Alterar Produto
        tk.Button(frame, text="Alterar Produto", command=self.alterar_produto,
                 height=2, width=20, bg="#9C27B0", fg="white").pack(pady=5)
        
        tk.Button(frame, text="Salvar no Arquivo", command=self.salvar_joias,
                 height=2, width=20, bg="#607D8B", fg="white").pack(pady=5)
        
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
        janela.geometry("700x500")
        
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
        tk.Label(scrollable_frame, text="Categoria", font=("Arial", 10, "bold"), width=15).grid(row=0, column=3, padx=5, pady=5)
        
        # Lista de joias
        for i, joia in enumerate(self.joias, 1):
            categoria = self.determinar_categoria(joia["preço"])
            tk.Label(scrollable_frame, text=joia["nome"], width=20, anchor="w").grid(row=i, column=0, padx=5, pady=2)
            tk.Label(scrollable_frame, text=joia["material"], width=15, anchor="w").grid(row=i, column=1, padx=5, pady=2)
            tk.Label(scrollable_frame, text=f"R$ {joia['preço']:.2f}", width=15, anchor="w").grid(row=i, column=2, padx=5, pady=2)
            tk.Label(scrollable_frame, text=categoria, width=15, anchor="w").grid(row=i, column=3, padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def listar_por_categoria(self):
        """Lista joias agrupadas por categoria"""
        if not self.joias:
            messagebox.showinfo("Info", "Nenhuma joia cadastrada!")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Joias por Categoria")
        janela.geometry("700x600")
        
        # Frame com scrollbar
        frame_principal = tk.Frame(janela)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame_principal)
        scrollbar = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Organiza joias por categoria
        joias_por_categoria = {"LUXO": [], "PREMIUM": [], "STANDARD": [], "BÁSICA": []}
        
        for joia in self.joias:
            categoria = self.determinar_categoria(joia["preço"])
            joias_por_categoria[categoria].append(joia)
        
        row = 0
        
        # Para cada categoria
        for categoria, joias in joias_por_categoria.items():
            if joias:  # Só mostra categorias que têm joias
                # Título da categoria
                tk.Label(scrollable_frame, text=f"📦 {categoria}", 
                        font=("Arial", 12, "bold"), bg="#E0E0E0").grid(
                        row=row, column=0, columnspan=4, sticky="ew", pady=10)
                row += 1
                
                # Cabeçalho da tabela
                tk.Label(scrollable_frame, text="Nome", font=("Arial", 10, "bold"), width=20).grid(row=row, column=0, padx=2, pady=2)
                tk.Label(scrollable_frame, text="Material", font=("Arial", 10, "bold"), width=15).grid(row=row, column=1, padx=2, pady=2)
                tk.Label(scrollable_frame, text="Preço", font=("Arial", 10, "bold"), width=15).grid(row=row, column=2, padx=2, pady=2)
                row += 1
                
                # Joias da categoria
                for joia in joias:
                    tk.Label(scrollable_frame, text=joia["nome"], width=20, anchor="w").grid(row=row, column=0, padx=2, pady=1)
                    tk.Label(scrollable_frame, text=joia["material"], width=15, anchor="w").grid(row=row, column=1, padx=2, pady=1)
                    tk.Label(scrollable_frame, text=f"R$ {joia['preço']:.2f}", width=15, anchor="w").grid(row=row, column=2, padx=2, pady=1)
                    row += 1
                
                # Linha em branco entre categorias
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def alterar_produto(self):
        """NOVA FUNÇÃO: Alterar dados de um produto existente"""
        if not self.joias:
            messagebox.showinfo("Info", "Nenhuma joia cadastrada para alterar!")
            return
        
        janela = tk.Toplevel(self.root)
        janela.title("Alterar Produto")
        janela.geometry("400x500")
        
        # Frame de seleção
        frame_selecao = tk.Frame(janela, padx=10, pady=10)
        frame_selecao.pack(fill=tk.X)
        
        tk.Label(frame_selecao, text="Selecione a joia para alterar:", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Lista de joias para seleção
        lista_joias = tk.Listbox(frame_selecao, height=6, width=50)
        lista_joias.pack(pady=5)
        
        for i, joia in enumerate(self.joias):
            lista_joias.insert(tk.END, f"{i+1}. {joia['nome']} - {joia['material']} - R$ {joia['preço']:.2f}")
        
        # Frame de edição (inicialmente vazio)
        frame_edicao = tk.Frame(janela, padx=10, pady=10)
        
        # Variáveis para os campos de edição
        nome_var = tk.StringVar()
        material_var = tk.StringVar()
        preco_var = tk.StringVar()
        indice_selecionado = None
        
        def carregar_dados_edicao():
            nonlocal indice_selecionado
            selecao = lista_joias.curselection()
            
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione uma joia para alterar!")
                return
            
            indice_selecionado = selecao[0]
            joia = self.joias[indice_selecionado]
            
            # Preenche os campos com os dados atuais
            nome_var.set(joia["nome"])
            material_var.set(joia["material"])
            preco_var.set(str(joia["preço"]))
            
            # Mostra o frame de edição
            frame_edicao.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def salvar_alteracoes():
            nonlocal indice_selecionado
            if indice_selecionado is None:
                messagebox.showerror("Erro", "Nenhuma joia selecionada!")
                return
            
            novo_nome = nome_var.get().strip()
            novo_material = material_var.get().strip()
            novo_preco = preco_var.get().strip()
            
            if not novo_nome or not novo_material or not novo_preco:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
                return
            
            try:
                novo_preco_float = float(novo_preco)
                if novo_preco_float <= 0:
                    messagebox.showerror("Erro", "O preço deve ser maior que zero!")
                    return
                
                # Atualiza os dados da joia
                self.joias[indice_selecionado]["nome"] = novo_nome
                self.joias[indice_selecionado]["material"] = novo_material
                self.joias[indice_selecionado]["preço"] = novo_preco_float
                
                # Salva no arquivo
                self.salvar_joias()
                
                messagebox.showinfo("Sucesso", "Joia alterada com sucesso!")
                janela.destroy()
                
            except ValueError:
                messagebox.showerror("Erro", "Digite um preço válido!")
        
        # Botão para carregar dados
        btn_carregar = tk.Button(frame_selecao, text="Carregar para Edição", 
                                command=carregar_dados_edicao, bg="#2196F3", fg="white")
        btn_carregar.pack(pady=5)
        
        # Campos de edição
        tk.Label(frame_edicao, text="Novo Nome:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nome = tk.Entry(frame_edicao, textvariable=nome_var, width=30)
        entry_nome.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(frame_edicao, text="Novo Material:").grid(row=1, column=0, sticky="w", pady=5)
        entry_material = tk.Entry(frame_edicao, textvariable=material_var, width=30)
        entry_material.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(frame_edicao, text="Novo Preço R$:").grid(row=2, column=0, sticky="w", pady=5)
        entry_preco = tk.Entry(frame_edicao, textvariable=preco_var, width=30)
        entry_preco.grid(row=2, column=1, pady=5, padx=5)
        
        # Botões de ação
        frame_botoes = tk.Frame(frame_edicao, pady=10)
        frame_botoes.grid(row=3, column=0, columnspan=2)
        
        btn_salvar = tk.Button(frame_botoes, text="💾 Salvar Alterações", 
                              command=salvar_alteracoes, bg="#4CAF50", fg="white", width=20)
        btn_salvar.pack(pady=5)
        
        btn_cancelar = tk.Button(frame_botoes, text="❌ Cancelar", 
                                command=janela.destroy, bg="#f44336", fg="white", width=20)
        btn_cancelar.pack(pady=5)
    
    def sair(self):
        """Salva automaticamente antes de sair"""
        self.salvar_joias()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = JoalheriaApp(root)
    root.mainloop()