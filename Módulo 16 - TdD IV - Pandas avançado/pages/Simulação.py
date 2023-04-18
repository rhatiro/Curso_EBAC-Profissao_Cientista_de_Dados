import streamlit as st

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


st.set_page_config(
    page_title="Projeto #02 | Previsão de renda",
    page_icon="https://raw.githubusercontent.com/rhatiro/previsao-renda/main/ebac-course-utils/media/icon/favicon.ico",
    layout="wide",
    initial_sidebar_state="auto",
)


st.sidebar.markdown('''
<div style="text-align:center">
<img src="https://raw.githubusercontent.com/rhatiro/previsao-renda/main/ebac-course-utils/media/logo/newebac_logo_black_half.png" alt="ebac-logo" width=100%>
</div>

# **Profissão: Cientista de Dados**
### [**Projeto #02** | Previsão de renda](https://github.com/rhatiro/previsao-renda)

**Por:** [Roberto Hatiro Nishiyama](https://www.linkedin.com/in/rhatiro/)<br>
**Data:** 14 de abril de 2023.<br>
<!-- **Última atualização:** 14 de abril de 2023. -->

---
''', unsafe_allow_html=True)


with st.sidebar.expander("Bibliotecas/Pacotes", expanded=False):
    st.code('''
    import streamlit as st

    import numpy as np
    import pandas as pd

    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor
    ''', language='python')


filepath = './input/previsao_de_renda.csv'
renda = pd.read_csv(filepath_or_buffer=filepath)
renda.drop(columns=['Unnamed: 0', 'id_cliente'], inplace=True)
renda.drop_duplicates(inplace=True, ignore_index=True)
renda.drop(columns='data_ref', inplace=True)
renda.dropna(inplace=True)
renda_dummies = pd.get_dummies(data=renda)
X = renda_dummies.drop(columns='renda')
y = renda_dummies['renda']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)
reg_tree = DecisionTreeRegressor(random_state=42,
                                 max_depth=8,
                                 min_samples_leaf=4)
reg_tree.fit(X_train, y_train)


st.header("Simulando a previsão de renda")
with st.form("my_form"):
    st.subheader("Preencha os campos abaixo:")

    sexo = st.radio("Sexo", ('M', 'F'))
    veiculo = st.checkbox("Posse de veículo")
    imovel = st.checkbox("Posse de imóvel")
    filhos = st.number_input("Quantidade de filhos", 0, 15)
    tiporenda = st.selectbox("Tipo de renda", [
                             'Sem renda', 'Empresário', 'Assalariado', 'Servidor público', 'Pensionista', 'Bolsista'])
    if tiporenda == 'Sem renda':
        tiporenda = None
    educacao = st.selectbox("Educação", [
                            'Primário', 'Secundário', 'Superior incompleto', 'Superior completo', 'Pós graduação'])
    estadocivil = st.selectbox(
        "Estado civil", ['Solteiro', 'União', 'Casado', 'Separado', 'Viúvo'])
    residencia = st.selectbox("Tipo de residência", [
                              'Casa', 'Governamental', 'Com os pais', 'Aluguel', 'Estúdio', 'Comunitário'])
    idade = st.slider("Idade", 18, 100)
    tempoemprego = st.slider("Tempo de emprego", 0, 50)
    qtdpessoasresidencia = st.number_input(
        "Quantidade de pessoas na residência", 1, 15)

    submitted = st.form_submit_button("Simular")
    if submitted:
        entrada = pd.DataFrame([{'sexo': sexo,
                                 'posse_de_veiculo': veiculo,
                                 'posse_de_imovel': imovel,
                                 'qtd_filhos': filhos,
                                 'tipo_renda': tiporenda,
                                 'educacao': educacao,
                                 'estado_civil': estadocivil,
                                 'tipo_residencia': residencia,
                                 'idade': idade,
                                 'tempo_emprego': tempoemprego,
                                 'qt_pessoas_residencia': qtdpessoasresidencia}])
        entrada = pd.concat([X, pd.get_dummies(entrada)]
                            ).fillna(value=0).tail(1)
        st.write(
            f"Renda estimada: R${str(np.round(reg_tree.predict(entrada).item(), 2)).replace('.', ',')}")
