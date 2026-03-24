import streamlit as st
import pandas as pd
import io
import csv

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fusion CSV",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fusion intelligente de fichiers CSV")
st.markdown("Upload tes fichiers CSV → détection automatique → nettoyage → export propre")

# -----------------------------
# FONCTION : détection séparateur
# -----------------------------
def detect_separator(file):
    sample = file.read(2048).decode("utf-8", errors="ignore")
    file.seek(0)
    sniffer = csv.Sniffer()
    try:
        sep = sniffer.sniff(sample).delimiter
    except:
        sep = ";"  # fallback
    return sep

# -----------------------------
# UPLOAD
# -----------------------------
files = st.file_uploader(
    "📂 Glisse-dépose tes fichiers CSV",
    type=["csv"],
    accept_multiple_files=True
)

# -----------------------------
# TRAITEMENT
# -----------------------------
if files:

    df_list = []
    erreurs = []

    for file in files:
        try:
            # Détection séparateur
            sep = detect_separator(file)

            # Lecture
            df = pd.read_csv(file, sep=sep, encoding="utf-8", engine="python")

            # Nettoyage colonnes
            df.columns = df.columns.str.strip()

            # Supprimer colonnes vides
            df = df.dropna(axis=1, how="all")

            # Ajouter source propre
            df["source"] = file.name.replace(".csv", "")

            df_list.append(df)

        except Exception as e:
            erreurs.append(f"{file.name} : {e}")

    if erreurs:
        st.error("❌ Erreurs :")
        for err in erreurs:
            st.write(err)

    if df_list:
        df_final = pd.concat(df_list, ignore_index=True, sort=False)

        # Nettoyage final
        df_final = df_final.dropna(axis=1, how="all")

        st.success(f"✅ {len(df_list)} fichiers fusionnés")

        # -----------------------------
        # PREVIEW
        # -----------------------------
        st.subheader("🔍 Aperçu")
        st.dataframe(df_final.head(100), use_container_width=True)

        st.write("**Dimensions :**", df_final.shape)

        # -----------------------------
        # EXPORT CSV propre
        # -----------------------------
        csv_export = df_final.to_csv(index=False, sep=";").encode("utf-8")

        st.download_button(
            "📥 Télécharger CSV",
            csv_export,
            "fusion_propre.csv",
            "text/csv"
        )

        # -----------------------------
        # EXPORT EXCEL (BONUS PRO)
        # -----------------------------
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            df_final.to_excel(writer, index=False)

        st.download_button(
            "📥 Télécharger Excel (.xlsx)",
            excel_buffer.getvalue(),
            "fusion_propre.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # -----------------------------
        # INFOS
        # -----------------------------
        with st.expander("📋 Infos colonnes"):
            st.write(df_final.dtypes)

else:
    st.info("👆 Ajoute des fichiers CSV pour commencer")
