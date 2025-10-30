# ❓ FAQ - Perguntas Frequentes

[🇧🇷 Português](docs/FAQ.md) | [🇺🇸 English](docs/FAQ_EN.md)

---

## Índice

- [Questões Gerais](#questões-gerais)
- [Instalação](#instalação)
- [Uso do Sistema](#uso-do-sistema)
- [Autômatos Celulares](#autômatos-celulares)
- [Exportação](#exportação)
- [Solução de Problemas](#solução-de-problemas)

---

## Questões Gerais

### O que é este projeto?

Um sistema que transforma **autômatos celulares** (padrões matemáticos) em **composições musicais** profissionais. É uma ferramenta para composição algorítmica, educação musical e pesquisa.

### Preciso saber programar para usar?

**Não!** Ambas as versões (web e desktop) têm interfaces gráficas intuitivas. Conhecimento de programação é opcional para uso avançado.

### Preciso saber teoria musical?

**Não é obrigatório**, mas ajuda! O sistema funciona mesmo sem conhecimento musical, mas entender conceitos como:
- Notas e oitavas
- Fórmulas de compasso
- Duração rítmica

...permitirá explorar melhor as possibilidades.

### Este projeto é gratuito?

**Sim!** É 100% gratuito e open-source sob licença MIT. Você pode usar, modificar e distribuir livremente.

### Posso usar em projetos comerciais?

**Sim!** A licença MIT permite uso comercial sem restrições.

---

## Instalação

### Quais são os requisitos do sistema?

**Mínimos:**
- Python 3.8+
- 4GB RAM
- 500MB espaço em disco

**Recomendados:**
- Python 3.10+
- 8GB RAM
- Processador multi-core

### Funciona no Windows/Mac/Linux?

**Sim!** O projeto é multiplataforma:
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu, Fedora, etc.)

### Como instalo o Python?

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe a versão mais recente
3. Durante a instalação, marque **"Add Python to PATH"**
4. Verifique: `python --version`

### Qual versão devo usar: Web ou Desktop?

| Característica | Web (Streamlit) | Desktop (Tkinter) |
|----------------|-----------------|-------------------|
| Instalação | Mais simples | Requer mais dependências |
| Interface | Navegador | Aplicação nativa |
| Performance | Depende do navegador | Geralmente mais rápida |
| Compartilhamento | Fácil (deploy online) | Apenas local |
| **Recomendação** | Iniciantes | Usuários avançados |

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:**

```bash
# Certifique-se de que instalou as dependências corretas
pip install -r requirements-streamlit.txt

# Ou instale manualmente
pip install streamlit music21 numpy matplotlib
```

---

## Uso do Sistema

### Como começo a usar?

1. **Abra a aplicação** (web ou desktop)
2. **Selecione instrumentos** (pelo menos 1)
3. **Configure parâmetros** para cada instrumento
4. **Gere os CAs** clicando em "Gerar CA"
5. **Crie a partitura** clicando em "Gerar Partitura"
6. **Exporte** no formato desejado

### Quantos instrumentos posso usar?

- **Máximo**: 48 instrumentos simultâneos (12 tipos × 4 instâncias cada)
- **Recomendado para iniciantes**: 2-4 instrumentos
- **Performance ideal**: 6-12 instrumentos

### O que significa cada parâmetro?

| Parâmetro | Significado | Impacto Musical |
|-----------|-------------|-----------------|
| **Gerações** | Duração temporal | Comprimento da música |
| **Tamanho** | Largura espacial | Diversidade horizontal |
| **Estados** | Número de notas | Paleta harmônica |
| **Vizinhança** | Raio de influência | Conexões/densidade |
| **Célula Inicial** | Ponto de partida | Simetria do resultado |

### Quanto tempo leva para gerar uma composição?

**Tempos típicos:**
- Configuração: 2-5 minutos
- Geração dos CAs: 1-10 segundos por instrumento
- Criação da partitura: 5-15 segundos
- **Total**: ~5-10 minutos para uma peça completa

### Posso salvar minhas configurações?

**Atualmente:** As configurações são mantidas durante a sessão.

**Planejado:** Sistema de presets e salvamento de projetos na próxima versão.

**Workaround:** Exporte e salve os parâmetros manualmente em um arquivo de texto.

---

## Autômatos Celulares

### O que é exatamente um autômato celular?

Um sistema matemático onde:
1. Uma **grade de células** possui estados (números)
2. Cada célula evolui baseada em **regras simples**
3. O próximo estado depende do **estado atual + vizinhos**

**Exemplo visual:**
```
t=0:  ░░░░█░░░░  (1 célula ativa)
t=1:  ░░░█░█░░░
t=2:  ░░█░░░█░░
t=3:  ░█░░░░░█░
```

### Qual regra devo escolher?

| Tipo | Quando Usar | Resultado |
|------|-------------|-----------|
| **Determinística** | Melodias claras | Padrões regulares |
| **Thresholds** | Dinâmica/contraste | Transições súbitas |
| **Aleatória** | Experimentação | Imprevisível |
| **Matemática** | Algoritmos específicos | Customizado |
| **Time-Sensitive** | Evolução temporal | Modulação automática |

### Por que meu CA parece muito "regular"?

**Causa:** Regra Determinística com poucos estados

**Soluções:**
1. Aumente o número de estados (10-12)
2. Tente regra Matemática: `(state ^ neighbor_sum) % num_states`
3. Use vizinhança maior (3-4)

### Por que meu CA converge para zero (tudo cinza)?

**Causa:** Regra que tende a estabilizar em estado 0

**Soluções:**
1. Use regra Time-Sensitive
2. Aumente a célula inicial
3. Teste regra Matemática: `(state + neighbor_sum + 1) % num_states`

### Como faço para repetir um resultado?

**Importante:** Os CAs são determinísticos!

Para repetir:
1. Use **mesmos parâmetros**
2. Mesma **regra**
3. Mesma **célula inicial**

**Exceção:** Regra Aleatória sempre gera resultados diferentes.

### Posso visualizar o CA antes de gerar música?

**Sim!** Clique em "Gerar CA" e visualize o heatmap **antes** de criar a partitura.

---

## Exportação

### Quais formatos são suportados?

| Formato | Extensão | Para Que Serve |
|---------|----------|----------------|
| **MIDI** | .mid | Playback, importar em DAWs |
| **MusicXML** | .musicxml | Editar em softwares de notação |
| **Lilypond** | .ly | Gravura profissional |
| **PNG** | .png | Imagens dos CAs |

### Como abro um arquivo MIDI?

**Opções:**
1. **VLC Media Player** (recomendado, gratuito)
2. **Windows Media Player** (Windows)
3. **QuickTime** (macOS)
4. **DAWs**: FL Studio, Ableton, Logic Pro, GarageBand

### Como edito a partitura gerada?

**Fluxo recomendado:**

```
CA Composer → Exportar MusicXML → Abrir no MuseScore → Editar → PDF
```

**MuseScore** é gratuito e poderoso: [musescore.org](https://musescore.org)

### O arquivo MusicXML não abre!

**Soluções:**
1. Atualize o software de notação
2. Tente **"Importar"** em vez de "Abrir"
3. Verifique o tamanho do arquivo (não deve estar vazio)
4. Use MIDI como alternativa

### Como imprimo a partitura?

**Método 1: Via Lilypond/Hacklily**
1. Gere código Lilypond
2. Abra no Hacklily
3. Exporte como PDF
4. Imprima o PDF

**Método 2: Via MusicXML**
1. Exporte MusicXML
2. Abra no MuseScore
3. Arquivo → Exportar → PDF
4. Imprima o PDF

### Posso compartilhar minhas composições online?

**Sim!** Várias formas:

1. **Hacklily:**
   - Copie a URL gerada
   - Compartilhe o link (exemplo: `hacklily.org/#code=...`)

2. **YouTube:**
   - Grave tela + áudio MIDI
   - Faça upload

3. **SoundCloud/Bandcamp:**
   - Exporte MIDI → converta para MP3
   - Faça upload

4. **MuseScore.com:**
   - Importe MusicXML
   - Publique na plataforma

---

## Solução de Problemas

### A aplicação não inicia

**Desktop:**
```bash
# Verifique se instalou as dependências
pip list | grep customtkinter
pip list | grep music21

# Se faltarem, instale
pip install -r requirements-desktop.txt
```

**Web:**
```bash
# Verifique se Streamlit está instalado
streamlit --version

# Se não, instale
pip install streamlit
```

### Erro: "Command 'python' not found"

**Solução:**

**Windows:**
```bash
# Tente com 'py'
py --version
py -m streamlit run arquivo.py
```

**macOS/Linux:**
```bash
# Tente com 'python3'
python3 --version
python3 -m streamlit run arquivo.py
```

### A interface está muito lenta

**Causas comuns:**
1. Muitos instrumentos (>12)
2. Gerações muito altas (>100)
3. Grade muito grande (>100)

**Soluções:**
1. Reduza número de instrumentos
2. Use gerações 30-60
3. Tamanho da grade 30-50

### "PermissionError" ao exportar arquivos

**Causa:** Windows bloqueando arquivo temporário

**Solução:**
1. Execute como administrador
2. Feche outros programas que podem estar usando arquivos
3. Reinicie o computador

### MIDI não reproduz som

**Causa:** Falta de sintetizador MIDI no sistema

**Soluções:**

**Windows:**
1. Use VLC Media Player
2. Ou instale [Microsoft GS Wavetable Synth]

**macOS:**
1. Use QuickTime
2. Ou GarageBand

**Linux:**
```bash
sudo apt-get install fluidsynth
```

### Erro: "Music21 environment not configured"

**Solução:**

```python
# Execute uma vez
from music21 import configure
configure.run()
```

### Como reporto um bug?

1. Vá para [GitHub Issues](https://github.com/seu-usuario/ca-music-composer/issues)
2. Clique em "New Issue"
3. Escolha template "Bug Report"
4. Preencha com:
   - Descrição do problema
   - Passos para reproduzir
   - Sistema operacional
   - Versão do Python
   - Screenshots (se aplicável)

---

## Perguntas Técnicas

### O código é open source?

**Sim!** Totalmente open source sob licença MIT.

**GitHub:** [github.com/seu-usuario/ca-music-composer](https://github.com/seu-usuario/ca-music-composer)

### Posso modificar o código?

**Sim!** Você é livre para:
- ✅ Modificar o código
- ✅ Adicionar features
- ✅ Criar versões derivadas
- ✅ Usar comercialmente

**Pedimos apenas:** Mantenha a licença MIT e dê crédito ao projeto original.

### Posso contribuir com o projeto?

**Sim, por favor!** Veja [CONTRIBUTING.md](CONTRIBUTING.md)

**Áreas de contribuição:**
- 🐛 Correção de bugs
- ✨ Novas features
- 📝 Documentação
- 🌍 Traduções
- 🎵 Exemplos musicais

### Onde está a documentação técnica?

- [📖 Tutorial Completo](docs/TUTORIAL.md)
- [🏗️ Arquitetura](docs/ARCHITECTURE.md)
- [🔧 API Reference](docs/API.md)

### Qual framework foi usado?

**Interface:**
- Web: Streamlit
- Desktop: CustomTkinter

**Processamento:**
- Music21 (notação musical)
- NumPy (computação científica)
- Matplotlib (visualizações)

---

## Ainda Tem Dúvidas?

### 💬 Entre em Contato

- **GitHub Discussions:** [Discussões](https://github.com/seu-usuario/ca-music-composer/discussions)
- **Email:** seu.email@example.com
- **Issues:** [Reportar Bug](https://github.com/seu-usuario/ca-music-composer/issues)

### 📚 Recursos Adicionais

- [Tutorial Completo](docs/TUTORIAL.md)
- [Exemplos](examples/)
- [Vídeos no YouTube](https://youtube.com/...)

---

<div align="center">

**Não encontrou sua resposta?**

[📧 Envie sua pergunta](https://github.com/seu-usuario/ca-music-composer/discussions/new)

[⬆ Voltar ao topo](#-faq---perguntas-frequentes)

</div>
