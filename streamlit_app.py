import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_manager import (
    load_gdp_data, load_sentiment_data, load_expectations_data,
    load_unemployment_data, load_housing_data, load_vehicle_data,
    refresh_all_api_data, get_data_status, save_csv
)

# Page configuration
st.set_page_config(
    page_title="U.S. Economic Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #3b82f6;
    }
    .metric-card-alert {
        background-color: #fef2f2;
        border-radius: 10px;
        padding: 20px;
        border-left: 4px solid #dc2626;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# DATA - Load from CSV files (with fallback to defaults)
# =============================================================================

gdp_data = load_gdp_data()
sentiment_data = load_sentiment_data()
expectations_data = load_expectations_data()
unemployment_data = load_unemployment_data()
housing_data = load_housing_data()
vehicle_data = load_vehicle_data()

# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Section",
    ["Overview", "GDP Controversy", "Consumer Sentiment", "Labor Market",
     "Housing", "Vehicles", "K-Shape Analysis", "Investment Guidance", "Data Management"]
)

st.sidebar.markdown("---")

# Data Refresh Section
st.sidebar.markdown("### Data Refresh")
if st.sidebar.button("🔄 Refresh from APIs", help="Refresh GDP, Unemployment, and Sentiment data from FRED API"):
    with st.sidebar:
        with st.spinner("Refreshing data..."):
            # Get API keys from secrets
            fred_key = st.secrets.get("FRED_API_KEY", None)
            bea_key = st.secrets.get("BEA_API_KEY", None)

            if fred_key:
                results = refresh_all_api_data(fred_key, bea_key)

                success_count = sum(1 for r in results.values() if r[0])
                st.sidebar.success(f"Refreshed {success_count}/5 datasets")

                # Show details in expander
                with st.sidebar.expander("Refresh Details"):
                    for name, (success, msg, _) in results.items():
                        if success:
                            st.write(f"✅ {name}: {msg}")
                        else:
                            st.write(f"⚠️ {name}: {msg}")

                # Rerun to reload data
                st.rerun()
            else:
                st.sidebar.error("API keys not configured. Add FRED_API_KEY to secrets.")

# Data status
data_status = get_data_status()
with st.sidebar.expander("📅 Data Status"):
    for name, info in data_status.items():
        st.write(f"**{name}:** {info['last_updated']}")

st.sidebar.markdown("---")
st.sidebar.markdown("### Data Sources")
st.sidebar.markdown("""
- Bureau of Economic Analysis
- Rosenberg Research
- Federal Reserve Banks
- Bureau of Labor Statistics
- University of Michigan
- Conference Board
- National Association of Realtors
- Cox Automotive / KBB
""")

# =============================================================================
# MAIN CONTENT
# =============================================================================

st.title("🇺🇸 U.S. Economic Analysis Dashboard")
st.markdown("**Year-End 2025 | Data, Tensions, and Contested Narratives**")
st.markdown("---")

# -----------------------------------------------------------------------------
# OVERVIEW PAGE
# -----------------------------------------------------------------------------
if page == "Overview":
    st.header("Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Q2-Q3 2025 GDP (Official)", "3.8-4.3%", "BEA Releases")
    with col2:
        st.metric("Q2-Q3 2025 GDP (Disputed)", "0.8-1.5%?", "Rosenberg Methodology", delta_color="inverse")
    with col3:
        st.metric("Michigan Sentiment", "52.9", "2nd lowest ever", delta_color="inverse")
    with col4:
        st.metric("Unemployment", "4.6%", "Nov 2025")
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Expectations Index", "70.7", "11 mo. below 80", delta_color="inverse")
    with col6:
        st.metric("Median Home Price", "$417K", "5.0x income")
    with col7:
        st.metric("New Vehicle ATP", "$49,814", "8 models <$25K")
    with col8:
        st.metric("Recent Grad Unemployment", "9.7%", "= HS diploma rate", delta_color="inverse")
    
    st.markdown("---")
    
    st.warning("""
    **THE CENTRAL PARADOX**
    
    Official GDP shows 3.8-4.3% growth in Q2-Q3 2025 while consumer sentiment sits at the second-lowest level ever recorded. 
    Either consumers are irrational—or the GDP figures don't reflect their economic reality.
    """)
    
    # Quick GDP chart
    fig = px.bar(gdp_data, x='Quarter', y='GDP', 
                 title='Quarterly GDP Growth (Annualized %)',
                 color='GDP',
                 color_continuous_scale=['#dc2626', '#fbbf24', '#22c55e'])
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# GDP CONTROVERSY PAGE
# -----------------------------------------------------------------------------
elif page == "GDP Controversy":
    st.header("The Q2 & Q3 2025 GDP Controversy")
    
    # GDP Chart with both disputed points
    fig = go.Figure()
    fig.add_trace(go.Bar(x=gdp_data['Quarter'], y=gdp_data['GDP'], name='Official GDP %',
                         marker_color='#3b82f6'))
    fig.add_trace(go.Scatter(x=['Q2 25', 'Q3 25'], y=[1.0, 0.8], mode='markers+lines', 
                             name='Disputed GDP %',
                             marker=dict(color='#dc2626', size=15, symbol='diamond'),
                             line=dict(color='#dc2626', width=2, dash='dot')))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=2)
    fig.update_layout(title='Quarterly GDP Growth (Annualized %)', height=450,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Both Q2 and Q3 2025 Are Disputed")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **Q2 2025 - Official: 3.8%**
        
        BEA stated growth was "primarily reflected by a decrease in imports." 
        
        Key factors:
        - Imports plunged **-29.3%** (massive mechanical boost)
        - Consumer spending: +2.5% (modest)
        - Government spending: -0.1% (contracted)
        
        **Estimated organic growth: ~0.5-1.5%**
        """)
    
    with col2:
        st.info("""
        **Q3 2025 - Official: 4.3%**
        
        Rosenberg called this "fugazi" (fake).
        
        Key factors:
        - Imports: -4.7% (continued boost)
        - Government spending: +2.2% (surge)
        - Consumer spending funded by savings drawdown
        
        **Rosenberg's calculation: ~0.8%**
        """)
    
    st.markdown("---")
    st.subheader("Comparison of Distortion Factors")
    
    comparison_df = pd.DataFrame({
        'Factor': ['Import Change', 'Government Spending', 'Consumer Spending', 'Primary Distortion', 'Official GDP', 'Estimated Organic GDP'],
        'Q2 2025': ['-29.3%', '-0.1%', '+2.5%', 'Massive import collapse', '3.8%', '~0.5-1.5%'],
        'Q3 2025': ['-4.7%', '+2.2%', '+3.5%', 'Gov spending + imports', '4.3%', '~0.8%']
    })
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("The True 2025 Trajectory?")
    
    trajectory_df = pd.DataFrame({
        'Quarter': ['Q1 2025', 'Q2 2025', 'Q3 2025'],
        'Official GDP': ['-0.5%', '3.8%', '4.3%'],
        'Disputed GDP': ['-0.5%', '~0.5-1.5%', '~0.8%'],
        'Interpretation': ['Contraction (undisputed)', 'Weak, not strong', 'Weak, not surging']
    })
    st.dataframe(trajectory_df, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **Official Narrative:**
        Economy contracted in Q1, then roared back with 3.8% and 4.3% growth. Resilient consumer, strong recovery.
        """)
    with col2:
        st.error("""
        **Disputed Narrative:**
        Economy contracted in Q1, limped along at ~1% in Q2-Q3, masked by import collapse and government spending. Persistently weak.
        """)
    
    st.markdown("---")
    st.subheader("If Disputed Figures Are Correct:")
    
    implications = {
        "The 'Paradox' Disappears": "Consumers are accurately perceiving a weak economy that headline numbers mask.",
        "Expectations Index Validated": "The 11-month recession signal is working—detecting weakness official stats miss.",
        "Full-Year 2025 Is Weak": "Three consecutive quarters of contraction or near-zero growth. Not a 'soft landing.'",
        "Fed Policy Looks Different": "Rate cuts look late and possibly insufficient, not unnecessary.",
        "Political Narrative Inverts": "Tariff 'success' story flips to 'economy weak despite trade policy.'"
    }
    
    for title, desc in implications.items():
        st.markdown(f"**{title}:** {desc}")

# -----------------------------------------------------------------------------
# CONSUMER SENTIMENT PAGE
# -----------------------------------------------------------------------------
elif page == "Consumer Sentiment":
    st.header("Consumer Sentiment Indices")
    
    # Dual-axis sentiment chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=sentiment_data['Period'], y=sentiment_data['Michigan'],
                             name='Michigan Index', line=dict(color='#dc2626', width=2)),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=sentiment_data['Period'], y=sentiment_data['Conference Board'],
                             name='Conference Board', line=dict(color='#3b82f6', width=2)),
                  secondary_y=True)
    fig.update_layout(title='Consumer Sentiment: Michigan vs Conference Board', height=400)
    fig.update_yaxes(title_text="Michigan Index", secondary_y=False, range=[40, 110])
    fig.update_yaxes(title_text="Conference Board", secondary_y=True, range=[70, 140])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Expectations Index: Recession Signal Tracker")
    st.markdown("*Below 80 = historically signals recession ahead*")
    
    # Expectations chart with threshold
    fig2 = go.Figure()
    colors = ['#dc2626' if v < 80 else '#22c55e' for v in expectations_data['Value']]
    fig2.add_trace(go.Bar(x=expectations_data['Month'], y=expectations_data['Value'],
                          marker_color=colors, name='Expectations Index'))
    fig2.add_hline(y=80, line_dash="dash", line_color="#dc2626", line_width=2,
                   annotation_text="Recession Threshold (80)")
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.error("""
    ⚠️ **The Expectations Index has been below 80 for 11 consecutive months**—the longest sustained 
    recession signal in decades. Yet no recession has occurred by traditional measures.
    """)

# -----------------------------------------------------------------------------
# LABOR MARKET PAGE
# -----------------------------------------------------------------------------
elif page == "Labor Market":
    st.header("Labor Market: The Hidden Stratification")
    
    # Unemployment comparison chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unemployment_data['Year'], y=unemployment_data['Overall'],
                             name='Overall Rate', line=dict(color='#3b82f6', width=3)))
    fig.add_trace(go.Scatter(x=unemployment_data['Year'], y=unemployment_data['Young Grads (22-27)'],
                             name='College Grads 22-27', line=dict(color='#22c55e', width=2)))
    fig.add_trace(go.Scatter(x=unemployment_data['Year'], y=unemployment_data['Recent Grads'],
                             name='Recent Graduates', line=dict(color='#dc2626', width=3)))
    fig.update_layout(title='Unemployment: Overall vs. Young Graduates', height=400,
                      yaxis_range=[0, 12])
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Unemployment", "4.6%", "Highest since Oct 2021")
    with col2:
        st.metric("Recent Grad Unemployment", "9.7%", "= High school diploma rate", delta_color="inverse")
    with col3:
        st.metric("Recent Grad Underemployment", "41.8%", "Up from ~35% in 2019", delta_color="inverse")
    
    st.warning("""
    **THE K-SHAPE IN LABOR**
    
    Overall unemployment at 4.6% masks a generational crisis:
    - Entry-level hiring: **-23%** vs. March 2020
    - Only **30%** of recent grads have full-time jobs in their field
    - Monthly job creation since March: **35K** (vs. ~180K typical)
    """)

# -----------------------------------------------------------------------------
# HOUSING PAGE
# -----------------------------------------------------------------------------
elif page == "Housing":
    st.header("Housing Affordability Crisis")
    
    # Housing price and affordability chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=housing_data['Year'], y=housing_data['Median Price ($K)'],
                         name='Median Price ($K)', marker_color='#3b82f6'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=housing_data['Year'], y=housing_data['Cost as % of Income'],
                             name='Cost as % of Income', line=dict(color='#dc2626', width=3)),
                  secondary_y=True)
    fig.update_layout(title='Housing: Price and Affordability', height=400)
    fig.update_yaxes(title_text="Median Price ($K)", secondary_y=False)
    fig.update_yaxes(title_text="Cost as % of Income", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Median Home Price", "$417K", "Down from $449K peak")
    with col2:
        st.metric("Price-to-Income", "5.0x", "Historic norm: 3-4x", delta_color="inverse")
    with col3:
        st.metric("First-Time Buyer Age", "40", "Up from 33 in 2019", delta_color="inverse")
    with col4:
        st.metric("$75K HH Can Afford", "21%", "Down from 49% in 2019", delta_color="inverse")
    
    st.markdown("---")
    st.markdown("""
    **The Housing K-Shape:**
    - Median buyer age: **59** (record high)
    - Institutional investors: **30%** of purchases (H1 2025)
    - First-time buyers: pushed out
    
    The market hasn't collapsed because high-income and institutional buyers keep it elevated—but accessibility has collapsed.
    """)

# -----------------------------------------------------------------------------
# VEHICLES PAGE
# -----------------------------------------------------------------------------
elif page == "Vehicles":
    st.header("Vehicle Market: Affordability Collapse")
    
    # Vehicle price and models chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=vehicle_data['Year'], y=vehicle_data['Avg Transaction Price'],
                         name='Avg Transaction Price ($)', marker_color='#3b82f6'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=vehicle_data['Year'], y=vehicle_data['Models Under $25K'],
                             name='Models Under $25K', line=dict(color='#dc2626', width=3)),
                  secondary_y=True)
    fig.update_layout(title='Vehicle Prices and Affordability', height=400)
    fig.update_yaxes(title_text="Avg Transaction Price ($)", secondary_y=False)
    fig.update_yaxes(title_text="Models Under $25K", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Transaction Price", "$49,814", "Sept hit $50,080")
    with col2:
        st.metric("Models Under $25K", "8", "Down from 30 in 2019", delta_color="inverse")
    with col3:
        st.metric("Avg Monthly Payment", "$754", "Up from $554 in 2019")
    with col4:
        st.metric("Buyers w/ $1K+ Payment", "~20%", "Up from ~5% in 2019", delta_color="inverse")
    
    st.warning("""
    **THE K-SHAPE IN VEHICLES**
    
    More vehicles now sell **above $75K** than **below $25K**. 
    
    The market is functioning—for those who can afford it. Price-sensitive buyers have been 
    structurally excluded, not temporarily priced out.
    """)

# -----------------------------------------------------------------------------
# K-SHAPE ANALYSIS PAGE
# -----------------------------------------------------------------------------
elif page == "K-Shape Analysis":
    st.header("The K-Shaped Economy Explained")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style='font-size: 150px; text-align: center; color: #d1d5db;'>K</div>
        """, unsafe_allow_html=True)
    with col2:
        st.success("**↗ Upper arm:** Asset owners, high income, luxury markets—recovering and growing")
        st.error("**↘ Lower arm:** Non-asset owners, middle income—stagnating or declining")
    
    st.markdown("---")
    st.subheader("K-Shape Manifestations Across Markets")
    
    k_shape_data = pd.DataFrame({
        'Category': ['Housing Buyers', 'Vehicle Market', 'Labor Market', 'Consumer Sentiment'],
        'Upper Arm (Rising)': [
            'Median age 59, cash buyers up',
            'More sales >$75K than <$25K',
            'Overall unemployment 4.6%',
            'Asset owners see strong economy'
        ],
        'Lower Arm (Declining)': [
            'First-time buyer age → 40',
            'Only 8 models under $25K',
            'Recent grad unemployment 9.7%',
            'Non-asset owners see weakness'
        ]
    })
    
    st.dataframe(k_shape_data, use_container_width=True, hide_index=True)
    
    st.info("""
    **Investment Implication**
    
    The K-shape is not temporary. It's structural. Prudent investors should:
    - **Overweight:** Companies serving the upper arm (luxury, wealth management, premium services)
    - **Underweight:** Companies dependent on broad middle-class spending, credit access, or entry-level employment
    """)

# -----------------------------------------------------------------------------
# INVESTMENT GUIDANCE PAGE
# -----------------------------------------------------------------------------
elif page == "Investment Guidance":
    st.header("What Should a Prudent Investor Do in 2026?")
    
    st.markdown("""
    Given the tensions identified—contested GDP figures for **both Q2 and Q3 2025**, record-low consumer sentiment, 
    11 months of recession signals, and K-shaped market dynamics—the following framework 
    may guide prudent investment decisions.
    """)
    
    st.markdown("---")
    
    with st.expander("1. Acknowledge Elevated Uncertainty", expanded=True):
        st.markdown("""
        The data does not support high-conviction directional bets. If official GDP is accurate, 
        the economy has been strong since Q2. If the critics are correct, the economy has been 
        weak for most of 2025 and recession risk is elevated.
        
        **Implication:** Reduce concentration. Diversify across asset classes, geographies, 
        and factor exposures. Avoid maximum-risk positions.
        """)
    
    with st.expander("2. Respect the Consumer Sentiment Signal"):
        st.markdown("""
        Consumer sentiment at the second-lowest level on record will affect corporate earnings 
        in consumer-facing sectors—even if GDP is strong.
        
        **Implication:** Underweight consumer discretionary, particularly companies dependent 
        on middle-income households. Overweight consumer staples and companies serving 
        high-income demographics.
        """)
    
    with st.expander("3. Prepare for Policy Volatility"):
        st.markdown("""
        Tariff policy remains uncertain. The Fed may pause, cut, or reverse course. 
        Political dynamics may shift fiscal policy.
        
        **Implication:** Maintain higher-than-normal cash reserves. Consider options strategies 
        for downside protection. Favor companies with pricing power and domestic supply chains.
        """)
    
    with st.expander("4. Position for K-Shaped Reality"):
        st.markdown("""
        High-income households continue spending; lower and middle-income households are stretched. 
        This is structural, not temporary.
        
        **Implication:** Favor luxury goods, premium services, wealth management. Be cautious with 
        companies dependent on broad middle-class spending or entry-level employment.
        """)
    
    with st.expander("5. Watch Leading Indicators, Not Headlines"):
        st.markdown("""
        The GDP controversy shows headline numbers can mislead. The Expectations Index, initial 
        jobless claims, and credit card delinquency may provide earlier signals.
        
        **Implication:** Build a dashboard of leading indicators. React to their trends rather 
        than waiting for official GDP prints.
        """)
    
    st.markdown("---")
    st.subheader("Portfolio Positioning Framework")
    
    positioning = pd.DataFrame({
        'Category': ['Equities', 'Fixed Income', 'Real Assets', 'Cash', 'Geography'],
        'Overweight': ['Quality, pricing power, luxury', 'High-quality duration', 
                       'Rental housing, infrastructure', 'Elevated (opportunity fund)', 
                       'Selective international'],
        'Underweight': ['Discretionary, credit-dependent', 'Consumer credit, high yield',
                        'Speculative development', 'Minimum allocation', 
                        'Maximum U.S. concentration']
    })
    
    st.dataframe(positioning, use_container_width=True, hide_index=True)
    
    st.success("""
    **THE OVERARCHING PRINCIPLE**
    
    When official data and lived experience diverge this sharply, prudent investors should not assume 
    either is definitively correct. The appropriate response is to position for multiple scenarios, 
    maintain flexibility, and avoid maximum exposure to any single narrative.
    """)
    
    st.markdown("---")
    st.caption("""
    **DISCLAIMER:** This analysis is for informational purposes only and does not constitute investment advice.
    All investments carry risk, including potential loss of principal. Investors should consult qualified
    financial advisors before making investment decisions.
    """)

# -----------------------------------------------------------------------------
# DATA MANAGEMENT PAGE
# -----------------------------------------------------------------------------
elif page == "Data Management":
    st.header("Data Management")
    st.markdown("View, edit, and export the underlying data used in this dashboard.")

    # Data status overview
    st.subheader("Data Status")
    status_cols = st.columns(3)
    data_status = get_data_status()
    for i, (name, info) in enumerate(data_status.items()):
        with status_cols[i % 3]:
            st.metric(
                name,
                f"{info['rows']} rows",
                f"Updated: {info['last_updated']}"
            )

    st.markdown("---")

    # Data viewer/editor
    st.subheader("View & Edit Data")

    data_choice = st.selectbox(
        "Select Dataset",
        ["GDP", "Consumer Sentiment", "Expectations Index", "Unemployment", "Housing", "Vehicles"]
    )

    # Map selection to data and filename
    data_map = {
        "GDP": (gdp_data, "gdp_data.csv"),
        "Consumer Sentiment": (sentiment_data, "sentiment_data.csv"),
        "Expectations Index": (expectations_data, "expectations_data.csv"),
        "Unemployment": (unemployment_data, "unemployment_data.csv"),
        "Housing": (housing_data, "housing_data.csv"),
        "Vehicles": (vehicle_data, "vehicle_data.csv")
    }

    selected_data, filename = data_map[data_choice]

    # Display editable dataframe
    st.markdown(f"**{data_choice} Data** (`{filename}`)")

    edited_df = st.data_editor(
        selected_data,
        use_container_width=True,
        num_rows="dynamic",
        key=f"editor_{data_choice}"
    )

    # Save button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("💾 Save Changes", type="primary"):
            save_csv(edited_df, filename)
            st.success(f"Saved {filename}!")
            st.rerun()

    with col2:
        # Download button
        csv_data = edited_df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv_data,
            file_name=filename,
            mime="text/csv"
        )

    st.markdown("---")

    # API refresh section
    st.subheader("API Data Sources")

    st.info("""
    **Available via FRED API:**
    - GDP Growth Rate (quarterly)
    - Unemployment Rate (monthly/annual)
    - Michigan Consumer Sentiment

    **Manual Update Required:**
    - Conference Board Consumer Confidence (proprietary)
    - Disputed GDP figures (Rosenberg Research)
    - Graduate unemployment rates (BLS special reports)
    - Housing data (NAR/Zillow)
    - Vehicle data (Cox Automotive/KBB)
    """)

    # Refresh specific datasets
    st.markdown("**Refresh Individual Datasets:**")

    refresh_cols = st.columns(3)
    with refresh_cols[0]:
        if st.button("🔄 Refresh GDP"):
            fred_key = st.secrets.get("FRED_API_KEY", None)
            if fred_key:
                from data_manager import refresh_gdp_data
                success, msg, _ = refresh_gdp_data(fred_key)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("FRED API key not configured")

    with refresh_cols[1]:
        if st.button("🔄 Refresh Unemployment"):
            fred_key = st.secrets.get("FRED_API_KEY", None)
            if fred_key:
                from data_manager import refresh_unemployment_data
                success, msg, _ = refresh_unemployment_data(fred_key)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("FRED API key not configured")

    with refresh_cols[2]:
        if st.button("🔄 Refresh Sentiment"):
            fred_key = st.secrets.get("FRED_API_KEY", None)
            if fred_key:
                from data_manager import refresh_sentiment_data
                success, msg, _ = refresh_sentiment_data(fred_key)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("FRED API key not configured")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 12px;'>
    U.S. Economic Analysis Dashboard | December 2025<br>
    Sources: BEA, Rosenberg Research, Federal Reserve Banks, BLS, University of Michigan, 
    Conference Board, NAR, Cox Automotive/KBB, Brookings, Yale Budget Lab
</div>
""", unsafe_allow_html=True)
