import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NSE Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .stApp { background: #07090f; }
  section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #1e2736; }
  section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
  .header-banner {
    background: linear-gradient(135deg, #0d1117 0%, #0f2138 50%, #07090f 100%);
    border: 1px solid #1e3a5f; border-radius: 12px;
    padding: 24px 32px; margin-bottom: 20px; position: relative; overflow: hidden;
  }
  .header-banner::before {
    content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%;
    background: radial-gradient(circle at 70% 50%, rgba(0,212,255,0.05) 0%, transparent 60%);
    pointer-events: none;
  }
  .header-title { font-family:'Space Mono',monospace; font-size:2rem; font-weight:700; color:#fff; margin:0; }
  .header-title span { color:#00d4ff; }
  .header-sub { color:#7a8899; font-size:0.85rem; margin-top:6px; letter-spacing:2px; text-transform:uppercase; }
  .live-badge {
    display:inline-flex; align-items:center; gap:6px;
    background:rgba(0,255,136,0.1); border:1px solid rgba(0,255,136,0.3);
    border-radius:20px; padding:4px 12px; font-size:0.72rem;
    font-family:'Space Mono',monospace; color:#00ff88; letter-spacing:1px;
  }
  .live-dot { width:7px; height:7px; background:#00ff88; border-radius:50%; animation:pulse 1.5s infinite; }
  @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
  .kpi-card {
    background:#0d1117; border:1px solid #1e2736; border-radius:10px;
    padding:18px 20px; position:relative; overflow:hidden;
  }
  .kpi-card::after { content:''; position:absolute; top:0; left:0; width:3px; height:100%; border-radius:10px 0 0 10px; }
  .kpi-green::after  { background:#00ff88; }
  .kpi-blue::after   { background:#00d4ff; }
  .kpi-yellow::after { background:#ffd700; }
  .kpi-orange::after { background:#ff6b35; }
  .kpi-red::after    { background:#ff4d6d; }
  .kpi-purple::after { background:#9f7aea; }
  .kpi-label { font-size:0.68rem; text-transform:uppercase; letter-spacing:2px; color:#7a8899; margin-bottom:8px; }
  .kpi-value { font-family:'Space Mono',monospace; font-size:1.75rem; font-weight:700; color:#fff; line-height:1; }
  .kpi-sub   { font-size:0.7rem; color:#7a8899; margin-top:6px; }
  .kpi-sub .up   { color:#00ff88; }
  .kpi-sub .down { color:#ff4d6d; }
  .section-title {
    font-family:'Space Mono',monospace; font-size:0.75rem; text-transform:uppercase;
    letter-spacing:3px; color:#00d4ff; margin-bottom:12px;
    border-bottom:1px solid #1e2736; padding-bottom:8px;
  }
  .insight-card {
    background:linear-gradient(135deg,#0d1117,#111827); border:1px solid #1e2736;
    border-left:3px solid #00d4ff; border-radius:8px; padding:14px 18px;
    margin-bottom:10px; font-size:0.82rem; color:#c9d1d9; line-height:1.6;
  }
  .insight-card .tag {
    display:inline-block; background:rgba(0,212,255,0.15); color:#00d4ff;
    border-radius:4px; padding:1px 8px; font-size:0.68rem;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;
  }
  .stTabs [data-baseweb="tab-list"] { background:#0d1117; border-bottom:1px solid #1e2736; gap:0; }
  .stTabs [data-baseweb="tab"] {
    background:transparent; color:#7a8899 !important;
    font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:1.5px;
    text-transform:uppercase; padding:10px 18px; border-bottom:2px solid transparent;
  }
  .stTabs [aria-selected="true"] {
    color:#00d4ff !important; border-bottom:2px solid #00d4ff !important;
    background:rgba(0,212,255,0.05) !important;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SHARED LAYOUT BUILDER  ← fixes all duplicate-key errors
# ─────────────────────────────────────────────
LEGEND_STYLE = dict(
    bgcolor="rgba(13,17,23,0.9)",
    bordercolor="#1e2736",
    borderwidth=1,
    font=dict(size=10)
)
AXIS_STYLE = dict(gridcolor="#1a2234", zerolinecolor="#1a2234", tickfont=dict(size=9))

def base_layout(height=360, title="", extra=None):
    """Return a clean layout dict with no duplicate keys."""
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#c9d1d9", size=11),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        legend=LEGEND_STYLE,
        xaxis=AXIS_STYLE,
        yaxis=AXIS_STYLE,
    )
    if title:
        layout["title"] = dict(text=title, font=dict(color="#c9d1d9", size=13))
    if extra:
        layout.update(extra)
    return layout

def apply(fig, height=360, title="", extra=None):
    fig.update_layout(**base_layout(height=height, title=title, extra=extra))
    return fig

# ─────────────────────────────────────────────
# COLOR MAPS
# ─────────────────────────────────────────────
COLOR_MAP = {
    "Large Cap":           "#00d4ff",
    "Mid Cap":             "#00ff88",
    "Small Cap":           "#ffd700",
    "Micro Cap":           "#ff6b35",
    "Sectoral Large Cap":  "#9f7aea",
    "Defensive Large Cap": "#f6ad55",
    "Large Cap Pharma":    "#68d391",
}
RISK_COLOR = {
    "Low":       "#00ff88",
    "Medium":    "#00d4ff",
    "High":      "#ffd700",
    "Very High": "#ff6b35",
    "Extreme":   "#ff4d6d",
}

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    data = {
        "index_name":         ["NIFTY 50","NIFTY NEXT 50","NIFTY MIDCAP 100","NIFTY MIDCAP 150",
                                "NIFTY SMALLCAP 100","NIFTY SMALLCAP 250","NIFTY MICROCAP 250",
                                "NIFTY BANK","NIFTY FMCG","NIFTY PHARMA"],
        "market_cap_category":["Large Cap","Large Cap","Mid Cap","Mid Cap",
                                "Small Cap","Small Cap","Micro Cap",
                                "Sectoral Large Cap","Defensive Large Cap","Large Cap Pharma"],
        "cagr_1y":  [18.2,20.5,24.9,23.8,28.1,26.9,31.8,16.1,12.6,15.4],
        "cagr_3y":  [14.6,16.9,20.1,19.5,23.5,22.1,26.4,12.9,13.8,14.1],
        "cagr_5y":  [13.9,15.2,18.5,17.9,21.2,20.3,23.7,11.8,14.9,15.6],
        "volatility":[12.8,14.6,18.1,17.4,22.7,21.8,27.6,14.2,9.4,11.2],
        "avg_pe":   [22.4,26.1,31.4,30.2,37.4,35.9,42.5,18.6,45.2,34.8],
        "avg_pb":   [3.8,4.2,5.3,5.1,6.6,6.3,7.8,2.9,10.2,5.9],
        "index_level":[21750,61250,49250,18940,14350,11860,16230,46250,54280,19760],
        "risk_level": ["High","High","High","High","Very High","Very High","Extreme","Medium","Low","Medium"],
        "risk_score": [3,3,3,3,4,4,5,2,1,2],
        "return_category":["Moderate","High","High","High","Excellent","Excellent","Excellent","Moderate","High","High"],
        "risk_adjusted_return":[1.086,1.041,1.022,1.029,0.933,0.931,0.859,0.831,1.585,1.393],
        "valuation_score":[85.12,109.62,166.42,154.02,246.84,226.17,331.50,53.94,461.04,205.32],
    }
    df = pd.DataFrame(data)
    df["short_name"] = df["index_name"].str.replace("NIFTY ","", regex=False)
    return df

df_full = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 10px;'>
      <div style='font-family:Space Mono,monospace;font-size:1.1rem;color:#00d4ff;font-weight:700;'>NSE ANALYTICS</div>
      <div style='font-size:0.68rem;color:#7a8899;letter-spacing:2px;margin-top:4px;'>FY2024–25 · 10 INDICES</div>
    </div>
    <hr style='border-color:#1e2736;margin:8px 0 16px;'>
    """, unsafe_allow_html=True)

    st.markdown("**📂 MARKET SEGMENT**")
    cap_options = sorted(df_full["market_cap_category"].unique())
    selected_caps = st.multiselect("cap_sel", cap_options, default=cap_options, label_visibility="collapsed")

    st.markdown("<br>**⚠️ RISK LEVEL**", unsafe_allow_html=True)
    risk_options = ["Low","Medium","High","Very High","Extreme"]
    selected_risks = st.multiselect("risk_sel", risk_options, default=risk_options, label_visibility="collapsed")

    st.markdown("<br>**📊 CAGR HORIZON**", unsafe_allow_html=True)
    cagr_period = st.radio("cagr_radio", ["1 Year","3 Year","5 Year"], index=2, horizontal=True, label_visibility="collapsed")
    cagr_col = {"1 Year":"cagr_1y","3 Year":"cagr_3y","5 Year":"cagr_5y"}[cagr_period]

    st.markdown("<br>**📥 EXPORT**", unsafe_allow_html=True)
    st.download_button(
        "⬇ Download CSV",
        data=df_full.to_csv(index=False).encode(),
        file_name="nse_index_analytics.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown("""
    <hr style='border-color:#1e2736;margin:16px 0 12px;'>
    <div style='font-size:0.68rem;color:#3d4f63;text-align:center;line-height:1.8;'>
      Data: NSE India · FY2024-25<br>Risk metrics are indicative only
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────────
df = df_full[
    df_full["market_cap_category"].isin(selected_caps) &
    df_full["risk_level"].isin(selected_risks)
].copy()

if df.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
col_h1, col_h2 = st.columns([4,1])
with col_h1:
    st.markdown("""
    <div class="header-banner">
      <div class="header-title">NSE <span>Market Intelligence</span> Dashboard</div>
      <div class="header-sub">Risk · Return · Valuation Analysis across Market Cap Categories</div>
    </div>""", unsafe_allow_html=True)
with col_h2:
    st.markdown("""
    <div style='padding-top:20px;'>
      <div class="live-badge"><span class="live-dot"></span>LIVE DATA</div>
      <div style='font-size:0.68rem;color:#3d4f63;font-family:Space Mono,monospace;margin-top:8px;'>FY2024-25</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
avg_cagr   = df["cagr_5y"].mean()
best_rar_v = df["risk_adjusted_return"].max()
best_rar_n = df.loc[df["risk_adjusted_return"].idxmax(), "short_name"]
avg_pe     = df["avg_pe"].mean()
n_idx      = len(df)
best_1y_v  = df["cagr_1y"].max()
best_1y_n  = df.loc[df["cagr_1y"].idxmax(), "short_name"]
avg_vol    = df["volatility"].mean()

k1,k2,k3,k4,k5,k6 = st.columns(6)
for col_w, accent, label, val, sub in [
    (k1,"green", "AVG 5Y CAGR",   f"{avg_cagr:.1f}%",  f'<span class="up">▲ Best: {df["cagr_5y"].max():.1f}%</span>'),
    (k2,"blue",  "BEST RISK-ADJ", f"{best_rar_v:.2f}",  f'<span class="up">{best_rar_n}</span>'),
    (k3,"yellow","AVG P/E RATIO", f"{avg_pe:.1f}x",     f'Range: {df["avg_pe"].min():.1f} – {df["avg_pe"].max():.1f}'),
    (k4,"orange","INDICES",        str(n_idx),           "Across market segments"),
    (k5,"green", "BEST 1Y RETURN",f"{best_1y_v:.1f}%",  best_1y_n),
    (k6,"purple","AVG VOLATILITY",f"{avg_vol:.1f}%",    f'Lowest: {df["volatility"].min():.1f}%'),
]:
    col_w.markdown(f"""
    <div class="kpi-card kpi-{accent}">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{val}</div>
      <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGATION TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈  RETURNS", "⚠️  RISK", "💰  VALUATION",
    "🎯  EFFICIENCY", "🔍  DEEP DIVE", "📋  DATA TABLE",
])

# ══════════════════════════════════════════════
# TAB 1 — RETURNS
# ══════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-title'>CAGR Performance Analysis</div>", unsafe_allow_html=True)

    df_melt = df.melt(
        id_vars=["short_name","market_cap_category"],
        value_vars=["cagr_1y","cagr_3y","cagr_5y"],
        var_name="Period", value_name="CAGR"
    )
    df_melt["Period"] = df_melt["Period"].map({"cagr_1y":"1Y","cagr_3y":"3Y","cagr_5y":"5Y"})

    fig1 = px.bar(df_melt, x="short_name", y="CAGR", color="Period", barmode="group",
                  color_discrete_map={"1Y":"#00d4ff","3Y":"#9f7aea","5Y":"#00ff88"},
                  labels={"short_name":"Index","CAGR":"CAGR (%)"})
    fig1.update_traces(marker_line_width=0)
    apply(fig1, height=360, title="Multi-Period CAGR Comparison — 1Y / 3Y / 5Y")
    st.plotly_chart(fig1, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        df_rank = df[["short_name", cagr_col]].sort_values(cagr_col, ascending=True)
        fig2 = px.bar(df_rank, x=cagr_col, y="short_name", orientation="h",
                      color=cagr_col, color_continuous_scale=["#1a2234","#00ff88"],
                      labels={cagr_col:f"{cagr_period} CAGR (%)","short_name":""})
        apply(fig2, height=320, title=f"Ranking — {cagr_period} CAGR",
              extra={"coloraxis_showscale": False})
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        fig3 = px.scatter(df, x="cagr_5y", y="cagr_1y", text="short_name",
                          color="market_cap_category", color_discrete_map=COLOR_MAP,
                          labels={"cagr_5y":"5Y CAGR (%)","cagr_1y":"1Y CAGR (%)"})
        fig3.update_traces(textposition="top center", textfont=dict(size=8), marker=dict(size=14))
        mn, mx = df["cagr_5y"].min()-1, df["cagr_5y"].max()+1
        fig3.add_shape(type="line", x0=mn, y0=mn, x1=mx, y1=mx,
                       line=dict(color="#1e3a5f", dash="dash", width=1))
        apply(fig3, height=320, title="Return Momentum: 1Y vs 5Y CAGR")
        st.plotly_chart(fig3, use_container_width=True)

    cat_perf = df.groupby("market_cap_category")[["cagr_1y","cagr_3y","cagr_5y"]].mean().round(2)
    cat_perf.columns = ["1Y","3Y","5Y"]
    fig4 = px.imshow(cat_perf,
                     color_continuous_scale=[[0,"#0d1117"],[0.5,"#1e3a5f"],[1,"#00ff88"]],
                     text_auto=True, labels=dict(x="Period",y="Category",color="CAGR %"))
    fig4.update_traces(textfont=dict(size=12, color="white"))
    apply(fig4, height=280, title="Avg CAGR Heatmap by Market Segment",
          extra={"xaxis": dict(side="bottom", gridcolor="rgba(0,0,0,0)"),
                 "yaxis": dict(showgrid=False, gridcolor="rgba(0,0,0,0)")})
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 2 — RISK
# ══════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>Risk Analysis & Distribution</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        risk_counts = df["risk_level"].value_counts().reset_index()
        risk_counts.columns = ["risk_level","count"]
        fig5 = px.pie(risk_counts, names="risk_level", values="count",
                      hole=0.6, color="risk_level", color_discrete_map=RISK_COLOR)
        fig5.update_traces(textinfo="label+percent", textfont_size=10)
        # pie charts must NOT have xaxis/yaxis in layout
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#c9d1d9", size=11),
            margin=dict(l=10,r=10,t=40,b=60), height=340,
            title=dict(text="Risk Level Distribution", font=dict(color="#c9d1d9",size=13)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3,
                        bgcolor="rgba(13,17,23,0.9)", bordercolor="#1e2736",
                        borderwidth=1, font=dict(size=10))
        )
        st.plotly_chart(fig5, use_container_width=True)

    with c2:
        fig6 = px.bar(df.sort_values("volatility", ascending=False),
                      x="short_name", y="volatility",
                      color="risk_level", color_discrete_map=RISK_COLOR,
                      labels={"short_name":"","volatility":"Volatility (%)"})
        fig6.update_traces(marker_line_width=0)
        apply(fig6, height=340, title="Volatility by Index")
        st.plotly_chart(fig6, use_container_width=True)

    fig7 = px.scatter(df, x="volatility", y="cagr_5y",
                      size="index_level", color="market_cap_category",
                      color_discrete_map=COLOR_MAP, hover_name="index_name",
                      hover_data={"volatility":":.1f","cagr_5y":":.1f","risk_level":True},
                      labels={"volatility":"Volatility (%)","cagr_5y":"5Y CAGR (%)"})
    xs = np.linspace(df["volatility"].min()-2, df["volatility"].max()+2, 100)
    fig7.add_trace(go.Scatter(x=xs, y=8+0.52*xs, mode="lines",
                               line=dict(color="#1e3a5f", dash="dash", width=1.5),
                               name="Market Line"))
    apply(fig7, height=360, title="Risk-Return Scatter — Bubble size = Index Level")
    st.plotly_chart(fig7, use_container_width=True)

    # Radar
    radar_cats = ["Volatility","PE Ratio","PB Ratio","Risk Score","5Y CAGR"]
    clrs = ["#00d4ff","#00ff88","#ffd700","#ff6b35","#ff4d6d","#9f7aea","#f6ad55","#68d391"]
    fig8 = go.Figure()
    for i, (_, row_r) in enumerate(df.iterrows()):
        vals = [
            row_r["volatility"]/df["volatility"].max(),
            row_r["avg_pe"]/df["avg_pe"].max(),
            row_r["avg_pb"]/df["avg_pb"].max(),
            row_r["risk_score"]/5,
            row_r["cagr_5y"]/df["cagr_5y"].max(),
        ]
        vals.append(vals[0])
        fig8.add_trace(go.Scatterpolar(
            r=vals, theta=radar_cats+[radar_cats[0]],
            mode="lines", name=row_r["short_name"],
            line=dict(width=1.5, color=clrs[i % len(clrs)]), opacity=0.8
        ))
    fig8.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#c9d1d9", size=11),
        margin=dict(l=10,r=10,t=40,b=10), height=440,
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True, range=[0,1], gridcolor="#1e2736", tickfont=dict(size=8)),
                   angularaxis=dict(gridcolor="#1e2736", tickfont=dict(size=10))),
        legend=dict(bgcolor="rgba(13,17,23,0.9)", bordercolor="#1e2736",
                    borderwidth=1, font=dict(size=9)),
        title=dict(text="Multi-Dimensional Risk Radar", font=dict(color="#c9d1d9",size=13))
    )
    st.plotly_chart(fig8, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 3 — VALUATION
# ══════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-title'>Valuation Metrics — P/E · P/B · Score</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig9 = make_subplots(specs=[[{"secondary_y": True}]])
        fig9.add_trace(go.Bar(x=df["short_name"], y=df["avg_pe"], name="Avg P/E",
                               marker_color="#ff6b35", opacity=0.85), secondary_y=False)
        fig9.add_trace(go.Scatter(x=df["short_name"], y=df["avg_pb"], name="Avg P/B",
                                   mode="lines+markers", line=dict(color="#00d4ff",width=2),
                                   marker=dict(size=7)), secondary_y=True)
        fig9.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#c9d1d9", size=11),
            margin=dict(l=10,r=10,t=40,b=10), height=340,
            legend=LEGEND_STYLE,
            xaxis=dict(gridcolor="#1a2234", tickfont=dict(size=9)),
            title=dict(text="P/E (Bar) vs P/B (Line)", font=dict(color="#c9d1d9",size=13))
        )
        fig9.update_yaxes(title_text="P/E Ratio", secondary_y=False,
                          gridcolor="#1a2234", tickfont=dict(size=9))
        fig9.update_yaxes(title_text="P/B Ratio", secondary_y=True,
                          gridcolor="#1a2234", tickfont=dict(size=9), showgrid=False)
        st.plotly_chart(fig9, use_container_width=True)

    with c2:
        fig10 = px.bar(df.sort_values("valuation_score", ascending=True),
                       x="valuation_score", y="short_name", orientation="h",
                       color="valuation_score",
                       color_continuous_scale=[[0,"#00ff88"],[0.5,"#ffd700"],[1,"#ff4d6d"]],
                       labels={"valuation_score":"Valuation Score (PE×PB)","short_name":""})
        apply(fig10, height=340, title="Valuation Score — Overvaluation Risk",
              extra={"coloraxis_showscale": False})
        st.plotly_chart(fig10, use_container_width=True)

    fig11 = px.scatter(df, x="avg_pe", y="avg_pb", text="short_name",
                       size="valuation_score", color="market_cap_category",
                       color_discrete_map=COLOR_MAP,
                       labels={"avg_pe":"P/E Ratio","avg_pb":"P/B Ratio"})
    fig11.update_traces(textposition="top center", textfont=dict(size=8))
    fig11.add_vline(x=df["avg_pe"].median(), line_dash="dash", line_color="#1e3a5f",
                    annotation_text="Median PE", annotation_font=dict(size=9,color="#7a8899"))
    fig11.add_hline(y=df["avg_pb"].median(), line_dash="dash", line_color="#1e3a5f",
                    annotation_text="Median PB", annotation_font=dict(size=9,color="#7a8899"))
    apply(fig11, height=380, title="P/E vs P/B Quadrant Analysis")
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("<div class='section-title'>VALUATION INSIGHTS</div>", unsafe_allow_html=True)
    most_over  = df.loc[df["valuation_score"].idxmax(), "index_name"]
    most_under = df.loc[df["valuation_score"].idxmin(), "index_name"]
    low_pe_idx = df.loc[df["avg_pe"].idxmin(), "index_name"]
    for tag, txt in [
        ("OVERVALUED",  f"<b>{most_over}</b> carries the highest valuation score ({df['valuation_score'].max():.0f}), indicating significant premium pricing."),
        ("UNDERVALUED", f"<b>{most_under}</b> has the lowest valuation score ({df['valuation_score'].min():.0f}), potentially offering value entry points."),
        ("LOWEST P/E",  f"<b>{low_pe_idx}</b> trades at the lowest P/E ({df['avg_pe'].min():.1f}x) in the current selection."),
    ]:
        st.markdown(f'<div class="insight-card"><div class="tag">{tag}</div><br>{txt}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 4 — EFFICIENCY
# ══════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-title'>Risk-Adjusted Return Efficiency</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.5,1])
    with c1:
        fig12 = px.bar(df.sort_values("risk_adjusted_return"),
                       x="risk_adjusted_return", y="short_name", orientation="h",
                       color="risk_adjusted_return",
                       color_continuous_scale=[[0,"#ff4d6d"],[0.5,"#ffd700"],[1,"#00ff88"]],
                       labels={"risk_adjusted_return":"Risk-Adjusted Return (CAGR÷Vol)","short_name":""})
        fig12.add_vline(x=1.0, line_dash="dash", line_color="#ffffff",
                        annotation_text="Benchmark = 1.0",
                        annotation_font=dict(size=9,color="#7a8899"))
        apply(fig12, height=380, title="Risk-Adjusted Return Ranking",
              extra={"coloraxis_showscale": False})
        st.plotly_chart(fig12, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title' style='margin-top:0'>TOP 5 BY EFFICIENCY</div>", unsafe_allow_html=True)
        top5 = df.nlargest(5,"risk_adjusted_return")[["short_name","risk_adjusted_return","risk_level"]]
        for rank, (_, r) in enumerate(top5.iterrows(), 1):
            medal = ["🥇","🥈","🥉","4️⃣","5️⃣"][rank-1]
            color = RISK_COLOR.get(r["risk_level"],"#fff")
            st.markdown(f"""
            <div class="insight-card" style="border-left-color:{color};margin-bottom:8px;">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <span>{medal} <b>{r['short_name']}</b></span>
                <span style="font-family:Space Mono,monospace;color:{color};font-size:1rem;font-weight:700;">{r['risk_adjusted_return']:.3f}</span>
              </div>
              <div style="font-size:0.7rem;color:#7a8899;margin-top:4px;">Risk Level: {r['risk_level']}</div>
            </div>""", unsafe_allow_html=True)

    fig13 = px.scatter(df, x="volatility", y="risk_adjusted_return",
                       text="short_name", color="risk_level",
                       color_discrete_map=RISK_COLOR,
                       size=[abs(x)*30 for x in df["risk_adjusted_return"]],
                       labels={"volatility":"Volatility (%)","risk_adjusted_return":"Risk-Adjusted Return"})
    fig13.update_traces(textposition="top center", textfont=dict(size=8))
    fig13.add_hline(y=1.0, line_dash="dash", line_color="#1e3a5f",
                    annotation_text="RAR = 1.0", annotation_font=dict(size=9,color="#7a8899"))
    apply(fig13, height=360, title="Efficiency Frontier — RAR vs Volatility")
    st.plotly_chart(fig13, use_container_width=True)

    ret_cat = df.groupby("return_category").agg(
        count=("index_name","count"),
        avg_rar=("risk_adjusted_return","mean"),
        avg_cagr=("cagr_5y","mean")
    ).reset_index()
    fig14 = px.bar(ret_cat, x="return_category", y="avg_cagr",
                   color="avg_rar", text="count",
                   color_continuous_scale=[[0,"#1a2234"],[1,"#00d4ff"]],
                   labels={"return_category":"Return Category","avg_cagr":"Avg 5Y CAGR (%)"})
    fig14.update_traces(textposition="outside", textfont=dict(color="#c9d1d9"))
    apply(fig14, height=300, title="Return Categories — Avg CAGR coloured by Avg RAR")
    st.plotly_chart(fig14, use_container_width=True)

# ══════════════════════════════════════════════
# TAB 5 — DEEP DIVE
# ══════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-title'>Single Index Deep Dive</div>", unsafe_allow_html=True)

    sel_index = st.selectbox("Select Index", options=df["index_name"].tolist(), index=0)
    row = df[df["index_name"] == sel_index].iloc[0]

    d1,d2,d3,d4,d5 = st.columns(5)
    for col_w, label, val, ac in [
        (d1,"Market Segment",  row["market_cap_category"],  "#00d4ff"),
        (d2,"Risk Level",      row["risk_level"],            RISK_COLOR.get(row["risk_level"],"#fff")),
        (d3,"Return Category", row["return_category"],       "#00ff88"),
        (d4,"Risk Score",      f"{row['risk_score']}/5",     "#ffd700"),
        (d5,"Index Level",     f"{row['index_level']:,}",    "#ff6b35"),
    ]:
        col_w.markdown(f"""
        <div class="kpi-card kpi-blue" style="border-left-color:{ac};">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" style="font-size:1.1rem;color:{ac};">{val}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig15 = go.Figure(go.Bar(
            x=["1 Year","3 Year","5 Year"],
            y=[row["cagr_1y"], row["cagr_3y"], row["cagr_5y"]],
            marker_color=["#00d4ff","#9f7aea","#00ff88"],
            text=[f"{v:.1f}%" for v in [row["cagr_1y"],row["cagr_3y"],row["cagr_5y"]]],
            textposition="auto", textfont=dict(size=13,color="white")
        ))
        fig15.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans",color="#c9d1d9"),
            margin=dict(l=10,r=10,t=40,b=10), height=300, showlegend=False,
            xaxis=dict(gridcolor="#1a2234"), yaxis=dict(gridcolor="#1a2234"),
            title=dict(text=f"{row['short_name']} — CAGR by Period", font=dict(color="#c9d1d9",size=13))
        )
        st.plotly_chart(fig15, use_container_width=True)

    with c2:
        m_labels = ["5Y CAGR","Volatility","Avg PE","Avg PB","Risk-Adj Ret"]
        raw_v  = [row["cagr_5y"],row["volatility"],row["avg_pe"],row["avg_pb"],row["risk_adjusted_return"]]
        max_v  = [df["cagr_5y"].max(),df["volatility"].max(),df["avg_pe"].max(),df["avg_pb"].max(),df["risk_adjusted_return"].max()]
        norm_v = [v/m*100 for v,m in zip(raw_v,max_v)]
        fig16 = go.Figure(go.Bar(
            x=norm_v, y=m_labels, orientation="h",
            marker=dict(color=norm_v, colorscale=[[0,"#1a2234"],[0.5,"#00d4ff"],[1,"#00ff88"]], showscale=False),
            text=[f"{v:.2f}" for v in raw_v], textposition="auto", textfont=dict(size=10,color="white")
        ))
        fig16.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans",color="#c9d1d9"),
            margin=dict(l=10,r=10,t=40,b=10), height=300, showlegend=False,
            xaxis=dict(range=[0,115],showgrid=False,tickfont=dict(size=9)),
            yaxis=dict(gridcolor="#1a2234",tickfont=dict(size=9)),
            title=dict(text="Relative Metric Strength (% of max)", font=dict(color="#c9d1d9",size=13))
        )
        st.plotly_chart(fig16, use_container_width=True)

    st.markdown("<div class='section-title'>Comparison vs Universe</div>", unsafe_allow_html=True)
    c_cols   = ["cagr_1y","cagr_3y","cagr_5y","volatility","avg_pe","avg_pb","risk_adjusted_return"]
    c_labels = ["1Y CAGR","3Y CAGR","5Y CAGR","Volatility","Avg PE","Avg PB","Risk-Adj Ret"]
    fig17 = go.Figure()
    fig17.add_trace(go.Bar(name="This Index",   x=c_labels, y=[row[c] for c in c_cols],
                            marker_color="#00d4ff", opacity=0.9))
    fig17.add_trace(go.Bar(name="Universe Avg", x=c_labels, y=[df[c].mean() for c in c_cols],
                            marker_color="#ffd700", opacity=0.7))
    fig17.add_trace(go.Scatter(name="Best in Class", x=c_labels, y=[df[c].max() for c in c_cols],
                                mode="lines+markers", line=dict(color="#ff6b35",dash="dash",width=1.5),
                                marker=dict(size=6)))
    apply(fig17, height=340, title=f"{sel_index} vs Universe",
          extra={"barmode":"group"})
    st.plotly_chart(fig17, use_container_width=True)

    rar_rank  = int(df["risk_adjusted_return"].rank(ascending=False).loc[df["index_name"]==sel_index].values[0])
    cagr_rank = int(df["cagr_5y"].rank(ascending=False).loc[df["index_name"]==sel_index].values[0])
    eff_txt   = ("Above-average efficiency — more return per unit of risk than the universe average."
                 if row["risk_adjusted_return"] > df["risk_adjusted_return"].mean()
                 else "Below-average efficiency — higher risk relative to returns vs the universe average.")
    st.markdown(f"""
    <div class="insight-card">
      <div class="tag">ANALYSIS</div><br>
      <b>{sel_index}</b> belongs to <b>{row['market_cap_category']}</b> with risk rated <b>{row['risk_level']}</b> (score: {row['risk_score']}/5).
      It delivers a 5Y CAGR of <b>{row['cagr_5y']}%</b> (ranked <b>#{cagr_rank}</b> of {len(df)})
      at volatility of <b>{row['volatility']}%</b>.
      Risk-adjusted return: <b>{row['risk_adjusted_return']:.3f}</b> (ranked #{rar_rank}). {eff_txt}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 6 — DATA TABLE
# ══════════════════════════════════════════════
with tab6:
    st.markdown("<div class='section-title'>Full Dataset — NSE Index Analytics FY2024-25</div>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([2,1])
    with col_s1:
        sort_col = st.selectbox("Sort by",
            ["cagr_5y","cagr_1y","risk_adjusted_return","valuation_score","volatility","avg_pe"], index=0)
    with col_s2:
        sort_asc = st.toggle("Ascending order", value=False)

    display_df = (df.drop(columns=["short_name"])
                    .sort_values(sort_col, ascending=sort_asc)
                    .reset_index(drop=True))

    def highlight_risk(val):
        c = {"Low":"#00ff88","Medium":"#00d4ff","High":"#ffd700",
             "Very High":"#ff6b35","Extreme":"#ff4d6d"}.get(val,"")
        return f"color:{c};font-weight:600;" if c else ""

    fmt = {
        "cagr_1y":"{:.1f}%","cagr_3y":"{:.1f}%","cagr_5y":"{:.1f}%",
        "volatility":"{:.1f}%","avg_pe":"{:.1f}","avg_pb":"{:.2f}",
        "risk_adjusted_return":"{:.3f}","valuation_score":"{:.1f}","index_level":"{:,}"
    }
    styled = (
        display_df.style
        .applymap(highlight_risk, subset=["risk_level"])
        .format(fmt)
        .set_properties(**{"background-color":"#0d1117","color":"#c9d1d9","border-color":"#1e2736"})
        .set_table_styles([
            {"selector":"th","props":[("background","#07090f"),("color","#00d4ff"),
                                       ("font-family","Space Mono,monospace"),
                                       ("font-size","0.68rem"),("letter-spacing","1px"),
                                       ("text-transform","uppercase"),
                                       ("border-bottom","2px solid #1e2736")]},
            {"selector":"tr:hover td","props":[("background-color","#111827")]}
        ])
    )
    st.dataframe(styled, use_container_width=True, height=500)

    st.markdown("<div class='section-title' style='margin-top:20px;'>SUMMARY STATISTICS</div>", unsafe_allow_html=True)
    num_cols = ["cagr_1y","cagr_3y","cagr_5y","volatility","avg_pe","avg_pb","risk_adjusted_return"]
    st.dataframe(
        df[num_cols].describe().round(2).style
        .set_properties(**{"background-color":"#0d1117","color":"#c9d1d9","border-color":"#1e2736"})
        .set_table_styles([{"selector":"th","props":[("background","#07090f"),("color","#7a8899")]}]),
        use_container_width=True
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#1e2736;margin:30px 0 12px;'>
<div style='text-align:center;font-size:0.68rem;color:#3d4f63;font-family:Space Mono,monospace;
            letter-spacing:1px;padding-bottom:20px;'>
  NSE MARKET INTELLIGENCE DASHBOARD · FY2024-25 · DATA: NSE INDIA<br>
  <span style='color:#1e2736;'>Built for analytical &amp; educational purposes only · Not investment advice</span>
</div>
""", unsafe_allow_html=True)