import streamlit as st
import requests
import datetime
import time

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner - Suresh",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Professional CSS styling
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .company-brand {
        font-size: 0.9em;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    .chat-container {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #007bff;
    }
    .user-message {
        background: #007bff;
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        text-align: right;
        font-weight: 500;
    }
    .bot-message {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #28a745;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    .input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
        border: 1px solid #e9ecef;
    }
    .stButton>button {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background: #0056b3;
    }
    .stTextInput>div>div>input {
        border-radius: 6px;
        border: 1px solid #ced4da;
        padding: 0.5rem 1rem;
    }
    .sidebar-header {
        background: #343a40;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
    }
    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #007bff;
    }
    .metric-label {
        font-size: 0.9em;
        color: #6c757d;
        margin-top: 0.25rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Backend endpoint
BASE_URL = "http://localhost:8000"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = None

# Sidebar
with st.sidebar:
    st.markdown(
        '<div class="sidebar-header"><h4>AI Travel Planner</h4><div class="company-brand">by Suresh</div></div>',
        unsafe_allow_html=True,
    )

    # Stats
    st.markdown("### 📊 Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="metric-card"><div class="metric-value">{}</div><div class="metric-label">Queries Today</div></div>'.format(
                st.session_state.query_count
            ),
            unsafe_allow_html=True,
        )
    with col2:
        last_time = (
            st.session_state.last_query_time.strftime("%H:%M")
            if st.session_state.last_query_time
            else "None"
        )
        st.markdown(
            '<div class="metric-card"><div class="metric-value">{}</div><div class="metric-label">Last Query</div></div>'.format(
                last_time
            ),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.query_count = 0
        st.rerun()

    if st.button("📈 View Details", use_container_width=True):
        with st.expander("Usage Statistics", expanded=True):
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.write(f"**Total Queries:** {st.session_state.query_count}")
            st.write(f"**Chat Messages:** {len(st.session_state.messages)}")
            if st.session_state.last_query_time:
                st.write(
                    f"**Last Activity:** {st.session_state.last_query_time.strftime('%Y-%m-%d %H:%M')}"
                )
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Popular destinations
    st.markdown("### 🌍 Popular Destinations")
    destinations = [
        "Paris, France",
        "Tokyo, Japan",
        "Bali, Indonesia",
        "New York, USA",
        "Swiss Alps",
    ]
    selected_dest = st.selectbox(
        "Quick select:", ["Choose destination..."] + destinations
    )
    if selected_dest != "Choose destination...":
        st.session_state.quick_dest = f"Plan a 5-day trip to {selected_dest}"

# Main content
st.markdown(
    """
<div class="main-header">
    <h1>✈️ AI Travel Planner</h1>
    <p>Professional travel planning powered by advanced AI</p>
    <div class="company-brand">Developed by Suresh</div>
</div>
""",
    unsafe_allow_html=True,
)

# Chat history display
if st.session_state.messages:
    st.markdown("### 💬 Recent Conversations")
    for i, message in enumerate(st.session_state.messages[-6:]):  # Show last 6 messages
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message">👤 You: {message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            with st.expander(
                f"🤖 AI Response - {message['timestamp']}",
                expanded=(i == len(st.session_state.messages[-6:]) - 1),
            ):
                st.markdown(message["content"])

# Input section
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### 🎯 Plan Your Trip")

col1, col2 = st.columns([4, 1])

with col1:
    # Check if there's a quick destination selected
    default_input = st.session_state.get("quick_dest", "")
    user_input = st.text_input(
        "Enter your travel request",
        placeholder="e.g. Plan a 7-day trip to Kyoto, Japan with cultural experiences",
        value=default_input,
        key="user_input",
    )

with col2:
    submit_button = st.button("🚀 Generate Plan", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Clear quick destination after use
if "quick_dest" in st.session_state and user_input != st.session_state.quick_dest:
    del st.session_state.quick_dest

if submit_button and user_input.strip():
    # Add user message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
            "timestamp": datetime.datetime.now().strftime("%H:%M"),
        }
    )
    st.session_state.query_count += 1
    st.session_state.last_query_time = datetime.datetime.now()

    try:
        # Progress bar with professional messaging
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.info("🔍 Analyzing travel request...")
        progress_bar.progress(25)
        time.sleep(0.5)

        status_text.info("🌐 Gathering real-time travel data...")
        progress_bar.progress(50)
        time.sleep(0.5)

        # API call
        status_text.info("🤖 AI generating personalized itinerary...")
        progress_bar.progress(75)

        payload = {"question": user_input}
        response = requests.post(f"{BASE_URL}/query", json=payload, timeout=30)

        progress_bar.progress(100)
        status_text.success("✅ Travel plan generated successfully!")
        time.sleep(1)

        # Clear progress
        progress_bar.empty()
        status_text.empty()

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")

            # Add bot response to history
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "timestamp": datetime.datetime.now().strftime("%H:%M"),
                }
            )

            # Display the response
            st.markdown('<div class="bot-message">', unsafe_allow_html=True)
            st.markdown("## 🌍 Your Travel Itinerary")
            st.markdown(
                f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  |  **AI Travel Planner by Suresh**"
            )

            st.markdown("---")
            st.markdown(answer)
            st.markdown("---")

            # Success message
            st.success("✨ Your personalized travel plan is ready!")

            # Disclaimer
            st.info(
                "ℹ️ **Important:** This itinerary was generated by AI. Please verify all details including prices, availability, and requirements before booking."
            )

        else:
            st.error(f"❌ Unable to generate plan: {response.text}")
            # Add error to history
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": f"❌ Error: {response.text}",
                    "timestamp": datetime.datetime.now().strftime("%H:%M"),
                }
            )

    except requests.exceptions.Timeout:
        st.error("⏰ Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Connection issue. Please check your internet connection.")
    except Exception as e:
        st.error(f"💥 An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6c757d; padding: 1rem; font-size: 0.9em;">AI Travel Planner • Developed by Suresh • 2026</div>',
    unsafe_allow_html=True,
)
