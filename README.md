# GS-MISSION-CONTROL-AI-lc-AgroSat
# INTRODUCAO

Tecnologia espacial conectada a problemas reais da sociedade agronegócio, sustentabilidade,
comunicação e mobilidade impulsionados por dados orbitais e IA generativa.


# Integrantes:

- Caio Henrique Ferraz da Silva RM: 568992 Turma: 1CCPG
- Leonardo Figueredo do Santos RM:573653 Turma: 1CCPG


# Vídeo de Demonstração
Link do youtube da demonstracao do projeto

# Projeto

O Mission Control AI — AgroSat é uma solução desenvolvida em Python que simula a operação de um satélite de observação da Terra.

O sistema monitora a saúde dos sistemas da missão, detecta alguer anomalia automaticamente e utiliza Inteligência Artificial Generativa para interpretar os impactos dessas falhas.

A solução foi criada para demonstrar a aplicação prática de IA em sistemas espaciais, conectando eventos orbitais a impactos reais para produtores rurais e seguradoras agrícolas.

# Objetivos

O projeto tem como objetivo:

- Simular a operação de um satélite agrícola em órbita baixa.
- Monitorar parâmetros críticos de telemetria.
- Detectar falhas automaticamente por meio de regras de negócio.
- Gerar alertas operacionais.
- Utilizar IA para explicar impactos técnicos e econômicos.
- Demonstrar aplicações de sensoriamento remoto no agronegócio.


# Missão Simulada

## Satélite

**AgroSat-1**

Características:

- Órbita LEO (Órbita Terrestre Baixa)
- Altitude: 614 km
- Inclinação: 97.8°
- Órbita heliossíncrona (SSO)

## Objetivo da Missão

Capturar imagens multiespectrais para geração de índices NDVI (Normalized Difference Vegetation Index), permitindo:

- Monitoramento de lavouras
- Agricultura de precisão
- Planejamento de safras
- Seguros agrícolas baseados em índices
- Apoio à tomada de decisão no campo

# Aplicação no Agronegócio

O AgroSat 1 realiza o monitoramento de regiões agrícolas brasileiras, gerando dados que podem auxiliar:

- Produtores rurais
- Cooperativas agrícolas
- Empresas de tecnologia agrícola
- Seguradoras rurais
- Instituições de pesquisa

As imagens produzidas permitem avaliar:

- Saúde da vegetação
- Estresse hídrico
- Produtividade agrícola
- Evolução das lavouras

# Parâmetros Monitorados

O sistema monitora cinco parâmetros principais.

| Parâmetro | Unidade | Impacto |
|------------|---------|----------|
| Saúde do Sensor NDVI | % | Qualidade dos mapas de vegetação |
| Temperatura do Payload | °C | Precisão espectral |
| Armazenamento | % | Quantidade de imagens preservadas |
| Janela de Downlink | min | Tempo de entrega dos dados |
| Estabilidade de Atitude | arcseg | Nitidez das imagens |


# Sistema de Alertas

O sistema utiliza regras implementadas em Python para classificar o estado da missão.

## NORMAL

Todos os sistemas operando dentro dos limites esperados.

## ATENÇÃO

Indícios iniciais de degradação operacional.

Exemplos:

- Temperatura acima da faixa ideal
- Instabilidade de atitude moderada
- Armazenamento próximo do limite

## CRÍTICO

Anomalia significativa com risco operacional.

Exemplos:

- Armazenamento acima de 85%
- Downlink iminente
- Sensor degradado

##  EMERGÊNCIA

Risco imediato para a missão.

Exemplos:

- Falha crítica do sensor NDVI
- Sobreaquecimento do payload
- Perda de controle de atitude
- Múltiplas falhas simultâneas


#  Inteligência Artificial

A IA não toma decisões operacionais.

Todas as decisões são realizadas pela lógica implementada em Python.

A Inteligência Artificial é responsável por:

- Interpretar a telemetria
- Explicar os impactos das falhas
- Adaptar a linguagem ao perfil do usuário
- Gerar relatórios contextualizados


#  Personas Atendidas

## Engenheiro de Operações

Recebe informações técnicas sobre:

- Telemetria
- Saúde dos sistemas
- Procedimentos de mitigação
- Operação orbital

## Produtor Rural

Recebe informações sobre:

- Disponibilidade dos dados NDVI
- Impactos para a lavoura
- Tempo de entrega das imagens

## Analista de Seguro Agrícola

Recebe informações sobre:

- Validade dos dados
- Confiabilidade dos índices
- Utilização em processos de sinistro


# Arquitetura do Sistema

```text
mission-control-ai/
│
├── main.py
├── banner_ascii.py
├── requirements.txt
├── .env.example
│
├── src/
│   ├── engine.py
│   ├── telemetria.py
│   ├── alertas.py
│   └── ui.py
│
├── prompts/
│   └── system_prompt.md
│
├── data/
│
└── README.md
```


# Componentes Principais

## telemetria.py

Responsável por:

- Simular sensores
- Gerar dados orbitais
- Criar cenários de operação
- Inserir anomalias para testes


## alertas.py

É responsável por:

- Avaliar limites operacionais
- Gerar alertas
- Classificar severidade
- Executar ações automatizadas


## engine.py

Responsável por:

- Integrar IA e telemetria
- Construir prompts
- Gerenciar histórico da missão
- Produzir respostas inteligentes


## ui.py

Responsável pela interface do usuário.

Tecnologias utilizadas:

- Rich
- Prompt Toolkit
- PyFiglet

Funcionalidades:

- Painéis coloridos
- Histórico de comandos
- Banner ASCII
- Alertas visuais

# Comandos Disponíveis

| Comando | Função |
|----------|---------|
| /help | Exibe ajuda |
| /status | Mostra telemetria atual |
| /about | Informações do projeto |
| /clear | Limpa o terminal |
| /exit | Encerra o sistema |
| /resetar | Reinicia a telemetria |
| /anomalia ndvi | Falha do sensor NDVI |
| /anomalia temp | Sobreaquecimento |
| /anomalia storage | Armazenamento crítico |
| /anomalia downlink | Downlink iminente |
| /anomalia atitude | Instabilidade de atitude |
| /anomalia todos | Emergência total |
| /crise | Atalho para emergência total |

# Cenários de Demonstração: O sistema possui cenários prontos para demonstração.

### Operação Normal: Todos os sistemas funcionando corretamente.

### Armazenamento Crítico: Buffer próximo do limite máximo.

### Emergência Térmica: Payload acima de 65°C.

### Falha do Sensor NDVI: Dados multiespectrais inválidos.

### Instabilidade de Atitude: Imagens com perda de qualidade.

### Emergência Total: Todos os sistemas em estado crítico simultaneamente.

## Linguagem:

- Python 3.10+

## Bibliotecas:
- Ollama
- Rich
- Prompt Toolkit
- PyFiglet
- Python Dotenv
# Como Executar:

## 1. Clonar o repositório

```bash
git clone link do repositório
```

## 2. Entrar no projeto

```bash
cd nome do aquivo
```

## 3. Criar ambiente virtual

```bash
python -m venv .venv ou py -m venv .venv
```

## 4. Ativar ambiente

### Windows

```bash
.venv\Scripts\activate
```

### Linux/Mac

```bash
source .venv/bin/activate
```

## 5. Instalar dependências

```bash
pip install -r requirements.txt
```

## 6. Configurar a API Key

Criar o arquivo:

```env
.env
```

Adicionar:

```env
OLLAMA_API_KEY=sua_chave
```

## 7. Executar

```bash
python main.py ou py main.py
```
# Proposta de valor / modelo de negócio

Qual o problema real terrestre que esta missão resolve?

O Brasil perde em média 10 mil km² de floresta por ano, e a janela de resposta rápida a incêndios é de poucas horas. Quando o satélite de monitoramento falha ou opera com sensor degradado, órgãos como INPE e IBAMA ficam cegos para eventos que acontecem em tempo real. Cada hora de sensor térmico offline é uma janela onde focos ativos podem se transformar em incêndios de grande escala sem que nenhuma brigada seja acionada. O EnviroSat resolve isso garantindo continuidade operacional e comunicando proativamente qualquer degradação de capacidade — antes que ela vire problema irrecuperável.

Quem paga pela solução?

Modelo híbrido: o setor público (AEB, INPE, MMA, estados com programas de prevenção a incêndios) paga pela infraestrutura de monitoramento contínuo como serviço de utilidade pública. O setor privado (seguradoras agrícolas, empresas de carbono, grandes produtores com passivo ambiental) paga por acesso aos dados processados e aos relatórios de compliance gerados pela IA — especialmente o rastreio de áreas de preservação permanente.

Métrica de impacto

Se o EnviroSat operar com 100% de saúde por 1 ano: aproximadamente 800 mil km² de território nacional monitorados continuamente, detecção de até 12 mil focos ativos com latência inferior a 6 horas, redução estimada de 15–20% no tempo médio de mobilização de brigadas estaduais em áreas cobertas, e suporte a verificação de aproximadamente 2 mil laudos de compliance ambiental por ano para o mercado de crédito de carbono.

Modelo de negócio

Dado-como-serviço (DaaS) + SaaS de análise: o INPE/AEB financia a operação do satélite via concessão pública. O sistema de IA roda como plataforma SaaS acessível por API, com cobrança por volume de análises para clientes privados (seguradoras, empresas de carbono, cooperativas rurais). O modelo de alertas em tempo real para brigadas opera como serviço público gratuito integrado ao DETER.

# Conceitos Aplicados

- Inteligência Artificial Generativa
- Engenharia de Prompt
- Sensoriamento Remoto
- Sistemas Embarcados
- Monitoramento Espacial
- Agricultura de Precisão
- Análise de Risco
- Desenvolvimento em Python

# Conclusão:
O desenvolvimento do Mission Control AI AgroSat permitiu aplicar conceitos de Inteligência Artificial Generativa, Engenharia de Prompt, programação em Python e monitoramento de sistemas espaciais em um contexto realista voltado ao agronegócio brasileiro.

A solução demonstra como dados de telemetria de um satélite podem ser transformados em informações úteis para diferentes perfis de usuários, conectando eventos orbitais a impactos concretos para produtores rurais, engenheiros de operações e analistas de seguro agrícola.

Além de simular a operação de uma missão espacial, o projeto evidencia o potencial da IA como ferramenta de apoio à tomada de decisão, tornando informações técnicas mais acessíveis e facilitando a interpretação de situações críticas em tempo real.

Por meio da integração entre lógica de negócios, análise automatizada de alertas e modelos de linguagem, o AgroSat apresenta uma abordagem inovadora para o monitoramento de ativos espaciais e para o uso estratégico de dados no setor agrícola, reforçando a importância da tecnologia como instrumento para aumentar a eficiência, a sustentabilidade e a segurança das operações no campo.
