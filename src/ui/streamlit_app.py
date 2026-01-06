import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Enterprise Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .search-box {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .result-card {
        background: white;
        padding: 1.5rem;
        color: #111111;     
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .citation {
        background: #e7f3ff;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        border-left: 3px solid #2196F3;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []

def call_search_api(query, sources=None, max_results=10):
    """Call the search API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/search",
            json={
                "query": query,
                "sources": sources,
                "max_results": max_results
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error calling API: {e}")
        return None

def get_sources():
    """Get available sources"""
    try:
        response = requests.get(f"{API_BASE_URL}/sources")
        response.raise_for_status()
        return response.json()["sources"]
    except:
        return []

def get_stats():
    """Get system stats"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        response.raise_for_status()
        return response.json()
    except:
        return None

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x50/667eea/ffffff?text=Enterprise+Search", width=200)
    st.markdown("---")
    
    st.markdown("### 🎯 Data Sources")
    sources_data = get_sources()
    
    if sources_data:
        selected_sources = []
        for source in sources_data:
            if st.checkbox(f"{source['icon']} {source['name']}", value=True, key=source['id']):
                selected_sources.append(source['id'])
    else:
        selected_sources = None
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Settings")
    max_results = st.slider("Max Results", 5, 20, 10)
    
    st.markdown("---")
    
    # System stats
    stats = get_stats()
    if stats:
        st.markdown("### 📊 Statistics")
        st.metric("Total Documents", stats.get("total_documents", 0))
        st.metric("Queries Today", stats.get("queries_today", 0))
        st.metric("Avg Latency", f"{stats.get('avg_latency_ms', 0)}ms")

# Main content
st.markdown('<h1 class="main-header">🔍 Enterprise Intelligent Search</h1>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; color: #666; margin-bottom: 2rem;'>
    AI-powered search across Confluence, Jira, Slack, and Documents with accurate citations
</div>
""", unsafe_allow_html=True)

# Search interface
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "",
        placeholder="Ask anything about your enterprise data...",
        label_visibility="collapsed",
        key="search_input"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True, type="primary")

# Example queries
st.markdown("##### 💡 Try these examples:")
example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    if st.button("📚 Latest documentation updates", use_container_width=True):
        query = "What are the latest documentation updates?"
        search_button = True

with example_col2:
    if st.button("🎯 Sprint planning decisions", use_container_width=True):
        query = "What were the key decisions in last week's sprint planning?"
        search_button = True

with example_col3:
    if st.button("🔐 Authentication system docs", use_container_width=True):
        query = "Show me documentation about our authentication system"
        search_button = True

# Execute search
if search_button and query:
    with st.spinner("🤖 Searching across enterprise data sources..."):
        result = call_search_api(query, selected_sources, max_results)
        
        if result:
            # Add to history
            st.session_state.search_history.insert(0, {
                "query": query,
                "timestamp": datetime.now(),
                "result": result
            })
            
            # Display results
            st.markdown("---")
            
            # Answer section
            st.markdown("### 💬 Answer")
            
            # Confidence indicator
            confidence = result.get("confidence", 0)
            confidence_color = "green" if confidence > 0.7 else "orange" if confidence > 0.4 else "red"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col2:
                st.metric("Confidence", f"{confidence*100:.0f}%")
            with col3:
                st.metric("Latency", f"{result.get('latency_ms', 0)}ms")
            
            # Answer text
            st.markdown(f"""
            <div class='result-card'>
                <p style='font-size: 1.1rem; line-height: 1.6;'>{result.get('answer', 'No answer available')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Citations
            if result.get("citations"):
                st.markdown("### 📎 Citations")
                for citation in result["citations"]:
                    with st.expander(f"📄 [{citation['source_number']}] {citation['title']} ({citation['source']})"):
                        st.markdown(f"**Excerpt:** {citation['excerpt']}")
                        if citation.get('url'):
                            st.markdown(f"[🔗 View Source]({citation['url']})")
            
            # Documents
            if result.get("documents"):
                st.markdown("### 📚 Retrieved Documents")
                
                # Source distribution
                source_counts = {}
                for doc in result["documents"]:
                    source = doc["source"]
                    source_counts[source] = source_counts.get(source, 0) + 1
                
                # Visualization
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(source_counts.keys()),
                        y=list(source_counts.values()),
                        marker_color=['#667eea', '#764ba2', '#f093fb', '#4facfe']
                    )
                ])
                fig.update_layout(
                    title="Documents by Source",
                    xaxis_title="Source",
                    yaxis_title="Count",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Document list
                for idx, doc in enumerate(result["documents"], 1):
                    with st.expander(f"📄 {idx}. {doc['title']} ({doc['source']}) - Score: {doc['score']:.2f}"):
                        st.markdown(f"**Excerpt:** {doc['excerpt']}")
                        if doc.get('url'):
                            st.markdown(f"[🔗 View Full Document]({doc['url']})")
                        st.markdown(f"**Relevance Score:** {doc['score']:.3f}")

# Search history
if st.session_state.search_history:
    st.markdown("---")
    st.markdown("### 📜 Recent Searches")
    
    for idx, item in enumerate(st.session_state.search_history[:5]):
        with st.expander(f"🔍 {item['query']} - {item['timestamp'].strftime('%H:%M:%S')}"):
            st.markdown(f"**Answer:** {item['result'].get('answer', 'N/A')[:200]}...")
            st.markdown(f"**Sources:** {', '.join(item['result'].get('sources_searched', []))}")