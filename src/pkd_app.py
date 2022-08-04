import streamlit as st
import pandas as pd
import warnings

warnings.simplefilter("ignore")
import plotly.express as px
import numpy as np

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
    pkd = pd.read_csv("./data/PKD_Integrated.csv")
    domain = pd.read_csv("./data/PKD_domains.csv")
    domain["domain_info"] = domain["domain"] + " (" + domain["amino acid"] + ")"
    pkd = pkd.drop_duplicates(
        subset=["#chr", "pos(1-based)", "ref", "alt"], keep="first"
    ).reset_index(drop=True)
    pkd = pkd[pkd["aapos"] != -1].reset_index(drop=True)
    # pkd = pkd[['aaref','aaalt','aapos','genename','Ditto_Deleterious','clinvar_clnsig','Interpro_symbol','HGVSp_VEP']]
    # pkd.columns = ['aaref','aaalt','aapos','Gene','Ditto score','Clinvar Significance','Interpro symbol','HGVSp_VEP']
    pkd = pkd.replace(np.nan, "N/A")
    pkd["gnomAD_genomes_AF"] = pkd["gnomAD_genomes_AF"].replace(".", "N/A")
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
        "Benign/Likely_benign": "lightblue",
    }
    return pkd, class_color, domain


def domain_count(data, domain):
    for clinvar_class in list(data["clinvar_clnsig"].unique()):
        counts = []
        # Use .iterrows() to iterate over Pandas rows
        for idx, row in domain.iterrows():
            # domain.iloc[idx]['Pathogenic'] =
            counts.append(
                len(
                    data[
                        (data["aapos"] >= row["start"])
                        & (data["aapos"] <= row["end"])
                        & (data["clinvar_clnsig"] == clinvar_class)
                    ]
                )
            )
        domain[clinvar_class] = counts
    return domain


def pkd_plot(st, data, class_color, domain):
    st.write(f"Total variants = {len(data)}")
    st.write(f"Total domains = {len(domain)}")
    pkd1 = px.scatter(
        data,
        x="aapos",
        y="Ditto_Deleterious",
        color="clinvar_clnsig",
        hover_data=[
            "genename",
            "Interpro_symbol",
            "HGVSc_VEP",
            "CADD_phred",
            "gnomAD_genomes_AF",
            "Defect class",
            "Function",
        ],
        hover_name="HGVSp_VEP",
        labels={
            "aapos": "AA position",
            "Ditto_Deleterious": "Ditto Deleterious Score",
            "clinvar_clnsig": "Clinvar Significance",
        },
        color_discrete_map=class_color,
    )
    pkd1.add_hline(y=0.91, line_width=2, line_dash="dash", line_color="red")

    for idx, row in domain.iterrows():
        pkd1.add_vrect(
            x0=row["start"],
            x1=row["end"],
            line_width=0,
            opacity=0.2,
            fillcolor=row["color"],
            annotation_text=row["domain"],
            annotation_position="outside top",
            annotation_textangle=45,
            # annotation=dict(font_size=10, font_family="Times New Roman"),
        )

    # Plot!
    st.plotly_chart(pkd1, use_container_width=True)
    stack_bar = px.bar(
        domain,
        x="amino acid",
        y=list(data["clinvar_clnsig"].unique()),
        hover_name="domain_info",
        hover_data=["Gene symbol"],
        labels={
            "amino acid": "AA position range per domain",
            "clinvar_clnsig": "Clinvar Significance",
            "value": "# of variants",
            "variable": "Clinvar Significance",
        },
        title="Clinvar classifications by domain",
        color_discrete_map=class_color,
    )

    st.plotly_chart(stack_bar, use_container_width=True)
    return None


def main():

    # col1, col2 = st.columns([2, 1])

    pkd, class_color, domains = load_data()
    st.subheader("PKD1/2 Variants")
    domain = domain_count(pkd, domains)
    pkd_plot(st, pkd, class_color, domain)
    # st.write(domains[['Gene symbol','amino acid','domain']])
    st.subheader("PKD1 Variants")
    domain = domain_count(pkd[pkd["genename"] == "PKD1"], domains[domains["Gene symbol"] == "PKD1"])
    pkd_plot(
        st, pkd[pkd["genename"] == "PKD1"], class_color, domain[domain["Gene symbol"] == "PKD1"]
    )
    st.subheader("PKD2 Variants")
    domain = domain_count(pkd[pkd["genename"] == "PKD2"], domains[domains["Gene symbol"] == "PKD2"])
    pkd_plot(
        st, pkd[pkd["genename"] == "PKD2"], class_color, domain[domain["Gene symbol"] == "PKD2"]
    )


if __name__ == "__main__":
    main()
