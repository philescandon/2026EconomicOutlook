import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# DATA
# =============================================================================

# GDP Data - Both Q2 and Q3 2025 are disputed
gdp_data = pd.DataFrame({
    'Quarter': ['Q1 20', 'Q2 20', 'Q3 20', 'Q4 20', 'Q1 21', 'Q2 21', 'Q3 21', 'Q4 21',
                'Q1 22', 'Q2 22', 'Q3 22', 'Q4 22', 'Q1 23', 'Q2 23', 'Q3 23', 'Q4 23',
                'Q1 24', 'Q2 24', 'Q3 24', 'Q4 24', 'Q1 25', 'Q2 25', 'Q3 25'],
    'GDP': [-5.3, -28.0, 34.8, 4.0, 6.3, 7.0, 2.3, 6.9,
            -1.6, -0.6, 3.2, 2.6, 2.2, 2.1, 4.9, 3.4,
            1.4, 3.0, 2.8, 2.3, -0.5, 3.8, 4.3],
    'Disputed': [None]*21 + [1.0, 0.8]  # Q2: ~0.5-1.5% (using 1.0), Q3: 0.8%
})

# Consumer Sentiment Data
sentiment_data = pd.DataFrame({
    'Period': ['Jan 19', 'Jul 19', 'Dec 19', 'Jan 20', 'Apr 20', 'Jul 20', 'Dec 20',
               'Jan 21', 'Jul 21', 'Dec 21', 'Jan 22', 'Jun 22', 'Dec 22',
               'Jan 23', 'Jul 23', 'Dec 23', 'Jan 24', 'Jul 24', 'Dec 24',
               'Jan 25', 'Apr 25', 'Jul 25', 'Dec 25'],
    'Michigan': [91.2, 98.4, 99.3, 99.8, 71.8, 72.5, 80.7, 79.0, 81.2, 70.6,
                 67.2, 50.0, 59.7, 64.9, 71.6, 69.7, 79.0, 66.4, 74.0,
                 73.2, 52.2, 61.7, 52.9],
    'Conference Board': [121.7, 135.8, 126.5, 130.4, 85.7, 91.7, 87.1, 87.1, 125.1, 115.2,
                         111.1, 98.7, 109.0, 106.0, 114.0, 108.0, 110.9, 101.9, 104.7,
                         105.3, 86.0, 95.4, 89.1]
})

# Expectations Index Data
expectations_data = pd.DataFrame({
    'Month': ['Jan 24', 'Feb 24', 'Mar 24', 'Apr 24', 'May 24', 'Jun 24', 'Jul 24', 'Aug 24',
              'Sep 24', 'Oct 24', 'Nov 24', 'Dec 24', 'Jan 25', 'Feb 25', 'Mar 25', 'Apr 25',
              'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25'],
    'Value': [83.8, 79.8, 77.4, 68.8, 72.8, 79.0, 82.0, 82.5,
              82.4, 89.1, 86.0, 78.1, 76.7, 72.9, 65.2, 54.4,
              72.8, 71.5, 73.4, 75.6, 73.7, 70.7, 70.7, 70.7]
})

# Unemployment Data
unemployment_data = pd.DataFrame({
    'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
    'Overall': [3.5, 8.1, 5.4, 3.6, 3.6, 4.0, 4.6],
    'Young Grads (22-27)': [3.25, 6.5, 5.0, 3.5, 3.8, 4.2, 4.59],
    'Recent Grads': [5.0, 9.0, 7.5, 5.5, 6.0, 7.5, 9.7]
})

# Housing Data
housing_data = pd.DataFrame({
    'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
    'Median Price ($K)': [313, 329, 386, 449, 431, 420, 417],
    'Price-to-Income Ratio': [4.1, 4.3, 4.6, 5.2, 5.1, 5.0, 5.0],
    'Cost as % of Income': [35, 37, 40, 48, 47, 47, 47.7],
    'First-Time Buyer Age': [33, 34, 36, 38, 39, 39, 40]
})

# Vehicle Data
vehicle_data = pd.DataFrame({
    'Year': ['2019', '2020', '2021', '2022', '2023', '2024', '2025'],
    'Avg Transaction Price': [36718, 40107, 47000, 49929, 48528, 47500, 49814],
    'Models Under $25K': [30, 25, 20, 12, 10, 10, 8],
    'Avg Monthly Payment': [554, 575, 641, 717, 726, 734, 754]
})

# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Section",
    ["Overview", "GDP Controversy", "Consumer Sentiment", "Labor Market", 
     "Housing", "Vehicles", "K-Shape Analysis", "Investment Guidance"]
)

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

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 12px;'>
    U.S. Economic Analysis Dashboard | December 2025<br>
    Sources: BEA, Rosenberg Research, Federal Reserve Banks, BLS, University of Michigan, 
    Conference Board, NAR, Cox Automotive/KBB, Brookings, Yale Budget Lab
</div>
""", unsafe_allow_html=True)
