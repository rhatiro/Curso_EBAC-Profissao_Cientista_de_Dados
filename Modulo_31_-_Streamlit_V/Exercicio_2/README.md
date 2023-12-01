<img src="https://raw.githubusercontent.com/rhatiro/previsao-renda/main/ebac-course-utils/media/logo/newebac_logo_black_half.png" alt="ebac-logo">

---

# [**Profissão: Cientista de Dados**](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados)
### [**Módulo 31** | Streamlit V](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/tree/main/Modulo_31_-_Streamlit_V) | [Exercício 2](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/tree/main/Modulo_31_-_Streamlit_V/Exercicio_2)

**Por:** [Roberto Hatiro Nishiyama](https://www.linkedin.com/in/rhatiro/)<br>
**Data:** 30 de novembro de 2023.

---

# **Projeto de Agrupamento Hierárquico - Streamlit**

Este é um projeto desenvolvido em Python utilizando a biblioteca Streamlit para a visualização interativa de agrupamentos hierárquicos em dados da base [Online Shoppers Purchase Intention](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset) de Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2018). [Web Link](https://doi.org/10.1007/s00521-018-3523-0).

## Objetivo do Projeto

O principal objetivo deste projeto é agrupar as sessões de acesso ao portal através da exploração, análise e busca por padrões baseados no comportamento de navegação e nas informações temporais dos usuários.

- A pergunta central é: 

  > ***"Clientes com comportamentos de navegação diferentes possuem propensão a compra diferente?"***

---

## Visão Geral

A base trata de registros de 12.330 sessões de acesso a páginas, cada sessão sendo de um único usuário em um período de 12 meses, para posteriormente relacionar o design da página e o perfil do cliente.

<details>
  <summary>
    <h3>Dicionário de Dados</h3>
  </summary>

|Variável                |Descrição                                                                                                                      |
| :--------------------- |:----------------------------------------------------------------------------------------------------------------------------  |
|Administrative          | Quantidade de acessos em páginas administrativas                                                                              |
|Administrative_Duration | Tempo de acesso em páginas administrativas                                                                                    |
|Informational           | Quantidade de acessos em páginas informativas                                                                                 |
|Informational_Duration  | Tempo de acesso em páginas informativas                                                                                       |
|ProductRelated          | Quantidade de acessos em páginas de produtos                                                                                  |
|ProductRelated_Duration | Tempo de acesso em páginas de produtos                                                                                        |
|BounceRates             | *Percentual de visitantes que entram no site e saem sem acionar outros *requests* durante a sessão                            |
|ExitRates               | * Soma de vezes que a página é visualizada por último em uma sessão dividido pelo total de visualizações                      |
|PageValues              | * Representa o valor médio de uma página da Web que um usuário visitou antes de concluir uma transação de comércio eletrônico |
|SpecialDay              | Indica a proximidade a uma data festiva (dia das mães etc)                                                                    |
|Month                   | Mês                                                                                                                           |
|OperatingSystems        | Sistema operacional do visitante                                                                                              |
|Browser                 | Browser do visitante                                                                                                          |
|Region                  | Região                                                                                                                        |
|TrafficType             | Tipo de tráfego                                                                                                               |
|VisitorType             | Tipo de visitante: novo ou recorrente                                                                                         |
|Weekend                 | Indica final de semana                                                                                                        |
|Revenue                 | Indica se houve compra ou não                                                                                                 |

*Variáveis calculadas pelo Google Analytics*

</details>

---

## Link para a aplicação (*Deploy* do projeto)
https://rhatiro--ebac--projeto-de-agrupamento-hierarquico.streamlit.app/

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=white)](https://rhatiro--ebac--projeto-de-agrupamento-hierarquico.streamlit.app/)

---

<details>
  <summary>
    <h3>Requirements</h3>
  </summary>
  
```bash
altair==5.1.2
attrs==23.1.0
blinker==1.7.0
cachetools==5.3.2
certifi==2023.11.17
charset-normalizer==3.3.2
click==8.1.7
contourpy==1.2.0
cycler==0.12.1
fonttools==4.45.1
gitdb==4.0.11
GitPython==3.1.40
gower==0.1.2
idna==3.5
importlib-metadata==6.8.0
importlib-resources==6.1.1
Jinja2==3.1.2
jsonschema==4.20.0
jsonschema-specifications==2023.11.1
kiwisolver==1.4.5
markdown-it-py==3.0.0
MarkupSafe==2.1.3
matplotlib==3.8.2
mdurl==0.1.2
numpy==1.26.2
packaging==23.2
pandas==2.1.3
Pillow==10.1.0
protobuf==4.25.1
pyarrow==14.0.1
pydeck==0.8.1b0
Pygments==2.17.2
pyparsing==3.1.1
python-dateutil==2.8.2
pytz==2023.3.post1
referencing==0.31.0
requests==2.31.0
rich==13.7.0
rpds-py==0.13.1
scipy==1.11.4
seaborn==0.13.0
six==1.16.0
smmap==5.0.1
streamlit==1.28.2
tenacity==8.2.3
toml==0.10.2
toolz==0.12.0
tornado==6.3.3
typing_extensions==4.8.0
tzdata==2023.3
tzlocal==5.2
urllib3==2.1.0
validators==0.22.0
zipp==3.17.0
```

</details>

#### *Imports*
```python
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
```

---

*Baseado no [Exercício 2](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/blob/main/Mo%CC%81dulo%2030%20-%20Hiera%CC%81rquicos%20%3A%20aglomerativos/Exerci%CC%81cio%202/mod30_tarefa02-roberto_hatiro.ipynb) do [Módulo 30](https://github.com/rhatiro/Curso_EBAC-Profissao_Cientista_de_Dados/tree/main/Mo%CC%81dulo%2030%20-%20Hiera%CC%81rquicos%20%3A%20aglomerativos).*
