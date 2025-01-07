import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm
from plotly.subplots import make_subplots
from styles import get_page_styling,get_particles_js,URLS

# config
st.set_page_config(
    page_title="BMW Stock Analytics",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)



#st.markdown(particles_js, unsafe_allow_html=True)
st.markdown(get_page_styling(), unsafe_allow_html=True)

components.html(get_particles_js(), height=800, scrolling=False)


# Load  data
@st.cache_data
def load_data():
    df = pd.read_csv('data/BMW_Data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar with enhanced styling
with st.sidebar:
    st.image(URLS["BMW"], width=200)
    st.markdown("""
        <div class="glass-card">
            <h1 style='color: #1E88E5; text-align: center; margin-bottom: 20px;'>
                🚗 Dashboard Controls
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Date range selector with presets
    date_preset = st.selectbox(
        "Select Time Period",
        ["Custom", "1 Month", "3 Months", "6 Months", "1 Year", "5 Years", "All Time"]
    )
    
    if date_preset == "Custom":
        date_range = st.date_input(
            "Select Custom Date Range",
            value=(df['Date'].min(), df['Date'].max()),
            min_value=df['Date'].min().date(),
            max_value=df['Date'].max().date()
        )
    else:
        end_date = df['Date'].max()
        if date_preset == "1 Month":
            start_date = end_date - timedelta(days=30)
        elif date_preset == "3 Months":
            start_date = end_date - timedelta(days=90)
        elif date_preset == "6 Months":
            start_date = end_date - timedelta(days=180)
        elif date_preset == "1 Year":
            start_date = end_date - timedelta(days=365)
        elif date_preset == "5 Years":
            start_date = end_date - timedelta(days=1825)
        else:  # All Time
            start_date = df['Date'].min()
        date_range = (start_date.date(), end_date.date())

    st.markdown("""
        <div class="glass-card">
            <h3 style='color: #1E88E5;'>📈 Technical Indicators</h3>
        </div>
    """, unsafe_allow_html=True)
    
    show_ma = st.checkbox("Show Moving Averages", True)
    show_bb = st.checkbox("Show Bollinger Bands", True)
    
    ma_periods = st.multiselect(
        "Moving Average Periods",
        options=[20, 50, 100, 200],
        default=[20, 50]
    )

# Filter data based on date range
mask = (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
filtered_df = df.loc[mask]

# Main header with glassmorphism effect
st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 30px 0;">
        <h1 style='font-size: 42px; margin-bottom: 10px;'>
            <span style='color: #1E88E5;'>BMW</span> Stock Analytics Dashboard
        </h1>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 18px;'>
            Comprehensive analysis and real-time insights
        </p>
    </div>
""", unsafe_allow_html=True)

# Key metrics with enhanced glassmorphism styling
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-value">${:,.2f}</div>
            <div class="metric-label">Current Price</div>
        </div>
    """.format(filtered_df['Close'].iloc[-1]), unsafe_allow_html=True)

with col2:
    price_change = ((filtered_df['Close'].iloc[-1] - filtered_df['Close'].iloc[0]) / 
                    filtered_df['Close'].iloc[0] * 100)
    color = "#00ff88" if price_change >= 0 else "#ff4444"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="background: linear-gradient(45deg, {color}, {color}); -webkit-background-clip: text;">
                {price_change:,.2f}%
            </div>
            <div class="metric-label">Price Change</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_volume = filtered_df['Volume'].mean()
    st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:,.0f}</div>
            <div class="metric-label">Average Volume</div>
        </div>
    """.format(avg_volume), unsafe_allow_html=True)

with col4:
    volatility = filtered_df['Close'].pct_change().std() * np.sqrt(252) * 100
    st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:,.2f}%</div>
            <div class="metric-label">Annualized Volatility</div>
        </div>
    """.format(volatility), unsafe_allow_html=True)

# Main chart section with glassmorphism
st.markdown("""
    <div class="glass-card">
        <h2 class="custom-header">📈 Price Analysis</h2>
    </div>
""", unsafe_allow_html=True)

# Create subplot with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                    vertical_spacing=0.03, 
                    row_heights=[0.7, 0.3])

# Candlestick chart with enhanced styling
fig.add_trace(go.Candlestick(
    x=filtered_df['Date'],
    open=filtered_df['Open'],
    high=filtered_df['High'],
    low=filtered_df['Low'],
    close=filtered_df['Close'],
    name='OHLC',
    increasing_line_color='#00ff88',
    decreasing_line_color='#ff4444'
), row=1, col=1)

# Add Moving Averages
if show_ma:
    for period in ma_periods:
        ma = filtered_df['Close'].rolling(window=period).mean()
        fig.add_trace(go.Scatter(
            x=filtered_df['Date'],
            y=ma,
            name=f'{period}-day MA',
            line=dict(width=1)
        ), row=1, col=1)

# Add Bollinger Bands
if show_bb:
    ma20 = filtered_df['Close'].rolling(window=20).mean()
    stddev = filtered_df['Close'].rolling(window=20).std()
    upper_band = ma20 + (stddev * 2)
    lower_band = ma20 - (stddev * 2)
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=upper_band,
        name='Upper BB',
        line=dict(color='rgba(173, 204, 255, 0.7)', width=1),
        fill=None
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=lower_band,
        name='Lower BB',
        line=dict(color='rgba(173, 204, 255, 0.7)', width=1),
        fill='tonexty',
        fillcolor='rgba(173, 204, 255, 0.1)'
    ), row=1, col=1)

# Volume bars
colors = ['#00ff88' if row['Close'] >= row['Open'] else '#ff4444' 
          for index, row in filtered_df.iterrows()]

fig.add_trace(go.Bar(
    x=filtered_df['Date'],
    y=filtered_df['Volume'],
    name='Volume',
    marker_color=colors,
    opacity=0.8
), row=2, col=1)

# Update layout for professional look
fig.update_layout(
    template='plotly_dark',
    height=800,
    margin=dict(l=0, r=0, t=0, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_rangeslider_visible=False,
    showlegend=True,
    legend=dict(
        bgcolor='rgba(0,0,0,0)',
        bordercolor='rgba(255,255,255,0.1)',
        borderwidth=1
    ),
    xaxis2_rangeslider_visible=False
)

# Update yaxis labels
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

st.plotly_chart(fig, use_container_width=True, config={
    'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
    'scrollZoom': True
})

# Advanced Analysis Section
st.markdown("""
    <div class="custom-container">
        <h2 class="custom-header">📊 Advanced Analysis</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Returns Distribution
    filtered_df['Returns'] = filtered_df['Close'].pct_change()
    fig_returns = go.Figure()
    
    fig_returns.add_trace(go.Histogram(
        x=filtered_df['Returns'],
        nbinsx=50,
        name='Returns',
        marker_color='#1E88E5',
        opacity=0.7
    ))
    
    # Add normal distribution curve
    returns_mean = filtered_df['Returns'].mean()
    returns_std = filtered_df['Returns'].std()
    x = np.linspace(returns_mean - 4*returns_std, returns_mean + 4*returns_std, 100)
    y = norm.pdf(x, returns_mean, returns_std)
    
    fig_returns.add_trace(go.Scatter(
        x=x,
        y=y * len(filtered_df['Returns']) * (filtered_df['Returns'].max() - filtered_df['Returns'].min()) / 50,
        mode='lines',
        name='Normal Distribution',
        line=dict(color='#00ff88', width=2)
    ))
    
    fig_returns.update_layout(
        title='Returns Distribution',
        template='plotly_dark',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_returns, use_container_width=True)

with col2:
    # Volatility Analysis
    window = 20
    filtered_df['Volatility'] = filtered_df['Returns'].rolling(window=window).std() * np.sqrt(252) * 100
    
    fig_vol = go.Figure()
    
    fig_vol.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Volatility'],
        name='Rolling Volatility',
        line=dict(color='#1E88E5', width=2)
    ))
    
    fig_vol.update_layout(
        title=f'{window}-Day Rolling Volatility',
        template='plotly_dark',
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='Annualized Volatility (%)'
    )
    
    st.plotly_chart(fig_vol, use_container_width=True)

# Statistics and Insights Section
st.markdown("""
    <div class="custom-container">
        <h2 class="custom-header">📈 Key Statistics & Insights</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E88E5;">Price Statistics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    stats_df = pd.DataFrame({
        'Metric': [
            'Highest Price',
            'Lowest Price',
            'Average Price',
            'Price Range',
            'Current vs Avg'
        ],
        'Value': [
            f"${filtered_df['High'].max():.2f}",
            f"${filtered_df['Low'].min():.2f}",
            f"${filtered_df['Close'].mean():.2f}",
            f"${filtered_df['High'].max() - filtered_df['Low'].min():.2f}",
            f"{((filtered_df['Close'].iloc[-1] / filtered_df['Close'].mean()) - 1) * 100:.1f}%"
        ]
    })
    st.dataframe(stats_df, hide_index=True, use_container_width=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E88E5;">Return Statistics</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate additional return metrics
    daily_returns = filtered_df['Returns'].dropna()
    annualized_return = np.mean(daily_returns) * 252 * 100
    sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
    
    returns_stats = pd.DataFrame({
        'Metric': [
            'Daily Returns Mean',
            'Daily Returns Std',
            'Annualized Return',
            'Sharpe Ratio',
            'Positive Days %'
        ],
        'Value': [
            f"{daily_returns.mean()*100:.2f}%",
            f"{daily_returns.std()*100:.2f}%",
            f"{annualized_return:.2f}%",
            f"{sharpe_ratio:.2f}",
            f"{(daily_returns > 0).mean()*100:.1f}%"
        ]
    })
    st.dataframe(returns_stats, hide_index=True, use_container_width=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <h3 style="color: #1E88E5;">Volume Analysis</h3>
        </div>
    """, unsafe_allow_html=True)
    
    volume_stats = pd.DataFrame({
        'Metric': [
            'Highest Volume',
            'Lowest Volume',
            'Avg Daily Volume',
            'Volume Trend',
            'Volume Volatility'
        ],
        'Value': [
            f"{filtered_df['Volume'].max():,.0f}",
            f"{filtered_df['Volume'].min():,.0f}",
            f"{filtered_df['Volume'].mean():,.0f}",
            f"{((filtered_df['Volume'].tail(5).mean() / filtered_df['Volume'].head(5).mean()) - 1) * 100:.1f}%",
            f"{filtered_df['Volume'].std() / filtered_df['Volume'].mean() * 100:.1f}%"
        ]
    })
    st.dataframe(volume_stats, hide_index=True, use_container_width=True)

# Technical Patterns Section
st.markdown("""
    <div class="custom-container">
        <h2 class="custom-header">🔍 Technical Analysis Insights</h2>
    </div>
""", unsafe_allow_html=True)

def calculate_rsi(data, periods=14):
    close_delta = data['Close'].diff()
    gain = (close_delta.where(close_delta > 0, 0)).rolling(window=periods).mean()
    loss = (-close_delta.where(close_delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Calculate technical indicators
filtered_df['RSI'] = calculate_rsi(filtered_df)
filtered_df['SMA_20'] = filtered_df['Close'].rolling(window=20).mean()
filtered_df['SMA_50'] = filtered_df['Close'].rolling(window=50).mean()

# Create technical analysis signals
signals = []

# RSI signals
last_rsi = filtered_df['RSI'].iloc[-1]
if last_rsi > 70:
    signals.append(("RSI Overbought", "warning"))
elif last_rsi < 30:
    signals.append(("RSI Oversold", "success"))

# Moving Average signals
if filtered_df['SMA_20'].iloc[-1] > filtered_df['SMA_50'].iloc[-1] and \
   filtered_df['SMA_20'].iloc[-2] <= filtered_df['SMA_50'].iloc[-2]:
    signals.append(("Golden Cross Detected", "success"))
elif filtered_df['SMA_20'].iloc[-1] < filtered_df['SMA_50'].iloc[-1] and \
     filtered_df['SMA_20'].iloc[-2] >= filtered_df['SMA_50'].iloc[-2]:
    signals.append(("Death Cross Detected", "warning"))

# Display technical signals
col1, col2 = st.columns([2, 1])

with col1:
    # RSI Chart
    fig_rsi = go.Figure()
    
    fig_rsi.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['RSI'],
        name='RSI',
        line=dict(color='#1E88E5', width=2)
    ))
    
   
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5)
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5)
    
    fig_rsi.update_layout(
        title='Relative Strength Index (RSI)',
        template='plotly_dark',
        height=300,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        yaxis_title='RSI'
    )
    
    st.plotly_chart(fig_rsi, use_container_width=True)

with col2:
    st.markdown("""
        <div class="metric-card" style="height: 300px; overflow-y: auto;">
            <h3 style="color: #1E88E5;">Technical Signals</h3>
    """, unsafe_allow_html=True)
    
    for signal, signal_type in signals:
        color = "#00ff88" if signal_type == "success" else "#ff4444"
        st.markdown(f"""
            <div style="margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(0,0,0,0.2);">
                <span style="color: {color};">●</span> {signal}
            </div>
        """, unsafe_allow_html=True)
    
    if not signals:
        st.markdown("""
            <div style="margin: 10px 0; padding: 10px; border-radius: 5px; background-color: rgba(0,0,0,0.2);">
                No significant technical signals detected
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer info
st.markdown("""
    <div style="text-align: center; margin-top: 30px; padding: 20px; background-color: rgba(0,0,0,0.2); border-radius: 10px;">
        <p style="color: #888888;">BMW Stock Analytics Dashboard • Last Updated: {}</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)