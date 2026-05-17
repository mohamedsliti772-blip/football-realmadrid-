#CE PROJET REFLETE LA PERFORMANCE DE REAL MADRID DANS 2024



# =============================================================================
#  Real Madrid – Dashboard Analytics  |  Saison 2024
# =============================================================================
#importation des bibliothèques:

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from math import pi

# ── Configuration générale de la page ────────────────────────────────────────
st.set_page_config(
    page_title="Real Madrid – Analytics 2024",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Palette couleurs Real Madrid ──────────────────────────────────────────────
GOLD   = "#C8A84B"
WHITE  = "#FFFFFF"
DARK   = "#1a1a2e"
PURPLE = "#16213e"

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    .main {{ background-color: {DARK}; }}
    .block-container {{ padding: 1.5rem 2rem; }}
    h1, h2, h3 {{ color: {GOLD}; }}
    .stMetric label {{ color: {GOLD} !important; font-weight: bold; }}
    .stMetric value {{ color: {WHITE} !important; }}
    .sidebar .sidebar-content {{ background: {PURPLE}; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
#chargement data:
# =============================================================================

@st.cache_data
def load_data():
    """Charge les 4 fichiers CSV dans des DataFrames."""
    joueurs  = pd.read_csv("joueurs_realmadrid_2024.csv")
    matchs   = pd.read_csv("matchs_realmadrid_2024.csv")
    finances = pd.read_csv("finances_realmadrid_2024.csv")
    titres   = pd.read_csv("titres_realmadrid_2024.csv")
    return joueurs, matchs, finances, titres

joueurs, matchs, finances, titres = load_data()

# =============================================================================
# EXPLORATION INITIALE DES DONNÉES
# =============================================================================

# ── Aperçu des 5 premières lignes (df.head) ───────────────────────────────────
print("=" * 60)
print("HEAD – joueurs (5 premières lignes)")
print("=" * 60)
print(joueurs.head(5))

print("\n" + "=" * 60)
print("HEAD – matchs (5 premières lignes)")
print("=" * 60)
print(matchs.head(5))

print("\n" + "=" * 60)
print("HEAD – finances (5 premières lignes)")
print("=" * 60)
print(finances.head(5))

print("\n" + "=" * 60)
print("HEAD – titres (5 premières lignes)")
print("=" * 60)
print(titres.head(5))

# ── Informations sur les types et valeurs manquantes (df.info) ────────────────
print("\n" + "=" * 60)
print("INFO – joueurs")
print("=" * 60)
joueurs.info()

print("\n" + "=" * 60)
print("INFO – matchs")
print("=" * 60)
matchs.info()

print("\n" + "=" * 60)
print("INFO – finances")
print("=" * 60)
finances.info()

print("\n" + "=" * 60)
print("INFO – titres")
print("=" * 60)
titres.info()

# ── Statistiques descriptives en utilisant l'instruction (df.describe) ───────────────────────────────────
print("\n" + "=" * 60)
print("DESCRIBE – joueurs")
print("=" * 60)
print(joueurs.describe())

print("\n" + "=" * 60)
print("DESCRIBE – matchs")
print("=" * 60)
print(matchs.describe())

print("\n" + "=" * 60)
print("DESCRIBE – finances")
print("=" * 60)
print(finances.describe())

print("\n" + "=" * 60)
print("DESCRIBE – titres")
print("=" * 60)
print(titres.describe())

# ── Dimensions des datasets ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("SHAPE – dimensions de chaque dataset")
print("=" * 60)
print(f"joueurs  : {joueurs.shape[0]} lignes × {joueurs.shape[1]} colonnes")
print(f"matchs   : {matchs.shape[0]} lignes × {matchs.shape[1]} colonnes")
print(f"finances : {finances.shape[0]} lignes × {finances.shape[1]} colonnes")
print(f"titres   : {titres.shape[0]} lignes × {titres.shape[1]} colonnes")

# ── Valeurs manquantes ────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("VALEURS MANQUANTES (isnull().sum())")
print("=" * 60)
print("-- joueurs --")
print(joueurs.isnull().sum())
print("\n-- matchs --")
print(matchs.isnull().sum())
print("\n-- finances --")
print(finances.isnull().sum())
print("\n-- titres --")
print(titres.isnull().sum())

# ── Doublons ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("DOUBLONS (duplicated().sum())")
print("=" * 60)
print(f"joueurs  : {joueurs.duplicated().sum()} doublon(s)")
print(f"matchs   : {matchs.duplicated().sum()} doublon(s)")
print(f"finances : {finances.duplicated().sum()} doublon(s)")
print(f"titres   : {titres.duplicated().sum()} doublon(s)")

# =============================================================================
# NETTOYAGE DES DONNÉES
# =============================================================================

# ── JOUEURS ───────────────────────────────────────────────────────────────────
joueurs.columns = joueurs.columns.str.strip()               # Supprimer espaces dans noms de colonnes
joueurs["joueur"]      = joueurs["joueur"].str.strip()      # Espaces parasites dans les valeurs
joueurs["poste"]       = joueurs["poste"].str.strip()
joueurs["nationalite"] = joueurs["nationalite"].str.strip()
joueurs["recrue_2024"] = joueurs["recrue_2024"].astype(bool)

# Cast colonnes entières
for col in ["age", "matchs_joues", "buts", "passes_decisives"]:
    joueurs[col] = pd.to_numeric(joueurs[col], errors="coerce").fillna(0).astype(int)

# Cast colonnes flottantes
for col in ["note_moyenne", "valeur_marche_M€", "salaire_mensuel_M€", "prix_achat_M€"]:
    joueurs[col] = pd.to_numeric(joueurs[col], errors="coerce").fillna(0.0)

# Supprimer les doublons sur la clé métier
joueurs = joueurs.drop_duplicates(subset=["joueur"]).reset_index(drop=True)

# ── MATCHS ────────────────────────────────────────────────────────────────────
matchs.columns      = matchs.columns.str.strip()
matchs["competition"] = matchs["competition"].str.strip()
matchs["adversaire"]  = matchs["adversaire"].str.strip()
matchs["resultat"]    = matchs["resultat"].str.strip()
matchs["domicile"]    = matchs["domicile"].astype(bool)

for col in ["buts_rm", "buts_adv"]:
    matchs[col] = pd.to_numeric(matchs[col], errors="coerce").fillna(0).astype(int)

matchs = matchs.drop_duplicates().reset_index(drop=True)

# ── FINANCES ──────────────────────────────────────────────────────────────────
finances.columns = finances.columns.str.strip()
finances["mois"] = finances["mois"].str.strip()

for col in [c for c in finances.columns if c != "mois"]:
    finances[col] = pd.to_numeric(finances[col], errors="coerce").fillna(0.0)

finances = finances.drop_duplicates(subset=["mois"]).reset_index(drop=True)

# ── TITRES ────────────────────────────────────────────────────────────────────
titres.columns = titres.columns.str.strip()
titres["competition"]     = titres["competition"].str.strip()
titres["points_ou_etape"] = titres["points_ou_etape"].str.strip()
titres["gagne"]           = titres["gagne"].astype(bool)
titres["rang_final"]      = pd.to_numeric(titres["rang_final"], errors="coerce").fillna(0).astype(int)

titres = titres.drop_duplicates(subset=["competition"]).reset_index(drop=True)

# ── Vérification finale après nettoyage ───────────────────────────────────────
print("\n" + "=" * 60)
print("VÉRIFICATION FINALE APRÈS NETTOYAGE")
print("=" * 60)
for nom, df in [("joueurs", joueurs), ("matchs", matchs), ("finances", finances), ("titres", titres)]:
    print(f"{nom:10s} | shape={df.shape} | nulls={df.isnull().sum().sum()} | doublons={df.duplicated().sum()}")

# =============================================================================
# BARRE LATÉRALE – Navigation
# =============================================================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    width=100,
)
st.sidebar.title("⚽ Real Madrid 2024")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Vue d'ensemble",
        "📊 Performances Équipe",
        "👤 Performances Joueurs",
        "💰 Stratégie Financière",
        "🔄 Mercato",
        "🌍 Géographie",
        "🔗 Corrélations",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard réalisé avec Streamlit · Données réalistes")

# =============================================================================
# PAGE 1 – VUE D'ENSEMBLE
# =============================================================================

#Voici la page de vue d'ensemble 

#yassine bouali // mohamed arbi sliti

#le grand chelem sportif 

if page == "🏠 Vue d'ensemble":

    st.title("🏆 Real Madrid CF – Saison 2024")
    st.markdown("##### Tableau de bord analytique pour l'administration du club")
    st.markdown("---")

    # ── KPIs principaux ───────────────────────────────────────────────────────
    col1, col2, col3, col4, col5 = st.columns(5)

    victoires   = (matchs["resultat"] == "Victoire").sum()
    nuls        = (matchs["resultat"] == "Nul").sum()
    defaites    = (matchs["resultat"] == "Défaite").sum()
    total_buts  = matchs["buts_rm"].sum()
    titres_won  = titres["gagne"].sum()

    col1.metric("🏅 Titres remportés",   f"{titres_won} / {len(titres)}")
    col2.metric("✅ Victoires",          f"{victoires} / {len(matchs)}")
    col3.metric("➖ Nuls",              str(nuls))
    col4.metric("❌ Défaites",          str(defaites))
    col5.metric("⚽ Buts marqués",      str(total_buts))

    st.markdown("---")

    # ── Palmares ──────────────────────────────────────────────────────────────
    st.subheader("🏆 Palmarès de la saison")
    df_titres_display = titres.copy()
    df_titres_display["Statut"] = df_titres_display["gagne"].map({True: "✅ Gagné", False: "🥈 Finaliste"})
    st.dataframe(
        df_titres_display[["competition","Statut","points_ou_etape"]].rename(columns={
            "competition": "Compétition",
            "points_ou_etape": "Résultat"
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # ── Résultats par compétition (donut chart) ───────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📈 Répartition des résultats")
        res_counts = matchs["resultat"].value_counts().reset_index()
        res_counts.columns = ["Résultat", "Nombre"]
        fig_donut = px.pie(
            res_counts, names="Résultat", values="Nombre",
            hole=0.45,
            color_discrete_map={"Victoire": GOLD, "Nul": "#8899aa", "Défaite": "#cc3333"},
            template="plotly_dark",
        )
        fig_donut.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_b:
        st.subheader("🏟️ Buts par compétition")
        buts_comp = matchs.groupby("competition")[["buts_rm","buts_adv"]].sum().reset_index()
        fig_bar = px.bar(
            buts_comp, x="competition", y=["buts_rm","buts_adv"],
            barmode="group",
            labels={"value": "Buts", "competition": "Compétition", "variable": ""},
            color_discrete_map={"buts_rm": GOLD, "buts_adv": "#cc3333"},
            template="plotly_dark",
        )
        fig_bar.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
        st.plotly_chart(fig_bar, use_container_width=True)

# =============================================================================
# PAGE 2 – PERFORMANCES ÉQUIPE
# =============================================================================

elif page == "📊 Performances Équipe":

    st.title("📊 Performances de l'Équipe")
    st.markdown("---")

    # ── Filtre compétition ────────────────────────────────────────────────────
    comps = ["Toutes"] + sorted(matchs["competition"].unique().tolist())
    comp_sel = st.selectbox("Filtrer par compétition", comps)

    df_m = matchs if comp_sel == "Toutes" else matchs[matchs["competition"] == comp_sel]

    # ── Métriques rapides ─────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Matchs joués",   len(df_m))
    c2.metric("Victoires",      (df_m["resultat"] == "Victoire").sum())
    c3.metric("Buts marqués",   df_m["buts_rm"].sum())
    c4.metric("Buts encaissés", df_m["buts_adv"].sum())

    st.markdown("---")

    # ── Évolution cumulée des buts ────────────────────────────────────────────
    st.subheader("📈 Évolution cumulative des buts")
    df_m_reset = df_m.reset_index(drop=True)
    df_m_reset["match_n"]      = df_m_reset.index + 1
    df_m_reset["buts_cum"]     = df_m_reset["buts_rm"].cumsum()
    df_m_reset["encaissés_cum"] = df_m_reset["buts_adv"].cumsum()

    fig_line = px.line(
        df_m_reset, x="match_n", y=["buts_cum","encaissés_cum"],
        labels={"match_n": "Numéro du match", "value": "Buts cumulés", "variable": ""},
        color_discrete_map={"buts_cum": GOLD, "encaissés_cum": "#cc3333"},
        template="plotly_dark",
    )
    fig_line.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_line, use_container_width=True)

    # ── Domicile vs Extérieur ─────────────────────────────────────────────────
    st.subheader("🏠 Domicile vs 🚌 Extérieur")
    df_m["lieu"] = df_m["domicile"].map({True: "Domicile", False: "Extérieur"})
    dom_res = df_m.groupby(["lieu","resultat"]).size().reset_index(name="count")

    fig_dom = px.bar(
        dom_res, x="lieu", y="count", color="resultat", barmode="stack",
        color_discrete_map={"Victoire": GOLD, "Nul": "#8899aa", "Défaite": "#cc3333"},
        template="plotly_dark",
        labels={"lieu": "", "count": "Nombre de matchs"},
    )
    fig_dom.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_dom, use_container_width=True)

    # ── Heatmap adversaires (La Liga) ─────────────────────────────────────────
    st.subheader("🔥 Heatmap des scores (La Liga)")
    liga = matchs[matchs["competition"] == "La Liga"].copy()
    liga_pivot = liga.groupby("adversaire")[["buts_rm","buts_adv"]].mean().round(2)

    fig_hm, ax = plt.subplots(figsize=(10, 7))
    fig_hm.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    sns.heatmap(
        liga_pivot, annot=True, fmt=".1f", cmap="YlOrRd",
        ax=ax, cbar_kws={"shrink": 0.8},
        linewidths=0.5, linecolor="#333",
    )
    ax.set_title("Buts moyens par adversaire (La Liga)", color=GOLD, fontsize=13)
    ax.tick_params(colors=WHITE)
    ax.set_xlabel("", color=WHITE)
    ax.set_ylabel("Adversaire", color=WHITE)
    plt.tight_layout()
    st.pyplot(fig_hm)

# =============================================================================
# PAGE 3 – PERFORMANCES JOUEURS
# =============================================================================

elif page == "👤 Performances Joueurs":

    st.title("👤 Performances Individuelles")
    st.markdown("---")

    # ── Filtres ───────────────────────────────────────────────────────────────
    postes_list = ["Tous"] + sorted(joueurs["poste"].unique().tolist())
    poste_sel = st.selectbox("Filtrer par poste", postes_list)
    df_j = joueurs if poste_sel == "Tous" else joueurs[joueurs["poste"] == poste_sel]

    # ── Tableau joueurs ───────────────────────────────────────────────────────
    st.subheader("📋 Tableau des joueurs")
    cols_display = ["joueur","poste","nationalite","age","matchs_joues",
                    "buts","passes_decisives","note_moyenne","valeur_marche_M€"]
    st.dataframe(
        df_j[cols_display].sort_values("note_moyenne", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # ── Top buteurs ───────────────────────────────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("⚽ Top Buteurs")
        top_but = df_j.nlargest(8, "buts")
        fig_but = px.bar(
            top_but, x="buts", y="joueur", orientation="h",
            color="buts", color_continuous_scale=[[0, "#333"], [1, GOLD]],
            template="plotly_dark",
            labels={"buts": "Buts", "joueur": ""},
        )
        fig_but.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK,
                               font_color=WHITE, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_but, use_container_width=True)

    with col_b:
        st.subheader("🎯 Top Passeurs")
        top_pas = df_j.nlargest(8, "passes_decisives")
        fig_pas = px.bar(
            top_pas, x="passes_decisives", y="joueur", orientation="h",
            color="passes_decisives", color_continuous_scale=[[0, "#333"], [1, "#4fc3f7"]],
            template="plotly_dark",
            labels={"passes_decisives": "Passes D.", "joueur": ""},
        )
        fig_pas.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK,
                               font_color=WHITE, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_pas, use_container_width=True)

    st.markdown("---")

    # ── Radar chart – comparaison deux joueurs ────────────────────────────────
    st.subheader("🕸️ Radar – Comparaison de deux joueurs")

    col1, col2 = st.columns(2)
    j1 = col1.selectbox("Joueur 1", joueurs["joueur"].tolist(), index=15)  # Vinícius
    j2 = col2.selectbox("Joueur 2", joueurs["joueur"].tolist(), index=14)  # Bellingham

    categories = ["buts","passes_decisives","note_moyenne","matchs_joues","valeur_marche_M€"]
    labels_rad  = ["Buts","Passes D.","Note","Matchs","Valeur M€"]

    def get_radar_values(nom):
        row = joueurs[joueurs["joueur"] == nom].iloc[0]
        raw = [row[c] for c in categories]
        # normalisation 0-10
        maxs = [joueurs[c].max() for c in categories]
        return [round(v / m * 10, 2) if m > 0 else 0 for v, m in zip(raw, maxs)]

    vals1 = get_radar_values(j1)
    vals2 = get_radar_values(j2)

    # Construction du radar avec matplotlib
    N = len(labels_rad)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    v1 = vals1 + vals1[:1]
    v2 = vals2 + vals2[:1]

    fig_radar, ax_r = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig_radar.patch.set_facecolor(DARK)
    ax_r.set_facecolor(DARK)
    ax_r.plot(angles, v1, "o-", linewidth=2, color=GOLD,   label=j1)
    ax_r.fill(angles, v1, alpha=0.25, color=GOLD)
    ax_r.plot(angles, v2, "o-", linewidth=2, color="#4fc3f7", label=j2)
    ax_r.fill(angles, v2, alpha=0.25, color="#4fc3f7")
    ax_r.set_xticks(angles[:-1])
    ax_r.set_xticklabels(labels_rad, color=WHITE, fontsize=10)
    ax_r.yaxis.set_tick_params(labelcolor=WHITE)
    ax_r.set_ylim(0, 10)
    ax_r.tick_params(colors=WHITE)
    ax_r.spines["polar"].set_color("#444")
    ax_r.grid(color="#444")
    ax_r.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1),
                 labelcolor=WHITE, facecolor=DARK, edgecolor=GOLD)
    st.pyplot(fig_radar)

    st.markdown("---")

    # ── Scatter Buts vs Note ──────────────────────────────────────────────────
    st.subheader("📊 Buts vs Note Moyenne (par poste)")
    fig_sc = px.scatter(
        joueurs, x="buts", y="note_moyenne", color="poste",
        size="valeur_marche_M€", hover_name="joueur",
        size_max=40, template="plotly_dark",
        labels={"buts": "Buts", "note_moyenne": "Note Moyenne"},
    )
    fig_sc.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_sc, use_container_width=True)

# =============================================================================
# PAGE 4 – STRATÉGIE FINANCIÈRE
# =============================================================================

elif page == "💰 Stratégie Financière":

    st.title("💰 Stratégie Financière – 2024")
    st.markdown("---")

    # ── KPIs financiers ───────────────────────────────────────────────────────
    total_rev  = finances[[c for c in finances.columns if "revenus" in c]].sum().sum()
    total_dep  = finances[[c for c in finances.columns if "depenses" in c]].sum().sum()
    benefice   = finances["benefice_net_M€"].sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 Revenus totaux",   f"{total_rev:.1f} M€")
    c2.metric("💸 Dépenses totales", f"{total_dep:.1f} M€")
    delta_col = "normal" if benefice > 0 else "inverse"
    c3.metric("📈 Bénéfice net",     f"{benefice:.1f} M€", delta=f"{benefice:.1f} M€", delta_color=delta_col)

    st.markdown("---")

    # ── Évolution mensuelle revenus vs dépenses ───────────────────────────────
    st.subheader("📅 Revenus vs Dépenses par mois")

    finances["total_revenus"] = finances[[c for c in finances.columns if "revenus" in c]].sum(axis=1)
    finances["total_depenses"] = finances[[c for c in finances.columns if "depenses" in c]].sum(axis=1)

    fig_fin = go.Figure()
    fig_fin.add_trace(go.Bar(name="Revenus",   x=finances["mois"], y=finances["total_revenus"],  marker_color=GOLD))
    fig_fin.add_trace(go.Bar(name="Dépenses",  x=finances["mois"], y=finances["total_depenses"], marker_color="#cc3333"))
    fig_fin.add_trace(go.Scatter(name="Bénéfice net", x=finances["mois"], y=finances["benefice_net_M€"],
                                  mode="lines+markers", line=dict(color="#4fc3f7", width=2), marker=dict(size=7)))
    fig_fin.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE,
        yaxis_title="Millions €", xaxis_title="Mois",
    )
    st.plotly_chart(fig_fin, use_container_width=True)

    # ── Répartition des revenus (camembert) ───────────────────────────────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🥧 Sources de revenus")
        rev_cols = [c for c in finances.columns if "revenus" in c and c != "total_revenus"]
        rev_totals = finances[rev_cols].sum()
        fig_pie = px.pie(
            names=rev_totals.index.str.replace("revenus_","").str.replace("_M€","").str.replace("_"," "),
            values=rev_totals.values,
            color_discrete_sequence=[GOLD, "#e6c97a", "#4fc3f7", "#a5d6a7"],
            template="plotly_dark",
            hole=0.35,
        )
        fig_pie.update_layout(paper_bgcolor=DARK, font_color=WHITE)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("📤 Répartition des dépenses")
        dep_cols = [c for c in finances.columns if "depenses" in c and c != "total_depenses"]
        dep_totals = finances[dep_cols].sum()
        fig_dep = px.pie(
            names=dep_totals.index.str.replace("depenses_","").str.replace("_M€","").str.replace("_"," "),
            values=dep_totals.values,
            color_discrete_sequence=["#cc3333", "#ff7777", "#ff9999"],
            template="plotly_dark",
            hole=0.35,
        )
        fig_dep.update_layout(paper_bgcolor=DARK, font_color=WHITE)
        st.plotly_chart(fig_dep, use_container_width=True)

    # ── Masse salariale par poste ─────────────────────────────────────────────
    st.subheader("👥 Masse salariale par poste")
    sal_poste = joueurs.groupby("poste")["salaire_mensuel_M€"].sum().reset_index()
    sal_poste["annuel_M€"] = sal_poste["salaire_mensuel_M€"] * 12

    fig_sal = px.bar(
        sal_poste, x="poste", y="annuel_M€", color="poste",
        template="plotly_dark",
        labels={"annuel_M€": "Salaires annuels (M€)", "poste": "Poste"},
        color_discrete_sequence=[GOLD, "#4fc3f7", "#a5d6a7", "#ff9966"],
    )
    fig_sal.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK,
                           font_color=WHITE, showlegend=False)
    st.plotly_chart(fig_sal, use_container_width=True)

# =============================================================================
# PAGE 5 – MERCATO
# =============================================================================

elif page == "🔄 Mercato":

    st.title("🔄 Analyse Mercato – Été 2024")
    st.markdown("---")

    recrues = joueurs[joueurs["recrue_2024"] == True].copy()
    recrues["contribution_totale"] = recrues["buts"] + recrues["passes_decisives"]
    recrues["cout_par_but_M€"] = (
        recrues["prix_achat_M€"] / recrues["buts"].replace(0, np.nan)
    ).round(2)

    # ── Tableau recrues ───────────────────────────────────────────────────────
    st.subheader("🆕 Joueurs recrutés")
    st.dataframe(
        recrues[["joueur","poste","nationalite","age","prix_achat_M€",
                  "matchs_joues","buts","passes_decisives","note_moyenne",
                  "valeur_marche_M€","cout_par_but_M€"]]
              .sort_values("note_moyenne", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # ── Performance vs coût ───────────────────────────────────────────────────
    st.subheader("📊 Performance vs Coût d'acquisition")

    fig_mv = px.scatter(
        recrues, x="prix_achat_M€", y="note_moyenne",
        size="contribution_totale", color="poste",
        hover_name="joueur", size_max=50,
        template="plotly_dark",
        labels={"prix_achat_M€": "Prix d'achat (M€)", "note_moyenne": "Note moyenne"},
        text="joueur",
    )
    fig_mv.update_traces(textposition="top center", textfont_color=WHITE, textfont_size=10)
    fig_mv.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_mv, use_container_width=True)

    # ── Évolution valeur marchande ────────────────────────────────────────────
    st.subheader("📈 ROI potentiel – Valeur marchande vs Prix d'achat")

    recrues["plus_value_M€"] = recrues["valeur_marche_M€"] - recrues["prix_achat_M€"]

    fig_roi = go.Figure()
    fig_roi.add_trace(go.Bar(
        name="Prix d'achat", x=recrues["joueur"], y=recrues["prix_achat_M€"],
        marker_color="#cc3333",
    ))
    fig_roi.add_trace(go.Bar(
        name="Valeur actuelle", x=recrues["joueur"], y=recrues["valeur_marche_M€"],
        marker_color=GOLD,
    ))
    fig_roi.add_trace(go.Scatter(
        name="Plus-value", x=recrues["joueur"], y=recrues["plus_value_M€"],
        mode="lines+markers", line=dict(color="#4fc3f7", width=2), marker=dict(size=8),
    ))
    fig_roi.update_layout(
        barmode="group", template="plotly_dark",
        paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE,
        yaxis_title="Millions €", xaxis_title="Joueur",
        xaxis_tickangle=-30,
    )
    st.plotly_chart(fig_roi, use_container_width=True)

    # ── Contribution recrues vs anciens ──────────────────────────────────────
    st.subheader("🆚 Contribution recrues vs joueurs en place")

    anciens = joueurs[joueurs["recrue_2024"] == False].copy()
    anciens["contribution"] = anciens["buts"] + anciens["passes_decisives"]
    recrues["contribution"]  = recrues["buts"] + recrues["passes_decisives"]

    comp_data = pd.DataFrame({
        "Groupe":        ["Recrues 2024", "Joueurs en place"],
        "Buts":          [recrues["buts"].sum(),     anciens["buts"].sum()],
        "Passes D.":     [recrues["passes_decisives"].sum(), anciens["passes_decisives"].sum()],
        "Note moy.":     [recrues["note_moyenne"].mean().round(2), anciens["note_moyenne"].mean().round(2)],
    })

    fig_comp = px.bar(
        comp_data.melt(id_vars="Groupe", var_name="Métrique", value_name="Valeur"),
        x="Métrique", y="Valeur", color="Groupe", barmode="group",
        color_discrete_map={"Recrues 2024": GOLD, "Joueurs en place": "#4fc3f7"},
        template="plotly_dark",
    )
    fig_comp.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_comp, use_container_width=True)

# =============================================================================
# PAGE 6 – GÉOGRAPHIE
# =============================================================================

elif page == "🌍 Géographie":

    st.title("🌍 Visualisation Géographique")
    st.markdown("##### Répartition mondiale des joueurs et des adversaires")
    st.markdown("---")

    # ── Coordonnées pays des joueurs ──────────────────────────────────────────
    # Dictionnaire : nationalité → (latitude, longitude, pays ISO)
    pays_coords = {
        "Belgique":   (50.85, 4.35,  "BEL"),
        "Ukraine":    (50.45, 30.52, "UKR"),
        "Espagne":    (40.42, -3.70, "ESP"),
        "Brésil":     (-15.78, -47.93, "BRA"),
        "Allemagne":  (52.52, 13.40, "DEU"),
        "France":     (48.85, 2.35,  "FRA"),
        "Autriche":   (48.21, 16.37, "AUT"),
        "Croatie":    (45.81, 15.98, "HRV"),
        "Uruguay":    (-34.90, -56.19, "URY"),
        "Angleterre": (51.51, -0.13, "GBR"),
    }

    # Enrichissement du dataframe joueurs
    df_geo = joueurs.copy()
    df_geo["lat"]      = df_geo["nationalite"].map(lambda n: pays_coords.get(n, (0,0,""))[0])
    df_geo["lon"]      = df_geo["nationalite"].map(lambda n: pays_coords.get(n, (0,0,""))[1])
    df_geo["iso"]      = df_geo["nationalite"].map(lambda n: pays_coords.get(n, (0,0,""))[2])
    df_geo["contribution"] = df_geo["buts"] + df_geo["passes_decisives"]

    # ── Carte bubble – joueurs par pays ──────────────────────────────────────
    st.subheader("🗺️ Carte des joueurs par nationalité")

    # Agréger par pays
    df_pays = (
        df_geo.groupby(["nationalite","lat","lon","iso"])
        .agg(nb_joueurs=("joueur","count"),
             buts_total=("buts","sum"),
             note_moy=("note_moyenne","mean"),
             joueurs_list=("joueur", lambda x: ", ".join(x)))
        .reset_index()
    )
    df_pays["note_moy"] = df_pays["note_moy"].round(2)

    fig_map = px.scatter_geo(
        df_pays,
        lat="lat", lon="lon",
        size="nb_joueurs",
        color="note_moy",
        hover_name="nationalite",
        hover_data={"joueurs_list": True, "buts_total": True,
                    "note_moy": True, "lat": False, "lon": False},
        size_max=45,
        color_continuous_scale=[[0, "#1a1a2e"], [0.5, "#C8A84B"], [1, "#ffffff"]],
        projection="natural earth",
        template="plotly_dark",
        title="Taille = Nb joueurs · Couleur = Note moyenne",
        labels={"note_moy": "Note moy.", "joueurs_list": "Joueurs", "buts_total": "Buts totaux"},
    )
    fig_map.update_geos(
        bgcolor=DARK,
        landcolor="#2a2a4a",
        oceancolor="#0d0d1a",
        showocean=True,
        lakecolor="#0d0d1a",
        showlakes=True,
        showcountries=True,
        countrycolor="#444",
        showcoastlines=True,
        coastlinecolor="#555",
    )
    fig_map.update_layout(
        paper_bgcolor=DARK, font_color=WHITE,
        geo=dict(bgcolor=DARK),
        coloraxis_colorbar=dict(title="Note", tickfont=dict(color=WHITE), title_font=dict(color=WHITE)),
        height=520,
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # ── Choroplèthe – valeur marchande totale par pays ────────────────────────
    st.subheader("🌐 Valeur marchande totale par pays (choroplèthe)")

    df_choro = df_geo.groupby(["nationalite","iso"])["valeur_marche_M€"].sum().reset_index()

    fig_choro = px.choropleth(
        df_choro,
        locations="iso",
        color="valeur_marche_M€",
        hover_name="nationalite",
        color_continuous_scale=[[0, "#1a1a2e"], [0.4, "#7a5c1e"], [1, GOLD]],
        projection="natural earth",
        template="plotly_dark",
        labels={"valeur_marche_M€": "Valeur (M€)"},
        title="Valeur marchande totale des joueurs du Real Madrid par pays d'origine",
    )
    fig_choro.update_geos(
        bgcolor=DARK,
        landcolor="#2a2a4a",
        oceancolor="#0d0d1a",
        showocean=True,
        showcountries=True,
        countrycolor="#555",
    )
    fig_choro.update_layout(
        paper_bgcolor=DARK, font_color=WHITE,
        coloraxis_colorbar=dict(title="M€", tickfont=dict(color=WHITE), title_font=dict(color=WHITE)),
        height=480,
    )
    st.plotly_chart(fig_choro, use_container_width=True)

    st.markdown("---")

    # ── Villes des adversaires UCL ────────────────────────────────────────────
    st.subheader("✈️ Villes des adversaires – Champions League 2024")

    # Coordonnées des clubs adversaires UCL
    ucl_villes = {
        "Union Berlin":       (52.45, 13.57, "Berlin, Allemagne"),
        "Napoli":             (40.83, 14.26, "Naples, Italie"),
        "Braga":              (41.56, -8.43, "Braga, Portugal"),
        "RB Leipzig":         (51.34, 12.35, "Leipzig, Allemagne"),
        "Man City":           (53.48, -2.20, "Manchester, Angleterre"),
        "Bayern Munich":      (48.22,  11.62, "Munich, Allemagne"),
        "Borussia Dortmund":  (51.49,  7.45, "Dortmund, Allemagne"),
    }

    ucl_df = pd.DataFrame([
        {"club": k, "lat": v[0], "lon": v[1], "ville": v[2]}
        for k, v in ucl_villes.items()
    ])
    # Ajouter Real Madrid comme point de référence
    ucl_df = pd.concat([ucl_df, pd.DataFrame([{
        "club": "Real Madrid (Madrid)", "lat": 40.45, "lon": -3.69, "ville": "Madrid, Espagne"
    }])], ignore_index=True)
    ucl_df["couleur"] = ucl_df["club"].apply(lambda x: "Real Madrid" if "Real" in x else "Adversaire")

    fig_ucl = px.scatter_geo(
        ucl_df, lat="lat", lon="lon",
        text="club", hover_name="ville",
        color="couleur",
        color_discrete_map={"Real Madrid": GOLD, "Adversaire": "#cc3333"},
        projection="natural earth",
        template="plotly_dark",
        title="Villes des clubs affrontés en Champions League",
    )
    fig_ucl.update_traces(textposition="top center", textfont_size=10)
    fig_ucl.update_geos(
        scope="europe",
        bgcolor=DARK,
        landcolor="#2a2a4a",
        oceancolor="#0d0d1a",
        showocean=True,
        showcountries=True,
        countrycolor="#555",
    )
    fig_ucl.update_layout(
        paper_bgcolor=DARK, font_color=WHITE,
        height=480,
        legend=dict(font=dict(color=WHITE), bgcolor=DARK),
    )
    st.plotly_chart(fig_ucl, use_container_width=True)

    st.markdown("---")

    # ── Statistiques par continent ────────────────────────────────────────────
    st.subheader("🌎 Statistiques par continent")

    continent_map = {
        "Belgique": "Europe", "Ukraine": "Europe", "Espagne": "Europe",
        "Allemagne": "Europe", "France": "Europe", "Autriche": "Europe",
        "Croatie": "Europe", "Angleterre": "Europe",
        "Brésil": "Amérique du Sud", "Uruguay": "Amérique du Sud",
    }
    df_geo["continent"] = df_geo["nationalite"].map(continent_map)
    cont_stats = df_geo.groupby("continent").agg(
        nb_joueurs=("joueur","count"),
        buts=("buts","sum"),
        passes=("passes_decisives","sum"),
        note_moy=("note_moyenne","mean"),
    ).reset_index()
    cont_stats["note_moy"] = cont_stats["note_moy"].round(2)

    fig_cont = px.bar(
        cont_stats, x="continent", y=["buts","passes","nb_joueurs"],
        barmode="group", template="plotly_dark",
        color_discrete_sequence=[GOLD, "#4fc3f7", "#a5d6a7"],
        labels={"value": "Total", "continent": "Continent", "variable": "Métrique"},
        title="Contribution par continent",
    )
    fig_cont.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
    st.plotly_chart(fig_cont, use_container_width=True)

# =============================================================================
# PAGE 7 – CORRÉLATIONS
# =============================================================================

elif page == "🔗 Corrélations":

    st.title("🔗 Matrices de Corrélations")
    st.markdown("##### Analyse des relations statistiques entre variables clés")
    st.markdown("---")

    # ── Sélection du dataset ──────────────────────────────────────────────────
    dataset_choix = st.radio(
        "Choisir le dataset à analyser",
        ["Joueurs", "Finances"],
        horizontal=True,
    )

    st.markdown("---")

    if dataset_choix == "Joueurs":

        # ── Corrélation – variables joueurs ───────────────────────────────────
        st.subheader("👤 Matrice de corrélation – Joueurs")

        cols_corr = ["age", "matchs_joues", "buts", "passes_decisives",
                     "note_moyenne", "valeur_marche_M€", "salaire_mensuel_M€", "prix_achat_M€"]
        labels_fr = {
            "age": "Âge",
            "matchs_joues": "Matchs joués",
            "buts": "Buts",
            "passes_decisives": "Passes D.",
            "note_moyenne": "Note moy.",
            "valeur_marche_M€": "Valeur M€",
            "salaire_mensuel_M€": "Salaire M€",
            "prix_achat_M€": "Prix achat M€",
        }
        df_corr = joueurs[cols_corr].rename(columns=labels_fr)
        corr_matrix = df_corr.corr()

        # Heatmap seaborn
        fig_corr, ax_c = plt.subplots(figsize=(10, 8))
        fig_corr.patch.set_facecolor(DARK)
        ax_c.set_facecolor(DARK)
        mask = np.zeros_like(corr_matrix, dtype=bool)
        # Pas de masque – on affiche la matrice complète
        sns.heatmap(
            corr_matrix,
            annot=True, fmt=".2f",
            cmap="coolwarm",
            center=0, vmin=-1, vmax=1,
            ax=ax_c,
            linewidths=0.5, linecolor="#222",
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 9, "color": WHITE},
        )
        ax_c.set_title("Corrélations – Variables Joueurs", color=GOLD, fontsize=14, pad=15)
        ax_c.tick_params(colors=WHITE, labelsize=9)
        ax_c.set_xticklabels(ax_c.get_xticklabels(), rotation=35, ha="right", color=WHITE)
        ax_c.set_yticklabels(ax_c.get_yticklabels(), rotation=0, color=WHITE)
        plt.tight_layout()
        st.pyplot(fig_corr)

        st.markdown("---")

        # ── Interprétation automatique ────────────────────────────────────────
        st.subheader("💡 Corrélations les plus significatives")

        # Extraire les paires (triangle supérieur)
        pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                r = corr_matrix.iloc[i, j]
                pairs.append({
                    "Variable 1": corr_matrix.columns[i],
                    "Variable 2": corr_matrix.columns[j],
                    "Corrélation r": round(r, 3),
                    "Force": (
                        "🔴 Forte positive"   if r >= 0.6  else
                        "🟠 Modérée positive" if r >= 0.3  else
                        "🔵 Forte négative"   if r <= -0.6 else
                        "🟣 Modérée négative" if r <= -0.3 else
                        "⚪ Faible"
                    ),
                })
        df_pairs = pd.DataFrame(pairs).sort_values("Corrélation r", key=abs, ascending=False)
        st.dataframe(df_pairs.head(10), use_container_width=True, hide_index=True)

        st.markdown("---")

        # ── Scatter matrix (pair plot) ────────────────────────────────────────
        st.subheader("📐 Scatter Matrix – Variables clés")

        cols_scatter = ["buts", "passes_decisives", "note_moyenne",
                        "valeur_marche_M€", "salaire_mensuel_M€"]
        fig_scat = px.scatter_matrix(
            joueurs,
            dimensions=cols_scatter,
            color="poste",
            hover_name="joueur",
            template="plotly_dark",
            labels={c: c.replace("_"," ").replace("M€","(M€)") for c in cols_scatter},
            title="Scatter Matrix – Relations entre variables joueurs",
        )
        fig_scat.update_traces(diagonal_visible=True, marker=dict(size=5, opacity=0.8))
        fig_scat.update_layout(
            paper_bgcolor=DARK, plot_bgcolor=DARK,
            font_color=WHITE, height=650,
        )
        st.plotly_chart(fig_scat, use_container_width=True)

        st.markdown("---")

        # ── Corrélation par poste ─────────────────────────────────────────────
        st.subheader("🔍 Corrélation Buts / Note – par poste")

        fig_pos = px.scatter(
            joueurs, x="buts", y="note_moyenne",
            color="poste",
            hover_name="joueur",
            template="plotly_dark",
            labels={"buts": "Buts", "note_moyenne": "Note Moyenne", "poste": "Poste"},
            title="Tendance linéaire Buts → Note par poste",
        )
        # Droite de tendance globale calculée manuellement (sans statsmodels)
        x_vals = joueurs["buts"].values
        y_vals = joueurs["note_moyenne"].values
        m, b = np.polyfit(x_vals, y_vals, 1)
        x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
        y_line = m * x_line + b
        fig_pos.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines", name="Tendance globale",
            line=dict(color=GOLD, width=2, dash="dash"),
        ))
        fig_pos.update_layout(paper_bgcolor=DARK, plot_bgcolor=DARK, font_color=WHITE)
        st.plotly_chart(fig_pos, use_container_width=True)

    else:  # Finances

        # ── Corrélation – variables financières ───────────────────────────────
        st.subheader("💰 Matrice de corrélation – Finances mensuelles")

        fin_cols = [
            "revenus_matchday_M€", "revenus_droits_tv_M€",
            "revenus_sponsoring_M€", "revenus_ventes_joueurs_M€",
            "depenses_salaires_M€", "depenses_transferts_M€",
            "depenses_infrastructure_M€", "benefice_net_M€",
        ]
        labels_fin = {
            "revenus_matchday_M€":        "Rev. Matchday",
            "revenus_droits_tv_M€":       "Rev. TV",
            "revenus_sponsoring_M€":      "Rev. Sponsoring",
            "revenus_ventes_joueurs_M€":  "Ventes joueurs",
            "depenses_salaires_M€":       "Dép. Salaires",
            "depenses_transferts_M€":     "Dép. Transferts",
            "depenses_infrastructure_M€": "Dép. Infra",
            "benefice_net_M€":            "Bénéfice net",
        }
        df_fin_corr = finances[fin_cols].rename(columns=labels_fin)
        corr_fin = df_fin_corr.corr()

        fig_fc, ax_f = plt.subplots(figsize=(10, 8))
        fig_fc.patch.set_facecolor(DARK)
        ax_f.set_facecolor(DARK)
        sns.heatmap(
            corr_fin,
            annot=True, fmt=".2f",
            cmap="RdYlGn",
            center=0, vmin=-1, vmax=1,
            ax=ax_f,
            linewidths=0.5, linecolor="#222",
            cbar_kws={"shrink": 0.8},
            annot_kws={"size": 9, "color": "black"},
        )
        ax_f.set_title("Corrélations – Variables Financières", color=GOLD, fontsize=14, pad=15)
        ax_f.tick_params(colors=WHITE, labelsize=9)
        ax_f.set_xticklabels(ax_f.get_xticklabels(), rotation=35, ha="right", color=WHITE)
        ax_f.set_yticklabels(ax_f.get_yticklabels(), rotation=0, color=WHITE)
        plt.tight_layout()
        st.pyplot(fig_fc)

        st.markdown("---")

        # ── Corrélations significatives ───────────────────────────────────────
        st.subheader("💡 Corrélations les plus significatives")

        pairs_fin = []
        for i in range(len(corr_fin.columns)):
            for j in range(i+1, len(corr_fin.columns)):
                r = corr_fin.iloc[i, j]
                pairs_fin.append({
                    "Variable 1": corr_fin.columns[i],
                    "Variable 2": corr_fin.columns[j],
                    "Corrélation r": round(r, 3),
                    "Force": (
                        "🔴 Forte positive"   if r >= 0.6  else
                        "🟠 Modérée positive" if r >= 0.3  else
                        "🔵 Forte négative"   if r <= -0.6 else
                        "🟣 Modérée négative" if r <= -0.3 else
                        "⚪ Faible"
                    ),
                })
        df_pf = pd.DataFrame(pairs_fin).sort_values("Corrélation r", key=abs, ascending=False)
        st.dataframe(df_pf.head(10), use_container_width=True, hide_index=True)

