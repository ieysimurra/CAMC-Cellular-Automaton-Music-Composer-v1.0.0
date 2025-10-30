"""
🎵 Compositor com Autômatos Celulares - Versão Web (Streamlit)
Aplicação interativa para composição musical algorítmica

Características:
- Interface web responsiva
- Visualização de partituras com Lilypond
- Integração com Hacklily
- Playback de áudio (MIDI)
- Exportação em múltiplos formatos
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import io
import base64
import tempfile
import os
import time
from pathlib import Path
import random
import subprocess
import json

# Music21 para geração de partituras
from music21 import (
    note, stream, metadata, duration, clef, instrument,
    tempo, meter, converter
)



# ==================== GERAÇÃO MANUAL DE LILYPOND (SEM INSTALAÇÃO) ====================

def note_to_lilypond(n):
    """Converte uma nota Music21 para formato Lilypond"""
    if isinstance(n, note.Rest):
        duration_map = {
            4.0: 'r1', 2.0: 'r2', 1.0: 'r4', 0.5: 'r8', 0.25: 'r16',
        }
        return duration_map.get(n.quarterLength, 'r4')
    
    elif isinstance(n, note.Note):
        pitch_name = n.pitch.name.lower().replace('#', 'is').replace('-', 'es')
        
        octave = n.pitch.octave
        if octave >= 4:
            octave_mark = "'" * (octave - 3)
        elif octave == 3:
            octave_mark = ""
        else:
            octave_mark = "," * (3 - octave)
        
        duration_map = {
            4.0: '1', 2.0: '2', 1.0: '4', 0.5: '8', 0.25: '16',
        }
        duration_str = duration_map.get(n.quarterLength, '4')
        
        return f"{pitch_name}{octave_mark}{duration_str}"
    
    return ""


def instrument_to_lilypond_name(instrument_name):
    """Converte nome do instrumento Music21 para nome Lilypond"""
    instrument_map = {
        'Flute': 'Flauta', 'Oboe': 'Oboé', 'Clarinet': 'Clarinete',
        'Bassoon': 'Fagote', 'Horn': 'Trompa', 'Trumpet': 'Trompete',
        'Trombone': 'Trombone', 'Tuba': 'Tuba', 'Violin': 'Violino',
        'Viola': 'Viola', 'Violoncello': 'Violoncelo', 'Contrabass': 'Contrabaixo'
    }
    return instrument_map.get(instrument_name, instrument_name)


def score_to_lilypond_manual(score):
    """Gera código Lilypond manualmente SEM PRECISAR DO LILYPOND INSTALADO"""
    try:
        title = score.metadata.title if score.metadata and score.metadata.title else "Composição CA"
        composer = score.metadata.composer if score.metadata and score.metadata.composer else "Compositor"
        
        lily_code = f'''\\version "2.24.0"

\\header {{
  title = "{title}"
  composer = "{composer}"
  tagline = "Gerado por Compositor CA"
}}

'''
        
        if score.parts:
            first_part = score.parts[0]
            tempo_mark = first_part.flatten().getElementsByClass('MetronomeMark')
            time_sig = first_part.flatten().getElementsByClass('TimeSignature')
            
            tempo_bpm = tempo_mark[0].number if tempo_mark else 120
            
            if time_sig:
                ts = time_sig[0]
                time_str = f"{ts.numerator}/{ts.denominator}"
            else:
                time_str = "4/4"
        else:
            tempo_bpm = 120
            time_str = "4/4"
        
        if len(score.parts) > 1:
            lily_code += "\\score {\n  <<\n"
        
        for part_idx, part in enumerate(score.parts):
            instrument_obj = part.getInstrument()
            instrument_name = instrument_to_lilypond_name(instrument_obj.instrumentName) if instrument_obj else f"Instrumento {part_idx + 1}"
            part_name = part.partName if hasattr(part, 'partName') else instrument_name
            
            notes_in_part = [n for n in part.flatten().notes if isinstance(n, note.Note)]
            if notes_in_part:
                avg_midi = sum(n.pitch.midi for n in notes_in_part) / len(notes_in_part)
                clef = "bass" if avg_midi < 60 else "treble"
            else:
                clef = "treble"
            
            lily_code += f'''    \\new Staff \\with {{
      instrumentName = "{part_name}"
    }} {{
      \\clef {clef}
      \\time {time_str}
      \\tempo 4 = {tempo_bpm}
      
'''
            
            lily_notes = []
            for element in part.flatten().notes:
                lily_note = note_to_lilypond(element)
                if lily_note:
                    lily_notes.append(lily_note)
            
            for i in range(0, len(lily_notes), 8):
                line_notes = lily_notes[i:i+8]
                lily_code += "      " + " ".join(line_notes) + "\n"
            
            lily_code += "    }\n"
        
        if len(score.parts) > 1:
            lily_code += "  >>\n  \\layout { }\n  \\midi { }\n}\n"
        else:
            lily_code += "\\layout { }\n\\midi { }\n"
        
        return lily_code
        
    except Exception as e:
        st.error(f"Erro ao gerar Lilypond manualmente: {str(e)}")
        return None


def create_hacklily_iframe(lilypond_code, height=600):
    """Cria um iframe incorporado do Hacklily"""
    encoded = base64.b64encode(lilypond_code.encode()).decode()
    hacklily_url = f"https://www.hacklily.org/#code={encoded}"
    
    iframe_html = f"""
    <div style="border: 2px solid #4CAF50; border-radius: 10px; overflow: hidden; margin: 20px 0;">
        <div style="background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;">
            🎵 Editor Hacklily Incorporado - Edite, Reproduza e Exporte sua Partitura
        </div>
        <iframe 
            src="{hacklily_url}" 
            width="100%" 
            height="{height}" 
            frameborder="0"
            style="border: none;"
        ></iframe>
    </div>
    """
    
    return iframe_html

# Configuração da página
st.set_page_config(
    page_title="🎵 Compositor CA",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CONSTANTES ====================

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

COLORS = [
    "#FF0000", "#FF7F00", "#FFFF00", "#7FFF00", "#00FF00", "#00FF7F",
    "#00FFFF", "#007FFF", "#0000FF", "#7F00FF", "#FF00FF", "#FF007F"
]
PAUSE_COLOR = "#CCCCCC"

RHYTHMIC_VALUES = {
    "Colcheia (1/8)": 0.5,
    "Semínima (1/4)": 1.0,
    "Mínima (1/2)": 2.0,
    "Semibreve (1/1)": 4.0
}

RANDOM_DURATIONS = [0.5, 1.0, 2.0, 4.0]

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

CATEGORIES = {
    "🌬️ Sopros de Madeira": ["Flauta", "Oboé", "Clarinete", "Fagote"],
    "🎺 Sopros de Metal": ["Trompa", "Trompete", "Trombone", "Tuba"],
    "🎻 Cordas": ["Violino", "Viola", "Violoncelo", "Contrabaixo"]
}

# ==================== INICIALIZAÇÃO DO SESSION STATE ====================

if 'instrument_configs' not in st.session_state:
    st.session_state.instrument_configs = {}

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Instrumentos'

if 'generated_score' not in st.session_state:
    st.session_state.generated_score = None

if 'ca_figures' not in st.session_state:
    st.session_state.ca_figures = {}

if 'midi_data' not in st.session_state:
    st.session_state.midi_data = None

if 'lilypond_code' not in st.session_state:
    st.session_state.lilypond_code = None

# ==================== FUNÇÕES AUXILIARES ====================

def reorder_notes(initial_note, octaves, octave_mode):
    """Reordena as notas começando pela nota inicial"""
    notes = NOTES.copy()
    start_index = notes.index(initial_note)
    reordered = notes[start_index:] + notes[:start_index]
    
    note_list = [f"{note}{octaves[i % len(octaves)]}" for i, note in enumerate(reordered)]
    return note_list


def generate_rule_matrix(num_states, rule_type, **kwargs):
    """Gera a matriz de regras"""
    if rule_type == "Determinística":
        return np.array([[((i + j) % num_states) for j in range(num_states)] 
                        for i in range(num_states)])
    
    elif rule_type == "Thresholds":
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
    
    elif rule_type == "Aleatória":
        return np.random.randint(0, num_states, size=(num_states, num_states), dtype=int)
    
    elif rule_type == "Matemática":
        math_func_str = kwargs.get('math_function', '(state + neighbor_sum) % num_states')
        try:
            math_function = eval(f"lambda state, neighbor_sum, num_states: {math_func_str}")
        except:
            math_function = lambda state, neighbor_sum, num_states: (state + neighbor_sum) % num_states
        
        rule_matrix = np.zeros((num_states, num_states), dtype=int)
        for i in range(num_states):
            for j in range(num_states):
                try:
                    rule_matrix[i, j] = math_function(i, j, num_states) % num_states
                except:
                    rule_matrix[i, j] = (i + j) % num_states
        return rule_matrix
    
    elif rule_type == "Time-Sensitive":
        time_step = kwargs.get('time_step', 1)
        return np.array([[(i + j + time_step) % num_states for j in range(num_states)] 
                        for i in range(num_states)])
    
    return np.zeros((num_states, num_states), dtype=int)


def generate_ca(rule_matrix, generations, length, num_states, neighborhood_size, initial_cell):
    """Gera o autômato celular"""
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


def ca_to_music21(ca, num_states, rhythmic_value, randomize_rhythm, 
                  note_list, selected_instrument, time_signature='4/4'):
    """Converte CA em partitura"""
    s = stream.Part()
    s.insert(0, clef.TrebleClef())
    s.insert(0, getattr(instrument, selected_instrument)())
    
    # Parse time signature
    numerator, denominator = map(int, time_signature.split('/'))
    beats_per_measure = numerator * (4.0 / denominator)
    
    if randomize_rhythm:
        current_beat = 0.0
        
        for row in ca:
            for cell in row:
                available_durations = [d for d in RANDOM_DURATIONS 
                                      if d <= (beats_per_measure - current_beat)]
                
                if not available_durations:
                    current_beat = 0.0
                    available_durations = RANDOM_DURATIONS.copy()
                
                duration_value = random.choice(available_durations)
                
                if cell > 0:
                    pitch = note_list[(cell - 1) % len(note_list)]
                    new_note = note.Note(pitch)
                    new_note.quarterLength = duration_value
                    s.append(new_note)
                else:
                    new_rest = note.Rest()
                    new_rest.quarterLength = duration_value
                    s.append(new_rest)
                
                current_beat += duration_value
                if current_beat >= beats_per_measure:
                    current_beat = 0.0
    else:
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


def visualize_ca(ca_result, instrument_name):
    """Cria visualização do CA"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = [PAUSE_COLOR] + COLORS[:ca_result.max()]
    cmap = ListedColormap(colors)
    
    im = ax.imshow(ca_result, cmap=cmap, aspect='auto', interpolation='nearest')
    ax.set_title(f'Autômato Celular - {instrument_name}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Posição', fontsize=11)
    ax.set_ylabel('Geração (Tempo)', fontsize=11)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Estado', rotation=270, labelpad=15)
    
    plt.tight_layout()
    return fig


def fig_to_bytes(fig):
    """Converte figura matplotlib para bytes"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf.getvalue()


def score_to_lilypond(score):
    """
    Converte partitura para código Lilypond
    USA GERAÇÃO MANUAL - NÃO PRECISA DO LILYPOND INSTALADO!
    """
    try:
        # Gerar código manualmente
        lilypond_code = score_to_lilypond_manual(score)
        
        # Validar
        if lilypond_code and len(lilypond_code.strip()) > 0:
            st.success(f"✅ Código Lilypond gerado: {len(lilypond_code)} caracteres")
            return lilypond_code
        else:
            st.error("❌ Erro: Código Lilypond vazio")
            return None
            
    except Exception as e:
        st.error(f"❌ Erro ao gerar Lilypond: {str(e)}")
        st.info(f"💡 Verifique se a partitura está válida")
        return None


def score_to_midi_bytes(score):
    """Converte partitura para bytes MIDI com tratamento robusto e debug"""
    try:
        # Criar arquivo temporário
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mid', mode='wb')
        temp_filename = temp_file.name
        temp_file.close()
        
        # Escrever MIDI
        score.write('midi', fp=temp_filename)
        
        # Aguardar escrita completar
        time.sleep(0.2)
        
        # Verificar se arquivo foi criado
        if not os.path.exists(temp_filename):
            st.error("❌ Erro: Arquivo MIDI não foi criado")
            return None
        
        # Ler bytes
        with open(temp_filename, 'rb') as f:
            midi_bytes = f.read()
        
        # Verificar se tem conteúdo
        if len(midi_bytes) == 0:
            st.error("❌ Erro: Arquivo MIDI está vazio")
            return None
        
        # Tentar deletar (com retry)
        max_retries = 5
        for attempt in range(max_retries):
            try:
                os.unlink(temp_filename)
                break
            except (PermissionError, OSError):
                if attempt < max_retries - 1:
                    time.sleep(0.3)
                else:
                    pass
        
        return midi_bytes
        
    except Exception as e:
        st.error(f"❌ Erro ao gerar MIDI: {str(e)}")
        try:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
        except:
            pass
        return None


def create_hacklily_url(lilypond_code):
    """Cria URL para abrir no Hacklily"""
    # Codificar em base64
    encoded = base64.b64encode(lilypond_code.encode()).decode()
    return f"https://www.hacklily.org/#code={encoded}"




def create_midi_player_html(midi_bytes):
    """Cria player MIDI usando embed HTML"""
    # Converter para base64
    midi_b64 = base64.b64encode(midi_bytes).decode()
    
    html = f"""
    <div style="padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
        <h3 style="margin-top: 0;">🎹 MIDI Player</h3>
        <p style="margin-bottom: 15px; font-size: 14px;">
            ⚠️ <b>Importante:</b> O playback de MIDI no navegador tem suporte limitado.<br>
            Se não funcionar, faça o download e use um player externo (VLC, Windows Media Player, etc.)
        </p>
        <audio controls style="width: 100%;">
            <source src="data:audio/midi;base64,{midi_b64}" type="audio/midi">
            Seu navegador não suporta o elemento de áudio.
        </audio>
    </div>
    """
    return html


def render_lilypond_to_png(lilypond_code):
    """Renderiza Lilypond para PNG (requer lilypond instalado) - Windows safe"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ly_file = os.path.join(tmpdir, 'score.ly')
            
            # Escrever arquivo Lilypond
            with open(ly_file, 'w', encoding='utf-8') as f:
                f.write(lilypond_code)
            
            # Garantir que arquivo foi escrito
            time.sleep(0.1)
            
            # Executar lilypond
            result = subprocess.run(
                ['lilypond', '--png', '-o', tmpdir, ly_file],
                capture_output=True,
                timeout=30,
                text=True
            )
            
            # Esperar processamento completar
            time.sleep(0.2)
            
            # Procurar PNG gerado
            png_files = list(Path(tmpdir).glob('*.png'))
            if png_files:
                with open(png_files[0], 'rb') as f:
                    png_data = f.read()
                return png_data
            
    except FileNotFoundError:
        # Lilypond não instalado
        return None
    except subprocess.TimeoutExpired:
        # Timeout
        return None
    except Exception as e:
        # Outro erro
        return None
    
    return None


# ==================== INTERFACE STREAMLIT ====================

def main():
    # Header
    st.title("🎵 Compositor com Autômatos Celulares")
    st.markdown("### Composição Musical Algorítmica Interativa")
    
    # Sidebar para navegação
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1E3A8A/FFFFFF?text=CA+Music", 
                use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📍 Navegação")
        
        page = st.radio(
            "Selecione a seção:",
            ["🎼 Instrumentos", "⚙️ Configuração", "🎨 Visualização CA", "📝 Partitura"],
            key='navigation'
        )
        
        st.markdown("---")
        
        # Info sobre instrumentos configurados
        if st.session_state.instrument_configs:
            st.markdown("### 🎻 Instrumentos Ativos")
            for inst in st.session_state.instrument_configs.keys():
                has_ca = st.session_state.instrument_configs[inst].get('ca_result') is not None
                icon = "✅" if has_ca else "⚠️"
                st.markdown(f"{icon} {inst}")
        
        st.markdown("---")
        st.markdown("**Versão Web 1.0**")
        st.markdown("Desenvolvido com Streamlit")
    
    # Roteamento de páginas
    if "🎼 Instrumentos" in page:
        page_instruments()
    elif "⚙️ Configuração" in page:
        page_configuration()
    elif "🎨 Visualização" in page:
        page_visualization()
    elif "📝 Partitura" in page:
        page_score()


# ==================== PÁGINA 1: INSTRUMENTOS ====================

def page_instruments():
    st.header("🎼 Seleção de Instrumentos")
    st.markdown("Escolha os instrumentos para sua composição")
    
    st.markdown("---")
    
    # Organizar em colunas por categoria
    for category, instruments in CATEGORIES.items():
        st.subheader(category)
        
        cols = st.columns(len(instruments))
        
        for idx, inst in enumerate(instruments):
            with cols[idx]:
                st.markdown(f"**{inst}**")
                
                # Quantidade
                qty = st.number_input(
                    "Quantidade",
                    min_value=0,
                    max_value=4,
                    value=0,
                    key=f"qty_{inst}"
                )
                
                # Atualizar configurações
                current_instances = [k for k in st.session_state.instrument_configs.keys() 
                                    if k.startswith(inst)]
                
                # Adicionar/remover instâncias
                if qty > len(current_instances):
                    for i in range(len(current_instances), qty):
                        inst_name = f"{inst} {i+1}" if qty > 1 else inst
                        st.session_state.instrument_configs[inst_name] = {
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
                            'rule_type': 'Determinística',
                            'rule_params': {},
                            'ca_result': None
                        }
                elif qty < len(current_instances):
                    for i in range(qty, len(current_instances)):
                        inst_name = f"{inst} {i+1}" if len(current_instances) > 1 else inst
                        if inst_name in st.session_state.instrument_configs:
                            del st.session_state.instrument_configs[inst_name]
    
    st.markdown("---")
    
    # Resumo
    if st.session_state.instrument_configs:
        st.success(f"✅ {len(st.session_state.instrument_configs)} instrumento(s) selecionado(s)")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Instrumentos ativos:**")
            for inst in st.session_state.instrument_configs.keys():
                st.markdown(f"• {inst}")
        
        with col2:
            if st.button("➡️ Configurar", type="primary"):
                st.session_state.current_page = 'Configuração'
                st.rerun()
    else:
        st.info("ℹ️ Selecione pelo menos um instrumento para continuar")


# ==================== PÁGINA 2: CONFIGURAÇÃO ====================

def page_configuration():
    st.header("⚙️ Configuração dos Instrumentos")
    
    if not st.session_state.instrument_configs:
        st.warning("⚠️ Nenhum instrumento selecionado! Volte para a seção Instrumentos.")
        return
    
    # Seletor de instrumento
    inst_names = list(st.session_state.instrument_configs.keys())
    selected_inst = st.selectbox("Selecione o instrumento para configurar:", inst_names)
    
    config = st.session_state.instrument_configs[selected_inst]
    
    st.markdown("---")
    
    # Tabs para organizar configurações
    tab1, tab2, tab3 = st.tabs(["🎵 Música", "🔬 Autômato Celular", "🔢 Regras"])
    
    # TAB 1: Configurações Musicais
    with tab1:
        st.subheader("Configurações Musicais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config['initial_note'] = st.selectbox(
                "Nota Inicial",
                NOTES,
                index=NOTES.index(config.get('initial_note', 'C'))
            )
            
            config['octave_mode'] = st.selectbox(
                "Modo de Oitava",
                ["Crescente", "Decrescente", "Intercalada"],
                index=["Crescente", "Decrescente", "Intercalada"].index(
                    config.get('octave_mode', 'Crescente')
                )
            )
        
        with col2:
            octaves_str = st.text_input(
                "Oitavas (separadas por vírgula)",
                value=','.join(map(str, config.get('octaves', [4])))
            )
            config['octaves'] = [int(x.strip()) for x in octaves_str.split(',')]
            
            rhythm_key = st.selectbox(
                "Valor Rítmico Base",
                list(RHYTHMIC_VALUES.keys()),
                index=1
            )
            config['rhythmic_value'] = RHYTHMIC_VALUES[rhythm_key]
        
        config['randomize_rhythm'] = st.checkbox(
            "🎲 Randomizar durações (respeitando compassos)",
            value=config.get('randomize_rhythm', False)
        )
    
    # TAB 2: Parâmetros do CA
    with tab2:
        st.subheader("Parâmetros do Autômato Celular")
        
        col1, col2 = st.columns(2)
        
        with col1:
            config['num_states'] = st.slider(
                "Número de Estados",
                min_value=2,
                max_value=12,
                value=config.get('num_states', 8)
            )
            
            config['generations'] = st.slider(
                "Gerações (tempo musical)",
                min_value=10,
                max_value=100,
                value=config.get('generations', 20)
            )
            
            config['length'] = st.slider(
                "Comprimento (largura espacial)",
                min_value=20,
                max_value=150,
                value=config.get('length', 50)
            )
        
        with col2:
            config['neighborhood_size'] = st.slider(
                "Tamanho da Vizinhança",
                min_value=1,
                max_value=5,
                value=config.get('neighborhood_size', 1)
            )
            
            config['initial_cell'] = st.number_input(
                "Célula Inicial",
                min_value=0,
                max_value=config['length']-1,
                value=min(config.get('initial_cell', 25), config['length']-1)
            )
    
    # TAB 3: Regras
    with tab3:
        st.subheader("Regras de Transição")
        
        config['rule_type'] = st.selectbox(
            "Tipo de Regra",
            ["Determinística", "Thresholds", "Aleatória", "Matemática", "Time-Sensitive"],
            index=["Determinística", "Thresholds", "Aleatória", "Matemática", "Time-Sensitive"].index(
                config.get('rule_type', 'Determinística')
            )
        )
        
        # Parâmetros específicos
        if config['rule_type'] == "Thresholds":
            thresholds_str = st.text_input(
                "Thresholds (separados por vírgula)",
                value="3,6"
            )
            config['rule_params']['thresholds'] = [int(x.strip()) for x in thresholds_str.split(',')]
        
        elif config['rule_type'] == "Matemática":
            config['rule_params']['math_function'] = st.text_input(
                "Função Matemática",
                value="(state + neighbor_sum) % num_states",
                help="Variáveis: state, neighbor_sum, num_states"
            )
        
        elif config['rule_type'] == "Time-Sensitive":
            config['rule_params']['time_step'] = st.number_input(
                "Time Step",
                min_value=1,
                max_value=10,
                value=1
            )
    
    st.markdown("---")
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configuração", type="primary", use_container_width=True):
            st.success(f"✅ Configuração de '{selected_inst}' salva!")
    
    with col2:
        if st.button("🎨 Gerar CA", use_container_width=True):
            with st.spinner("Gerando autômato celular..."):
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
                
                # Armazenar
                config['ca_result'] = ca_result
                
                # Criar visualização
                fig = visualize_ca(ca_result, selected_inst)
                st.session_state.ca_figures[selected_inst] = fig
                
                st.success("✅ CA gerado com sucesso!")
                st.pyplot(fig)
    
    with col3:
        if config.get('ca_result') is not None:
            if st.button("📥 Baixar Imagem CA", use_container_width=True):
                if selected_inst in st.session_state.ca_figures:
                    img_bytes = fig_to_bytes(st.session_state.ca_figures[selected_inst])
                    st.download_button(
                        label="Salvar PNG",
                        data=img_bytes,
                        file_name=f"CA_{selected_inst.replace(' ', '_')}.png",
                        mime="image/png"
                    )


# ==================== PÁGINA 3: VISUALIZAÇÃO CA ====================

def page_visualization():
    st.header("🎨 Visualização dos Autômatos Celulares")
    
    if not st.session_state.instrument_configs:
        st.warning("⚠️ Nenhum instrumento configurado!")
        return
    
    # Filtrar instrumentos com CA gerado
    instruments_with_ca = {
        inst: config for inst, config in st.session_state.instrument_configs.items()
        if config.get('ca_result') is not None
    }
    
    if not instruments_with_ca:
        st.info("ℹ️ Nenhum CA gerado ainda. Configure os instrumentos e gere os CAs.")
        return
    
    st.markdown(f"**{len(instruments_with_ca)} CA(s) gerado(s)**")
    
    # Botão para gerar todos os CAs
    if st.button("🔄 Gerar Todos os CAs", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        total = len(st.session_state.instrument_configs)
        
        for idx, (inst, config) in enumerate(st.session_state.instrument_configs.items()):
            status_text.text(f"Gerando CA para {inst}...")
            progress_bar.progress((idx + 1) / total)
            
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
            
            config['ca_result'] = ca_result
            
            # Criar visualização
            fig = visualize_ca(ca_result, inst)
            st.session_state.ca_figures[inst] = fig
        
        status_text.text("✅ Todos os CAs gerados!")
        st.rerun()
    
    st.markdown("---")
    
    # Visualizar todos os CAs em grid
    cols_per_row = 2
    instruments = list(instruments_with_ca.keys())
    
    for i in range(0, len(instruments), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(instruments):
                inst = instruments[i + j]
                
                with col:
                    st.subheader(inst)
                    
                    if inst in st.session_state.ca_figures:
                        st.pyplot(st.session_state.ca_figures[inst])
                        
                        # Botão de download
                        img_bytes = fig_to_bytes(st.session_state.ca_figures[inst])
                        st.download_button(
                            label="📥 Baixar PNG",
                            data=img_bytes,
                            file_name=f"CA_{inst.replace(' ', '_')}.png",
                            mime="image/png",
                            key=f"download_ca_{inst}"
                        )


# ==================== PÁGINA 4: PARTITURA ====================

def page_score():
    st.header("📝 Geração e Visualização da Partitura")
    
    if not st.session_state.instrument_configs:
        st.warning("⚠️ Nenhum instrumento configurado!")
        return
    
    # Verificar se todos têm CA
    missing_ca = [inst for inst, config in st.session_state.instrument_configs.items()
                  if config.get('ca_result') is None]
    
    if missing_ca:
        st.error(f"⚠️ Os seguintes instrumentos não têm CA gerado:\n\n" + "\n".join(f"• {i}" for i in missing_ca))
        return
    
    st.markdown("---")
    
    # Configurações globais da partitura
    st.subheader("⚙️ Configurações Globais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_title = st.text_input("Título", value="Composição CA")
    
    with col2:
        composer = st.text_input("Compositor", value="Algoritmo")
    
    with col3:
        tempo_bpm = st.number_input("Tempo (BPM)", min_value=40, max_value=240, value=120)
    
    with col4:
        time_sig = st.selectbox("Compasso", ["2/4", "3/4", "4/4", "5/4", "6/8", "9/8", "12/8"], index=2)
    
    st.markdown("---")
    
    # Botão de geração
    if st.button("🎼 GERAR PARTITURA", type="primary", use_container_width=True):
        with st.spinner("Gerando partitura..."):
            # Criar partitura
            score = stream.Score()
            
            # Metadados
            score.metadata = metadata.Metadata()
            score.metadata.title = score_title
            score.metadata.composer = composer
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_instruments = len(st.session_state.instrument_configs)
            
            for idx, (inst_name, config) in enumerate(st.session_state.instrument_configs.items()):
                status_text.text(f"Processando {inst_name}... ({idx+1}/{total_instruments})")
                progress_bar.progress((idx + 1) / total_instruments)
                
                # Reordenar notas
                note_list = reorder_notes(
                    config['initial_note'],
                    config['octaves'],
                    config['octave_mode']
                )
                
                # Converter CA para música
                part = ca_to_music21(
                    config['ca_result'],
                    config['num_states'],
                    config['rhythmic_value'],
                    config['randomize_rhythm'],
                    note_list,
                    INSTRUMENTS_PT[config['base_instrument']],
                    time_sig
                )
                
                # Adicionar metadados
                part.partName = inst_name
                part.insert(0, tempo.MetronomeMark(number=tempo_bpm))
                part.insert(0, meter.TimeSignature(time_sig))
                
                score.append(part)
            
            # Armazenar partitura
            st.session_state.generated_score = score
            
            # Gerar MIDI
            st.session_state.midi_data = score_to_midi_bytes(score)
            
            # Gerar Lilypond
            st.session_state.lilypond_code = score_to_lilypond(score)
            
            status_text.text("✅ Partitura gerada com sucesso!")
            st.success("🎉 Partitura pronta!")
    
    # Se partitura foi gerada, mostrar opções
    if st.session_state.generated_score:
        st.markdown("---")
        st.subheader("📊 Informações da Partitura")
        
        score = st.session_state.generated_score
        
        # Estatísticas
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Título:** {score.metadata.title}")
            st.markdown(f"**Compositor:** {score.metadata.composer}")
            st.markdown(f"**Instrumentos:** {len(score.parts)}")
            
            for part in score.parts:
                num_notes = len([n for n in part.flatten().notes if isinstance(n, note.Note)])
                num_rests = len([n for n in part.flatten().notes if isinstance(n, note.Rest)])
                st.markdown(f"• **{part.partName}**: {num_notes} notas, {num_rests} pausas")
        
        with col2:
            st.metric("Total de Notas", sum(len([n for n in p.flatten().notes if isinstance(n, note.Note)]) 
                                            for p in score.parts))
            st.metric("Total de Pausas", sum(len([n for n in p.flatten().notes if isinstance(n, note.Rest)]) 
                                             for p in score.parts))
        
        st.markdown("---")
        
        # Seção de exportação
        st.subheader("📤 Exportação e Visualização")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🎹 Playback", "📄 MusicXML", "🎵 Lilypond", "🌐 Hacklily"])
        
        # TAB 1: Playback MIDI
        with tab1:
            st.markdown("### 🎹 Reproduzir Partitura")
            
            if st.session_state.midi_data and len(st.session_state.midi_data) > 0:
                # Exibir tamanho do arquivo para debug
                st.success(f"✅ Arquivo MIDI gerado: {len(st.session_state.midi_data)} bytes")
                
                # Botão de download (sempre funciona)
                st.download_button(
                    label="📥 Baixar MIDI",
                    data=st.session_state.midi_data,
                    file_name=f"{score_title.replace(' ', '_')}.mid",
                    mime="audio/midi",
                    type="primary"
                )
                
                st.markdown("---")
                
                # Player HTML
                st.markdown("#### 🔊 Reproduzir no Navegador")
                st.info("""
                **Nota sobre compatibilidade:**
                - ✅ O download sempre funcionará
                - ⚠️ O playback no navegador pode não funcionar em todos os casos
                - 💡 Recomendamos usar um player externo para melhor resultado
                """)
                
                # Player HTML
                player_html = create_midi_player_html(st.session_state.midi_data)
                st.components.v1.html(player_html, height=200)
                
            else:
                st.error("❌ MIDI não foi gerado corretamente")
                st.info("💡 Tente gerar a partitura novamente")
        
        # TAB 2: MusicXML
        with tab2:
            st.markdown("### 📄 Exportar MusicXML")
            st.info("Formato universal compatível com MuseScore, Finale, Sibelius, etc.")
            
            # Gerar MusicXML com tratamento robusto
            try:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.musicxml', mode='w', encoding='utf-8')
                temp_filename = temp_file.name
                temp_file.close()
                
                score.write('musicxml', fp=temp_filename)
                time.sleep(0.1)
                
                with open(temp_filename, 'rb') as f:
                    musicxml_data = f.read()
                
                # Tentar deletar com retry
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        os.unlink(temp_filename)
                        break
                    except PermissionError:
                        if attempt < max_retries - 1:
                            time.sleep(0.2)
                        else:
                            pass
                
                st.download_button(
                    label="📥 Baixar MusicXML",
                    data=musicxml_data,
                    file_name=f"{score_title.replace(' ', '_')}.musicxml",
                    mime="application/xml",
                    type="primary"
                )
                
            except Exception as e:
                st.error(f"Erro ao gerar MusicXML: {e}")
                st.info("Tente novamente ou use outro formato de exportação.")
        
        # TAB 3: Lilypond
        with tab3:
            st.markdown("### 🎵 Código Lilypond")
            
            if st.session_state.lilypond_code and len(st.session_state.lilypond_code.strip()) > 0:
                # Exibir info
                st.success(f"✅ Código Lilypond gerado: {len(st.session_state.lilypond_code)} caracteres")
                
                # Preview do código
                preview_length = min(1500, len(st.session_state.lilypond_code))
                st.code(st.session_state.lilypond_code[:preview_length] + "\n...", language="text")
                
                # Download
                st.download_button(
                    label="📥 Baixar .ly",
                    data=st.session_state.lilypond_code,
                    file_name=f"{score_title.replace(' ', '_')}.ly",
                    mime="text/plain",
                    type="primary"
                )
                
                st.markdown("---")
                
                # Renderizar PNG (opcional)
                if st.button("🖼️ Renderizar Partitura (PNG)", help="Requer Lilypond instalado no sistema"):
                    with st.spinner("Renderizando com Lilypond..."):
                        png_data = render_lilypond_to_png(st.session_state.lilypond_code)
                        
                        if png_data:
                            st.image(png_data, caption="Partitura renderizada")
                            
                            st.download_button(
                                label="📥 Baixar PNG",
                                data=png_data,
                                file_name=f"{score_title.replace(' ', '_')}.png",
                                mime="image/png"
                            )
                        else:
                            st.error("❌ Lilypond não está instalado ou não foi encontrado")
                            st.info("📥 Para instalar Lilypond: https://lilypond.org/download.html")
            else:
                st.error("❌ Código Lilypond não foi gerado")
                st.warning("""
                **Possíveis causas:**
                - Erro na conversão da partitura
                - Problema com arquivos temporários
                - Partitura vazia ou inválida
                
                **Solução:** Tente gerar a partitura novamente
                """)
        
        # TAB 4: Hacklily
        with tab4:
            st.markdown("### 🌐 Visualizar no Hacklily")
            
            if st.session_state.lilypond_code and len(st.session_state.lilypond_code.strip()) > 0:
                
                # Opção de visualização
                view_mode = st.radio(
                    "Como deseja visualizar a partitura?",
                    ["🖼️ Visualizar Aqui na Página (Recomendado)", "📱 Abrir em Nova Aba"],
                    horizontal=True,
                    help="Escolha entre visualizar o editor incorporado ou abrir em nova aba"
                )
                
                st.markdown("---")
                
                if view_mode == "🖼️ Visualizar Aqui na Página (Recomendado)":
                    # NOVA OPÇÃO: Visualizar na página
                    st.success("✨ Editor Hacklily incorporado abaixo!")
                    st.info("📖 Você pode editar o código, reproduzir a música e exportar como PDF diretamente no editor!")
                    
                    # Altura do iframe
                    iframe_height = st.slider(
                        "Altura do editor", 
                        min_value=400, 
                        max_value=1000, 
                        value=650, 
                        step=50,
                        help="Ajuste a altura do editor para sua preferência"
                    )
                    
                    # Renderizar iframe
                    iframe_html = create_hacklily_iframe(
                        st.session_state.lilypond_code, 
                        height=iframe_height
                    )
                    
                    st.components.v1.html(iframe_html, height=iframe_height + 60)
                    
                    st.markdown("---")
                    st.markdown("**💡 Dicas de uso:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("- ✏️ Edite o código diretamente no editor")
                        st.markdown("- 🎵 Clique em 'Play' para ouvir")
                        st.markdown("- 📄 Use 'Export PDF' para salvar")
                    with col2:
                        st.markdown("- 💾 Alterações não afetam o original")
                        st.markdown("- 🔄 Recarregue a página para resetar")
                        st.markdown("- 📋 Copie o código se precisar")
                    
                else:
                    # Opção original: abrir em nova aba
                    st.info("🚀 A partitura será aberta no Hacklily em uma nova aba do navegador")
                    
                    hacklily_url = create_hacklily_url(st.session_state.lilypond_code)
                    
                    st.markdown(f"""
                    <a href="{hacklily_url}" target="_blank">
                        <button style="
                            background-color: #4CAF50;
                            color: white;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border: none;
                            border-radius: 4px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        ">
                            🌐 Abrir no Hacklily (Nova Aba)
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("**📖 Instruções:**")
                    st.markdown("1. ✅ Clique no botão acima")
                    st.markdown("2. 🎵 Partitura carrega automaticamente")
                    st.markdown("3. ✏️ Edite, reproduza e exporte")
                
                # Seções comuns
                st.markdown("---")
                
                with st.expander("📝 Ver código Lilypond completo"):
                    st.code(st.session_state.lilypond_code, language="text")
                    st.download_button(
                        label="📥 Baixar código .ly",
                        data=st.session_state.lilypond_code,
                        file_name=f"{score_title.replace(' ', '_')}.ly",
                        mime="text/plain"
                    )
                
                with st.expander("🔗 Ver URL do Hacklily"):
                    hacklily_url = create_hacklily_url(st.session_state.lilypond_code)
                    st.code(hacklily_url, language="text")
                    st.caption("💡 Copie esta URL para compartilhar a partitura")
                
                with st.expander("ℹ️ Sobre o Hacklily"):
                    st.markdown("""
                    **Hacklily** é um editor online de partituras baseado em Lilypond.
                    
                    **Recursos:**
                    - ✏️ Edição de código Lilypond em tempo real
                    - 🎵 Reprodução MIDI da partitura
                    - 📄 Exportação para PDF
                    - 🔗 Compartilhamento via URL
                    - 💾 Salvamento local
                    
                    **Site oficial:** https://www.hacklily.org
                    """)
                
            else:
                st.error("❌ Código Lilypond não disponível")
                st.warning("⚠️ O Hacklily requer código Lilypond para funcionar")
                st.info("💡 Gere a partitura primeiro clicando em 'Gerar Partitura' na aba 'Partitura'")
                
                # Mostrar motivo se houver erro
                if hasattr(st.session_state, 'lilypond_error'):
                    st.error(f"**Erro detectado:** {st.session_state.lilypond_error}")


# ==================== EXECUTAR APLICAÇÃO ====================

if __name__ == "__main__":
    main()