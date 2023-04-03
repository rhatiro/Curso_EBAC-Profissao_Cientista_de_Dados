import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os


print('EBAC - Curso Profissão: Cientista de Dados')
print('Módulo 14 | Scripting | Exercício 2')
print('Aluno: Roberto Hatiro Nishiyama')
print('Data: 3 de abril de 2023.\n')


sns.set_theme()

def plot_pivot_table(df: pd.DataFrame, 
                     value: str, 
                     index: str, 
                     func: str, 
                     ylabel: str, 
                     xlabel: str, 
                     opcao: str='nenhuma'
                    ) -> None:
    if opcao == 'nenhuma':
        pd.pivot_table(data=df, 
                       values=value, 
                       index=index,
                       aggfunc=func
                      ).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(data=df, 
                       values=value, 
                       index=index,
                       aggfunc=func
                      ).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(data=df, 
                       values=value, 
                       index=index,
                       aggfunc=func
                      ).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None


for mes in sys.argv[1:]:
    sinasc = pd.read_csv(f'https://raw.githubusercontent.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/main/Mo%CC%81dulo%2014%20-%20Scripting/database/input/SINASC_RO_2019_{mes}.csv')

    max_data = sinasc.DTNASC.max()[:7]
    os.makedirs('./output/figs/'+max_data, exist_ok=True)

    plot_pivot_table(df=sinasc, 
                     value='IDADEMAE', 
                     index='DTNASC', 
                     func='count', 
                     ylabel='Quantidade de nascimentos', 
                     xlabel='Data de nascimento')
    plt.savefig('./output/figs/'+max_data+'/Quantidade de nascimentos.png')
    plt.close()

    plot_pivot_table(df=sinasc, 
                     value='IDADEMAE', 
                     index=['DTNASC', 'SEXO'], 
                     func='mean', 
                     ylabel='Média da idade das mães', 
                     xlabel='Data de nascimento', 
                     opcao='unstack')
    plt.savefig('./output/figs/'+max_data+'/Média da idade das mães por sexo.png')
    plt.close()

    plot_pivot_table(df=sinasc, 
                     value='PESO', 
                     index=['DTNASC', 'SEXO'], 
                     func='mean', 
                     ylabel='Média do peso dos bebês', 
                     xlabel='Data de nascimento',
                     opcao='unstack')
    plt.savefig('./output/figs/'+max_data+'/Média do peso dos bebês por sexo.png')
    plt.close()

    plot_pivot_table(df=sinasc, 
                     value='APGAR1', 
                     index='ESCMAE', 
                     func='median', 
                     ylabel='Mediana do APGAR1', 
                     xlabel='Escolaridade',
                     opcao='sort')
    plt.savefig('./output/figs/'+max_data+'/Mediana do APGAR1 por escolaridade das mães.png')
    plt.close()

    plot_pivot_table(df=sinasc, 
                     value='APGAR1', 
                     index='GESTACAO', 
                     func='mean', 
                     ylabel='Média do APGAR1', 
                     xlabel='Gestação',
                     opcao='sort')
    plt.savefig('./output/figs/'+max_data+'/Média do APGAR1 por gestação.png')
    plt.close()

    plot_pivot_table(df=sinasc, 
                     value='APGAR5', 
                     index='GESTACAO', 
                     func='mean', 
                     ylabel='Média do APGAR5', 
                     xlabel='Gestação',
                     opcao='sort')
    plt.savefig('./output/figs/'+max_data+'/Média do APGAR5 por gestação.png')
    plt.close()
    
    print('Data inicial:', sinasc.DTNASC.min())
    print('Data final:', sinasc.DTNASC.max())
    print('Nome da pasta:', max_data, '\n')
    