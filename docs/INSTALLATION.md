# 🔧 Guia de Instalação Completo - Passo a Passo

[🇧🇷 Português](docs/INSTALLATION_PT.md) | [🇺🇸 English](docs/INSTALLATION.md)

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Instalação no Windows](#instalação-no-windows)
3. [Instalação no macOS](#instalação-no-macos)
4. [Instalação no Linux](#instalação-no-linux)
5. [Verificação da Instalação](#verificação-da-instalação)
6. [Solução de Problemas](#solução-de-problemas)

---

## Pré-requisitos

### Requisitos de Sistema

| Componente | Mínimo | Recomendado |
|------------|---------|-------------|
| **SO** | Windows 10, macOS 10.14, Ubuntu 18.04 | Mais recente |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 4GB | 8GB+ |
| **Espaço** | 500MB | 1GB |
| **Processador** | Dual-core | Quad-core+ |

### Software Necessário

- ✅ **Python 3.8+** (obrigatório)
- ✅ **pip** (geralmente vem com Python)
- ✅ **Git** (recomendado, mas opcional)
- ⚪ **MuseScore** (opcional, para edição de partituras)
- ⚪ **VLC Media Player** (opcional, para playback MIDI)

---

## Instalação no Windows

### Opção 1: Instalação Rápida (Recomendada)

#### Passo 1: Instalar Python

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Clique em "Download Python 3.11.x" (versão mais recente)
3. Execute o instalador baixado
4. ⚠️ **IMPORTANTE**: Marque **"Add Python to PATH"**
5. Clique em "Install Now"
6. Aguarde a instalação completar

**Verificar instalação:**
```cmd
python --version
```
Deve mostrar: `Python 3.11.x` (ou sua versão)

#### Passo 2: Baixar o Projeto

**Com Git (Recomendado):**
```cmd
# Abra o Command Prompt ou PowerShell
cd Desktop
git clone https://github.com/seu-usuario/ca-music-composer.git
cd ca-music-composer
```

**Sem Git (Download Manual):**
1. Vá para https://github.com/seu-usuario/ca-music-composer
2. Clique em "Code" → "Download ZIP"
3. Extraia o ZIP para Desktop
4. Abra Command Prompt:
```cmd
cd Desktop\ca-music-composer
```

#### Passo 3: Criar Ambiente Virtual

```cmd
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Você verá (venv) antes do prompt
```

#### Passo 4: Instalar Dependências

**Para versão Web (Streamlit):**
```cmd
pip install -r requirements-streamlit.txt
```

**Para versão Desktop:**
```cmd
pip install -r requirements-desktop.txt
```

**Para instalar ambas:**
```cmd
pip install -r requirements-streamlit.txt
pip install -r requirements-desktop.txt
```

#### Passo 5: Executar a Aplicação

**Versão Web:**
```cmd
streamlit run CA-poly-instrument-11-streamlit.py
```

**Versão Desktop:**
```cmd
python CA-poly-instrument-13-complexRhy.py
```

---

### Opção 2: Instalação via Anaconda

#### Passo 1: Instalar Anaconda

1. Baixe Anaconda: [anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)
2. Execute o instalador
3. Siga o wizard de instalação

#### Passo 2: Criar Ambiente Conda

```cmd
# Abra Anaconda Prompt

# Criar ambiente
conda create -n ca-music python=3.10

# Ativar ambiente
conda activate ca-music

# Navegar para o projeto
cd Desktop\ca-music-composer

# Instalar dependências
pip install -r requirements-streamlit.txt
```

---

## Instalação no macOS

### Passo 1: Instalar Homebrew (se não tiver)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Passo 2: Instalar Python

```bash
brew install python@3.11
```

Verificar:
```bash
python3 --version
```

### Passo 3: Baixar o Projeto

```bash
cd ~/Desktop
git clone https://github.com/seu-usuario/ca-music-composer.git
cd ca-music-composer
```

### Passo 4: Criar Ambiente Virtual

```bash
# Criar ambiente
python3 -m venv venv

# Ativar
source venv/bin/activate
```

### Passo 5: Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements-streamlit.txt
```

### Passo 6: Executar

```bash
# Web
streamlit run CA-poly-instrument-11-streamlit.py

# Desktop
python CA-poly-instrument-13-complexRhy.py
```

---

## Instalação no Linux

### Ubuntu/Debian

#### Passo 1: Atualizar Sistema

```bash
sudo apt update
sudo apt upgrade
```

#### Passo 2: Instalar Python e Dependências

```bash
# Instalar Python
sudo apt install python3.10 python3.10-venv python3-pip

# Instalar Git
sudo apt install git
```

#### Passo 3: Baixar Projeto

```bash
cd ~/Desktop
git clone https://github.com/seu-usuario/ca-music-composer.git
cd ca-music-composer
```

#### Passo 4: Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Passo 5: Dependências

```bash
pip install --upgrade pip
pip install -r requirements-streamlit.txt
```

#### Passo 6: Executar

```bash
streamlit run CA-poly-instrument-11-streamlit.py
```

### Fedora/RHEL

```bash
# Instalar Python
sudo dnf install python3 python3-pip git

# Resto igual ao Ubuntu
```

### Arch Linux

```bash
# Instalar Python
sudo pacman -S python python-pip git

# Resto igual ao Ubuntu
```

---

## Verificação da Instalação

### Teste Rápido

Execute este comando para verificar todas as dependências:

```python
# Crie um arquivo test_install.py com este conteúdo:

import sys

def test_imports():
    print("Testing imports...")
    
    try:
        import streamlit
        print("✓ streamlit")
    except:
        print("✗ streamlit - INSTALL: pip install streamlit")
    
    try:
        import numpy
        print("✓ numpy")
    except:
        print("✗ numpy - INSTALL: pip install numpy")
    
    try:
        import matplotlib
        print("✓ matplotlib")
    except:
        print("✗ matplotlib - INSTALL: pip install matplotlib")
    
    try:
        from music21 import note
        print("✓ music21")
    except:
        print("✗ music21 - INSTALL: pip install music21")
    
    try:
        import customtkinter
        print("✓ customtkinter (for desktop version)")
    except:
        print("✗ customtkinter - INSTALL: pip install customtkinter")
    
    print("\nPython version:", sys.version)

if __name__ == "__main__":
    test_imports()
```

Execute:
```bash
python test_install.py
```

### Teste Funcional

**Teste Streamlit:**
```bash
streamlit hello
```
Deve abrir uma demo no navegador.

**Teste Music21:**
```python
python -c "from music21 import note; n = note.Note('C4'); print('Music21 OK!')"
```

---

## Solução de Problemas

### Problema: "python: command not found"

**Windows:**
```cmd
# Use 'py' em vez de 'python'
py --version
py -m pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Use 'python3' em vez de 'python'
python3 --version
python3 -m pip install -r requirements.txt
```

---

### Problema: "pip: command not found"

**Instalar pip:**

**Windows:**
```cmd
python -m ensurepip --upgrade
```

**macOS/Linux:**
```bash
python3 -m ensurepip --upgrade
```

---

### Problema: "Permission denied" (Linux/macOS)

**Solução 1 (Recomendada):**
```bash
# Use ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Solução 2 (Não recomendada):**
```bash
pip install --user -r requirements.txt
```

---

### Problema: Erro ao instalar music21

**Windows:**
```cmd
# Instale Microsoft C++ Build Tools
# Baixe de: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**macOS:**
```bash
xcode-select --install
```

**Linux:**
```bash
sudo apt install build-essential python3-dev
```

---

### Problema: Streamlit não abre no navegador

**Solução:**
```bash
# Execute com porta específica
streamlit run CA-poly-instrument-11-streamlit.py --server.port 8502

# Abra manualmente:
# http://localhost:8502
```

---

### Problema: "ModuleNotFoundError"

**Causa:** Dependência não instalada

**Solução:**
```bash
# Reinstalar todas as dependências
pip install -r requirements-streamlit.txt --force-reinstall
```

---

### Problema: Ambiente virtual não ativa

**Windows:**
```cmd
# Se PowerShell bloqueou execução de scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Tente novamente
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Verifique se criou corretamente
ls venv/bin/activate

# Ative com caminho completo
source $(pwd)/venv/bin/activate
```

---

## Instalação de Ferramentas Opcionais

### MuseScore (Editor de Partituras)

**Windows/macOS:**
1. Baixe: [musescore.org/download](https://musescore.org/download)
2. Execute o instalador
3. Siga o wizard

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install musescore3

# Fedora
sudo dnf install musescore

# Arch
sudo pacman -S musescore
```

### VLC Media Player (Playback MIDI)

**Windows/macOS:**
1. Baixe: [videolan.org/vlc](https://www.videolan.org/vlc/)
2. Instale normalmente

**Linux:**
```bash
sudo apt install vlc
```

### Lilypond (Gravura Musical)

**Windows:**
```
Baixe: https://lilypond.org/windows.html
```

**macOS:**
```bash
brew install lilypond
```

**Linux:**
```bash
sudo apt install lilypond
```

---

## Atualizando a Instalação

### Atualizar Código

```bash
git pull origin main
```

### Atualizar Dependências

```bash
pip install -r requirements-streamlit.txt --upgrade
```

### Atualizar Python (se necessário)

**Windows:**
Baixe nova versão de python.org

**macOS:**
```bash
brew upgrade python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt upgrade python3
```

---

## Desinstalação

### Remover Ambiente Virtual

```bash
# Desativar ambiente (se ativo)
deactivate

# Deletar diretório
# Windows:
rmdir /s venv

# macOS/Linux:
rm -rf venv
```

### Remover Projeto

```bash
# Apenas delete a pasta ca-music-composer
```

### Desinstalar Python (opcional)

**Windows:**
Painel de Controle → Programas → Desinstalar

**macOS:**
```bash
brew uninstall python@3.11
```

**Linux:**
```bash
sudo apt remove python3.10
```

---

## Suporte Adicional

### Documentação

- [README Principal](../README.md)
- [Tutorial Completo](TUTORIAL.md)
- [FAQ](FAQ.md)
- [Troubleshooting](TROUBLESHOOTING.md)

### Comunidade

- **Issues:** [GitHub Issues](https://github.com/seu-usuario/ca-music-composer/issues)
- **Discussions:** [GitHub Discussions](https://github.com/seu-usuario/ca-music-composer/discussions)
- **Email:** seu.email@example.com

---

## ✅ Checklist de Instalação

Antes de reportar problemas, verifique:

- [ ] Python 3.8+ instalado
- [ ] pip funcionando
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas sem erros
- [ ] `python test_install.py` passa todos os testes
- [ ] Aplicação executa sem erros

---

<div align="center">

**Instalação completa! Divirta-se compondo! 🎵**

[⬆ Voltar ao Índice](#-índice) | [📖 Ir para Tutorial](TUTORIAL.md)

</div>
