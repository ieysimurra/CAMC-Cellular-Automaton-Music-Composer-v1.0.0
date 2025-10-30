import customtkinter as ctk
from tkinter import ttk, Canvas, messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
import subprocess
import os
import tempfile
from pathlib import Path
from music21 import note, stream, metadata, duration, clef, instrument, converter, tempo, meter
import random
import threading
import time

# Configurações do customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Constantes do sistema musical
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
COLORS = [
    "#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00", "#00FF7F",
    "#00FFFF", "#007FFF", "#0000FF", "#7F00FF", "#FF00FF", "#FF007F"
]
PAUSE_COLOR = "#CCCCCC"

# NOVO: Durações que respeitam compassos (SEM quiálteras no modo aleatório)
RHYTHMIC_VALUES = {
    "Colcheia (1/8)": 0.5,
    "Semínima (1/4)": 1.0,
    "Mínima (1/2)": 2.0,
    "Semibreve (1/1)": 4.0
}

# Durações válidas para modo aleatório (sem quiálteras)
RANDOM_DURATIONS = [0.5, 1.0, 2.0, 4.0]  # Colcheia, Semínima, Mínima, Semibreve

# Durações com quiálteras (apenas para uso explícito)
VALID_DURATIONS_WITH_TRIPLETS = {
    "Colcheia": 0.5,
    "Semínima": 1.0,
    "Mínima": 2.0,
    "Semibreve": 4.0,
    "Tercina Colcheia": "8th_triplet",
    "Tercina Semínima": "quarter_triplet",
}

INSTRUMENTS_PT = {
    "Flauta": "Flute", "Oboé": "Oboe", "Clarinete": "Clarinet",
    "Fagote": "Bassoon", "Trompa": "Horn", "Trompete": "Trumpet",
    "Trombone": "Trombone", "Tuba": "Tuba", "Violino": "Violin",
    "Viola": "Viola", "Violoncelo": "Violoncello", "Contrabaixo": "Contrabass"
}

INSTRUMENT_RANGES = {
    "Flauta": {"lowest": ("C", 4), "highest": ("C", 7)},
    "Oboé": {"lowest": ("B", 3), "highest": ("A", 6)},
    "Clarinete": {"lowest": ("D", 3), "highest": ("G", 6)},
    "Fagote": {"lowest": ("B", 1), "highest": ("E", 5)},
    "Trompa": {"lowest": ("B", 1), "highest": ("F", 5)},
    "Trompete": {"lowest": ("E", 3), "highest": ("C", 6)},
    "Trombone": {"lowest": ("E", 2), "highest": ("F", 5)},
    "Tuba": {"lowest": ("D", 1), "highest": ("F", 4)},
    "Violino": {"lowest": ("G", 3), "highest": ("E", 7)},
    "Viola": {"lowest": ("C", 3), "highest": ("A", 6)},
    "Violoncelo": {"lowest": ("C", 2), "highest": ("A", 5)},
    "Contrabaixo": {"lowest": ("E", 1), "highest": ("G", 4)}
}


class CellularAutomatonMusicGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🎵 Compositor com Autômatos Celulares 🎨 [VERSÃO OTIMIZADA]")
        self.geometry("1400x900")
        
        # Variáveis de estado
        self.instrument_configs = {}
        self.current_instrument = None
        self.ca_result = None
        self.score = None
        self.musescore_path = None
        self.ca_figures = {}  # NOVO: Armazenar figuras dos CAs para exportação
        
        # Configuração da janela principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Container principal com abas REORGANIZADAS
        self.tabview = ctk.CTkTabview(self, width=1380, height=880)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # NOVO: Apenas 3 abas principais
        self.tab_instruments = self.tabview.add("🎼 Instrumentos")
        self.tab_config = self.tabview.add("⚙️ Configuração Completa")
        self.tab_score = self.tabview.add("📝 Partitura")
        
        # Construir cada aba
        self.build_instruments_tab()
        self.build_unified_config_tab()  # NOVO: Aba unificada
        self.build_score_tab()
        
    def build_instruments_tab(self):
        """Aba de seleção de instrumentos"""
        main_frame = ctk.CTkScrollableFrame(self.tab_instruments)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text="🎻 Selecione os Instrumentos 🎺",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=20)
        
        desc = ctk.CTkLabel(
            main_frame,
            text="Escolha instrumentos e defina quantas instâncias de cada deseja",
            font=ctk.CTkFont(size=14),
            wraplength=800
        )
        desc.pack(pady=10)
        
        instruments_frame = ctk.CTkFrame(main_frame)
        instruments_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.instrument_quantities = {}
        
        categories = {
            "🌬️ Sopros de Madeira": ["Flauta", "Oboé", "Clarinete", "Fagote"],
            "🎺 Sopros de Metal": ["Trompa", "Trompete", "Trombone", "Tuba"],
            "🎻 Cordas": ["Violino", "Viola", "Violoncelo", "Contrabaixo"]
        }
        
        row = 0
        for category, instruments in categories.items():
            cat_label = ctk.CTkLabel(
                instruments_frame,
                text=category,
                font=ctk.CTkFont(size=18, weight="bold")
            )
            cat_label.grid(row=row, column=0, columnspan=3, pady=(20, 10), sticky="w", padx=20)
            row += 1
            
            for inst in instruments:
                inst_label = ctk.CTkLabel(
                    instruments_frame,
                    text=inst,
                    font=ctk.CTkFont(size=14)
                )
                inst_label.grid(row=row, column=0, padx=20, pady=5, sticky="w")
                
                qty_label = ctk.CTkLabel(
                    instruments_frame,
                    text="Quantidade:",
                    font=ctk.CTkFont(size=12)
                )
                qty_label.grid(row=row, column=1, padx=10, pady=5, sticky="e")
                
                qty_var = ctk.IntVar(value=0)
                qty_spinbox = ctk.CTkEntry(
                    instruments_frame,
                    width=60,
                    textvariable=qty_var
                )
                qty_spinbox.grid(row=row, column=2, padx=10, pady=5, sticky="w")
                
                btn_frame = ctk.CTkFrame(instruments_frame, fg_color="transparent")
                btn_frame.grid(row=row, column=3, padx=5, pady=5)
                
                def make_increment(var, max_val=4):
                    def increment():
                        current = var.get()
                        if current < max_val:
                            var.set(current + 1)
                    return increment
                
                def make_decrement(var):
                    def decrement():
                        current = var.get()
                        if current > 0:
                            var.set(current - 1)
                    return decrement
                
                btn_plus = ctk.CTkButton(
                    btn_frame,
                    text="+",
                    width=30,
                    command=make_increment(qty_var)
                )
                btn_plus.pack(side="left", padx=2)
                
                btn_minus = ctk.CTkButton(
                    btn_frame,
                    text="-",
                    width=30,
                    command=make_decrement(qty_var)
                )
                btn_minus.pack(side="left", padx=2)
                
                self.instrument_quantities[inst] = qty_var
                row += 1
        
        # Botão para confirmar seleção
        confirm_btn = ctk.CTkButton(
            main_frame,
            text="✅ Confirmar Seleção de Instrumentos",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.confirm_instruments
        )
        confirm_btn.pack(pady=30)
        
    def confirm_instruments(self):
        """Confirma a seleção de instrumentos e cria configurações"""
        selected = []
        for inst, qty_var in self.instrument_quantities.items():
            qty = qty_var.get()
            for i in range(qty):
                inst_name = f"{inst} {i+1}" if qty > 1 else inst
                selected.append(inst_name)
                
                # Criar configuração padrão se não existir
                if inst_name not in self.instrument_configs:
                    self.instrument_configs[inst_name] = {
                        'base_instrument': inst,
                        'initial_note': 'C',
                        'octave_mode': 'Crescente',
                        'octaves': [4],
                        'rhythmic_value': 1.0,
                        'randomize_rhythm': False,
                        'num_states': 8,
                        'generations': 20,
                        'length': 50,
                        'neighborhood_size': 1,
                        'initial_cell': 25,
                        'rule_type': 1,
                        'rule_params': {},
                        'ca_result': None
                    }
        
        if not selected:
            messagebox.showwarning("Atenção", "Selecione pelo menos um instrumento!")
            return
        
        messagebox.showinfo(
            "Instrumentos Selecionados",
            f"Total de instrumentos: {len(selected)}\n\n" + "\n".join(selected)
        )
        
        # Mudar para aba de configuração
        self.tabview.set("⚙️ Configuração Completa")
        self.update_config_instrument_list()
        
    def build_unified_config_tab(self):
        """NOVA: Aba unificada com Configuração + Regras + Visualização"""
        # Frame principal com scroll
        main_frame = ctk.CTkScrollableFrame(self.tab_config)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="⚙️ Configuração Completa dos Instrumentos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=15)
        
        # Seletor de instrumento
        selector_frame = ctk.CTkFrame(main_frame)
        selector_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            selector_frame,
            text="Instrumento:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10)
        
        self.config_instrument_var = ctk.StringVar(value="Nenhum")
        self.config_instrument_menu = ctk.CTkOptionMenu(
            selector_frame,
            variable=self.config_instrument_var,
            values=["Nenhum"],
            command=self.load_instrument_config,
            width=300
        )
        self.config_instrument_menu.pack(side="left", padx=10)
        
        # Container para os 3 painéis lado a lado
        panels_frame = ctk.CTkFrame(main_frame)
        panels_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        panels_frame.grid_columnconfigure(0, weight=1)
        panels_frame.grid_columnconfigure(1, weight=1)
        panels_frame.grid_columnconfigure(2, weight=1)
        
        # PAINEL 1: Configurações Musicais
        music_panel = ctk.CTkFrame(panels_frame)
        music_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(
            music_panel,
            text="🎵 Configurações Musicais",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Nota inicial
        note_frame = ctk.CTkFrame(music_panel)
        note_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(note_frame, text="Nota Inicial:").pack(anchor="w", padx=5)
        self.initial_note_var = ctk.StringVar(value="C")
        ctk.CTkOptionMenu(
            note_frame,
            variable=self.initial_note_var,
            values=NOTES
        ).pack(fill="x", padx=5, pady=5)
        
        # Modo de oitava
        octave_mode_frame = ctk.CTkFrame(music_panel)
        octave_mode_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(octave_mode_frame, text="Modo de Oitava:").pack(anchor="w", padx=5)
        self.octave_mode_var = ctk.StringVar(value="Crescente")
        ctk.CTkOptionMenu(
            octave_mode_frame,
            variable=self.octave_mode_var,
            values=["Crescente", "Decrescente", "Intercalada"]
        ).pack(fill="x", padx=5, pady=5)
        
        # Oitavas
        octaves_frame = ctk.CTkFrame(music_panel)
        octaves_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(octaves_frame, text="Oitavas (separadas por vírgula):").pack(anchor="w", padx=5)
        self.octaves_entry = ctk.CTkEntry(octaves_frame)
        self.octaves_entry.insert(0, "4")
        self.octaves_entry.pack(fill="x", padx=5, pady=5)
        
        # Valor rítmico
        rhythm_frame = ctk.CTkFrame(music_panel)
        rhythm_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(rhythm_frame, text="Valor Rítmico Base:").pack(anchor="w", padx=5)
        self.rhythmic_value_var = ctk.StringVar(value="Semínima (1/4)")
        ctk.CTkOptionMenu(
            rhythm_frame,
            variable=self.rhythmic_value_var,
            values=list(RHYTHMIC_VALUES.keys())
        ).pack(fill="x", padx=5, pady=5)
        
        # Randomizar ritmo
        self.randomize_rhythm_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            music_panel,
            text="🎲 Randomizar Durações (sem quiálteras)",
            variable=self.randomize_rhythm_var,
            font=ctk.CTkFont(size=12)
        ).pack(pady=10)
        
        # PAINEL 2: Parâmetros do CA
        ca_panel = ctk.CTkFrame(panels_frame)
        ca_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(
            ca_panel,
            text="🔬 Parâmetros do Autômato",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Número de estados
        states_frame = ctk.CTkFrame(ca_panel)
        states_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(states_frame, text="Estados (2-12):").pack(anchor="w", padx=5)
        self.num_states_var = ctk.IntVar(value=8)
        ctk.CTkSlider(
            states_frame,
            from_=2,
            to=12,
            number_of_steps=10,
            variable=self.num_states_var
        ).pack(fill="x", padx=5)
        self.states_label = ctk.CTkLabel(states_frame, text="8")
        self.states_label.pack()
        self.num_states_var.trace_add("write", lambda *args: self.states_label.configure(text=str(self.num_states_var.get())))
        
        # Gerações
        gen_frame = ctk.CTkFrame(ca_panel)
        gen_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(gen_frame, text="Gerações (10-100):").pack(anchor="w", padx=5)
        self.generations_var = ctk.IntVar(value=30)
        ctk.CTkSlider(
            gen_frame,
            from_=10,
            to=100,
            number_of_steps=18,
            variable=self.generations_var
        ).pack(fill="x", padx=5)
        self.gen_label = ctk.CTkLabel(gen_frame, text="30")
        self.gen_label.pack()
        self.generations_var.trace_add("write", lambda *args: self.gen_label.configure(text=str(self.generations_var.get())))
        
        # Comprimento
        length_frame = ctk.CTkFrame(ca_panel)
        length_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(length_frame, text="Comprimento (20-150):").pack(anchor="w", padx=5)
        self.length_var = ctk.IntVar(value=50)
        ctk.CTkSlider(
            length_frame,
            from_=20,
            to=150,
            number_of_steps=26,
            variable=self.length_var
        ).pack(fill="x", padx=5)
        self.length_label = ctk.CTkLabel(length_frame, text="50")
        self.length_label.pack()
        self.length_var.trace_add("write", lambda *args: self.length_label.configure(text=str(self.length_var.get())))
        
        # Vizinhança
        neigh_frame = ctk.CTkFrame(ca_panel)
        neigh_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(neigh_frame, text="Tamanho Vizinhança (1-5):").pack(anchor="w", padx=5)
        self.neighborhood_var = ctk.IntVar(value=1)
        ctk.CTkSlider(
            neigh_frame,
            from_=1,
            to=5,
            number_of_steps=4,
            variable=self.neighborhood_var
        ).pack(fill="x", padx=5)
        self.neigh_label = ctk.CTkLabel(neigh_frame, text="1")
        self.neigh_label.pack()
        self.neighborhood_var.trace_add("write", lambda *args: self.neigh_label.configure(text=str(self.neighborhood_var.get())))
        
        # Célula inicial
        initial_frame = ctk.CTkFrame(ca_panel)
        initial_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(initial_frame, text="Célula Inicial:").pack(anchor="w", padx=5)
        self.initial_cell_entry = ctk.CTkEntry(initial_frame)
        self.initial_cell_entry.insert(0, "25")
        self.initial_cell_entry.pack(fill="x", padx=5, pady=5)
        
        # PAINEL 3: Regras
        rules_panel = ctk.CTkFrame(panels_frame)
        rules_panel.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        ctk.CTkLabel(
            rules_panel,
            text="🔢 Regras de Transição",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Tipo de regra
        rule_type_frame = ctk.CTkFrame(rules_panel)
        rule_type_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(rule_type_frame, text="Tipo de Regra:").pack(anchor="w", padx=5)
        self.rule_type_var = ctk.StringVar(value="Determinística")
        rule_menu = ctk.CTkOptionMenu(
            rule_type_frame,
            variable=self.rule_type_var,
            values=["Determinística", "Thresholds", "Aleatória", "Matemática", "Time-Sensitive"],
            command=self.update_rule_params_ui
        )
        rule_menu.pack(fill="x", padx=5, pady=5)
        
        # Frame para parâmetros específicos da regra
        self.rule_params_frame = ctk.CTkFrame(rules_panel)
        self.rule_params_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botões de ação
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            action_frame,
            text="💾 Salvar Configuração",
            command=self.save_current_config,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, expand=True, fill="x")
        
        ctk.CTkButton(
            action_frame,
            text="🎨 Gerar e Visualizar CA",
            command=self.generate_and_visualize_ca,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, expand=True, fill="x")
        
        # Frame para visualização do CA
        self.ca_viz_frame = ctk.CTkFrame(main_frame)
        self.ca_viz_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botão para salvar imagem
        self.save_ca_btn = ctk.CTkButton(
            main_frame,
            text="💾 Salvar Visualização do CA",
            command=self.save_ca_visualization,
            height=35,
            state="disabled"
        )
        self.save_ca_btn.pack(pady=10)
        
    def update_config_instrument_list(self):
        """Atualiza lista de instrumentos no menu de configuração"""
        instruments = list(self.instrument_configs.keys())
        if instruments:
            self.config_instrument_menu.configure(values=instruments)
            self.config_instrument_var.set(instruments[0])
            self.load_instrument_config(instruments[0])
        else:
            self.config_instrument_menu.configure(values=["Nenhum"])
            self.config_instrument_var.set("Nenhum")
    
    def load_instrument_config(self, instrument_name):
        """Carrega configuração do instrumento selecionado"""
        if instrument_name == "Nenhum" or instrument_name not in self.instrument_configs:
            return
        
        config = self.instrument_configs[instrument_name]
        
        # Carregar valores nos widgets
        self.initial_note_var.set(config.get('initial_note', 'C'))
        self.octave_mode_var.set(config.get('octave_mode', 'Crescente'))
        self.octaves_entry.delete(0, 'end')
        self.octaves_entry.insert(0, ','.join(map(str, config.get('octaves', [4]))))
        
        # Encontrar chave do valor rítmico
        rhythm_val = config.get('rhythmic_value', 1.0)
        rhythm_key = "Semínima (1/4)"
        for key, val in RHYTHMIC_VALUES.items():
            if val == rhythm_val:
                rhythm_key = key
                break
        self.rhythmic_value_var.set(rhythm_key)
        
        self.randomize_rhythm_var.set(config.get('randomize_rhythm', False))
        self.num_states_var.set(config.get('num_states', 8))
        self.generations_var.set(config.get('generations', 20))
        self.length_var.set(config.get('length', 50))
        self.neighborhood_var.set(config.get('neighborhood_size', 1))
        self.initial_cell_entry.delete(0, 'end')
        self.initial_cell_entry.insert(0, str(config.get('initial_cell', 25)))
        
        # Carregar tipo de regra
        rule_type_map = {1: "Determinística", 2: "Thresholds", 3: "Aleatória", 
                        4: "Matemática", 5: "Time-Sensitive"}
        self.rule_type_var.set(rule_type_map.get(config.get('rule_type', 1), "Determinística"))
        self.update_rule_params_ui(rule_type_map.get(config.get('rule_type', 1), "Determinística"))
        
    def update_rule_params_ui(self, rule_type):
        """Atualiza interface de parâmetros da regra"""
        # Limpar frame
        for widget in self.rule_params_frame.winfo_children():
            widget.destroy()
        
        if rule_type == "Thresholds":
            ctk.CTkLabel(
                self.rule_params_frame,
                text="Thresholds (separados por vírgula):",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=5, pady=5)
            
            self.thresholds_entry = ctk.CTkEntry(self.rule_params_frame)
            self.thresholds_entry.insert(0, "3,6")
            self.thresholds_entry.pack(fill="x", padx=5, pady=5)
            
        elif rule_type == "Matemática":
            ctk.CTkLabel(
                self.rule_params_frame,
                text="Função matemática:",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=5, pady=5)
            
            ctk.CTkLabel(
                self.rule_params_frame,
                text="Variáveis: state, neighbor_sum, num_states",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            ).pack(anchor="w", padx=5)
            
            self.math_func_entry = ctk.CTkEntry(self.rule_params_frame)
            self.math_func_entry.insert(0, "(state + neighbor_sum) % num_states")
            self.math_func_entry.pack(fill="x", padx=5, pady=5)
            
        elif rule_type == "Time-Sensitive":
            ctk.CTkLabel(
                self.rule_params_frame,
                text="Time Step:",
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w", padx=5, pady=5)
            
            self.time_step_entry = ctk.CTkEntry(self.rule_params_frame)
            self.time_step_entry.insert(0, "1")
            self.time_step_entry.pack(fill="x", padx=5, pady=5)
        else:
            ctk.CTkLabel(
                self.rule_params_frame,
                text=f"Regra {rule_type} não requer parâmetros adicionais",
                font=ctk.CTkFont(size=11),
                text_color="gray"
            ).pack(pady=20)
    
    def save_current_config(self):
        """Salva configuração atual do instrumento"""
        instrument_name = self.config_instrument_var.get()
        if instrument_name == "Nenhum" or instrument_name not in self.instrument_configs:
            messagebox.showwarning("Atenção", "Selecione um instrumento válido!")
            return
        
        try:
            # Coletar valores
            octaves = [int(x.strip()) for x in self.octaves_entry.get().split(',')]
            rhythmic_value = RHYTHMIC_VALUES[self.rhythmic_value_var.get()]
            initial_cell = int(self.initial_cell_entry.get())
            
            # Mapear tipo de regra
            rule_type_map = {"Determinística": 1, "Thresholds": 2, "Aleatória": 3,
                           "Matemática": 4, "Time-Sensitive": 5}
            rule_type = rule_type_map[self.rule_type_var.get()]
            
            # Coletar parâmetros da regra
            rule_params = {}
            if self.rule_type_var.get() == "Thresholds":
                rule_params['thresholds'] = [int(x.strip()) for x in self.thresholds_entry.get().split(',')]
            elif self.rule_type_var.get() == "Matemática":
                rule_params['math_function'] = self.math_func_entry.get()
            elif self.rule_type_var.get() == "Time-Sensitive":
                rule_params['time_step'] = int(self.time_step_entry.get())
            
            # Atualizar configuração
            self.instrument_configs[instrument_name].update({
                'initial_note': self.initial_note_var.get(),
                'octave_mode': self.octave_mode_var.get(),
                'octaves': octaves,
                'rhythmic_value': rhythmic_value,
                'randomize_rhythm': self.randomize_rhythm_var.get(),
                'num_states': self.num_states_var.get(),
                'generations': self.generations_var.get(),
                'length': self.length_var.get(),
                'neighborhood_size': self.neighborhood_var.get(),
                'initial_cell': initial_cell,
                'rule_type': rule_type,
                'rule_params': rule_params
            })
            
            messagebox.showinfo("Sucesso", f"Configuração de '{instrument_name}' salva!")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Valores inválidos: {e}")
    
    def generate_and_visualize_ca(self):
        """Gera o CA e visualiza imediatamente"""
        instrument_name = self.config_instrument_var.get()
        if instrument_name == "Nenhum" or instrument_name not in self.instrument_configs:
            messagebox.showwarning("Atenção", "Selecione um instrumento válido!")
            return
        
        # Salvar configuração atual
        self.save_current_config()
        
        config = self.instrument_configs[instrument_name]
        
        try:
            # Gerar matriz de regras
            rule_matrix = generate_rule_matrix(
                config['num_states'],
                config['rule_type'],
                **config['rule_params']
            )
            
            # Gerar CA
            ca_result = generate_ca(
                rule_matrix,
                config['generations'],
                config['length'],
                config['num_states'],
                config['neighborhood_size'],
                config['initial_cell']
            )
            
            # Armazenar resultado
            self.instrument_configs[instrument_name]['ca_result'] = ca_result
            
            # Visualizar
            self.visualize_ca_in_frame(ca_result, instrument_name)
            
            # Ativar botão de salvar
            self.save_ca_btn.configure(state="normal")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar CA: {e}")
    
    def visualize_ca_in_frame(self, ca_result, instrument_name):
        """Visualiza o CA no frame da aba de configuração"""
        # Limpar frame anterior
        for widget in self.ca_viz_frame.winfo_children():
            widget.destroy()
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Criar colormap personalizado
        colors = [PAUSE_COLOR] + COLORS[:ca_result.max()]
        cmap = ListedColormap(colors)
        
        # Plotar
        im = ax.imshow(ca_result, cmap=cmap, aspect='auto', interpolation='nearest')
        ax.set_title(f'Autômato Celular - {instrument_name}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Posição', fontsize=11)
        ax.set_ylabel('Geração (Tempo)', fontsize=11)
        
        # Colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Estado', rotation=270, labelpad=15)
        
        plt.tight_layout()
        
        # Armazenar figura para exportação
        self.ca_figures[instrument_name] = fig
        
        # Incorporar no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.ca_viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def save_ca_visualization(self):
        """NOVO: Salva a visualização do CA atual como imagem"""
        instrument_name = self.config_instrument_var.get()
        if instrument_name not in self.ca_figures:
            messagebox.showwarning("Atenção", "Nenhuma visualização disponível!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("PDF Document", "*.pdf"),
                ("All Files", "*.*")
            ],
            initialfile=f"CA_{instrument_name.replace(' ', '_')}.png"
        )
        
        if filename:
            try:
                self.ca_figures[instrument_name].savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Sucesso", f"Imagem salva em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar imagem: {e}")
    
    def build_score_tab(self):
        """Aba de partitura com otimizações"""
        main_frame = ctk.CTkFrame(self.tab_score)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="📝 Geração e Exportação da Partitura",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame de configurações globais
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="⚙️ Configurações Globais da Partitura",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Título da obra
        title_frame = ctk.CTkFrame(config_frame)
        title_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(title_frame, text="Título:").pack(side="left", padx=5)
        self.score_title_entry = ctk.CTkEntry(title_frame, width=300)
        self.score_title_entry.insert(0, "Composição com Autômatos Celulares")
        self.score_title_entry.pack(side="left", padx=5)
        
        # Compositor
        composer_frame = ctk.CTkFrame(config_frame)
        composer_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(composer_frame, text="Compositor:").pack(side="left", padx=5)
        self.composer_entry = ctk.CTkEntry(composer_frame, width=300)
        self.composer_entry.insert(0, "Composição Algorítmica")
        self.composer_entry.pack(side="left", padx=5)
        
        # Tempo
        tempo_frame = ctk.CTkFrame(config_frame)
        tempo_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(tempo_frame, text="Tempo (BPM):").pack(side="left", padx=5)
        self.tempo_entry = ctk.CTkEntry(tempo_frame, width=100)
        self.tempo_entry.insert(0, "120")
        self.tempo_entry.pack(side="left", padx=5)
        
        # Fórmula de compasso
        meter_frame = ctk.CTkFrame(config_frame)
        meter_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(meter_frame, text="Compasso:").pack(side="left", padx=5)
        self.meter_var = ctk.StringVar(value="4/4")
        ctk.CTkOptionMenu(
            meter_frame,
            variable=self.meter_var,
            values=["2/4", "3/4", "4/4", "5/4", "6/8", "9/8", "12/8"]
        ).pack(side="left", padx=5)
        
        # Botão de geração
        generate_frame = ctk.CTkFrame(main_frame)
        generate_frame.pack(fill="x", padx=20, pady=20)
        
        self.generate_score_btn = ctk.CTkButton(
            generate_frame,
            text="🎼 GERAR PARTITURA",
            command=self.generate_score_optimized,
            height=60,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#2E7D32",
            hover_color="#1B5E20"
        )
        self.generate_score_btn.pack(fill="x", padx=50)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(generate_frame)
        self.progress_bar.pack(fill="x", padx=50, pady=10)
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(generate_frame, text="")
        self.progress_label.pack()
        
        # Frame para visualização
        self.score_viz_frame = ctk.CTkFrame(main_frame)
        self.score_viz_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botões de exportação
        export_frame = ctk.CTkFrame(main_frame)
        export_frame.pack(fill="x", padx=20, pady=10)
        
        self.export_musicxml_btn = ctk.CTkButton(
            export_frame,
            text="💾 Exportar MusicXML",
            command=self.export_musicxml,
            state="disabled"
        )
        self.export_musicxml_btn.pack(side="left", padx=10, expand=True, fill="x")
        
        self.export_midi_btn = ctk.CTkButton(
            export_frame,
            text="🎹 Exportar MIDI",
            command=self.export_midi,
            state="disabled"
        )
        self.export_midi_btn.pack(side="left", padx=10, expand=True, fill="x")
        
        self.open_musescore_btn = ctk.CTkButton(
            export_frame,
            text="📖 Abrir no MuseScore",
            command=self.open_musescore,
            state="disabled"
        )
        self.open_musescore_btn.pack(side="left", padx=10, expand=True, fill="x")
    
    def generate_score_optimized(self):
        """OTIMIZADO: Geração de partitura com feedback de progresso"""
        # Verificar se há instrumentos configurados
        if not self.instrument_configs:
            messagebox.showwarning("Atenção", "Nenhum instrumento configurado!")
            return
        
        # Verificar se todos têm CA gerado
        missing_ca = [inst for inst, config in self.instrument_configs.items() 
                     if config.get('ca_result') is None]
        
        if missing_ca:
            messagebox.showwarning(
                "Atenção",
                f"Os seguintes instrumentos não têm CA gerado:\n\n" + "\n".join(missing_ca) +
                "\n\nGere os CAs na aba 'Configuração Completa'."
            )
            return
        
        # Desabilitar botão durante geração
        self.generate_score_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Iniciando geração...")
        
        # Thread para não travar a interface
        def generate_thread():
            try:
                start_time = time.time()
                
                # Criar partitura
                self.progress_label.configure(text="Criando estrutura da partitura...")
                self.progress_bar.set(0.1)
                self.update()
                
                self.score = stream.Score()
                
                # Metadados
                self.score.metadata = metadata.Metadata()
                self.score.metadata.title = self.score_title_entry.get()
                self.score.metadata.composer = self.composer_entry.get()
                
                # Tempo e compasso
                tempo_bpm = int(self.tempo_entry.get())
                meter_str = self.meter_var.get()
                
                total_instruments = len(self.instrument_configs)
                
                for idx, (inst_name, config) in enumerate(self.instrument_configs.items()):
                    progress = 0.1 + (0.7 * (idx / total_instruments))
                    self.progress_bar.set(progress)
                    self.progress_label.configure(text=f"Processando {inst_name}... ({idx+1}/{total_instruments})")
                    self.update()
                    
                    # Reordenar notas
                    note_list = reorder_notes(
                        config['initial_note'],
                        config['octaves'],
                        config['octave_mode']
                    )
                    
                    # Converter CA para música (OTIMIZADO)
                    part = ca_to_music21_optimized(
                        config['ca_result'],
                        config['num_states'],
                        config['rhythmic_value'],
                        config['randomize_rhythm'],
                        note_list,
                        INSTRUMENTS_PT[config['base_instrument']],
                        meter_str  # NOVO: passar compasso
                    )
                    
                    # Adicionar nome da parte
                    part.partName = inst_name
                    
                    # Adicionar tempo e compasso no início
                    part.insert(0, tempo.MetronomeMark(number=tempo_bpm))
                    part.insert(0, meter.TimeSignature(meter_str))
                    
                    self.score.append(part)
                
                self.progress_label.configure(text="Renderizando visualização...")
                self.progress_bar.set(0.9)
                self.update()
                
                # Visualizar (simplificado)
                self.visualize_score_simple()
                
                # Habilitar botões
                self.export_musicxml_btn.configure(state="normal")
                self.export_midi_btn.configure(state="normal")
                self.open_musescore_btn.configure(state="normal")
                
                elapsed = time.time() - start_time
                self.progress_bar.set(1.0)
                self.progress_label.configure(text=f"✅ Partitura gerada em {elapsed:.1f}s!")
                
                messagebox.showinfo("Sucesso", f"Partitura gerada com sucesso!\nTempo: {elapsed:.1f} segundos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar partitura:\n{e}")
                import traceback
                traceback.print_exc()
            finally:
                self.generate_score_btn.configure(state="normal")
        
        thread = threading.Thread(target=generate_thread)
        thread.start()
    
    def visualize_score_simple(self):
        """Visualização simplificada da partitura (mais rápida)"""
        for widget in self.score_viz_frame.winfo_children():
            widget.destroy()
        
        # Info básica em vez de renderização completa
        info_text = f"""
📊 INFORMAÇÕES DA PARTITURA

Título: {self.score.metadata.title}
Compositor: {self.score.metadata.composer}

Instrumentos: {len(self.score.parts)}

"""
        for part in self.score.parts:
            num_notes = len([n for n in part.flatten().notes if isinstance(n, note.Note)])
            num_rests = len([n for n in part.flatten().notes if isinstance(n, note.Rest)])
            info_text += f"  • {part.partName}: {num_notes} notas, {num_rests} pausas\n"
        
        info_text += f"\n✅ Partitura pronta para exportação!"
        
        info_label = ctk.CTkLabel(
            self.score_viz_frame,
            text=info_text,
            font=ctk.CTkFont(size=13),
            justify="left"
        )
        info_label.pack(pady=20, padx=20)
    
    def export_musicxml(self):
        """Exporta partitura como MusicXML"""
        if not self.score:
            messagebox.showwarning("Atenção", "Gere a partitura primeiro!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".musicxml",
            filetypes=[("MusicXML", "*.musicxml"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.score.write('musicxml', fp=filename)
                messagebox.showinfo("Sucesso", f"MusicXML salvo em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar:\n{e}")
    
    def export_midi(self):
        """Exporta partitura como MIDI"""
        if not self.score:
            messagebox.showwarning("Atenção", "Gere a partitura primeiro!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".mid",
            filetypes=[("MIDI", "*.mid"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                self.score.write('midi', fp=filename)
                messagebox.showinfo("Sucesso", f"MIDI salvo em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar:\n{e}")
    
    def open_musescore(self):
        """Abre a partitura no MuseScore"""
        if not self.score:
            messagebox.showwarning("Atenção", "Gere a partitura primeiro!")
            return
        
        try:
            # Salvar temporariamente
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.musicxml')
            self.score.write('musicxml', fp=temp_file.name)
            temp_file.close()
            
            # Tentar abrir
            if os.name == 'nt':  # Windows
                subprocess.Popen(['musescore', temp_file.name])
            elif os.name == 'posix':  # macOS/Linux
                subprocess.Popen(['musescore', temp_file.name])
            else:
                messagebox.showinfo("Info", f"Arquivo salvo em:\n{temp_file.name}\nAbra manualmente no MuseScore.")
                
        except FileNotFoundError:
            messagebox.showerror(
                "MuseScore Não Encontrado",
                "MuseScore não está instalado ou não está no PATH do sistema.\n\n"
                "Exporte como MusicXML e abra manualmente."
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir MuseScore:\n{e}")


# Funções auxiliares otimizadas
def reorder_notes(initial_note, octaves, octave_mode):
    """Reordena as notas começando pela nota inicial"""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    start_index = notes.index(initial_note)
    reordered = notes[start_index:] + notes[:start_index]
    
    note_list = [f"{note}{octaves[i % len(octaves)]}" for i, note in enumerate(reordered)]
    return note_list


def generate_rule_matrix(num_states, rule_type, **kwargs):
    """Gera a matriz de regras baseada no tipo selecionado"""
    if rule_type == 1:  # Determinística
        return np.array([[((i + j) % num_states) for j in range(num_states)] for i in range(num_states)])
    
    elif rule_type == 2:  # Thresholds
        thresholds = sorted(kwargs.get('thresholds', [3, 6]))
        rule_matrix = np.zeros((num_states, num_states), dtype=int)
        
        for i in range(num_states):
            for j in range(num_states):
                for t_index, threshold in enumerate(thresholds):
                    if j < threshold:
                        rule_matrix[i, j] = (i + (t_index + 1)) % num_states
                        break
                else:
                    rule_matrix[i, j] = 0
        return rule_matrix
    
    elif rule_type == 3:  # Aleatória
        return np.random.randint(0, num_states, size=(num_states, num_states), dtype=int)
    
    elif rule_type == 4:  # Matemática
        math_func_str = kwargs.get('math_function')
        if math_func_str:
            try:
                math_function = eval(f"lambda state, neighbor_sum, num_states: {math_func_str}")
            except:
                math_function = lambda state, neighbor_sum, num_states: (state + neighbor_sum) % num_states
        else:
            math_function = lambda state, neighbor_sum, num_states: (state + neighbor_sum) % num_states
        
        rule_matrix = np.zeros((num_states, num_states), dtype=int)
        
        for i in range(num_states):
            for j in range(num_states):
                try:
                    rule_matrix[i, j] = math_function(i, j, num_states) % num_states
                except:
                    rule_matrix[i, j] = (i + j) % num_states
        return rule_matrix
    
    elif rule_type == 5:  # Time-sensitive
        time_step = kwargs.get('time_step', 1)
        return np.array([[(i + j + time_step) % num_states for j in range(num_states)] for i in range(num_states)])
    
    return np.zeros((num_states, num_states), dtype=int)


def generate_ca(rule_matrix, generations, length, num_states, neighborhood_size, initial_cell):
    """Gera o autômato celular - OTIMIZADO"""
    ca = np.zeros((generations, length), dtype=int)
    ca[0, initial_cell] = 1
    
    for gen in range(1, generations):
        for i in range(length):
            neighbor_sum = 0
            for offset in range(-neighborhood_size, neighborhood_size + 1):
                if offset != 0:
                    neighbor_index = (i + offset) % length
                    neighbor_sum += ca[gen - 1, neighbor_index]
            
            current_state = ca[gen - 1, i]
            ca[gen, i] = rule_matrix[current_state, neighbor_sum % num_states]
    
    return ca


def ca_to_music21_optimized(ca, num_states, rhythmic_value, randomize_rhythm, note_list, 
                            selected_instrument, time_signature='4/4'):
    """
    OTIMIZADO: Converte o autômato celular em partitura com sistema rítmico inteligente
    que respeita compassos e NÃO usa quiálteras no modo aleatório
    """
    s = stream.Part()
    s.insert(0, clef.TrebleClef())
    s.insert(0, getattr(instrument, selected_instrument)())
    
    # Parsear fórmula de compasso
    numerator, denominator = map(int, time_signature.split('/'))
    beats_per_measure = numerator * (4.0 / denominator)  # Em quarter notes
    
    if randomize_rhythm:
        # NOVO: Sistema que respeita compassos
        current_beat = 0.0
        
        for row in ca:
            for cell in row:
                # Escolher duração que caiba no compasso
                available_durations = [d for d in RANDOM_DURATIONS if d <= (beats_per_measure - current_beat)]
                
                if not available_durations:
                    # Resetar compasso
                    current_beat = 0.0
                    available_durations = RANDOM_DURATIONS.copy()
                
                duration_value = random.choice(available_durations)
                
                # Adicionar nota ou pausa
                if cell > 0:
                    pitch = note_list[(cell - 1) % len(note_list)]
                    new_note = note.Note(pitch)
                    new_note.quarterLength = duration_value
                    s.append(new_note)
                else:
                    new_rest = note.Rest()
                    new_rest.quarterLength = duration_value
                    s.append(new_rest)
                
                # Atualizar posição no compasso
                current_beat += duration_value
                if current_beat >= beats_per_measure:
                    current_beat = 0.0
    else:
        # Modo fixo (sem randomização)
        for row in ca:
            for cell in row:
                if cell > 0:
                    pitch = note_list[(cell - 1) % len(note_list)]
                    new_note = note.Note(pitch)
                    new_note.quarterLength = rhythmic_value
                    s.append(new_note)
                else:
                    new_rest = note.Rest()
                    new_rest.quarterLength = rhythmic_value
                    s.append(new_rest)
    
    return s


if __name__ == "__main__":
    app = CellularAutomatonMusicGUI()
    app.mainloop()