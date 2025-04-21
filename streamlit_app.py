import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import matplotlib.pyplot as plt
from datetime import datetime, time
from wordcloud import WordCloud
import base64
import re
import sqlite3
import os

# --- Custom CSS for dashboard look and dark mode toggle ---
st.markdown('''
    <style>
    body {background-color: #f4f6fa;}
    .main {background-color: #f4f6fa;}
    .st-emotion-cache-1v0mbdj {background: #181c25 !important; color: #fff !important;}
    .dashboard-title-box {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 16px #00000022;
        padding: 1.2rem 2rem 0.8rem 2rem;
        margin-bottom: 1rem;
        text-align: center;
    }
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a237e;
        margin-bottom: 0.3rem;
        text-shadow: none;
    }
    .dashboard-subtitle-box {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px #00000022;
        padding: 0.7rem 1.5rem 0.7rem 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .dashboard-subtitle {
        font-size: 1.2rem;
        color: #3949ab;
        margin-bottom: 0;
        text-shadow: none;
    }
    .section-header-box {
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 8px #00000022;
        padding: 0.5rem 1.2rem;
        margin-bottom: 1.2rem;
        display: inline-block;
    }
    .section-header {
        font-size: 1.15rem;
        font-weight: bold;
        color: #3949ab;
        margin: 0;
        text-shadow: none;
    }
    .stButton>button {
        background-color: #3949ab !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: 2px solid #fff !important;
        font-weight: bold !important;
        box-shadow: 0 2px 8px #181c2533;
        transition: background 0.2s, color 0.2s;
    }
    .stButton>button:hover {
        background-color: #5c6bc0 !important;
        color: #fff !important;
        border: 2px solid #3949ab !important;
    }
    .stFileUploader>div {background-color: #e9ecef; border-radius: 8px;}
    .stDataFrame {background: #fff; border-radius: 10px;}
    .st-expander {background: #f8f9fa; border-radius: 10px;}
    .stTabs [data-baseweb="tab-list"] {
        background: linear-gradient(90deg,#3949ab 0%,#5c6bc0 100%) !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 12px #3949ab33;
        padding: 0.3rem 0.3rem 0.3rem 0.3rem;
        margin-bottom: 1.3rem;
        display: flex;
        justify-content: center;
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #fff !important;
        background: #3949ab !important;
        border-radius: 12px 12px 0 0 !important;
        margin-right: 6px !important;
        font-weight: bold !important;
        font-size: 1.15rem !important;
        border: 2px solid #fff !important;
        box-shadow: 0 2px 8px #181c2533;
        padding: 0.5rem 1.4rem !important;
        transition: background 0.2s, color 0.2s, transform 0.15s;
        cursor: pointer;
        opacity: 0.85;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #5c6bc0 !important;
        color: #fff !important;
        transform: translateY(-2px) scale(1.04);
        opacity: 1;
    }
    .stTabs [aria-selected="true"] {
        background: #fff !important;
        color: #3949ab !important;
        border-bottom: 3px solid #3949ab !important;
        box-shadow: 0 4px 16px #3949ab33;
        opacity: 1;
        transform: scale(1.07);
        z-index: 2;
        position: relative;
    }
    .stTabs [aria-selected="false"] {
        opacity: 0.7;
    }
    .tab-desc {
        font-size: 0.95rem;
        color: #3949ab;
        text-align: center;
        margin-bottom: 1.3rem;
        margin-top: -0.7rem;
    }
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #3949ab !important;
        text-shadow: 1px 1px 2px #fff, 0 0 10px #000;
    }
    .stDownloadButton>button {
        background: linear-gradient(90deg, #3949ab 0%, #5c6bc0 100%) !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: 2px solid #fff !important;
        font-weight: bold !important;
        box-shadow: 0 2px 8px #181c2533;
    }
    .stDownloadButton>button:hover {
        background: linear-gradient(90deg, #5c6bc0 0%, #3949ab 100%) !important;
        color: #fff !important;
        border: 2px solid #3949ab !important;
    }
    /* Sidebar beautification */
    section[data-testid="stSidebar"] {
        background-color: #f4f6fa !important;
        box-shadow: none !important;
    }
    .sidebar-filter-box {
        background: rgba(220, 230, 250, 0.98);
        border-radius: 14px;
        box-shadow: 0 2px 12px #3949ab22;
        padding: 1.2rem 1.1rem 1.1rem 1.1rem;
        margin-bottom: 1.3rem;
        border: 1.5px solid #bfcbe3;
    }
    .sidebar-filter-label {
        color: #3949ab;
        font-weight: 600;
        font-size: 1.07rem;
        margin-bottom: 0.01rem;
        margin-top: 0.15rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .sidebar-filter-box .stMultiSelect, 
    .sidebar-filter-box .stTextInput, 
    .sidebar-filter-box .stDateInput, 
    .sidebar-filter-box .stTimeInput {
        margin-top: -0.25rem !important;
        margin-bottom: 0.22rem !important;
    }
    .sidebar-filter-box .stMultiSelect > div[data-baseweb],
    .sidebar-filter-box .stTextInput > div[data-baseweb],
    .sidebar-filter-box .stDateInput > div[data-baseweb],
    .sidebar-filter-box .stTimeInput > div[data-baseweb] {
        margin-top: -0.35rem !important;
        margin-bottom: 0.10rem !important;
    }
    .filter-logs-heading {
        font-size: 2.1rem;
        font-weight: 900;
        color: #1a4bb3 !important;
        letter-spacing: 1px;
        text-align: center;
        margin-bottom: 1.1rem;
        margin-top: 0rem;
        text-shadow: 0 2px 8px #3949ab11, 0 0 2px #fff;
    }
    section[data-testid="stSidebar"] input, section[data-testid="stSidebar"] textarea, section[data-testid="stSidebar"] select {
        background-color: #fff !important;
        color: #181c25 !important;
        border-radius: 7px !important;
        border: 1.5px solid #bfcbe3 !important;
    }
    </style>
''', unsafe_allow_html=True)

# --- Beautiful Brown Header (Top of App) with Shadow Text Effect ---
st.markdown('''
    <div style="width:100%;background:#5d4037;padding:0.6rem 0 0.4rem 0;margin-bottom:0.8rem;border-radius:0 0 16px 16px;box-shadow:0 2px 10px #0002;text-align:center;">
        <span style="font-size:2.1rem;font-weight:700;color:#fff;letter-spacing:1px;vertical-align:middle;
            text-shadow: 2px 2px 8px #3e2723, 0 2px 6px #0004;">
            📝 Log Analyzer
        </span>
    </div>
''', unsafe_allow_html=True)

# --- SQLite persistence helpers ---
@st.cache_data(show_spinner=False)
def load_logs_from_db():
    try:
        conn = sqlite3.connect("logs.db")
        df = pd.read_sql_query("SELECT * FROM logs", conn)
        conn.close()
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
        return df
    except Exception:
        return pd.DataFrame(columns=["Timestamp", "Level", "Message"])

# --- Ensure a directory for storing uploaded files ---
UPLOAD_DIR = "uploaded_logs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Sidebar: Filter Controls Only (Top-aligned, Clean) ---
with st.sidebar:
    st.markdown('<div class="sidebar-filter-box">\n  <div class="filter-logs-heading">🧰 Filter Logs</div>\n', unsafe_allow_html=True)
    with st.form("sidebar_filter_form", clear_on_submit=False):
        st.markdown('<div class="sidebar-filter-label">🔔 Log Levels</div>', unsafe_allow_html=True)
        level_filter = st.multiselect(
            label="",
            options=["INFO", "WARNING", "ERROR", "DEBUG"],
            default=[],
            help="Filter by log severity level.",
            key="level_multiselect"
        )
        st.markdown('<div class="sidebar-filter-label">🔍 Search by keyword</div>', unsafe_allow_html=True)
        keyword = st.text_input("", value="", help="Type to search log messages.", key="keyword_input")
        st.markdown('<div class="sidebar-filter-label">📅 Date range</div>', unsafe_allow_html=True)
        date_range = st.date_input("", value=[], key="date_range_input")
        col_time1, col_time2 = st.columns(2)
        with col_time1:
            st.markdown('<div class="sidebar-filter-label">⏰ Start</div>', unsafe_allow_html=True)
            start_time = st.time_input("", value=None, help="Start time for log filtering.", key="start_time_input")
        with col_time2:
            st.markdown('<div class="sidebar-filter-label">⏰ End</div>', unsafe_allow_html=True)
            end_time = st.time_input("", value=None, help="End time for log filtering.", key="end_time_input")
        submitted = st.form_submit_button("✅ Apply Filters", type="primary", help="Apply the selected filters.", use_container_width=True)
        if submitted:
            st.session_state['level_filter'] = level_filter
            st.session_state['keyword'] = keyword
            st.session_state['date_range'] = date_range
            st.session_state['start_time'] = start_time
            st.session_state['end_time'] = end_time
    st.markdown('</div>', unsafe_allow_html=True)

level_filter = st.session_state.get('level_filter', [])
keyword = st.session_state.get('keyword', "")
date_range = st.session_state.get('date_range', [])
start_time = st.session_state.get('start_time', None)
end_time = st.session_state.get('end_time', None)

# --- Upload file and show prompt if not uploaded ---
uploaded_file = st.file_uploader(
    "Choose a .log or .txt file",
    type=["log", "txt"],
    help="Format: YYYY-MM-DD HH:MM:SS LEVEL Message"
)

# Show uploaded file info with grey background
if uploaded_file:
    st.markdown(f'''
        <div style="background:#e3e6eb;padding:1rem 1.5rem;border-radius:10px;margin-bottom:1.2rem;display:flex;align-items:center;gap:1rem;">
            <span style="font-size:1.8rem;color:#3949ab;">🗂️</span>
            <span style="font-size:1.08rem;color:#222;font-weight:600;">{uploaded_file.name}</span>
            <span style="font-size:0.98rem;color:#555;">{round(uploaded_file.size/1024,2)} KB</span>
        </div>
    ''', unsafe_allow_html=True)

if uploaded_file:
    st.session_state['uploaded_file'] = uploaded_file
    # Save the uploaded file to disk for persistent storage
    file_save_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    lines = stringio.readlines()
    data = []
    skipped_lines = 0
    log_patterns = [
        r'^(?P<date>\d{4}-\d{2}-\d{2})[ T](?P<time>\d{2}:\d{2}:\d{2})\s+(?P<level>[A-Z]+)\s+(?P<msg>.+)$',
        r'^(?P<date>\d{4}-\d{2}-\d{2})[T ](?P<time>\d{2}:\d{2}:\d{2})(Z)?\s*\[?(?P<level>[A-Z]+)\]?\s*:?.*?(?P<msg>.+)$',
        r'^\[?(?P<date>\d{4}-\d{2}-\d{2})[ T](?P<time>\d{2}:\d{2}:\d{2})\]?\s*\[?(?P<level>[A-Z]+)\]?\s*:?.*?(?P<msg>.+)$',
        r'^(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<level>[A-Z]+)\s+(?P<msg>.+)$',
        r'^(?P<level>[A-Z]+)\s+(?P<date>\d{4}-\d{2}-\d{2})[ T](?P<time>\d{2}:\d{2}:\d{2})\s+(?P<msg>.+)$',
    ]
    for line in lines:
        line = line.strip()
        if not line:
            continue
        matched = False
        for pat in log_patterns:
            match = re.match(pat, line)
            if match:
                gd = match.groupdict()
                # Compose timestamp
                if 'date' in gd and 'time' in gd:
                    ts_str = f"{gd['date']} {gd['time']}"
                elif 'time' in gd:
                    ts_str = f"{datetime.now().date()} {gd['time']}"
                else:
                    ts_str = None
                try:
                    timestamp = pd.to_datetime(ts_str, errors='coerce') if ts_str else None
                    level = gd.get('level', '').upper()
                    message = gd.get('msg', '')
                    data.append({"Timestamp": timestamp, "Level": level, "Message": message})
                    matched = True
                    break
                except Exception:
                    continue
        if not matched:
            skipped_lines += 1
    df = pd.DataFrame(data)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])
    # Save to SQLite
    try:
        conn = sqlite3.connect("logs.db")
        df.to_sql("logs", conn, if_exists='replace', index=False)
        conn.close()
    except Exception as e:
        st.warning(f"Could not save logs to DB: {e}")
else:
    df = load_logs_from_db()

# Always ensure Timestamp is datetime before using .dt
if not df.empty:
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# --- Apply filters safely ---
if level_filter:
    df = df[df['Level'].isin(level_filter)]
if isinstance(keyword, str) and keyword.strip():
    df = df[df['Message'].astype(str).str.contains(keyword, case=False, na=False)]
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df['Timestamp'].dt.date >= start_date.date()) & (df['Timestamp'].dt.date <= end_date.date())]
from datetime import time as dt_time
safe_start_time = start_time or dt_time(0, 0)
safe_end_time = end_time or dt_time(23, 59, 59)
if not df.empty:
    # Only filter on .dt.time if Timestamp is datetimelike
    df = df[pd.to_datetime(df['Timestamp'], errors='coerce').dt.time.between(safe_start_time, safe_end_time)]

if df.empty:
    st.warning("No log entries after applying filters. Try relaxing your filters.")

# --- Metrics ---
st.markdown("---")
colA, colB, colC = st.columns(3)
colA.metric("Total Logs", len(df))
colB.metric("Unique Errors", df[df['Level']=="ERROR"]["Message"].nunique())
colC.metric("Most Frequent Level", df['Level'].mode()[0] if not df.empty else "-")

# --- Expander for Errors/Warnings ---
with st.expander("🔴 Recent Errors & Warnings", expanded=True):
    recent_issues = df[df['Level'].isin(['ERROR', 'WARNING'])].sort_values('Timestamp', ascending=False).head(5)
    if recent_issues.empty:
        st.success("No recent errors or warnings!")
    else:
        for _, row in recent_issues.iterrows():
            st.error(f"{row['Timestamp']} [{row['Level']}] {row['Message']}")

# --- Tabs for Visualizations ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Bar Chart",
    "🥧 Pie Chart",
    "📈 Time Chart",
    "☁️ Word Cloud"
])

with tab1:
    st.markdown('<div class="section-header-box"><span class="section-header">📊 Log Level Counts (Bar Chart)</span></div>', unsafe_allow_html=True)
    level_counts = df['Level'].value_counts().reset_index()
    level_counts.columns = ['Level', 'Count']
    fig_bar = px.bar(level_counts, x='Level', y='Count', color='Level', text='Count',
                    color_discrete_sequence=px.colors.qualitative.Dark24)
    fig_bar.update_layout(showlegend=False, plot_bgcolor='#f4f6fa')
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header-box"><span class="section-header">🥧 Log Level Distribution (Pie Chart)</span></div>', unsafe_allow_html=True)
    fig_pie = px.pie(level_counts, names='Level', values='Count',
                    color_discrete_sequence=px.colors.qualitative.Dark24,
                    hole=0.4)
    fig_pie.update_traces(textinfo='percent+label', pull=[0.05]*len(level_counts))
    fig_pie.update_layout(showlegend=True, plot_bgcolor='#f4f6fa')
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header-box"><span class="section-header">📈 Log Entries Over Time (Line Chart)</span></div>', unsafe_allow_html=True)
    if not df.empty:
        df['Minute'] = df['Timestamp'].dt.floor('T')
        timeline = df.groupby('Minute').size().reset_index(name='Count')
        fig_line = px.line(timeline, x='Minute', y='Count', markers=True,
                          labels={'Minute': 'Timestamp (minute)', 'Count': 'Log Entries'},
                          color_discrete_sequence=['#007bff'])
        fig_line.update_layout(plot_bgcolor='#f4f6fa')
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No log data available for timeline chart.")

with tab4:
    st.markdown('<div class="section-header-box"><span class="section-header">☁️ Word Cloud of Log Messages</span></div>', unsafe_allow_html=True)
    if not df.empty:
        text = ' '.join(df['Message'].dropna().tolist())
        if text:
            wordcloud = WordCloud(width=800, height=200, background_color='white').generate(text)
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("No messages to generate word cloud.")

# --- Data Table & Export ---
st.markdown("---")
st.markdown('<div class="section-header-box"><span class="section-header">🗂️ Log Entries Table & Export</span></div>', unsafe_allow_html=True)
st.dataframe(df[['Timestamp', 'Level', 'Message']], use_container_width=True, height=350)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Logs as CSV", data=csv, file_name="filtered_logs.csv", mime="text/csv")
