import streamlit as st
import webbrowser
from datetime import datetime, timedelta
import pytz
import threading

# Luxury UI Configuration
st.set_page_config(
    page_title="Executive Command Center",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Luxury UI
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #1a1a1a, #252525) !important;
        border-right: 1px solid #333;
    }
    
    /* Title styling */
    .header {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 1px;
        color: #d4af37;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Menu buttons */
    .menu-btn {
        border: 1px solid #444 !important;
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a) !important;
        color: #d4af37 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        margin: 8px 0 !important;
        transition: all 0.3s !important;
    }
    
    .menu-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        background: linear-gradient(145deg, #252525, #303030) !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(30,30,30,0.7) !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 6px !important;
    }
    
    /* Success messages */
    .stAlert {
        background: rgba(30,70,30,0.3) !important;
        border: 1px solid #2e7d32 !important;
    }
    
    /* Channel cards */
    .channel-card {
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 15px;
        margin-bottom: 15px;
        background: linear-gradient(145deg, #1a1a1a, #252525);
        transition: all 0.3s;
    }
    
    .channel-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.2);
    }
    
    .channel-name {
        color: #d4af37;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

def display_luxury_menu():
    st.sidebar.markdown("""
    <h1 class='header'>EXECUTIVE COMMAND CENTER</h1>
    """, unsafe_allow_html=True)
    
    menu_options = [
        {"icon": "📱", "name": "Secure Messenger"},
        {"icon": "📈", "name": "Market Terminal"},
        {"icon": "🔗", "name": "Private Trading Channels"},
        {"icon": "💼", "name": "Network Hub"}
    ]
    
    for option in menu_options:
        if st.sidebar.button(f"{option['icon']} {option['name']}", key=option['name'], help=f"Access {option['name']}"):
            st.session_state.current_view = option['name']
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Exit Session"):
        st.session_state.clear()

def send_whatsapp_message(phone, message):
    webbrowser.open(f"https://wa.me/{phone}?text={message}")

def schedule_message(phone, message, scheduled_time, timezone):
    def send_at_scheduled_time():
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        wait_seconds = (scheduled_time - now).total_seconds()
        
        if wait_seconds > 0:
            with st.spinner(f"Message scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}"):
                time.sleep(wait_seconds)
                send_whatsapp_message(phone, message)
                st.success(f"Message sent to {phone} at {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
                st.session_state.scheduled_messages.remove((phone, message, scheduled_time, timezone))
                st.experimental_rerun()
    
    thread = threading.Thread(target=send_at_scheduled_time)
    thread.daemon = True
    thread.start()

def secure_messenger():
    st.markdown("### 📱 Secure Communications")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/1384/1384023.png", width=80)
    
    with col2:
        phone = st.text_input("Recipient Number (+Country Code)")
        message = st.text_area("Encrypted Message", height=100)
        
        schedule_type = st.radio("Delivery Timing:", ["Send Now", "Schedule for Later"], horizontal=True)
        
        if schedule_type == "Schedule for Later":
            col1, col2 = st.columns(2)
            with col1:
                schedule_date = st.date_input("Date", min_value=datetime.now().date())
            with col2:
                schedule_time = st.time_input("Time (24hr format)")
            
            timezone = st.selectbox("Timezone", pytz.all_timezones, index=pytz.all_timezones.index('Asia/Kolkata'))
            scheduled_datetime = datetime.combine(schedule_date, schedule_time)
            scheduled_datetime = pytz.timezone(timezone).localize(scheduled_datetime)
            
            if st.button("⏰ Schedule Message"):
                if phone and message:
                    if scheduled_datetime > datetime.now(pytz.timezone(timezone)):
                        schedule_message(phone, message, scheduled_datetime, timezone)
                    else:
                        st.error("Scheduled time must be in the future")
                else:
                    st.error("Please enter both phone number and message")
        else:
            if st.button("🔒 Send Secure Message"):
                if phone and message:
                    send_whatsapp_message(phone, message)
                    st.success("Secure channel established")
                else:
                    st.error("Authentication required")

def market_terminal():
    st.markdown("### 📈 Market Intelligence Terminal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        exchange = st.selectbox(
            "Exchange",
            ("NASDAQ", "NYSE", "NSE", "BSE", "LSE"),
            index=0,
        )
    
    with col2:
        symbol = st.text_input("Asset Symbol", "AAPL")
    
    if st.button("🚀 Launch Analysis", key="launch_chart"):
        url = f"https://www.tradingview.com/chart/?symbol={exchange}:{symbol}" 
        webbrowser.open(url)
        st.success(f"Market terminal accessing {exchange}:{symbol}")

def private_channel_finder():
    st.markdown("### 🔗 Private Trading Channel Finder")
    st.markdown("Discover elite trading communities with verified track records")
    
    # Trading Channel Database
    TRADING_CHANNELS = [
        {
            "name": "StocksCharge",
            "url": "https://t.me/stockscharge",
            "description": "Daily stock picks & market analysis with 85% accuracy",
            "members": "45K+",
            "focus": "Indian Stocks"
        },
        {
            "name": "TWK Official",
            "url": "https://t.me/twkofficial79",
            "description": "Swing trading strategies for NSE/BSE",
            "members": "32K+",
            "focus": "Technical Analysis"
        },
        {
            "name": "US Stock Hub",
            "url": "https://t.me/USStockHub",
            "description": "NASDAQ/NYSE alerts and pre-market movers",
            "members": "28K+",
            "focus": "US Markets"
        },
        {
            "name": "Crypto Signals",
            "url": "https://t.me/CryptoSG",
            "description": "Bitcoin/Altcoin trading signals",
            "members": "51K+",
            "focus": "Cryptocurrency"
        },
        {
            "name": "Forex Elite",
            "url": "https://t.me/ForexElite",
            "description": "Daily FX trading setups",
            "members": "18K+",
            "focus": "Forex"
        }
    ]
    
    # Search functionality
    search_term = st.text_input("Search channels by name or focus area:")
    
    # Filter channels based on search
    filtered_channels = [
        channel for channel in TRADING_CHANNELS
        if search_term.lower() in channel["name"].lower() 
        or search_term.lower() in channel["focus"].lower()
    ] if search_term else TRADING_CHANNELS
    
    # Display channel cards
    for channel in filtered_channels:
        with st.container():
            st.markdown(f"""
            <div class="channel-card">
                <div class="channel-name">{channel['name']}</div>
                <div>📌 {channel['focus']}</div>
                <div>👥 {channel['members']} members</div>
                <div>📝 {channel['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Join {channel['name']}", key=f"join_{channel['name']}"):
                webbrowser.open(channel['url'])
                st.success(f"Opening {channel['name']}...")

def network_hub():
    st.markdown("### 💼 Professional Network Hub")
    
    post = st.text_area("Strategic Update", height=120)
    media_url = st.text_input("Media Reference (URL)")
    
    if st.button("🌐 Publish to Network", key="publish_post"):
        if post:
            share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={media_url if media_url else 'https://example.com'}&text={post}"
            webbrowser.open(share_url)
            st.success("Broadcast to professional network")
        else:
            st.error("Content required for transmission")

def main():
    if 'current_view' not in st.session_state:
        st.session_state.current_view = "Secure Messenger"
    
    display_luxury_menu()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.current_view == "Secure Messenger":
        secure_messenger()
    elif st.session_state.current_view == "Market Terminal":
        market_terminal()
    elif st.session_state.current_view == "Private Trading Channels":
        private_channel_finder()
    elif st.session_state.current_view == "Network Hub":
        network_hub()

if __name__ == "__main__":
    main()
