# GS-MISSION-CONTROL-AI-lc-AgroSat

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

---

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

---

# Parâmetros Monitorados

O sistema monitora cinco parâmetros principais.

| Parâmetro | Unidade | Impacto |
|------------|---------|----------|
| Saúde do Sensor NDVI | % | Qualidade dos mapas de vegetação |
| Temperatura do Payload | °C | Precisão espectral |
| Armazenamento | % | Quantidade de imagens preservadas |
| Janela de Downlink | min | Tempo de entrega dos dados |
| Estabilidade de Atitude | arcseg | Nitidez das imagens |

---

# Sistema de Alertas

O sistema utiliza regras implementadas em Python para classificar o estado da missão.