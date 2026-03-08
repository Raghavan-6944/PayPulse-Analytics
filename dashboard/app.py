import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="PAY pulse ANALYTICS | Explore Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Dark Theme
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #140c31 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #1a1245; }
::-webkit-scrollbar-thumb { background: #5f4bbf; border-radius: 10px; }

/* ── Navbar ── */
.pulse-navbar {
    background: #1a1245;
    padding: 12px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.pulse-logo { display: flex; align-items: center; gap: 12px; }
.pulse-logo-icon {
    width: 40px; height: 40px; background: #6739b7;
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 14px; font-weight: 800; color: white;
}
.pulse-logo-text { font-size: 18px; font-weight: 700; color: white; }
.pulse-nav-links { display: flex; gap: 36px; align-items: center; }
.pulse-nav-link {
    color: rgba(255,255,255,0.6); font-size: 13px; font-weight: 600;
    letter-spacing: 1px; padding-bottom: 4px; cursor: pointer;
}
.pulse-nav-link.active { color: #ffd326; border-bottom: 2px solid #ffd326; }

/* ── Domain Toggle Pills ── */
.domain-toggle { display: flex; gap: 12px; padding: 14px 24px 0; }
.domain-pill {
    padding: 8px 22px; border-radius: 24px; font-size: 13px; font-weight: 600;
    cursor: pointer; border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.6);
}
.domain-pill.active { background: #6739b7; color: white; border-color: #6739b7; }

/* ── Location badge ── */
.location-badge {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
    color: white; padding: 8px 20px; border-radius: 24px; font-size: 14px; font-weight: 600;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 24px !important; color: white !important; font-size: 14px !important;
}
div[data-baseweb="select"] svg { fill: white !important; }
div[data-baseweb="popover"] { background: #1a1245 !important; }
li[role="option"]:hover { background: rgba(103,57,183,0.4) !important; }

/* ── Column layout ── */
[data-testid="stHorizontalBlock"] { align-items: flex-start !important; gap: 0 !important; }
[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    background: #1c1447 !important;
    border-left: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stHorizontalBlock"] > div:nth-child(1) { background: #140c31 !important; }
[data-testid="column"] { background: transparent !important; padding: 0 !important; }

/* ── Info panel elements ── */
.panel-title { font-size: 20px; font-weight: 700; color: #00d4e0; margin-bottom: 4px; }
.panel-subtitle { font-size: 12px; color: rgba(255,255,255,0.45); margin-bottom: 12px; }
.hero-metric {
    font-size: 32px; font-weight: 800; color: #00d4e0;
    letter-spacing: -1px; line-height: 1.1; margin: 4px 0 16px 0; word-break: break-all;
}
.sub-metrics { display: flex; gap: 32px; margin-bottom: 8px; flex-wrap: wrap; }
.sub-metric-label { font-size: 12px; color: rgba(255,255,255,0.55); margin-bottom: 4px; }
.sub-metric-value { font-size: 16px; font-weight: 700; color: #6ad4d8; }
.pulse-divider { height: 1px; background: rgba(255,255,255,0.08); margin: 16px 0; }
.cat-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 12px; }
.cat-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.cat-name { font-size: 13px; color: rgba(255,255,255,0.75); font-weight: 500; }
.cat-value { font-size: 14px; font-weight: 700; color: #00d4e0; }
.tab-row { display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }
.tab-btn {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
    color: rgba(255,255,255,0.7); padding: 6px 18px; border-radius: 20px;
    font-size: 12px; font-weight: 600; cursor: pointer;
}
.tab-btn.active { background: white; color: #140c31; border-color: white; }
.rank-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 12px; }
.rank-row {
    display: flex; align-items: center; gap: 12px; padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.rank-num { font-size: 13px; color: rgba(255,255,255,0.35); width: 20px; font-style: italic; }
.rank-name { font-size: 13px; font-weight: 600; color: white; flex: 1; }
.rank-value { font-size: 13px; font-weight: 700; color: #00d4e0; }
.explore-btn {
    display: inline-flex; align-items: center; gap: 8px; background: transparent;
    border: 1.5px solid rgba(255,255,255,0.5); color: white; padding: 10px 24px;
    border-radius: 30px; font-size: 12px; font-weight: 700; letter-spacing: 1.5px;
    margin-top: 12px; cursor: pointer;
}
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
.modebar { background: transparent !important; }
.modebar-btn path { fill: rgba(255,255,255,0.5) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────

st.markdown("""
<div class="pulse-navbar">
    <div class="pulse-logo">
        <div class="pulse-logo-icon">PP</div>
        <div><div class="pulse-logo-text">PAY pulse ANALYTICS</div></div>
    </div>
    <div class="pulse-nav-links">
        <span class="pulse-nav-link active">EXPLORE DATA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost", user="root",
        password="mysql123", database="phonepe_db"
    )

conn = get_connection()

# ─────────────────────────────────────────────
# LOAD GeoJSON
# ─────────────────────────────────────────────

@st.cache_data
def load_geojson():
    path = os.path.join(os.path.dirname(__file__), "india_state_geo.json")
    with open(path, "r") as f:
        return json.load(f)

india_geojson = load_geojson()
feat0_props = india_geojson["features"][0]["properties"]
GEO_ID_KEY = "ST_NM" if "ST_NM" in feat0_props else "NAME_1"

# ─────────────────────────────────────────────
# DOMAIN TOGGLE + YEAR/QUARTER FILTERS
# ─────────────────────────────────────────────

st.markdown('<div style="padding: 14px 24px 0px 24px;">', unsafe_allow_html=True)

domain_col, f1, f2, f3, spacer = st.columns([2.5, 1.2, 1, 1, 4])

with domain_col:
    domain = st.radio(
        "", ["Transactions", "Users"],
        horizontal=True, key="domain_sel",
        label_visibility="collapsed"
    )

with f1:
    st.markdown('<div class="location-badge">🇮🇳&nbsp; All India</div>', unsafe_allow_html=True)

with f2:
    year_df = pd.read_sql(
        "SELECT DISTINCT year FROM aggregated_transaction ORDER BY year", conn)
    year = st.selectbox("", year_df["year"], key="year_sel",
                        label_visibility="collapsed")

with f3:
    q_labels = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
    q_df = pd.read_sql(
        "SELECT DISTINCT quarter FROM aggregated_transaction ORDER BY quarter", conn)
    q_opts = q_df["quarter"].tolist()
    q_display = [q_labels.get(q, f"Q{q}") for q in q_opts]
    q_sel = st.selectbox("", q_display, key="quarter_sel",
                         label_visibility="collapsed")
    quarter = q_opts[q_display.index(q_sel)]

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def fmt_cr(amount):
    cr = amount / 1e7
    if cr >= 1e5:
        return f"&#8377;{cr/1e5:.2f} Lakh Cr"
    return f"&#8377;{cr:,.0f} Cr"

def fmt_rank_val(count):
    cr = count / 1e7
    if cr >= 100: return f"{cr/100:.2f}B"
    if cr >= 1:   return f"{cr:.2f}Cr"
    lakh = count / 1e5
    if lakh >= 1: return f"{lakh:.2f}L"
    return f"{int(count):,}"

def make_choropleth(df, color_col, hover_label):
    color_scale = [
        [0.0,  "#0d0b35"],
        [0.15, "#1a3060"],
        [0.35, "#0e7cab"],
        [0.55, "#00c4b8"],
        [0.75, "#f5c518"],
        [1.0,  "#e8421e"],
    ]
    fig = px.choropleth_mapbox(
        df,
        geojson=india_geojson,
        locations="state_clean",
        featureidkey=f"properties.{GEO_ID_KEY}",
        color=color_col,
        color_continuous_scale=color_scale,
        mapbox_style="carto-darkmatter",
        zoom=3.8,
        center={"lat": 22.5, "lon": 80.0},
        opacity=0.85,
        hover_name="state_clean",
        hover_data={color_col: ":,", "state_clean": False},
        labels={color_col: hover_label},
        height=480,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False,
        hoverlabel=dict(bgcolor="#1a1245", font_color="white",
                        font_size=13, bordercolor="rgba(255,255,255,0.2)"),
    )
    return fig

def build_ranks_html(df, val_col, name_col="entity_name"):
    html = ""
    for idx, row in df.head(10).iterrows():
        html += (
            f'<div class="rank-row">'
            f'<span class="rank-num">{idx+1}</span>'
            f'<span class="rank-name">{row[name_col]}</span>'
            f'<span class="rank-value">{fmt_rank_val(row[val_col])}</span>'
            f'</div>'
        )
    return html

# ─────────────────────────────────────────────
# ══════════ TRANSACTIONS DOMAIN ══════════
# ─────────────────────────────────────────────

if domain == "Transactions":

    # — Data queries —
    summary = pd.read_sql(f"""
        SELECT SUM(transaction_count) AS total_count,
               SUM(transaction_amount) AS total_amount
        FROM aggregated_transaction
        WHERE year={year} AND quarter={quarter}
    """, conn)
    total_count  = int(summary.iloc[0]["total_count"] or 0)
    total_amount = float(summary.iloc[0]["total_amount"] or 0)
    avg_val      = int(total_amount / total_count) if total_count > 0 else 0

    cat_df = pd.read_sql(f"""
        SELECT transaction_type, SUM(transaction_count) AS count
        FROM aggregated_transaction
        WHERE year={year} AND quarter={quarter}
        GROUP BY transaction_type ORDER BY count DESC
    """, conn)

    state_df = pd.read_sql(f"""
        SELECT state, SUM(transaction_count) AS count,
               SUM(transaction_amount) AS amount
        FROM aggregated_transaction
        WHERE year={year} AND quarter={quarter}
        GROUP BY state ORDER BY count DESC
    """, conn)
    state_df["state_clean"] = state_df["state"].str.strip().str.title()

    # Top districts from top_transaction
    top_dist_df = pd.read_sql(f"""
        SELECT entity_name, SUM(count) AS count
        FROM top_transaction
        WHERE year={year} AND quarter={quarter}
        GROUP BY entity_name ORDER BY count DESC
        LIMIT 10
    """, conn)

    # Top pin codes — top_transaction entries that look like pin codes (all digits, 6 chars)
    top_pin_df = pd.read_sql(f"""
        SELECT entity_name, SUM(count) AS count
        FROM top_transaction
        WHERE year={year} AND quarter={quarter}
          AND entity_name REGEXP '^[0-9]{{6}}$'
        GROUP BY entity_name ORDER BY count DESC
        LIMIT 10
    """, conn)

    # ─ Layout ─
    map_col, info_col = st.columns([62, 38])

    with map_col:
        st.markdown('<div style="padding: 8px 16px 8px 24px;">', unsafe_allow_html=True)
        st.plotly_chart(
            make_choropleth(state_df, "count", "Transactions"),
            use_container_width=True, config={"displayModeBar": False}
        )

        # ── Category Pie Chart ──
        if not cat_df.empty:
            fig_pie = px.pie(
                cat_df, names="transaction_type", values="count",
                color_discrete_sequence=["#00d4e0","#6739b7","#f5c518",
                                          "#e8421e","#0e7cab"],
                hole=0.45,
                height=300,
            )
            fig_pie.update_traces(textinfo="percent+label",
                                  textfont_color="white",
                                  marker=dict(line=dict(color="#140c31", width=2)))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=30, b=10),
                font_color="white",
                title=dict(text="Transaction Category Distribution",
                           font_color="white", font_size=14, x=0.02),
                legend=dict(font_color="white", bgcolor="rgba(0,0,0,0)"),
                showlegend=True,
            )
            st.plotly_chart(fig_pie, use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown('<div class="explore-btn">EXPLORE SPECIAL DATA POINTS &nbsp; ⬆⬆</div>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with info_col:
        # ── Build categories HTML ──
        cats_html = ""
        for _, row in cat_df.iterrows():
            cats_html += (
                f'<div class="cat-row">'
                f'<span class="cat-name">{row["transaction_type"]}</span>'
                f'<span class="cat-value">{int(row["count"]):,}</span>'
                f'</div>'
            )

        # ── States ranks ──
        states_top10 = state_df.head(10).reset_index(drop=True)
        state_ranks = ""
        for idx, row in states_top10.iterrows():
            state_ranks += (
                f'<div class="rank-row">'
                f'<span class="rank-num">{idx+1}</span>'
                f'<span class="rank-name">{row["state_clean"]}</span>'
                f'<span class="rank-value">{fmt_rank_val(row["count"])}</span>'
                f'</div>'
            )

        # ── District ranks ──
        dist_ranks = build_ranks_html(top_dist_df.reset_index(drop=True), "count") \
            if not top_dist_df.empty else \
            '<div style="color:rgba(255,255,255,0.4);font-size:12px;">No district data.</div>'

        # ── Pin code ranks ──
        pin_ranks = build_ranks_html(top_pin_df.reset_index(drop=True), "count") \
            if not top_pin_df.empty else \
            '<div style="color:rgba(255,255,255,0.4);font-size:12px;">No pin code data.</div>'

        # ── Render tabs as Streamlit tabs ──
        tab_s, tab_d, tab_p = st.tabs(["🗺 States", "🏙 Districts", "📮 Postal Codes"])

        panel_top = (
            '<div style="padding:18px 20px 10px 16px; background:#1c1447;">'
            '<div class="panel-title">Transactions</div>'
            '<div class="panel-subtitle">All PhonePe transactions (UPI + Cards + Wallets)</div>'
            f'<div class="hero-metric">{total_count:,}</div>'
            '<div class="sub-metrics">'
            '<div>'
            '<div class="sub-metric-label">Total payment value</div>'
            f'<div class="sub-metric-value">{fmt_cr(total_amount)}</div>'
            '</div>'
            '<div>'
            '<div class="sub-metric-label">Avg. transaction value</div>'
            f'<div class="sub-metric-value">&#8377;{avg_val:,}</div>'
            '</div>'
            '</div>'
            '<div class="pulse-divider"></div>'
            '<div class="cat-title">Categories</div>'
            + cats_html +
            '<div class="pulse-divider"></div>'
        )

        with tab_s:
            st.markdown(
                panel_top
                + '<div class="rank-title">Top 10 States</div>'
                + state_ranks
                + '</div>',
                unsafe_allow_html=True
            )

        with tab_d:
            st.markdown(
                panel_top
                + '<div class="rank-title">Top 10 Districts</div>'
                + dist_ranks
                + '</div>',
                unsafe_allow_html=True
            )

        with tab_p:
            st.markdown(
                panel_top
                + '<div class="rank-title">Top 10 Postal Codes</div>'
                + pin_ranks
                + '</div>',
                unsafe_allow_html=True
            )

# ─────────────────────────────────────────────
# ══════════ USERS DOMAIN ══════════
# ─────────────────────────────────────────────

else:  # domain == "Users"

    # — Data queries —
    user_summary = pd.read_sql(f"""
        SELECT SUM(registered_users) AS total_users,
               SUM(app_opens) AS total_opens
        FROM map_user
        WHERE year={year} AND quarter={quarter}
    """, conn)
    total_users  = int(user_summary.iloc[0]["total_users"] or 0)
    total_opens  = int(user_summary.iloc[0]["total_opens"] or 0)

    # State-level users
    user_state_df = pd.read_sql(f"""
        SELECT state,
               SUM(registered_users) AS registered_users,
               SUM(app_opens) AS app_opens
        FROM map_user
        WHERE year={year} AND quarter={quarter}
        GROUP BY state ORDER BY registered_users DESC
    """, conn)
    user_state_df["state_clean"] = user_state_df["state"].str.strip().str.title()

    # Brand breakdown from aggregated_user
    brand_df = pd.read_sql(f"""
        SELECT brand, SUM(count) AS count
        FROM aggregated_user
        WHERE year={year} AND quarter={quarter}
        GROUP BY brand ORDER BY count DESC
        LIMIT 10
    """, conn)

    # Top districts by registered users
    top_dist_users = pd.read_sql(f"""
        SELECT district AS entity_name, SUM(registered_users) AS count
        FROM map_user
        WHERE year={year} AND quarter={quarter}
        GROUP BY district ORDER BY count DESC
        LIMIT 10
    """, conn)

    # ─ Layout ─
    map_col, info_col = st.columns([62, 38])

    with map_col:
        st.markdown('<div style="padding: 8px 16px 8px 24px;">', unsafe_allow_html=True)
        st.plotly_chart(
            make_choropleth(user_state_df, "registered_users", "Registered Users"),
            use_container_width=True, config={"displayModeBar": False}
        )

        # ── Brand bar chart ──
        if not brand_df.empty:
            fig_bar = px.bar(
                brand_df.head(10),
                x="brand", y="count",
                color="count",
                color_continuous_scale=["#1a3060","#00c4b8","#f5c518"],
                labels={"brand": "Device Brand", "count": "Users"},
                height=280,
                title="Top Device Brands",
                text_auto=".2s",
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=40, b=10),
                font_color="white",
                title_font_color="white",
                xaxis=dict(tickfont_color="white", gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(tickfont_color="white", gridcolor="rgba(255,255,255,0.05)"),
                coloraxis_showscale=False,
            )
            fig_bar.update_traces(textfont_color="white")
            st.plotly_chart(fig_bar, use_container_width=True,
                            config={"displayModeBar": False})

        st.markdown('<div class="explore-btn">EXPLORE SPECIAL DATA POINTS &nbsp; ⬆⬆</div>',
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with info_col:
        # ── Brand breakdown HTML ──
        brands_html = ""
        for _, row in brand_df.iterrows():
            brands_html += (
                f'<div class="cat-row">'
                f'<span class="cat-name">{row["brand"]}</span>'
                f'<span class="cat-value">{fmt_rank_val(row["count"])}</span>'
                f'</div>'
            )

        # ── State ranks ──
        state_ranks = ""
        for idx, row in user_state_df.head(10).reset_index(drop=True).iterrows():
            state_ranks += (
                f'<div class="rank-row">'
                f'<span class="rank-num">{idx+1}</span>'
                f'<span class="rank-name">{row["state_clean"]}</span>'
                f'<span class="rank-value">{fmt_rank_val(row["registered_users"])}</span>'
                f'</div>'
            )

        # ── District ranks ──
        dist_ranks = build_ranks_html(top_dist_users.reset_index(drop=True), "count") \
            if not top_dist_users.empty else \
            '<div style="color:rgba(255,255,255,0.4);font-size:12px;">No district data.</div>'

        panel_top = (
            '<div style="padding:18px 20px 10px 16px; background:#1c1447;">'
            '<div class="panel-title">Users</div>'
            '<div class="panel-subtitle">Registered PhonePe users &amp; app opens</div>'
            f'<div class="hero-metric">{total_users:,}</div>'
            '<div class="sub-metrics">'
            '<div>'
            '<div class="sub-metric-label">Registered Users</div>'
            f'<div class="sub-metric-value">{fmt_rank_val(total_users)}</div>'
            '</div>'
            '<div>'
            '<div class="sub-metric-label">App Opens</div>'
            f'<div class="sub-metric-value">{fmt_rank_val(total_opens)}</div>'
            '</div>'
            '</div>'
            '<div class="pulse-divider"></div>'
            '<div class="cat-title">Top Device Brands</div>'
            + brands_html +
            '<div class="pulse-divider"></div>'
        )

        tab_s, tab_d = st.tabs(["🗺 States", "🏙 Districts"])

        with tab_s:
            st.markdown(
                panel_top
                + '<div class="rank-title">Top 10 States</div>'
                + state_ranks
                + '</div>',
                unsafe_allow_html=True
            )

        with tab_d:
            st.markdown(
                panel_top
                + '<div class="rank-title">Top 10 Districts</div>'
                + dist_ranks
                + '</div>',
                unsafe_allow_html=True
            )