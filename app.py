import streamlit as st
import pandas as pd

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fusion CSV",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fusion de fichiers CSV")
st.markdown("Charge plusieurs fichiers CSV et télécharge un fichier fusionné.")

# -----------------------------
# OPTIONS
# -----------------------------
st.sidebar.header("⚙️ Paramètres")

sep = st.sidebar.selectbox("Séparateur", [",", ";", "\t"], index=1)
encoding = st.sidebar.selectbox("Encodage", ["utf-8", "latin1"], index=0)
add_source = st.sidebar.checkbox("Ajouter colonne 'source'", value=True)

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
            df = pd.read_csv(file, sep=sep, encoding=encoding)

            if add_source:
                df["source"] = file.name

            df_list.append(df)

        except Exception as e:
            erreurs.append(f"{file.name} : {e}")

    if erreurs:
        st.error("❌ Erreurs sur certains fichiers :")
        for err in erreurs:
            st.write(err)

    if df_list:
        df_final = pd.concat(df_list, ignore_index=True, sort=False)

        st.success(f"✅ {len(df_list)} fichiers fusionnés")

        # -----------------------------
        # PREVIEW
        # -----------------------------
        st.subheader("🔍 Aperçu des données")
        st.dataframe(df_final.head(100), use_container_width=True)

        st.write("**Dimensions :**", df_final.shape)

        # -----------------------------
        # DOWNLOAD
        # -----------------------------
        csv = df_final.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Télécharger le CSV fusionné",
            data=csv,
            file_name="fusion.csv",
            mime="text/csv"
        )

        # -----------------------------
        # INFOS COLONNES
        # -----------------------------
        with st.expander("📋 Infos colonnes"):
            st.write(df_final.dtypes)

else:
    st.info("👆 Ajoute au moins un fichier CSV pour commencer")
