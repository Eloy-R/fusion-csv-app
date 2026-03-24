import streamlit as st
import pandas as pd
import io
import csv

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fusionner CSV",
    page_icon="📊",
    layout="wide"
)

st.title("Fusionner CSV")

# -----------------------------
# FONCTION : détection séparateur
# -----------------------------
def detect_separator(file):
    sample = file.read(2048).decode("utf-8", errors="ignore")
    file.seek(0)
    try:
        sep = csv.Sniffer().sniff(sample).delimiter
    except:
        sep = ";"
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
    colonnes_reference = None

    for file in files:
        try:
            # Détection séparateur
            sep = detect_separator(file)

            # Lecture fichier
            df = pd.read_csv(file, sep=sep, encoding="utf-8", dtype=str, engine="python")

            # Nettoyage noms de colonnes
            df.columns = df.columns.str.strip()

            # Définir les colonnes de référence (premier fichier)
            if colonnes_reference is None:
                colonnes_reference = list(df.columns)

            # Ajouter colonne source (sans .csv)
            df["source"] = file.name.replace(".csv", "")

            df_list.append(df)

        except Exception as e:
            erreurs.append(f"{file.name} : {e}")

    # Affichage erreurs
    if erreurs:
        st.error("❌ Erreurs détectées :")
        for err in erreurs:
            st.write(err)

    # Fusion
    if df_list:

        df_final = pd.concat(df_list, ignore_index=True, sort=False)

        # -----------------------------
        # GARANTIR ORDRE DES COLONNES
        # -----------------------------
        colonnes_finales = colonnes_reference.copy()

        for col in df_final.columns:
            if col not in colonnes_finales:
                colonnes_finales.append(col)

        df_final = df_final[colonnes_finales]

        # Remplacer NaN par vide (important pour import)
        df_final = df_final.fillna("")

        st.success(f"✅ {len(df_list)} fichiers fusionnés")

        # -----------------------------
        # PREVIEW
        # -----------------------------
        st.subheader("🔍 Aperçu")
        st.dataframe(df_final.head(100), use_container_width=True)

        st.write("Dimensions :", df_final.shape)

        # -----------------------------
        # EXPORT CSV (format compatible)
        # -----------------------------
        csv_export = df_final.to_csv(index=False, sep=";").encode("utf-8")

        st.download_button(
            label="📥 Télécharger CSV",
            data=csv_export,
            file_name="fusion.csv",
            mime="text/csv"
        )

        # -----------------------------
        # EXPORT EXCEL (option bonus)
        # -----------------------------
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            df_final.to_excel(writer, index=False)

        st.download_button(
            label="📥 Télécharger Excel",
            data=excel_buffer.getvalue(),
            file_name="fusion.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("👆 Ajoute des fichiers CSV pour commencer")
