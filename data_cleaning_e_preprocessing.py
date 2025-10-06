# ===========================================
# Projeto: Data Cleaning e Preprocessing
# ===========================================

# Importação das bibliotecas
import pandas as pd
import numpy as np

# ===========================================
# 1 - Leitura dos dados
# ===========================================

df = pd.read_csv('dados_brutos.csv')
df.head()

# ===========================================
# 2️ - Informações gerais
# ===========================================

df.info()
df.describe()
df.isnull().sum()

# ===========================================
# 3️ - Tratamento de valores ausentes
# ===========================================

# Exemplo: preencher idade média
df['Idade'] = df['Idade'].fillna(df['Idade'].mean())

# Exemplo: remover registros com renda nula
df = df.dropna(subset=['Renda Individual Mensal'])

# ===========================================
# 4️ - Padronização de tipos
# ===========================================

df['Idade'] = df['Idade'].astype(int)
df['Cor'] = df['Cor'].str.title()  # deixa com inicial maiúscula

# ===========================================
# 5️ - Remoção de outliers
# ===========================================

# Exemplo: remover idades fora do intervalo esperado
df = df[(df['Idade'] > 10) & (df['Idade'] < 100)]

# Exemplo: remover rendas absurdamente altas (acima do percentil 99)
limite_renda = df['Renda Individual Mensal'].quantile(0.99)
df = df[df['Renda Individual Mensal'] < limite_renda]

# ===========================================
# 6️ - Criação de variáveis derivadas
# ===========================================

# Exemplo: faixa de renda
df['Faixa de Renda'] = pd.cut(
    df['Renda Individual Mensal'],
    bins=[0, 1500, 3000, 6000, 12000, np.inf],
    labels=['Até 1.5K', '1.5K-3K', '3K-6K', '6K-12K', '12K+']
)

# ===========================================
# 7️ - Exportação dos dados tratados
# ===========================================

df.to_csv('dados_tratados.csv', index=False)
print("Dados tratados exportados com sucesso!")
df.head()

# Quantas linhas havia antes e depois
print("Antes:", pd.read_csv('dados_brutos.csv').shape)
print("Depois:", pd.read_csv('dados_tratados.csv').shape)

# Comparar linhas removidas
bruto = pd.read_csv('dados_brutos.csv')
tratado = pd.read_csv('dados_tratados.csv')

# Mostrar as linhas que existiam no bruto e foram removidas
linhas_removidas = bruto[~bruto['Renda Individual Mensal'].isin(tratado['Renda Individual Mensal'])]
linhas_removidas.head()

set(tratado.columns) - set(bruto.columns)

"""## 📊 Interpretação dos Resultados

#####  **Distribuição de Renda:** o gráfico mostra que os dados brutos tinham valores muito altos (outliers) distorcendo a curva.
# Após a limpeza, a distribuição ficou mais concentrada nas faixas comuns (até R$12.000).

"""

import matplotlib.pyplot as plt
import seaborn as sns

bruto = pd.read_csv('dados_brutos.csv')
tratado = pd.read_csv('dados_tratados.csv')

plt.style.use('seaborn-v0_8')
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(bruto['Renda Individual Mensal'], bins=30, kde=True)
plt.title('Distribuição de Renda — Dados Brutos')
plt.xlabel('Renda Individual Mensal (R$)')
plt.ylabel('Frequência')

plt.subplot(1, 2, 2)
sns.histplot(tratado['Renda Individual Mensal'], bins=30, kde=True, color='green')
plt.title('Distribuição de Renda — Dados Tratados')
plt.xlabel('Renda Individual Mensal (R$)')
plt.ylabel('Frequência')

plt.tight_layout()
plt.show()

"""##### **Tratamento de Nulos:** a redução de registros e ausência de valores ausentes confirmam que a limpeza foi bem-sucedida."""

print("Comparação de Tamanho")
print("Antes da limpeza:", bruto.shape)
print("Depois da limpeza:", tratado.shape)

print("\n Valores nulos antes:")
print(bruto.isnull().sum())

print("\n Valores nulos depois:")
print(tratado.isnull().sum())

"""##### **Remoção de Outliers:** o corte no percentil 99 eliminou os rendimentos extremos que poderiam enviesar médias."""

# Contagem por faixa de renda após o tratamento
plt.figure(figsize=(8,5))
sns.countplot(x='Faixa de Renda', data=tratado, palette='viridis')
plt.title('Distribuição por Faixa de Renda (Após Limpeza)')
plt.xlabel('Faixa de Renda')
plt.ylabel('Número de Registros')
plt.show()

