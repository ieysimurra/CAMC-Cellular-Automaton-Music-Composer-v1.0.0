# 📖 Tutorial Completo: Compositor com Autômatos Celulares

[🇧🇷 Português](docs/TUTORIAL.md) | [🇺🇸 English](docs/TUTORIAL_EN.md)

---

## Índice

1. [Introdução](#introdução)
2. [Conceitos Básicos](#conceitos-básicos)
3. [Tutorial Passo a Passo](#tutorial-passo-a-passo)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Dicas Avançadas](#dicas-avançadas)
6. [Solução de Problemas](#solução-de-problemas)

---

## Introdução

Este tutorial vai guiá-lo através de todos os recursos do Compositor com Autômatos Celulares, desde conceitos básicos até técnicas avançadas de composição.

### O Que Você Vai Aprender

- ✅ Como autômatos celulares geram música
- ✅ Configurar instrumentos e parâmetros
- ✅ Escolher e ajustar regras de CA
- ✅ Exportar partituras em diferentes formatos
- ✅ Técnicas de composição avançadas

### Pré-requisitos

- 🎵 Conhecimento básico de notação musical (opcional)
- 🧮 Curiosidade sobre matemática e música
- 💻 Aplicação instalada (versão web ou desktop)

---

## Conceitos Básicos

### O Que É Um Autômato Celular?

Um **autômato celular (CA)** é um sistema matemático onde:

1. **Grade de células**: Cada célula tem um estado (número)
2. **Regras simples**: O próximo estado depende do estado atual e dos vizinhos
3. **Evolução temporal**: A grade evolui geração após geração

```
Exemplo Visual:

Geração 0:  0 0 0 0 1 0 0 0 0  (célula central ativa)
Geração 1:  0 0 0 1 0 1 0 0 0
Geração 2:  0 0 1 0 2 0 1 0 0
Geração 3:  0 1 0 2 1 2 0 1 0
...
```

### Como Isso Vira Música?

```python
Estado CA → Nota Musical
0         → Pausa (silêncio)
1         → C4 (dó central)
2         → C#4 (dó sustenido)
3         → D4 (ré)
...
```

Cada **linha** do CA vira um **momento musical**, e cada **coluna** vira uma **sequência temporal**.

---

## Tutorial Passo a Passo

### Passo 1: Abrir a Aplicação

#### Versão Web (Streamlit)

```bash
streamlit run CA-poly-instrument-11-streamlit.py
```

Abra o navegador em `http://localhost:8501`

#### Versão Desktop

```bash
python CA-poly-instrument-13-complexRhy.py
```

Uma janela gráfica será aberta.

---

### Passo 2: Selecionar Instrumentos

#### Interface Web

1. Na seção **"🎼 Instrumentos"**, você verá três categorias:
   - 🌬️ **Sopros de Madeira**: Flauta, Oboé, Clarinete, Fagote
   - 🎺 **Sopros de Metal**: Trompa, Trompete, Trombone, Tuba
   - 🎻 **Cordas**: Violino, Viola, Violoncelo, Contrabaixo

2. Escolha quantas instâncias de cada instrumento (0-4)

**Exemplo:**
```
Violino: 2 instâncias
Violoncelo: 1 instância
Flauta: 1 instância
```

3. Clique em **"✅ Confirmar Seleção"**

#### Interface Desktop

1. Vá para a aba **"🎼 Instrumentos"**
2. Use os botões **+** e **-** para ajustar quantidades
3. Clique em **"✅ Confirmar Seleção de Instrumentos"**

---

### Passo 3: Configurar Cada Instrumento

Agora você verá uma interface para configurar **cada instrumento individual**.

#### 3.1 Parâmetros do Autômato Celular

##### **Gerações** (10-100)
- **O que faz**: Define quantas "linhas de tempo" o CA terá
- **Impacto musical**: Duração da música
- **Recomendação**: 
  - Melodias curtas: 20-30
  - Peças médias: 40-60
  - Composições longas: 80-100

##### **Tamanho da Grade** (10-100)
- **O que faz**: Largura espacial do CA
- **Impacto musical**: Diversidade harmônica/melódica horizontal
- **Recomendação**: 30-50 para balanço entre complexidade e controle

##### **Número de Estados** (2-12)
- **O que faz**: Quantas notas diferentes podem aparecer
- **Impacto musical**: Paleta harmônica
- **Recomendação**:
  - 6-8: Melodias simples
  - 10-12: Harmonias complexas

##### **Tamanho da Vizinhança** (1-4)
- **O que faz**: Quantas células vizinhas influenciam a próxima geração
- **Impacto musical**: Densidade de conexões
- **Recomendação**:
  - 1-2: Padrões localizados
  - 3-4: Padrões mais espalhados

##### **Célula Inicial** (0 até tamanho-1)
- **O que faz**: Onde começa a evolução
- **Impacto musical**: Simetria do resultado
- **Recomendação**: Meio da grade (tamanho/2) para simetria

---

#### 3.2 Configuração Musical

##### **Nota Inicial** (C, C#, D, ..., B)
- **O que faz**: Primeira nota da escala
- **Impacto musical**: Tonalidade
- **Exemplos**:
  - C: Dó maior/menor
  - D: Ré maior/menor
  - G: Sol maior/menor

##### **Oitavas** (1-7)
- **O que faz**: Em quais registros as notas aparecerão
- **Recomendação por instrumento**:
  ```
  Flauta:       [5, 6]     (agudo)
  Violino:      [4, 5]     (médio-agudo)
  Viola:        [3, 4]     (médio)
  Violoncelo:   [2, 3]     (grave)
  Contrabaixo:  [1, 2]     (muito grave)
  ```

##### **Modo de Oitava**
- **Ascendente**: Notas sobem pelas oitavas (C4, C#4, D4, ..., B4, C5, ...)
- **Descendente**: Notas descem pelas oitavas

##### **Duração Rítmica**
- **Colcheia (0.5)**: Notas rápidas
- **Semínima (1.0)**: Andamento padrão ✅ Recomendado
- **Mínima (2.0)**: Notas lentas
- **Semibreve (4.0)**: Notas muito longas

##### **Randomizar Ritmo?**
- **Desligado**: Todas as notas têm a mesma duração
- **Ligado**: Durações variam automaticamente (respeitando compassos)

##### **Fórmula de Compasso**
- **4/4**: Padrão, 4 tempos por compasso
- **3/4**: Valsa, 3 tempos
- **6/8**: Binário composto
- **5/4**: Assimétrico (experimental)

---

#### 3.3 Tipo de Regra

##### **1. Determinística** ⭐ Recomendada para iniciantes

```
Fórmula: próximo_estado = (estado_atual + soma_vizinhos) % num_estados
```

**Características:**
- ✅ Padrões geométricos regulares
- ✅ Resultados previsíveis
- ✅ Boa para melodias claras

**Quando usar:**
- Melodias principais
- Contrapontos ordenados
- Estruturas formais

**Exemplo de resultado:**
```
♪ Sequências repetitivas
♪ Padrões fractais
♪ Simetria visual
```

---

##### **2. Thresholds (Limiares)**

```
Se soma_vizinhos < threshold_1: próximo_estado = ...
Se soma_vizinhos < threshold_2: próximo_estado = ...
```

**Configuração:**
- Define 2 valores de threshold (ex: [3, 6])
- Estados mudam quando limiares são ultrapassados

**Características:**
- ✅ Transições dramáticas
- ✅ Dinâmicas interessantes
- ⚠️ Pode gerar pausas súbitas

**Quando usar:**
- Contrastes forte/fraco
- Efeitos de crescendo/decrescendo
- Momentos climáticos

---

##### **3. Aleatória**

```
Fórmula: próximo_estado = random(0, num_estados)
```

**Características:**
- ✅ Imprevisibilidade total
- ✅ Texturas complexas
- ⚠️ Pode soar caótico

**Quando usar:**
- Improvisação algorítmica
- Backgrounds texturais
- Exploração experimental

**Dica:** Use em instrumentos de acompanhamento, não na melodia principal.

---

##### **4. Matemática (Personalizada)** 🎓 Avançado

```
Permite definir sua própria fórmula matemática
```

**Exemplos de expressões:**

```python
# Multiplicação com módulo
(state * neighbor_sum) % num_states

# Potenciação
(state ** 2 + neighbor_sum) % num_states

# XOR bit a bit (muito interessante!)
(state ^ neighbor_sum) % num_states

# Fibonacci-like
(state + neighbor_sum * 2) % num_states
```

**Quando usar:**
- Implementar algoritmos conhecidos
- Testar teorias matemáticas
- Criar assinaturas sonoras únicas

---

##### **5. Time-Sensitive (Sensível ao Tempo)**

```
Fórmula: (estado + vizinhos + tempo_atual) % num_estados
```

**Características:**
- ✅ Evolução harmônica automática
- ✅ Modulações temporais
- ✅ Nunca repete exatamente

**Quando usar:**
- Peças que devem evoluir harmonicamente
- Música ambiente/generativa
- Simulações de processos naturais

---

### Passo 4: Gerar o Autômato Celular

1. Após configurar todos os parâmetros, clique em **"🎨 Gerar CA"**

2. Uma visualização será gerada mostrando o autômato:
   ```
   [Heatmap colorido]
   Eixo Y: Tempo (gerações)
   Eixo X: Espaço (posição)
   Cores: Estados (notas)
   ```

3. **Interprete a visualização:**
   - **Padrões regulares**: Melodias previsíveis
   - **Caos visual**: Música imprevisível
   - **Regiões vazias (cinza)**: Pausas musicais
   - **Muitas cores**: Grande diversidade de notas

4. Se não gostar do resultado:
   - Ajuste parâmetros
   - Mude o tipo de regra
   - Gere novamente

---

### Passo 5: Gerar a Partitura

Depois de gerar CAs para **todos** os instrumentos:

1. Vá para a seção **"📝 Partitura"**

2. Clique em **"🎵 Gerar Partitura Completa"**

3. A partitura será processada e você verá:
   - ✅ Confirmação de sucesso
   - 📊 Estatísticas (número de notas, duração)
   - 🎵 Informações sobre instrumentos

---

### Passo 6: Exportar

#### Formato MIDI (.mid)

**Para que serve:**
- 🎹 Playback em qualquer player MIDI
- 🎚️ Importar em DAWs (FL Studio, Ableton, Logic Pro)
- 🎧 Ouvir o resultado

**Como fazer:**
1. Aba **"MIDI"**
2. Clique em **"📥 Baixar MIDI"**
3. Abra com VLC, Windows Media Player, ou sua DAW favorita

---

#### Formato MusicXML (.musicxml)

**Para que serve:**
- 📝 Editar em Finale, Sibelius, MuseScore
- ✏️ Refinar notação
- 🎼 Imprimir partituras profissionais

**Como fazer:**
1. Aba **"MusicXML"**
2. Clique em **"📥 Baixar MusicXML"**
3. Abra no MuseScore (gratuito) ou Finale

**Workflow recomendado:**
```
CA Composer → MusicXML → MuseScore → Refinar → PDF/Imprimir
```

---

#### Formato Lilypond (.ly)

**Para que serve:**
- 🎨 Gravura musical de altíssima qualidade
- 📄 Partituras para publicação
- 🌐 Edição online no Hacklily

**Como fazer:**
1. Aba **"Lilypond"**
2. Baixe o código .ly
3. Ou use o **Hacklily** integrado

---

#### Hacklily (Editor Web)

**O que é:** Editor Lilypond online com playback MIDI

**Recursos:**
- ✏️ Edite o código em tempo real
- 🎵 Reproduza a música no navegador
- 📄 Exporte como PDF
- 🔗 Compartilhe via URL

**Como usar:**
1. Aba **"Hacklily"**
2. Escolha **"Visualizar Aqui"** ou **"Abrir em Nova Aba"**
3. Edite, reproduza e exporte diretamente

---

## Exemplos Práticos

### Exemplo 1: Melodia Solo (Flauta)

**Objetivo:** Criar uma melodia simples e agradável

**Configuração:**
```yaml
Instrumento: Flauta (1 instância)

Parâmetros CA:
  - Gerações: 30
  - Tamanho: 40
  - Estados: 8
  - Vizinhança: 1
  - Célula Inicial: 20 (centro)
  - Regra: Determinística

Configuração Musical:
  - Nota Inicial: C
  - Oitavas: [5, 6]
  - Duração: Semínima (1.0)
  - Randomizar Ritmo: Não
  - Compasso: 4/4
```

**Resultado Esperado:**
- 🎵 Melodia de ~30 segundos
- 📊 Padrões geométricos claros
- 🎶 Fácil de seguir

---

### Exemplo 2: Duo Contrastante

**Objetivo:** Dois instrumentos com personalidades diferentes

**Violino (Melodia Principal):**
```yaml
Parâmetros CA:
  - Gerações: 50
  - Estados: 12
  - Regra: Determinística
  
Musical:
  - Nota Inicial: G
  - Oitavas: [4, 5]
  - Duração: Randomizada
```

**Violoncelo (Acompanhamento):**
```yaml
Parâmetros CA:
  - Gerações: 50
  - Estados: 6
  - Regra: Thresholds [4, 7]
  
Musical:
  - Nota Inicial: C
  - Oitavas: [2, 3]
  - Duração: Semibreve (4.0)
```

**Resultado Esperado:**
- 🎻 Violino: Melodia ativa e variada
- 🎼 Cello: Pedal harmônico sustentado

---

### Exemplo 3: Mini Orquestra

**Objetivo:** Textura orquestral completa

**Instrumentação:**
```yaml
Flautas (2):
  - Harmonia em terças (configurações similares, notas diferentes)
  
Clarinetes (2):
  - Contraponto (regras complementares)
  
Trompas (2):
  - Pedal harmônico (durações longas)
  
Cordas (Violino, Viola, Cello, Baixo):
  - Cada um com função distinta
```

**Dicas:**
1. **Sincronize gerações**: Todos com mesmo número
2. **Varie estados**: Melodia (12), Harmonia (8), Pedal (4)
3. **Ajuste oitavas**: Mantenha separação clara de registros

---

## Dicas Avançadas

### 🎯 Dica 1: Criar Cânone

**Técnica:** Use mesma configuração em instrumentos diferentes, mas ajuste **Célula Inicial**

```yaml
Violino 1:
  Célula Inicial: 20
  
Violino 2:
  Célula Inicial: 25 (+5 de defasagem)
```

**Resultado:** Melodias imitativas (cânone)

---

### 🎯 Dica 2: Controlar Densidade

**Problema:** Música muito densa/cheia

**Solução:** Ajuste **Número de Estados**

```yaml
Música densa (muitas notas):
  Estados: 12
  
Música esparsa (mais pausas):
  Estados: 4-6 (estados baixos = mais pausas)
```

---

### 🎯 Dica 3: Modulação Automática

**Use:** Regra Time-Sensitive

```yaml
Instrumento: Trompa
Regra: Time-Sensitive
Time Step: 1

Resultado: A harmonia "modula" gradualmente ao longo do tempo
```

---

### 🎯 Dica 4: Combinar Regras Complementares

**Princípio:** Use regras que se complementam

```yaml
Melodia (Violino):
  Regra: Determinística (previsível)
  
Harmonia (Viola):
  Regra: Thresholds (contrastante)
  
Textura (Flauta):
  Regra: Aleatória (fundo complexo)
```

---

## Solução de Problemas

### ❌ Problema: "Música soa aleatória demais"

**Soluções:**
1. Use regra **Determinística** em vez de Aleatória
2. Reduza **Número de Estados** para 6-8
3. Diminua **Tamanho da Vizinhança** para 1
4. Desative **Randomizar Ritmo**

---

### ❌ Problema: "Muitas pausas"

**Causa:** Muitos estados = mais chance de estado 0 (pausa)

**Soluções:**
1. Reduza **Número de Estados** para 6-8
2. Aumente **Célula Inicial** (mais atividade inicial)
3. Use regra que evita convergir para 0

---

### ❌ Problema: "Notas fora do range do instrumento"

**Causa:** Oitavas mal configuradas

**Soluções:**
1. Consulte tabela de ranges recomendados:
   ```
   Flauta: [5, 6]
   Violino: [4, 5]
   Viola: [3, 4]
   Cello: [2, 3]
   Baixo: [1, 2]
   ```

---

### ❌ Problema: "MusicXML não abre no MuseScore"

**Soluções:**
1. Verifique se MuseScore está atualizado
2. Tente **"Importar"** em vez de **"Abrir"**
3. Use formato MIDI como alternativa

---

### ❌ Problema: "MIDI não tem som"

**Causa:** Player MIDI não configurado

**Soluções:**
1. Use **VLC Media Player** (suporta MIDI)
2. Importe em uma DAW (FL Studio, Ableton)
3. Use player online: [Online Sequencer](https://onlinesequencer.net)

---

## Recursos Adicionais

### 📚 Leitura Recomendada

- [Wolfram MathWorld - Cellular Automata](https://mathworld.wolfram.com/CellularAutomaton.html)
- [Music21 Documentation](https://web.mit.edu/music21/doc/)
- [Lilypond Tutorial](https://lilypond.org/doc/v2.24/Documentation/learning/)

### 🎥 Vídeos

- [The Nature of Code - Cellular Automata](https://www.youtube.com/watch?v=DKGodqDs9sA)
- [Music from Cellular Automata](https://www.youtube.com/results?search_query=cellular+automata+music)

### 🔗 Ferramentas Relacionadas

- [MuseScore](https://musescore.org) - Editor de partituras gratuito
- [Hacklily](https://hacklily.org) - Editor Lilypond online
- [Golly](http://golly.sourceforge.net/) - Simulador de CAs

---

## Conclusão

Parabéns por completar o tutorial! 🎉

Agora você sabe:
- ✅ Como configurar instrumentos
- ✅ Ajustar parâmetros de CAs
- ✅ Escolher regras apropriadas
- ✅ Exportar em múltiplos formatos
- ✅ Solucionar problemas comuns

### Próximos Passos

1. **Experimente:** Crie suas primeiras composições
2. **Compartilhe:** Mostre seus resultados
3. **Contribua:** Sugira melhorias no GitHub
4. **Inspire:** Use em projetos musicais reais

---

**Divirta-se compondo com matemática e música! 🎵🧮**

[⬆ Voltar ao topo](#-tutorial-completo-compositor-com-autômatos-celulares)
