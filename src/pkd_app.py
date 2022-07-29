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
    class_color = {
                "Pathogenic": "brown",
                "Pathogenic/Likely_pathogenic": "red",
                "Likely_pathogenic": "orange",
                "Uncertain_significance": "green",
                "Conflicting_interpretations_of_pathogenicity": "green",
                "not_provided": "green",
                "Uncertain_significance,_other": "green",
                "other": "green",
                "Likely_benign": "lightblue",
                "Benign": "blue",
                "Benign/Likely_benign": "lightblue"}
    return pkd, class_color


def main():

    # col1, col2 = st.columns([2, 1])

    pkd, class_color = load_data()
    st.subheader("PKD1/2 Variants")
    st.write(f"Total variants = {len(pkd)}")
    fig = px.scatter(pkd, x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','Interpro symbol'], hover_name="HGVSp_VEP", color_discrete_map=class_color,)# marginal_x="histogram", marginal_y="histogram")
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("PKD1 Variants")
    st.write(f"Total variants = {len(pkd[pkd['Gene']=='PKD1'])}")
    pkd1 = px.scatter(pkd[pkd['Gene']=='PKD1'], x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','Interpro symbol'], hover_name="HGVSp_VEP", color_discrete_map=class_color,)
    # Plot!
    st.plotly_chart(pkd1, use_container_width=True)

    st.subheader("PKD2 Variants")
    st.write(f"Total variants = {len(pkd[pkd['Gene']=='PKD2'])}")
    pkd2 = px.scatter(pkd[pkd['Gene']=='PKD2'], x="aapos", y="Ditto score", color="Clinvar Significance", hover_data=['Gene','Interpro symbol'], hover_name="HGVSp_VEP", color_discrete_map=class_color,)
             #title="PKD2 Variants")#, symbol="Interpro symbol")
    # Plot!
    st.plotly_chart(pkd2, use_container_width=True)


if __name__ == "__main__":
    main()
