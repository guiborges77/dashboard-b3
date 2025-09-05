# Dashboard Interativo de Liquidez e Risco – B3

## Descrição do Projeto

Este projeto é um **dashboard interativo** que permite a análise rápida de **liquidez e risco** de ativos negociados na **B3 (Bolsa de Valores Brasileira)**. O objetivo é fornecer métricas resumidas, tabelas detalhadas e gráficos interativos para apoiar analistas, traders e gestores na tomada de decisões financeiras.

O dashboard exibe:
- **Volume total e quantidade negociada** de ativos.
- **Preço mínimo, máximo e médio**.
- **Tabelas detalhadas por ativo**.
- **Gráficos interativos** para visualização rápida de dados relevantes.
- Filtros para selecionar ativos específicos e analisar apenas os mais relevantes.

---

## Fonte dos Dados

Os dados utilizados neste projeto vêm de **arquivos CSV consolidados da B3**, contendo informações como:

- Código do ativo (`TckrSymb`)
- Volume financeiro (`NtlFinVol`)
- Quantidade negociada (`AdjstdQt`)
- Preço mínimo (`MinPric`)
- Preço máximo (`MaxPric`)
- Preço médio (`TradAvrgPric`)
- Data da negociação (`Date`)

> Esses arquivos podem ser obtidos a partir de **relatórios públicos da B3** ou bases históricas disponibilizadas para análise financeira.

---

## Funcionalidades

1. **Carregamento e leitura dos dados**
   - CSV lido usando `pandas.read_csv` com separador `;`.
   - Conversão de colunas numéricas com tratamento de valores ausentes (`NaN`).
   - Formatação monetária para BRL (`R$ 1.000,00`) usando `locale`.

2. **Pré-processamento**
   - Seleção das colunas relevantes.
   - Filtragem do **Top 10 ativos** por Volume Total para melhor performance.
   - Renomeação de colunas técnicas (`TckrSymb → Ativo`) e formatação de valores.

3. **Interface interativa**
   - Filtros de ativos via **sidebar**.
   - Métricas resumidas (Quantidade Total, Volume Total, Preço Mínimo/Máximo/Médio).
   - Tabela detalhada por ativo.
   - Gráficos de barra mostrando **Volume Total** e **Preço Médio**.

4. **Otimização**
   - Uso de `@st.cache_data` para evitar recarregamento constante do CSV.
   - Carregamento apenas do **Top 10 ativos** para aumentar a performance.

---

## Tecnologias Utilizadas

- **Python 3**
- **Pandas** → processamento e limpeza de dados
- **Streamlit** → dashboard interativo
- **Matplotlib e Seaborn** → gráficos de barra
- **Locale** → formatação monetária em BRL

---

## Como foi desenvolvida a solução

O projeto começou com a necessidade de criar um **painel interativo de liquidez e risco** da B3. Durante o desenvolvimento, foram tomadas decisões importantes:

- Corrigir colunas com cabeçalhos técnicos ou vazios.
- Formatar valores monetários no padrão brasileiro.
- Garantir que a primeira coluna de identificadores fosse visível e compreensível.
- Otimizar o carregamento usando cache e filtragem do Top 10 ativos.
- Exibir informações de forma clara, combinando **tabela**, **gráficos** e **métricas resumidas**.

O resultado final é uma ferramenta **visual, rápida e funcional** para análise de ativos financeiros.

---

## Observações Finais

Este dashboard é ideal para:

- Analistas financeiros que precisam monitorar liquidez e risco de ativos.
- Traders que desejam identificar rapidamente os ativos mais líquidos.
- Gestores que precisam de relatórios resumidos e gráficos para tomada de decisão.

