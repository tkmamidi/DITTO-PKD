import streamlit as st
import pandas as pd
import warnings
warnings.simplefilter("ignore")
import plotly.express as px

# import re

# Config the whole app
st.set_page_config(
    page_title="PKD1/2",
    page_icon="🧊",
    layout="wide",  # initial_sidebar_state="expanded",
)

st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>",
    unsafe_allow_html=True,
)
st.write(
    "<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-right:50px;}</style>",
    unsafe_allow_html=True,
)


@st.cache(allow_output_mutation=True)
def load_data():
    pkd = pd.read_csv('./data/PKD_Integrated.csv')
    pkd = pkd.drop_duplicates(
  subset = ['#chr', 'pos(1-based)',	'ref',	'alt'],
  keep = 'first').reset_index(drop = True)
    pkd = pkd[pkd['aapos']!=-1].reset_index(drop = True)
    pkd = pkd[['aaref','aaalt','aapos','genename','Ditto_Deleterious','clinvar_clnsig','Interpro_symbol','HGVSp_VEP']]
    pkd.columns = ['aaref','aaalt','aapos','Gene','Ditto score','Clinvar Significance','Interpro symbol','HGVSp_VEP']
    return pkd


def main():

    # col1, col2 = st.columns([2, 1])

    pkd = load_data()
    st.subheader("PKD1/2 Variants")
    fig = px.scatter(pkd, x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','HGVSp_VEP','Interpro symbol'])
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("PKD1 Variants")
    pkd1 = px.scatter(pkd[pkd['Gene']=='PKD1'], x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','HGVSp_VEP','Interpro symbol'])
    # Plot!
    st.plotly_chart(pkd1, use_container_width=True)

    st.subheader("PKD2 Variants")
    pkd2 = px.scatter(pkd[pkd['Gene']=='PKD2'], x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','HGVSp_VEP','Interpro symbol'])
    # Plot!
    st.plotly_chart(pkd2, use_container_width=True)


if __name__ == "__main__":
    main()
