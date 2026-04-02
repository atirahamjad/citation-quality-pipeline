import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="Citation Quality Assessment", page_icon="📄", layout="wide")

st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
    border: 1px solid #444;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.big-number { font-size: 2.5rem; font-weight: 700; color: #7c9ef8; }
.metric-label { font-size: 0.85rem; color: #aaa; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

SAMPLE_DIR = "sample_outputs"
EXCEL = os.path.join(SAMPLE_DIR, "THESIS_FINAL_ANALYSIS new.xlsx")

@st.cache_data
def load(sheet):
    return pd.read_excel(EXCEL, sheet_name=sheet)

st.title("Citation Quality Assessment Pipeline")
st.markdown("**An end-to-end ML pipeline automating academic citation quality assessment**  \nBuilt during a Research Assistantship at Sunway Business School · Pending publication · Under consideration for university-wide adoption")
st.divider()

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Precision", "95%", delta="vs manual review")
with col2:
    st.metric("Time Saved", "98%")
with col3:
    st.metric("Lines of Code", "12,500+")
with col4:
    st.metric("Citation Styles", "5")
with col5:
    st.metric("Journal Databases", "3")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Pipeline Overview", "Citation Analysis", "Journal Quality", "Reference Verification", "Interactive Charts"])

with tab1:
    summary = load("summary")
    meta = load("metadata")
    doc = load("doctype_distribution")
    sec = load("section_distribution")
    claims = load("claims_distribution")
    years = load("years_distribution")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Document stats")
        for _, row in meta.iterrows():
            st.markdown(f"**{row['metric']}:** {row['value']}")

        st.divider()
        st.subheader("Pipeline stages")
        stages = [
            ("Document ingestion", "Extracts full text, detects citation style with confidence score, identifies section boundaries"),
            ("Reference parsing", "Parses each entry into structured fields — authors, year, title, journal, DOI, volume, pages"),
            ("Citation extraction", "Detects all in-text markers, captures sentence context, classifies citation role"),
            ("Citation-reference linking", "Fuzzy-matches each marker to its reference using rapidfuzz, with confidence score"),
            ("Journal quality scoring", "Matches against JCR Web of Science, ABDC, and AJG-ABS databases"),
            ("Outlier detection & export", "Flags Q1 exceptional and problematic references, generates multi-sheet Excel report"),
        ]
        for title, desc in stages:
            with st.expander(title):
                st.write(desc)

    with col2:
        fig_doc = px.pie(doc, values="count", names="doc_type", title="Reference types",
                         color_discrete_sequence=px.colors.sequential.Plasma_r, hole=0.4)
        fig_doc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_doc, use_container_width=True)

        fig_sec = px.bar(sec.sort_values("count", ascending=True), x="count", y="section",
                         orientation="h", title="Citations by section",
                         color="count", color_continuous_scale="Viridis")
        fig_sec.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_sec, use_container_width=True)

with tab2:
    citations = load("citations")
    qual = load("reference_quality_scores")
    exceptional = load("exceptional_citations")
    outliers = load("outliers_flagged")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total citations", len(citations))
        st.metric("Exceptional citations", len(exceptional))
        st.metric("Flagged outliers", len(outliers))
    with col2:
        quad_counts = citations["quadrant"].value_counts().reset_index()
        quad_counts.columns = ["quadrant", "count"]
        fig_quad = px.pie(quad_counts, values="count", names="quadrant",
                          title="Citation quadrant distribution",
                          color_discrete_sequence=px.colors.qualitative.Bold, hole=0.3)
        fig_quad.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_quad, use_container_width=True)

    st.subheader("Citation quality scatter")
    fig_scatter = px.scatter(citations,
                             x="internal_similarity_score",
                             y="external_similarity_score",
                             color="quadrant",
                             hover_data=["in_text_marker", "section"],
                             title="Internal vs External similarity — all citations",
                             color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Reference quality scores")
    fig_qual = px.bar(qual.sort_values("reference_quality_score", ascending=False).head(20),
                      x="ref_key", y="reference_quality_score", color="classification",
                      title="Top 20 references by quality score",
                      color_discrete_sequence=px.colors.qualitative.Safe)
    fig_qual.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig_qual, use_container_width=True)

with tab3:
    jcr = load("jcr_matched_journals")
    abdc = load("abdc_matched_journals")
    ajg = load("ajg_matched_journals")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("JCR matched journals", len(jcr))
    with col2:
        st.metric("ABDC matched journals", len(abdc))
    with col3:
        st.metric("AJG matched journals", len(ajg))

    col1, col2 = st.columns(2)
    with col1:
        abdc_rating = abdc["abdc_rating"].value_counts().reset_index()
        abdc_rating.columns = ["rating", "count"]
        fig_abdc = px.bar(abdc_rating, x="rating", y="count",
                          title="ABDC journal ratings",
                          color="rating",
                          color_discrete_sequence=px.colors.sequential.Teal)
        fig_abdc.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_abdc, use_container_width=True)

    with col2:
        ajg_rating = ajg["ajg_rating"].value_counts().reset_index()
        ajg_rating.columns = ["rating", "count"]
        fig_ajg = px.bar(ajg_rating, x="rating", y="count",
                         title="AJG journal ratings",
                         color="rating",
                         color_discrete_sequence=px.colors.sequential.Magma)
        fig_ajg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_ajg, use_container_width=True)

    st.subheader("JCR — Journal Impact Factor distribution")
    fig_jif = px.histogram(jcr, x="jif_2024", nbins=15,
                           title="Journal Impact Factor (JIF 2024)",
                           color_discrete_sequence=["#7c9ef8"])
    fig_jif.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig_jif, use_container_width=True)

with tab4:
    verif = load("reference_verification")
    status_counts = verif["verification_status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    col1, col2 = st.columns(2)
    with col1:
        fig_verif = px.pie(status_counts, values="count", names="status",
                           title="Reference verification status",
                           color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.4)
        fig_verif.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_verif, use_container_width=True)

    with col2:
        fig_match = px.histogram(verif, x="match_score", nbins=20,
                                 title="Verification match score distribution",
                                 color_discrete_sequence=["#f87c7c"])
        fig_match.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_match, use_container_width=True)

    st.subheader("Full verification table")
    st.dataframe(verif[["ref_key", "verification_status", "match_score", "title", "authors_str", "year"]],
                 use_container_width=True)

with tab5:
    charts = {
        "Quality score distribution": "quality_score_visualization (5).html",
        "Correlation heatmap": "correlation_heatmap (6).html",
        "3D scatter plot": "correlation_3d_scatter (6).html",
        "Quadrant plot": "correlation_quadrant_plot (6).html",
        "Top & bottom references": "correlation_top_bottom (7).html",
        "Verification results": "verification_results (5).html",
    }
    selected = st.selectbox("Select chart", list(charts.keys()))
    html_path = os.path.join(SAMPLE_DIR, charts[selected])
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            st.components.v1.html(f.read(), height=700, scrolling=True)
    else:
        st.warning("File not found.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    with open(EXCEL, "rb") as f:
        st.download_button("Download full Excel report", data=f,
                           file_name="citation_quality_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
with col2:
    st.caption("Atirah Amjad · MsBA Distinction, Sunway University · github.com/atirahamjad/citation-quality-pipeline")

