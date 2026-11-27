import pandas as pd

df = pd.read_csv('salarios.csv')

print(df)

#traz os primeiros itens
print('------HEAD-----')
print(df.head())
#informações do dataframe
print('------DATAFRAME-----')
print(df.info())
#estatisticas
print('------ESTATISTICAS-----')
print(df.describe())

#Dois sistemas de filtros

print('------FILTROS-----')
print(df[(df['Idade'] >20) & (df['Salario'] > 6000)])

#CLASSIFICAR PELA IDADE
print('------CLASSIFICADOR-----')
df['Classificacao'] = df['Idade'].apply(
    lambda idade: 'Maior de idade'
)
print(df[['Nome','Idade','Classificacao']])

#Usando Lambda com for
print('------Lambda do for-----')
notas = [4, 5, 7, 2, 9]
df2 = pd.DataFrame({'Notas':notas})
df2['Resultado'] = df2['Notas'].apply(
    lambda nota: 'Aprovado' if nota >= 7 else 'Reprovado'   
)

#Usando Lambda com for
print('------Salarios do maior para o menor-----')
print(df.sort_values(by='Salario', ascending = False))

#Acessar linhas especificas
print('Primeiro Funcionario')
print(df.iloc[0])
print('Primeiros Funcionarios')
print(df.iloc[:3])

#CALCULOS
print('------CALCULOS------')
print(df['Salario'].count())
print(df['Idade'].mean())
print(df['Salario'].sum())
#Alem destes tem minimo e max
print(df['Idade'].min())
print(df['Salario'].max())
#Duas formas para salvar ou criar novo
df.to_csv('Salarios_atualizados.csv', index=False)
#ou sobrescrever o original
df.to_csv('salarios.csv', index=False)
