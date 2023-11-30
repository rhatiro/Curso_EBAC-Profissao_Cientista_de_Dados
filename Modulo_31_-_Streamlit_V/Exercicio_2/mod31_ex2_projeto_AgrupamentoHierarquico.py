import streamlit             as st
import io

import numpy                 as np
import pandas                as pd
import matplotlib.pyplot     as plt
import seaborn               as sns

from gower                   import gower_matrix

from scipy.spatial.distance  import squareform
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import fcluster



@st.cache_data(show_spinner=False)
def calcularGowerMatrix(data_x, cat_features):
    return gower_matrix(data_x=data_x, cat_features=cat_features)


@st.cache_data(show_spinner=False)
# Definir a função para criar um dendrograma
def dn(color_threshold: float, num_groups: int, Z: list) -> None:
    """
    Cria e exibe um dendrograma.

    Parameters:
        color_threshold (float): Valor de threshold de cor para a coloração do dendrograma.
        num_groups (int): Número de grupos para o título do dendrograma.
        Z (list): Matriz de ligação Z.

    Returns:
        None
    """
    plt.figure(figsize=(24, 6))
    plt.ylabel(ylabel='Distância')
    
    # Adicionar o número de grupos como título
    plt.title(f'Dendrograma Hierárquico - {num_groups} Grupos')

    # Criar o dendrograma com base na matriz de ligação Z
    dn = dendrogram(Z=Z, 
                    p=6, 
                    truncate_mode='level', 
                    color_threshold=color_threshold, 
                    show_leaf_counts=True, 
                    leaf_font_size=8, 
                    leaf_rotation=45, 
                    show_contracted=True)
    plt.yticks(np.linspace(0, .6, num=31))
    plt.xticks([])

    # Exibir o dendrograma criado
    st.pyplot(plt)

    # Imprimir o número de elementos em cada parte do dendrograma
    for i in dn.keys():
        st.text(f'dendrogram.{i}: {len(dn[i])}')


# Função principal da aplicação
def main():
    # Configuração inicial da página da aplicação
    st.set_page_config(
        page_title="EBAC | Módulo 31 | Projeto de Agrupamento hierárquico",
        page_icon='https://raw.githubusercontent.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/main/ebac-course-utils/media/icon/favicon.ico', 
        layout="wide",
        initial_sidebar_state="expanded",
    )


    st.sidebar.markdown('''
                        <div style="text-align:center">
                            <img src="https://raw.githubusercontent.com/rhatiro/previsao-renda/main/ebac-course-utils/media/logo/newebac_logo_black_half.png" alt="ebac-logo" width=50%>
                        </div>

                        # **Profissão: Cientista de Dados**
                        ### **Projeto de Agrupamento Hierárquico**

                        **Por:** [Roberto Hatiro Nishiyama](https://www.linkedin.com/in/rhatiro/)<br>
                        **Data:** 30 de novembro de 2023.<br>

                        ---
                        ''', unsafe_allow_html=True)
    

    with st.sidebar.expander(label="Índice", expanded=False):
        st.markdown('''
                    - [Entendimento do negócio](#intro)
                    - [Visualização dos dados](#visualizacao)
                        > - [Carregamento e leitura do arquivo csv](#read_csv)
                        > - [Contagem de valores da coluna Revenue](#value_counts)
                        > - [Representação gráfica da contagem](#countplot)
                    - [Análise descritiva](#descritiva)
                        > - [Estrutura do dataFrame](#info)
                        > - [Resumo estatístico para variáveis numéricas](#describe)
                        > - [Correlação entre variáveis](#corr)
                    - [Feature selection](#feature_selection)
                        > - [Padrão de navegação na sessão](#session_navigation_pattern)
                        > - [Características temporais](#temporal_indicators)
                        > - [Seleção de variáveis numéricas e categóricas](#cat_selection)
                        > - [Variáveis categóricas e seus valores únicos](#unique)
                    - [Processamento de Variáveis Dummy: Identificação categórica e análise dos tipos de dados](#dummy)
                    - [Agrupamentos hierárquicos](#agrupamento)
                        > - [Cálculo da matriz de distância Gower](#gower)
                        > - [Cálculo da matriz de ligação a partir da vetorização da distância Gower](#linkage)
                        > - [Dendrogramas para diferentes números de grupos](#dendrogram)
                    - [Construção, avaliação e análise dos grupos](#grupos)
                        > - [Agrupamento e resultados para 3 grupos](#grupo_3)
                        >> - [Distribuição percentual com tabela cruzada](#crosstab3perc)
                        >> - [Tabela cruzada percentual com renomeação](#crosstab3rename)
                        > - [Agrupamento e resultados para 4 grupos](#grupo_4)
                        >> - [Distribuição percentual com tabela cruzada](#crosstab4perc)
                        >> - [Tabela cruzada percentual com renomeação](#crosstab4rename)
                        > - [Pair Plot final](#pairplot)
                    - [Conclusão](#final)
                    ''', unsafe_allow_html=True)


    with st.sidebar.expander(label="Bibliotecas/Pacotes", expanded=False):
        st.code('''
                import streamlit             as st
                import io

                import numpy                 as np
                import pandas                as pd
                import matplotlib.pyplot     as plt
                import seaborn               as sns

                from gower                   import gower_matrix

                from scipy.spatial.distance  import squareform
                from scipy.cluster.hierarchy import linkage
                from scipy.cluster.hierarchy import dendrogram
                from scipy.cluster.hierarchy import fcluster
                ''', language='python')
        

    st.sidebar.markdown('''
                        ---
                        *Baseado no [Exercício 2](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/blob/main/Mo%CC%81dulo%2030%20-%20Hiera%CC%81rquicos%20%3A%20aglomerativos/Exerci%CC%81cio%202/mod30_tarefa02-roberto_hatiro.ipynb) do [Módulo 30](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/tree/main/Mo%CC%81dulo%2030%20-%20Hiera%CC%81rquicos%20%3A%20aglomerativos).*
                        ''')


    st.markdown('''
                <div style="text-align:center">
                    <img src="https://raw.githubusercontent.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/main/ebac-course-utils/media/logo/ebac_logo-data_science.png" alt="ebac_logo-data_science" width="100%">
                </div>

                ---

                <!-- # **Profissão: Cientista de Dados** -->
                ### **Módulo 31** | Streamlit V (Exercício 2)

                **Aluno:** [Roberto Hatiro Nishiyama](https://www.linkedin.com/in/rhatiro/)<br>
                **Data:** 30 de novembro de 2023.

                ---
                ''', unsafe_allow_html=True)


    st.markdown('''
                <a name="intro"></a> 

                # Agrupamento hierárquico

                Neste projeto foi utilizada a base [online shoppers purchase intention](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset) de Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2018). [Web Link](https://doi.org/10.1007/s00521-018-3523-0).

                A base trata de registros de 12.330 sessões de acesso a páginas, cada sessão sendo de um único usuário em um período de 12 meses, para posteriormente relacionar o design da página e o perfil do cliente.
                
                ***"Será que clientes com comportamento de navegação diferentes possuem propensão a compra diferente?"***

                O objetivo é agrupar as sessões de acesso ao portal considerando o comportamento de acesso e informações da data, como a proximidade a uma data especial, fim de semana e o mês.

                |Variável                |Descrição                                                                                                                      |Atributo   | 
                | :--------------------- |:----------------------------------------------------------------------------------------------------------------------------  | --------: | 
                |Administrative          | Quantidade de acessos em páginas administrativas                                                                              |Numérico   | 
                |Administrative_Duration | Tempo de acesso em páginas administrativas                                                                                    |Numérico   | 
                |Informational           | Quantidade de acessos em páginas informativas                                                                                 |Numérico   | 
                |Informational_Duration  | Tempo de acesso em páginas informativas                                                                                       |Numérico   | 
                |ProductRelated          | Quantidade de acessos em páginas de produtos                                                                                  |Numérico   | 
                |ProductRelated_Duration | Tempo de acesso em páginas de produtos                                                                                        |Numérico   | 
                |BounceRates             | *Percentual de visitantes que entram no site e saem sem acionar outros *requests* durante a sessão                            |Numérico   | 
                |ExitRates               | * Soma de vezes que a página é visualizada por último em uma sessão dividido pelo total de visualizações                      |Numérico   | 
                |PageValues              | * Representa o valor médio de uma página da Web que um usuário visitou antes de concluir uma transação de comércio eletrônico |Numérico   | 
                |SpecialDay              | Indica a proximidade a uma data festiva (dia das mães etc)                                                                    |Numérico   | 
                |Month                   | Mês                                                                                                                           |Categórico | 
                |OperatingSystems        | Sistema operacional do visitante                                                                                              |Categórico | 
                |Browser                 | Browser do visitante                                                                                                          |Categórico | 
                |Region                  | Região                                                                                                                        |Categórico | 
                |TrafficType             | Tipo de tráfego                                                                                                               |Categórico | 
                |VisitorType             | Tipo de visitante: novo ou recorrente                                                                                         |Categórico | 
                |Weekend                 | Indica final de semana                                                                                                        |Categórico | 
                |Revenue                 | Indica se houve compra ou não                                                                                                 |Categórico |

                *Variáveis calculadas pelo Google Analytics*

                ''', unsafe_allow_html=True)


    st.markdown(''' 
                ## Visualização dos Dados
                <a name="visualizacao"></a> 
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Carregar e ler dados de arquivo .csv
                <a name="read_csv"></a> 
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Ler o arquivo CSV 'online_shoppers_intention.csv' e armazenar os dados em um DataFrame chamado df
        df = pd.read_csv('https://raw.githubusercontent.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/main/Modulo_31_-_Streamlit_V/Exercicio_2/online_shoppers_intention.csv')

        # Exibir o DataFrame df, mostrando os dados carregados do arquivo CSV
        st.dataframe(df)


    st.markdown(''' 
                ### Visualização da contagem de valores na coluna 'Revenue'
                <a name="value_counts"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Exibir a contagem de valores na coluna 'Revenue'
        st.text(df.Revenue.value_counts())


    st.markdown(''' 
                ### Representação gráfica da contagem de 'Revenue' 
                <a name="countplot"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um gráfico de contagem (count plot) para a coluna 'Revenue' usando seaborn
        sns.countplot(x='Revenue', data=df)

        # Exibir o gráfico
        st.pyplot(plt)


    st.markdown(''' 
                ## Análise Descritiva
                <a name="descritiva"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Informações sobre a estrutura do DataFrame
                <a name="info"></a>
                ''', unsafe_allow_html=True)
    # Imprimir informações sobre a estrutura do DataFrame
    st.info(f''' 
            Quantidade de linhas: {df.shape[0]}

            Quantidade de colunas: {df.shape[1]}

            Quantidade de valores missing: {df.isna().sum().sum()} 
            ''')
    with st.echo():
        ""
        # Exibir informações detalhadas sobre o DataFrame, incluindo os tipos de dados de cada coluna e a contagem de valores não nulos
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())


    st.markdown(''' 
                ### Resumo estatístico para variáveis numéricas
                <a name="describe"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Exibir estatísticas descritivas para colunas numéricas do DataFrame
        st.dataframe(df.describe())


    st.markdown(''' 
                ### Representação gráfica da correlação entre variáveis
                <a name="corr"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um mapa de calor (heatmap) para visualizar a correlação entre as colunas do DataFrame
        sns.heatmap(df.corr(numeric_only=True), cmap='viridis')

        # Exibir o mapa de calor
        st.pyplot(plt)


    st.markdown('''
                ## Feature Selection
                <a name="feature_selection"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Seleção e análise das variáveis que descrevem o padrão de navegação na sessão
                <a name="session_navigation_pattern"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis que descrevem o padrão de navegação na sessão
        session_navigation_pattern = ['Administrative', 
                                      'Informational', 
                                      'ProductRelated', 
                                      'PageValues', 
                                      'OperatingSystems', 
                                      'Browser', 
                                      'TrafficType', 
                                      'VisitorType']

        # Obter os tipos de dados das variáveis relacionadas ao padrão de navegação na sessão, criar um DataFrame e renomear as colunas
        st.dataframe(df[session_navigation_pattern].dtypes.reset_index().rename(columns={'index': 'Variável (session_navigation_pattern)', 
                                                                                         0: 'Tipo'}), hide_index=True)

    st.markdown(''' 
                ### Seleção e análise das variáveis que indicam a característica da data
                <a name="temporal_indicators"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis que indicam a característica da data
        temporal_indicators = ['SpecialDay', 'Month', 'Weekend']

        # Obter os tipos de dados das variáveis relacionadas à característica da data, criar um DataFrame e renomear as colunas
        st.dataframe(df[temporal_indicators].dtypes.reset_index().rename(columns={'index': 'Variável (temporal_indicators)', 
                                                                                  0: 'Tipo'}), hide_index=True)


    st.markdown(''' 
                ### Seleção das variáveis numéricas e categóricas
                <a name="cat_selection"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Lista de variáveis numéricas
        numerical = ['ProductRelated', 'PageValues', 'SpecialDay']

        # Selecionar as variáveis relacionadas ao padrão de navegação e à característica da data
        df_ = df[session_navigation_pattern + temporal_indicators]

        # Selecionar as variáveis categóricas removendo as variáveis numéricas
        df_cat = df_.drop(columns=numerical)


    st.markdown(''' 
                ### Variáveis categóricas e seus valores únicos
                <a name="unique"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Imprimir os valores únicos para cada variável categórica
        [f'{cat}: {df[cat].unique()}' for cat in df_cat]


    st.markdown(''' 
                ## Processamento de Variáveis Dummy: Identificação categórica e análise dos tipos de dados
                <a name="dummy"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar variáveis dummy para as variáveis relacionadas ao padrão de navegação e à característica da data
        df_dummies = pd.get_dummies(data=df_, drop_first=False)

        # Obter as colunas que representam as variáveis categóricas
        categorical_features = df_dummies.drop(columns=numerical).columns.values

        # Criar uma lista de valores booleanos indicando se cada coluna é categórica
        cat_features = [True if column in categorical_features else False for column in df_dummies]

        # Obter os tipos de dados das variáveis dummy, criar um DataFrame e adicionar uma coluna indicando se a variável é categórica
        st.dataframe(df_dummies.dtypes.reset_index().rename(columns={'index': 'Variável', 
                                                                     0: 'Tipo'
                                                                     }).assign(Categorical=cat_features), hide_index=True)


    st.markdown(''' 
                ## Agrupamentos Hierárquicos com 3 e 4 grupos 
                <a name="agrupamento"></a>
                ''', unsafe_allow_html=True)


    st.markdown(''' 
                ### Cálculo da Matriz de Distância Gower
                <a name="gower"></a>
                ''', unsafe_allow_html=True)
    with st.spinner(text='Calculando matriz de distância Gower... (Tempo previsto: 4 minutos)'):
        with st.echo():
            ""
            # Calcular a matriz de distância Gower
            dist_gower = calcularGowerMatrix(data_x=df_dummies, cat_features=cat_features)
    st.success('Matriz de distância Gower calculada!')
    with st.echo():
        ""
        # Criar um DataFrame com a matriz de distância Gower
        st.dataframe(pd.DataFrame(dist_gower).head())


    st.markdown(''' 
                ### Cálculo da matriz de ligação a partir da vetorização da distância Gower
                <a name="linkage"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Converter a matriz de distância Gower em um vetor
        gdv = squareform(X=dist_gower, force='tovector')

        # Calcular a matriz de ligação usando o método 'complete'
        Z = linkage(y=gdv, method='complete')

        # Criar um DataFrame com a matriz de ligação
        st.dataframe(pd.DataFrame(data=Z, columns=['id1', 'id2', 'dist', 'n']), hide_index=True)


    st.markdown(''' 
                ### Visualização dos agrupamentos: Dendrogramas para diferentes números de grupos
                <a name="dendrogram"></a>
                ''', unsafe_allow_html=True)
    # Para cada quantidade desejada de grupos e valor de threshold de cor, criar e exibir o dendrograma com título
    for qtd, color_threshold in [(3, .53), (4, .5)]:
        st.info(f'\n{qtd} grupos:')
        # Exibir os dendrogramas criados
        dn(color_threshold=color_threshold, num_groups=qtd, Z=Z)


    st.markdown('''
                ## Construção, Avaliação e Análise dos Grupos
                <a name="grupos"></a>
                ''', unsafe_allow_html=True)
    

    st.markdown(''' 
                ### Agrupamento e atualização do dataFrame com resultados para 3 grupos
                <a name="grupo_3"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Adicionar uma coluna 'grupo_3' ao DataFrame com base no agrupamento hierárquico
        df['grupo_3'] = fcluster(Z=Z, t=3, criterion='maxclust')

        # Criar um DataFrame contendo a contagem de elementos em cada grupo
        st.dataframe(pd.DataFrame({'Grupo': df.grupo_3.value_counts().index, 
                                   'Quantidade': df.grupo_3.value_counts().values
                                   }).set_index('Grupo').style.format({'Quantidade': lambda x : '{:d}'.format(x)}))


    st.markdown(''' 
                ### Distribuição percentual com tabela cruzada para 3 grupos
                <a name="crosstab3perc"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar e exibir uma tabela cruzada normalizada por linha para as variáveis 'VisitorType', 'grupo_3' e 'Revenue'
        st.table(pd.crosstab(index=df.VisitorType, 
                             columns=[df.grupo_3, df.Revenue], 
                             normalize='index'
                             ).applymap(lambda x: f'{x*100:.0f} %'))


    st.markdown(''' 
                ### Tabela cruzada percentual com renomeação dos 3 grupos
                <a name="crosstab3rename"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar e exibir uma tabela cruzada normalizada por linha para as variáveis 'Revenue' e 'grupo_3', com renomeação dos grupos
        st.table(pd.crosstab(index=df.Revenue, 
                             columns=df.grupo_3, 
                             normalize='index'
                             ).applymap(lambda x: f'{x*100:.2f} %').rename(columns={1: '1 (Returning_Visitor)', 
                                                                                    2: '2 (New_Visitor)', 
                                                                                    3: '3 (Other)'}))


    st.markdown(''' 
                ### Agrupamento e atualização do dataFrame com resultados para 4 grupos
                <a name="grupo_4"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Adicionar uma coluna 'grupo_4' ao DataFrame com base no agrupamento hierárquico
        df['grupo_4'] = fcluster(Z=Z, t=4, criterion='maxclust')

        # Criar um DataFrame contendo a contagem de elementos em cada grupo
        st.dataframe(pd.DataFrame({'Grupo': df.grupo_4.value_counts().index, 
                                   'Quantidade': df.grupo_4.value_counts().values
                                   }).set_index('Grupo').sort_index().style.format({'Quantidade': lambda x : '{:d}'.format(x)}))


    st.markdown(''' 
                ### Distribuição percentual com tabela cruzada para 4 grupos
                <a name="crosstab4perc"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar e exibir uma tabela cruzada normalizada por coluna para as variáveis 'Month', 'grupo_4' e 'Revenue'
        st.table(pd.crosstab(index=df.Month, 
                             columns=[df.grupo_4, df.Revenue], 
                             normalize='columns'
                             ).applymap(lambda x: f'{x*100:.2f} %'))


    st.markdown(''' 
                ### Tabela cruzada percentual com renomeação dos 4 grupos
                <a name="crosstab4rename"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar e exibir uma tabela cruzada normalizada por linha para as variáveis 'Revenue', 'VisitorType', 'SpecialDay' e 'grupo_4', com renomeação dos grupos
        st.markdown(pd.crosstab(index=[df.Revenue, df.VisitorType, df.SpecialDay], 
                                columns=df.grupo_4, 
                                normalize='index'
                                ).applymap(lambda x: f'{x*100:.2f} %').rename(columns={1: '1 (Returning_Visitor - SpecialDay 0)', 
                                                                                       2: '2 (Returning_Visitor - SpecialDay 1)', 
                                                                                       3: '3 (New_Visitor)', 
                                                                                       4: '4 (Other)'
                                                                                       }).reset_index().style.hide(axis='index').to_html(), unsafe_allow_html=True)


    st.markdown(''' 
                <br>

                ### Pair Plot final
                <a name="pairplot"></a>
                ''', unsafe_allow_html=True)
    with st.echo():
        ""
        # Criar um pair plot para visualizar as relações entre as variáveis 'BounceRates', 'Revenue', 'SpecialDay', 'grupo_3' e 'grupo_4', colorindo pelo valor da variável 'Revenue'
        sns.pairplot(data=df[['BounceRates', 'Revenue', 'SpecialDay', 'grupo_3', 'grupo_4']], 
                     hue='Revenue')

        # Exibir o pair plot
        st.pyplot(plt)


    st.markdown('''
                ## Conclusão

                Na análise dos resultados do agrupamento hierárquico, destaca-se a relevância da abordagem centrada nas categorias de tipos de visitantes. Especificamente, ao agrupar em três categorias, o grupo `1 (Returning_Visitor)`, composto por visitantes recorrentes, sobressai ao apresentar a maior propensão à realização de compras. Essa conclusão é sustentada pela análise das relações entre as variáveis de navegação e as características temporais, que resultaram na formação de categorias distintas para os visitantes. Esse insight proporciona uma visão valiosa sobre o comportamento dos visitantes, permitindo a implementação de estratégias direcionadas para diferentes segmentos. Dessa forma, é possível otimizar a experiência do usuário e a eficácia das estratégias de marketing.
                
                ---
                <a name="final"></a>
                ''', unsafe_allow_html=True)


if __name__ == '__main__':
    main()
