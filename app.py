import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Credit Card Fraud Analytics & Risk Intelligence",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cute minimalist styling
st.markdown("""
    <style>
    /* Bubble animation on click */
    @keyframes bubbleUp {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.6); opacity: 0.5; }
        100% { transform: scale(2); opacity: 0; }
    }
    
    .stButton>button:active::after {
        content: '';
        position: absolute;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: rgba(255, 182, 193, 0.6);
        animation: bubbleUp 0.5s ease-out forwards;
        pointer-events: none;
    }
    
    .stButton>button { position: relative; overflow: visible; }
    
    /* Bubble burst on any clickable card */
    .stMetric:active::after,
    .stTabs [data-baseweb="tab"]:active::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: rgba(255, 182, 193, 0.5);
        animation: bubbleUp 0.4s ease-out forwards;
        top: 50%;
        left: 50%;
        pointer-events: none;
    }
    
    .stMetric, .stTabs [data-baseweb="tab"] { position: relative; overflow: visible; }
    </style>
    <style>
    /* Cute Custom Styling for dashboard */
    
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
        background-color: #FDFBF7; /* Soft vanilla paper-style background */
    }
    
    /* Cute & Minimal Metric cards */
    .stMetric {
        background: #ffffff;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 6px 20px rgba(255, 182, 193, 0.12); /* Soft pinkish shadow */
        border: 2px solid #FFE4E1; /* Misty Rose border */
        transition: all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .stMetric:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 28px rgba(255, 182, 193, 0.22);
        border: 2px solid #FFB6C1; /* Light Pink hover border */
    }
    
    /* Metric values cute bold */
    .stMetric [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #4A4A4A !important;
        font-family: 'Quicksand', 'Nunito', sans-serif;
    }
    
    /* Style metric labels */
    .stMetric [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 700 !important;
        color: #7A7A7A !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Standard Title with cute looks */
    h1 {
        color: #FF7482;
        text-align: center;
        padding: 15px;
        font-weight: 800;
        font-size: 2.5em;
        font-family: 'Quicksand', 'Nunito', sans-serif;
    }
    
    /* Sidebar styling - soft cream/pink border */
    [data-testid="stSidebar"] {
        background: #FFF9FA;
        box-shadow: 2px 0 12px rgba(255, 182, 193, 0.1);
        border-right: 2px solid #FFE4E1;
    }
    
    [data-testid="stSidebar"] * {
        color: #4A4A4A !important;
    }
    
    /* Cute Expander */
    .streamlit-expander {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 2px solid #FFE4E1 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02) !important;
    }
    
    /* Cute Tab layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: #FFF2F6; /* Soft Rose */
        padding: 8px;
        border-radius: 16px;
        border: 2px solid #FFE4E1;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 12px;
        padding: 8px 16px;
        color: #6A6A6A;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #FF7482 !important;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.2) !important;
    }
    
    /* Alert cards minimalist colors */
    .fraud-alert {
        background: #FFF5F5;
        color: #D64545;
        padding: 15px;
        border-radius: 14px;
        margin: 12px 0;
        border: 2px solid #FFCDCD;
        font-weight: 600;
    }
    
    .safe-alert {
        background: #F5FFF5;
        color: #2D8A2D;
        padding: 15px;
        border-radius: 14px;
        margin: 12px 0;
        border: 2px solid #CDFFCD;
        font-weight: 600;
    }
    
    /* Button Cute Pill shape */
    .stButton>button {
        background: #FFB6C1; /* Soft pink */
        color: #ffffff;
        border: none;
        border-radius: 25px;
        padding: 8px 28px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(255, 182, 193, 0.35);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #FF9EB4;
        transform: scale(1.04);
        box-shadow: 0 6px 15px rgba(255, 182, 193, 0.5);
    }
    
    /* Chart container rounding soft border */
    .js-plotly-plot {
        border-radius: 16px !important;
        background: #ffffff !important;
        border: 2px solid #FDF0F4;
        overflow: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    """Load and prepare the dataset"""
    df = pd.read_csv('final_dataset.csv')
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['transaction_month'] = df['transaction_date'].dt.to_period('M').astype(str)
    df['transaction_hour'] = df['transaction_date'].dt.hour
    return df

# Main app
def main():
    # Hero Section with animated credit card backgrounds
    import streamlit.components.v1 as components
    
    hero_html = """
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@600;700;800&family=Nunito:wght@600;700&display=swap" rel="stylesheet">
    <style>
        @keyframes floatCard {
            0%, 100% { transform: rotateY(-8deg) rotateX(4deg) translateY(0px); }
            50% { transform: rotateY(-4deg) rotateX(8deg) translateY(-15px); }
        }
        
        @keyframes floatCard2 {
            0%, 100% { transform: rotateY(6deg) rotateX(-3deg) translateY(0px); }
            50% { transform: rotateY(10deg) rotateX(3deg) translateY(-12px); }
        }
        
        @keyframes floatCard3 {
            0%, 100% { transform: rotateY(-5deg) rotateX(6deg) translateY(0px); }
            50% { transform: rotateY(3deg) rotateX(-4deg) translateY(-10px); }
        }
        
        @keyframes wordPop {
            0% { opacity: 0; transform: translateY(20px) scale(0.7); filter: blur(4px); }
            100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
        }
        
        @keyframes subtitleSlide {
            0% { opacity: 0; transform: translateX(-30px); }
            100% { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes descFade {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        
        .hero-wrapper {
            position: relative;
            background: linear-gradient(135deg, #FFF0F5 0%, #FFF8FA 40%, #FFFDF5 100%);
            padding: 55px 30px;
            border-radius: 28px;
            box-shadow: 0 20px 60px rgba(255,182,193,0.2), 0 4px 15px rgba(0,0,0,0.04);
            text-align: center;
            overflow: hidden;
            min-height: 320px;
            border: 3px solid #FFE4E1;
            perspective: 800px;
        }
        
        .card-3d {
            position: absolute;
            width: 220px;
            height: 138px;
            border-radius: 18px;
            border: 2px solid rgba(255,255,255,0.6);
            transform-style: preserve-3d;
            backface-visibility: hidden;
        }
        
        .card-3d .card-face {
            width: 100%;
            height: 100%;
            border-radius: 18px;
            position: relative;
            overflow: hidden;
        }
        
        .card-3d .chip {
            position: absolute;
            width: 38px;
            height: 28px;
            background: linear-gradient(135deg, #FFD700, #FFED80);
            border-radius: 5px;
            top: 32px;
            left: 22px;
            opacity: 0.7;
        }
        
        .card-3d .dots {
            position: absolute;
            bottom: 28px;
            left: 22px;
            color: rgba(255,255,255,0.7);
            font-size: 14px;
            letter-spacing: 3px;
            font-family: 'Courier New', monospace;
        }
        
        .card-a {
            background: linear-gradient(135deg, #FFB6C1, #FF8FA3);
            top: 8%;
            right: 6%;
            animation: floatCard 6s ease-in-out infinite;
            opacity: 0.35;
            box-shadow: 0 15px 40px rgba(255,143,163,0.25);
        }
        
        .card-b {
            background: linear-gradient(135deg, #DCD0FF, #B8A9E8);
            bottom: 8%;
            left: 4%;
            animation: floatCard2 7s ease-in-out infinite;
            opacity: 0.3;
            box-shadow: 0 15px 40px rgba(184,169,232,0.2);
        }
        
        .card-c {
            background: linear-gradient(135deg, #B5EAD7, #8FD3B6);
            top: 40%;
            left: 60%;
            animation: floatCard3 8s ease-in-out infinite;
            opacity: 0.2;
            box-shadow: 0 12px 35px rgba(143,211,182,0.15);
            width: 180px;
            height: 112px;
        }
        
        .hero-text {
            position: relative;
            z-index: 10;
        }
        
        .hero-title {
            font-size: 2.8em;
            color: #FF7482;
            margin: 0;
            padding: 5px;
            font-weight: 800;
            font-family: 'Quicksand', sans-serif;
        }
        
        .hero-title .word {
            display: inline-block;
            opacity: 0;
            animation: wordPop 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28) forwards;
        }
        
        .hero-subtitle {
            color: #FFA4B1;
            font-size: 1.4em;
            margin: 10px 0;
            font-weight: 700;
            font-family: 'Nunito', sans-serif;
            opacity: 0;
            animation: subtitleSlide 0.6s ease forwards;
            animation-delay: 1.8s;
        }
        
        .hero-desc {
            color: #888;
            font-size: 1em;
            margin: 14px 0 0 0;
            font-weight: 600;
            font-family: 'Nunito', sans-serif;
            opacity: 0;
            animation: descFade 0.8s ease forwards;
            animation-delay: 2.3s;
        }
    </style>
    
    <div class='hero-wrapper'>
        <div class='card-3d card-a'>
            <div class='card-face'>
                <div class='chip'></div>
                <div class='dots'>&bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull;</div>
            </div>
        </div>
        
        <div class='card-3d card-b'>
            <div class='card-face'>
                <div class='chip'></div>
                <div class='dots'>&bull;&bull;&bull;&bull; &bull;&bull;&bull;&bull;</div>
            </div>
        </div>
        
        <div class='card-3d card-c'>
            <div class='card-face'></div>
        </div>
        
        <div class='hero-text'>
            <h1 class='hero-title' id='heroTitle'></h1>
            <h2 class='hero-subtitle'>Risk Intelligence Center</h2>
            <p class='hero-desc'>Real-time simulated fraud detection dashboard</p>
        </div>
    </div>
    
    <script>
        // Word-by-word reveal for hero title
        const words = [String.fromCodePoint(0x1F338), 'Credit', 'Card', 'Fraud', 'Analytics'];
        const titleEl = document.getElementById('heroTitle');
        words.forEach((word, i) => {
            const span = document.createElement('span');
            span.className = 'word';
            span.textContent = word + ' ';
            span.style.animationDelay = (i * 0.28) + 's';
            titleEl.appendChild(span);
        });
    </script>
    """
    
    components.html(hero_html, height=380)
    
    # Load data
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure 'final_dataset.csv' is in the same directory as this app.")
        return
    
    # Enhanced Sidebar with collapsible filters
    st.sidebar.markdown("### 🎛️ Filter Controls")
    st.sidebar.markdown("---")
    
    # Date Range Filter with expander
    with st.sidebar.expander("📅 DATE RANGE FILTER", expanded=True):
        date_range = st.date_input(
            "Select Transaction Period",
            value=(df['transaction_date'].min(), df['transaction_date'].max()),
            min_value=df['transaction_date'].min(),
            max_value=df['transaction_date'].max(),
            help="Filter transactions by date range"
        )
        st.caption(f"📊 {(date_range[1] - date_range[0]).days} days selected")
    
    # Merchant Category Filter with expander
    with st.sidebar.expander("🏪 MERCHANT CATEGORY", expanded=False):
        select_all_merchants = st.checkbox("Select All Categories", value=True, key="merchant_all")
        if select_all_merchants:
            merchant_categories = df['merchant_category'].unique().tolist()
        else:
            merchant_categories = st.multiselect(
                "Choose categories",
                options=df['merchant_category'].unique(),
                default=df['merchant_category'].unique()
            )
        st.caption(f"✅ {len(merchant_categories)} categories selected")
    
    # Risk Segment Filter with expander
    with st.sidebar.expander("⚠️ RISK SEGMENT", expanded=False):
        select_all_risk = st.checkbox("Select All Risk Levels", value=True, key="risk_all")
        if select_all_risk:
            risk_segments = df['risk_segment'].unique().tolist()
        else:
            risk_segments = st.multiselect(
                "Choose risk levels",
                options=df['risk_segment'].unique(),
                default=df['risk_segment'].unique()
            )
        risk_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        risk_display = " ".join([risk_colors.get(r, "⚪") for r in risk_segments])
        st.caption(f"{risk_display} {len(risk_segments)} levels selected")
    
    # Transaction Type Filter with expander
    with st.sidebar.expander("💳 TRANSACTION TYPE", expanded=False):
        select_all_types = st.checkbox("Select All Types", value=True, key="type_all")
        if select_all_types:
            transaction_types = df['transaction_type'].unique().tolist()
        else:
            transaction_types = st.multiselect(
                "Choose transaction types",
                options=df['transaction_type'].unique(),
                default=df['transaction_type'].unique()
            )
        type_icons = {"Online": "🌐", "POS": "🏪", "ATM": "🏧"}
        type_display = " ".join([type_icons.get(t, "💳") for t in transaction_types])
        st.caption(f"{type_display} {len(transaction_types)} types selected")
    
    # Apply filters
    filtered_df = df[
        (df['transaction_date'].dt.date >= date_range[0]) &
        (df['transaction_date'].dt.date <= date_range[1]) &
        (df['merchant_category'].isin(merchant_categories)) &
        (df['risk_segment'].isin(risk_segments)) &
        (df['transaction_type'].isin(transaction_types))
    ]
    
    # Key Metrics Section with white background
    st.markdown("""
        <div style='
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        '>
    """, unsafe_allow_html=True)
    
    st.header("📊 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_transactions = len(filtered_df)
    total_fraud = filtered_df['is_fraud'].sum()
    fraud_rate = (total_fraud / total_transactions * 100) if total_transactions > 0 else 0
    total_amount = filtered_df['transaction_amount'].sum()
    avg_risk_score = filtered_df['fraud_risk_score'].mean()
    
    with col1:
        st.metric("Total Transactions", f"{total_transactions:,}")
    
    with col2:
        st.metric("Fraudulent Cases", f"{total_fraud:,}", delta=f"{fraud_rate:.2f}%", delta_color="inverse")
    
    with col3:
        st.metric("Total Amount", f"${total_amount:,.2f}")
    
    with col4:
        fraud_amount = filtered_df[filtered_df['is_fraud'] == 1]['transaction_amount'].sum()
        st.metric("Fraud Amount", f"${fraud_amount:,.2f}", delta=f"{(fraud_amount/total_amount*100):.2f}%", delta_color="inverse")
    
    with col5:
        st.metric("Avg Risk Score", f"{avg_risk_score:.2f}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tabs Section with white background
    st.markdown("""
        <div style='
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-top: 20px;
        '>
    """, unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🌸 Overview", "🔍 Fraud Patterns", "👤 Customer Vibes", "🌍 Geo Insights", "🛡️ Risk Radar", "💡 Live Simulator"])
    
    # Tab 1: Overview
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Fraud vs Non-Fraud Distribution
            st.subheader("🍩 Fraud vs Legit Transactions")
            fraud_counts = filtered_df['is_fraud'].value_counts()
            fig = go.Figure(data=[go.Pie(
                labels=['Legitimate', 'Fraudulent'],
                values=[fraud_counts.get(0, 0), fraud_counts.get(1, 0)],
                hole=0.4,
                marker_colors=['#A1E3B5', '#FF9E9E']
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            # Transaction Amount Distribution
            st.subheader("💰 How Much Are People Spending?")
            fig = px.histogram(
                filtered_df,
                x='transaction_amount',
                color='is_fraud',
                nbins=50,
                labels={'is_fraud': 'Fraud Status', 'transaction_amount': 'Amount ($)'},
                color_discrete_map={0: '#A1E3B5', 1: '#FF9E9E'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        # Time series analysis
        st.subheader("Transaction Trends Over Time")
        daily_transactions = filtered_df.groupby(filtered_df['transaction_date'].dt.date).agg({
            'transaction_id': 'count',
            'is_fraud': 'sum'
        }).reset_index()
        daily_transactions.columns = ['date', 'total_transactions', 'fraud_count']
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=daily_transactions['date'], y=daily_transactions['total_transactions'],
                      name="Total Transactions", line=dict(color='#1f77b4')),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=daily_transactions['date'], y=daily_transactions['fraud_count'],
                      name="Fraud Cases", line=dict(color='#FF7482')),
            secondary_y=True
        )
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Total Transactions", secondary_y=False)
        fig.update_yaxes(title_text="Fraud Cases", secondary_y=True)
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    # Tab 2: Fraud Analysis
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Fraud by Merchant Category
            st.subheader("🏪 Which Shops Get Targeted?")
            fraud_by_merchant = filtered_df.groupby('merchant_category').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_merchant.columns = ['merchant_category', 'fraud_count', 'total_count']
            fraud_by_merchant['fraud_rate'] = (fraud_by_merchant['fraud_count'] / fraud_by_merchant['total_count'] * 100)
            
            fig = px.bar(
                fraud_by_merchant.sort_values('fraud_rate', ascending=False),
                x='merchant_category',
                y='fraud_rate',
                color='fraud_rate',
                color_continuous_scale='RdPu',
                labels={'fraud_rate': 'Fraud Rate (%)', 'merchant_category': 'Category'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            # Fraud by Transaction Type
            st.subheader("📳 Online vs POS vs ATM")
            fraud_by_type = filtered_df.groupby('transaction_type').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_type.columns = ['transaction_type', 'fraud_count', 'total_count']
            fraud_by_type['fraud_rate'] = (fraud_by_type['fraud_count'] / fraud_by_type['total_count'] * 100)
            
            fig = px.bar(
                fraud_by_type,
                x='transaction_type',
                y='fraud_count',
                color='fraud_rate',
                color_continuous_scale='Pinkyl',
                labels={'fraud_count': 'Fraud Count', 'transaction_type': 'Type', 'fraud_rate': 'Fraud Rate (%)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        # Risk Score vs Actual Fraud
        st.subheader("🎯 Risk Score: Safe vs Fraud")
        fig = px.box(
            filtered_df,
            x='is_fraud',
            y='fraud_risk_score',
            color='is_fraud',
            labels={'is_fraud': 'Fraud Status', 'fraud_risk_score': 'Risk Score'},
            color_discrete_map={0: '#A1E3B5', 1: '#FF9E9E'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
        
        # Hourly fraud pattern
        st.subheader("🕰️ When Do Frauds Happen?")
        hourly_fraud = filtered_df.groupby('transaction_hour').agg({
            'is_fraud': ['sum', 'count']
        }).reset_index()
        hourly_fraud.columns = ['hour', 'fraud_count', 'total_count']
        hourly_fraud['fraud_rate'] = (hourly_fraud['fraud_count'] / hourly_fraud['total_count'] * 100)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hourly_fraud['hour'],
            y=hourly_fraud['fraud_rate'],
            mode='lines+markers',
            line=dict(color='#FF7482', width=3),
            marker=dict(size=8),
            fill='tozeroy'
        ))
        fig.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Fraud Rate (%)",
            height=400,
            xaxis=dict(tickmode='linear', tick0=0, dtick=1)
        )
        st.plotly_chart(fig, width="stretch")
    
    # Tab 3: Customer Insights
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Fraud by Income Band
            st.subheader("💳 Income Band → Fraud Trend")
            fraud_by_income = filtered_df.groupby('income_band').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_income.columns = ['income_band', 'fraud_count', 'total_count']
            fraud_by_income['fraud_rate'] = (fraud_by_income['fraud_count'] / fraud_by_income['total_count'] * 100)
            
            fig = px.bar(
                fraud_by_income,
                x='income_band',
                y='fraud_count',
                color='fraud_rate',
                color_continuous_scale='Pinkyl',
                labels={'fraud_count': 'Fraud Count', 'income_band': 'Income Band', 'fraud_rate': 'Fraud Rate (%)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            # Fraud by Risk Segment
            st.subheader("🧩 Risk Segment Breakdown")
            fraud_by_risk = filtered_df.groupby('risk_segment').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_risk.columns = ['risk_segment', 'fraud_count', 'total_count']
            fraud_by_risk['fraud_rate'] = (fraud_by_risk['fraud_count'] / fraud_by_risk['total_count'] * 100)
            
            fig = go.Figure(data=[go.Pie(
                labels=fraud_by_risk['risk_segment'],
                values=fraud_by_risk['fraud_count'],
                hole=0.4,
                marker_colors=['#FF9E9E', '#FFE5A3', '#A1E3B5']
            )])
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        # Credit Score vs Fraud
        st.subheader("📊 Credit Score vs Fraud Tendency")
        fig = px.histogram(
            filtered_df,
            x='credit_score',
            color='is_fraud',
            nbins=50,
            labels={'is_fraud': 'Fraud Status', 'credit_score': 'Credit Score'},
            color_discrete_map={0: '#A1E3B5', 1: '#FF9E9E'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
        
        # Age vs Fraud
        st.subheader("🎂 Age Group Insights")
        fig = px.box(
            filtered_df,
            x='is_fraud',
            y='age',
            color='is_fraud',
            labels={'is_fraud': 'Fraud Status', 'age': 'Age'},
            color_discrete_map={0: '#A1E3B5', 1: '#FF9E9E'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
    
    # Tab 4: Geographic Analysis
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Fraud by Home Country
            st.subheader("🏠 Home Country Fraud Map")
            fraud_by_country = filtered_df.groupby('home_country').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_country.columns = ['country', 'fraud_count', 'total_count']
            fraud_by_country['fraud_rate'] = (fraud_by_country['fraud_count'] / fraud_by_country['total_count'] * 100)
            
            fig = px.bar(
                fraud_by_country.sort_values('fraud_count', ascending=False),
                x='country',
                y='fraud_count',
                color='fraud_rate',
                color_continuous_scale='Pinkyl',
                labels={'fraud_count': 'Fraud Count', 'country': 'Country', 'fraud_rate': 'Fraud Rate (%)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        with col2:
            # Fraud by Merchant Country
            st.subheader("🌍 Merchant Country Fraud Map")
            fraud_by_merchant_country = filtered_df.groupby('merchant_country_x').agg({
                'is_fraud': ['sum', 'count']
            }).reset_index()
            fraud_by_merchant_country.columns = ['country', 'fraud_count', 'total_count']
            fraud_by_merchant_country['fraud_rate'] = (fraud_by_merchant_country['fraud_count'] / fraud_by_merchant_country['total_count'] * 100)
            
            fig = px.bar(
                fraud_by_merchant_country.sort_values('fraud_count', ascending=False),
                x='country',
                y='fraud_count',
                color='fraud_rate',
                color_continuous_scale='Pinkyl',
                labels={'fraud_count': 'Fraud Count', 'country': 'Country', 'fraud_rate': 'Fraud Rate (%)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")
        
        # Foreign Transaction Analysis
        st.subheader("✈️ Foreign vs Domestic Vibes")
        foreign_fraud = filtered_df.groupby('is_foreign_transaction').agg({
            'is_fraud': ['sum', 'count']
        }).reset_index()
        foreign_fraud.columns = ['is_foreign', 'fraud_count', 'total_count']
        foreign_fraud['fraud_rate'] = (foreign_fraud['fraud_count'] / foreign_fraud['total_count'] * 100)
        foreign_fraud['transaction_type'] = foreign_fraud['is_foreign'].map({0: 'Domestic', 1: 'Foreign'})
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Legitimate',
            x=foreign_fraud['transaction_type'],
            y=foreign_fraud['total_count'] - foreign_fraud['fraud_count'],
            marker_color='#A1E3B5'
        ))
        fig.add_trace(go.Bar(
            name='Fraudulent',
            x=foreign_fraud['transaction_type'],
            y=foreign_fraud['fraud_count'],
            marker_color='#FF7482'
        ))
        fig.update_layout(barmode='stack', height=400, yaxis_title='Transaction Count')
        st.plotly_chart(fig, width="stretch")
    
    # Tab 5: Risk Intelligence
    with tab5:
        st.subheader("🎯 High-Risk Watch")
        
        # Define risk threshold
        risk_threshold = st.slider("Risk Score Threshold", 0.0, 5.0, 1.0, 0.1)
        
        high_risk_transactions = filtered_df[filtered_df['fraud_risk_score'] >= risk_threshold]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("High-Risk Transactions", f"{len(high_risk_transactions):,}")
        with col2:
            st.metric("High-Risk Amount", f"${high_risk_transactions['transaction_amount'].sum():,.2f}")
        with col3:
            actual_fraud_in_high_risk = high_risk_transactions['is_fraud'].sum()
            st.metric("Actual Frauds", f"{actual_fraud_in_high_risk:,}")
        
        # Risk Score Heatmap
        st.subheader("🗺️ Risk Heatmap: Category × Type")
        heatmap_data = filtered_df.pivot_table(
            values='fraud_risk_score',
            index='merchant_category',
            columns='transaction_type',
            aggfunc='mean'
        )
        
        fig = px.imshow(
            heatmap_data,
            labels=dict(x="Transaction Type", y="Merchant Category", color="Avg Risk Score"),
            color_continuous_scale='Pinkyl',
            aspect="auto"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width="stretch")
        
        # Top Risky Transactions
        st.subheader("🚨 Top 20 Riskiest Transactions")
        top_risky = filtered_df.nlargest(20, 'fraud_risk_score')[
            ['transaction_id', 'transaction_date', 'customer_id', 'merchant_category',
             'transaction_amount', 'fraud_risk_score', 'is_fraud', 'risk_segment']
        ].copy()
        
        # Add visual indicator
        top_risky['status'] = top_risky['is_fraud'].map({0: '✅ Safe', 1: '⚠️ Fraud'})
        
        st.dataframe(
            top_risky.style.background_gradient(subset=['fraud_risk_score'], cmap='RdPu'),
            width="stretch",
            height=400
        )
        
        # Merchant Risk Analysis
        st.subheader("🏪 Merchant Risk Bubble Chart")
        merchant_risk = filtered_df.groupby('merchant_category').agg({
            'merchant_risk_score': 'mean',
            'fraud_risk_score': 'mean',
            'is_fraud': ['sum', 'count']
        }).reset_index()
        merchant_risk.columns = ['merchant_category', 'avg_merchant_risk', 'avg_fraud_risk', 'fraud_count', 'total_count']
        merchant_risk['fraud_rate'] = (merchant_risk['fraud_count'] / merchant_risk['total_count'] * 100)
        
        fig = px.scatter(
            merchant_risk,
            x='avg_merchant_risk',
            y='avg_fraud_risk',
            size='fraud_count',
            color='fraud_rate',
            hover_data=['merchant_category', 'fraud_count'],
            labels={
                'avg_merchant_risk': 'Average Merchant Risk Score',
                'avg_fraud_risk': 'Average Fraud Risk Score',
                'fraud_rate': 'Fraud Rate (%)'
            },
            color_continuous_scale='Pinkyl'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, width="stretch")
    
    # Tab 6: Live Simulation Center
    with tab6:
        st.subheader("💡 Live Transaction Tester")
        
        sim_mode = st.radio("Choose Simulation Mode", ["Manual Input Prediction", "Auto-Streaming Ticker (Mock)"])
        
        import joblib
        try:
            model = joblib.load('fraud_model.joblib')
            encoders = joblib.load('encoders.joblib')
        except:
            st.error("Model artifacts not found! Please run 'python train_live_model.py' first.")
            st.stop()
            
        if sim_mode == "Manual Input Prediction":
            st.markdown("### ✍️ Build Your Own Transaction")
            col1, col2 = st.columns(2)
            
            with col1:
                amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=150.0)
                merchant = st.selectbox("Merchant Category", options=encoders['merchant_category'].classes_)
                txn_type = st.selectbox("Transaction Type", options=encoders['transaction_type'].classes_)
                m_country = st.selectbox("Merchant Country", options=encoders['merchant_country_x'].classes_)
                hours_since = st.number_input("Hours Since Last Transaction", min_value=0, value=5)
            with col2:
                age = st.number_input("Customer Age", min_value=18, max_value=100, value=35)
                income = st.selectbox("Income Band", options=encoders['income_band'].classes_)
                credit = st.number_input("Credit Score", min_value=300, max_value=850, value=700)
                home = st.selectbox("Customer Home Country", options=encoders['home_country'].classes_)
                avg_val = st.number_input("Avg Transaction Value for Customer ($)", min_value=1.0, value=200.0)
                m_risk = st.number_input("Merchant Risk Score", min_value=0.0, max_value=1.0, value=0.1)
                is_foreign = 1 if m_country != home else 0
                
            if st.button("🌸 Check This Transaction"):
                # Encode
                encoded_data = {
                    'merchant_category': encoders['merchant_category'].transform([merchant])[0],
                    'transaction_type': encoders['transaction_type'].transform([txn_type])[0],
                    'merchant_country_x': encoders['merchant_country_x'].transform([m_country])[0],
                    'income_band': encoders['income_band'].transform([income])[0],
                    'home_country': encoders['home_country'].transform([home])[0],
                    'transaction_amount': amount,
                    'hours_since_last_txn': hours_since,
                    'is_foreign_transaction': is_foreign,
                    'age': age,
                    'credit_score': credit,
                    'avg_transaction_value': avg_val,
                    'merchant_risk_score': m_risk
                }
                
                features_order = ['merchant_category', 'transaction_type', 'merchant_country_x', 'income_band', 'home_country', 
                                 'transaction_amount', 'hours_since_last_txn', 'is_foreign_transaction', 'age', 'credit_score', 
                                 'avg_transaction_value', 'merchant_risk_score']
                
                input_df = pd.DataFrame([encoded_data])[features_order]
                prediction = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0][1]
                
                st.markdown("---")
                if prediction == 1 or proba > 0.5:
                    st.markdown(f"""
                        <div class='fraud-alert'>
                            <h3>🚨 ALERT: Suspicious Activity Detected!</h3>
                            <p><b>Prediction:</b> Fraudulent Transaction</p>
                            <p><b>Risk Probability:</b> {proba*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='safe-alert'>
                            <h3>✅ Transaction Approved</h3>
                            <p><b>Prediction:</b> Legitimate</p>
                            <p><b>Risk Score:</b> {proba*100:.1f}%</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
        else:
            st.markdown("### 🌟 Live Streaming Ticker")
            start_streaming = st.checkbox("Toggle Streaming (Auto-Update)")
            
            placeholder = st.empty()
            import time
            import random
            
            if start_streaming:
                while True:
                    # Pick random row
                    idx = random.randint(0, len(df)-1)
                    row = df.iloc[idx]
                    
                    card_status = "fraud-alert" if row['is_fraud'] == 1 else "safe-alert"
                    icon = "🚨 FRAUD" if row['is_fraud'] == 1 else "✅ SAFE"
                    
                    with placeholder.container():
                        st.markdown(f"""
                            <div class='{card_status}' style='padding: 20px; text-align: left;'>
                                <div style='display: flex; justify-content: space-between;'>
                                    <div>
                                        <h4 style='margin:0;'>{icon} Transaction: {str(row['transaction_id'])[:8]}...</h4>
                                        <p style='margin:5px 0;'>Type: {row['transaction_type']} | Category: {row['merchant_category']}</p>
                                    </div>
                                    <div style='text-align: right;'>
                                        <h3 style='margin:0; font-size: 24px;'>${row['transaction_amount']:,.2f}</h3>
                                        <span style='background: white; color: black; padding: 2px 8px; border-radius: 4px; font-size: 12px;'>Risk Level: {row['risk_segment']}</span>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        time.sleep(1.5)
                        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Cute minimalist footer
    st.markdown("""
        <div style='
            background: #FFF5F7;
            padding: 25px;
            border-radius: 20px;
            border: 2px solid #FFE4E1;
            margin-top: 30px;
            text-align: center;
        '>
            <h3 style='color: #FF7482; margin: 0;'>🌸 Credit Card Fraud Analytics</h3>
            <p style='color: #999; margin: 8px 0 0 0; font-size: 14px;'>Made with ❤️ using Streamlit & ML</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
