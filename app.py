# -----------------------------
# TRAITEMENT
# -----------------------------
if files:

    df_list = []
    erreurs = []
    colonnes_reference = None

    for i, file in enumerate(files):
        try:
            sep = detect_separator(file)

            df = pd.read_csv(file, sep=sep, encoding="utf-8", engine="python")

            # Nettoyage colonnes
            df.columns = df.columns.str.strip()

            # Définir ordre de référence (premier fichier)
            if colonnes_reference is None:
                colonnes_reference = list(df.columns)

            # Ajouter source
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

        # 🔥 GARANTIR ORDRE DES COLONNES
        colonnes_finales = colonnes_reference.copy()

        # Ajouter nouvelles colonnes à la fin
        for col in df_final.columns:
            if col not in colonnes_finales:
                colonnes_finales.append(col)

        df_final = df_final[colonnes_finales]

        # Remplacer NaN par vide
        df_final = df_final.fillna("")

        st.success(f"✅ {len(df_list)} fichiers fusionnés")

        # Preview
        st.subheader("🔍 Aperçu")
        st.dataframe(df_final.head(100), use_container_width=True)

        st.write("**Dimensions :**", df_final.shape)

        # Export CSV
        csv_export = df_final.to_csv(index=False, sep=";").encode("utf-8")

        st.download_button(
            "📥 Télécharger CSV",
            csv_export,
            "fusion.csv",
            "text/csv"
        )
