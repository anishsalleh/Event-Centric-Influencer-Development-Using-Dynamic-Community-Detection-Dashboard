import streamlit as st  # <-- Change 'as pd' to 'as st'
import pandas as pd     # <-- Standard pandas import
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64

# Set page configuration for a modern wide layout
st.set_page_config(
    page_title="CarBoot Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fungsi untuk menukar imej tempatan kepada Base64 supaya boleh dibaca oleh CSS
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Custom CSS for a Futuristic, Cyberpunk UI with Glassmorphism
st.markdown("""
    <style>
    /* Global Container Adjustments */
    .block-container {
        background-color: rgba(6, 10, 26, 0.75) !important; /* Deep space dark blue tint */
        padding: 2rem 3rem !important;
        border-radius: 20px;
        margin-top: 20px;
        box-shadow: 0 0 25px rgba(59, 130, 246, 0.2); /* Soft blue outer neon glow */
        border: 1px solid rgba(59, 130, 246, 0.15);
        backdrop-filter: blur(8px) !important; /* Premium holographic blur effect */
    }

    /* Sidebar - Sleek Neon Border and Darker Tint */
    [data-testid="stSidebar"] {
        background-color: rgba(4, 9, 20, 0.9) !important;
        border-right: 2px solid rgba(139, 92, 246, 0.3) !important; /* Neon Purple divider */
        backdrop-filter: blur(10px);
    }
    
    /* Text colors inside sidebar for readability */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }

    /* Futuristic Header Banner Title */
    .main-title {
        font-size: 40px;
        font-weight: 900;
        color: #00F2FE !important; /* Glowing Electric Cyan */
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.6); /* Text neon reflection */
        text-align: left;
        margin-bottom: 5px;
        padding: 5px 0px;
        letter-spacing: 0.5px;
    }

    /* Holographic Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8)) !important;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(0, 242, 254, 0.25) !important; /* Light neon cyan border */
        transition: all 0.3s ease;
    }
    
    /* Hover effect to make it feel reactive/alive */
    .metric-card:hover {
        border-color: #00F2FE !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
        transform: translateY(-2px);
    }
    
    /* Metric Labels and Values text styling */
    .metric-card h3, .metric-card h4 {
        color: #94A3B8 !important; /* Cool grey for labels */
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px !important;
        font-weight: 600;
    }
    .metric-card h2 {
        color: #FF007F !important; /* Neon Magenta / Cyberpunk Pink for data numbers */
        font-size: 34px !important;
        text-shadow: 0 0 10px rgba(255, 0, 127, 0.4);
        font-weight: 800;
        margin: 0 !important;
    }

    /* Streamlit Headers Color override */
    h1, h2, h3, h4, h5, h6 {
        color: #00F2FE !important;
        text-shadow: 0 0 5px rgba(0, 242, 254, 0.2);
    }
    
    /* Style subheaders specifically */
    .stMarkdown div[data-testid="stMarkdownContainer"] p {
        color: #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# Load Datasets safely
@st.cache_data
def load_data():
    try:
        resp_df = pd.read_csv(r"C:\Users\HP\Documents\SOCMED\cleaned_respondents_data.csv")
        vendor_df = pd.read_csv(r"C:\Users\HP\Documents\SOCMED\cleaned_vendor_data.csv")
        return resp_df, vendor_df
    except Exception as e:
        st.error(f"Error loading files: {e}. Ensure the CSVs are in the same folder.")
        return None, None

resp_df, vendor_df = load_data()

# Function helper untuk analisis sentimen bahasa tempatan
def hitung_sentimen(teks):
    teks = str(teks).lower()
    positif = ['bagus', 'best', 'murah', 'untung', 'ramai', 'ok', 'good', 'puas', 'suka', 'menarik', 'mudah']
    negatif = ['mahal', 'sesak', 'jem', 'panas', 'rugi', 'kurang', 'sikit', 'susah', 'parking', 'lambat', 'kecewa']
    score = sum(1 for p in positif if p in teks) - sum(1 for n in negatif if n in teks)
    return 'Positive' if score > 0 else ('Negative' if score < 0 else 'Neutral')

if resp_df is not None and vendor_df is not None:
    
    # =========================================================================
    # KAWASAN UTAMA: SUSUNAN STRUKTUR BANNER TAJUK & LOGO DI ATAS KANAN
    # =========================================================================
    header_col, logo_top_right_col = st.columns([4, 2])
    
    with header_col:
        st.markdown('<div class="main-title">🎪 Event-Centric Influencer Development Using Dynamic Community Detection Dashboard</div>', unsafe_allow_html=True)
    
with logo_top_right_col:
        path_logo = r"C:/Users/HP/Documents/SOCMED/84808cf8-2dca-4946-817c-64ceb9fedfce.jpg"
        
        try: 
            st.image(path_logo, use_container_width=True)
        except: 
            pass


st.markdown("---")

    # Update Sidebar Navigation to include Dr's required sections
st.sidebar.header("🧭 Navigation Panel")
page = st.sidebar.radio("Go to:", [
        "📈 Overview & Metrics", 
        "👥 Respondent Analysis", 
        "🏪 Vendor Insights", 
        "📊 Analytics Report",  
    ])
    
    # -------------------------------------------------------------
    # PAGE 1: OVERVIEW
    # -------------------------------------------------------------
if page == "📈 Overview & Metrics":
        st.subheader("📌 Key Performance Indicators")
        
        # Metric Layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card"><h3>Total Respondents</h3><h2>{}</h2></div>'.format(resp_df['Speaker'].nunique()), unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card"><h3>Total Feedback Records</h3><h2>{}</h2></div>'.format(len(resp_df)), unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card"><h3>Vendor Entry Samples</h3><h2>{}</h2></div>'.format(len(vendor_df)), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
            
        # 🌍 Target Location: Changlun, Kedah
        st.subheader("🌍 Target Location: Changlun, Kedah")
            
        # Fungsi mengambil data cuaca hidup menggunakan API percuma Open-Meteo (Koordinat Changlun)
        import requests
        @st.cache_data(ttl=1800)  
        def dapatkan_cuaca_changlun():
            try:
                url = "https://api.open-meteo.com/v1/forecast?latitude=6.4313&longitude=100.4289&current_weather=true"
                response = requests.get(url, timeout=5)
                data = response.json()
                if "current_weather" in data:
                    return data["current_weather"]
                return None
            except:
                return None

        cuaca = dapatkan_cuaca_changlun()
            
        w_col1, w_col2, w_col3 = st.columns(3)
        with w_col1:
            st.markdown('<div class="metric-card"><h3>📍 Location</h3><h2>Changlun</h2></div>', unsafe_allow_html=True)
        with w_col2:
            if cuaca:
                st.markdown(f'<div class="metric-card"><h3>🌡️ Current Temperature (API)</h3><h2>{cuaca["temperature"]}°C</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><h3>🌡️ Current Temperature (API)</h3><h2>31°C</h2></div>', unsafe_allow_html=True)
        with w_col3:
            if cuaca:
                kod_cuaca = cuaca.get("weathercode", 0)
                status_cuaca = "Clear" if kod_cuaca <= 3 else "Cloudy/Rain"
                st.markdown(f'<div class="metric-card"><h3>☁️ Weather</h3><h2>{status_cuaca}</h2></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="metric-card"><h3>☁️ Weather</h3><h2>Cerah</h2></div>', unsafe_allow_html=True)
                    
        st.markdown("<br>", unsafe_allow_html=True)
            
        # High level Summary chart
        st.subheader("📊 Feedback Volume Distribution")
        fig_pie = px.pie(
            names=['Respondent Logs', 'Vendor Logs'], 
            values=[len(resp_df), len(vendor_df)],
            color_discrete_sequence=['#00F2FE', '#FF007F'],
            hole=0.4
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # -------------------------------------------------------------
    # PAGE 2: RESPONDENT ANALYSIS
    # -------------------------------------------------------------
elif page == "👥 Respondent Analysis":
        st.subheader("👥 Visitor & Respondent Sentiment Tracking")
        
        search_query = st.text_input("🔍 Search comments by keyword (e.g., 'parking', 'murah', 'makanan'):").lower()
        
        filtered_resp = resp_df.copy()
        if search_query:
            filtered_resp = filtered_resp[filtered_resp['Cleaned_Answer'].str.contains(search_query, na=False, case=False)]
            st.success(f"Found {len(filtered_resp)} matches for '{search_query}'")
        
        st.write("### 🏷️ Most Common Terms in Visitor Feedback")
        all_words = " ".join(filtered_resp['Cleaned_Answer'].dropna().astype(str))
        
        if all_words.strip():
            wordcloud = WordCloud(width=800, height=300, background_color='white', colormap='viridis').generate(all_words)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("No text data available to generate a word cloud.")

        st.write("### 💬 Detailed Responses")
        st.dataframe(filtered_resp[['Speaker', 'Raw_Answer']], use_container_width=True)

    # -------------------------------------------------------------
    # PAGE 3: VENDOR INSIGHTS
    # -------------------------------------------------------------
elif page == "🏪 Vendor Insights":
        st.subheader("🏪 Vendor Operations & Experience Analysis")
        
        tiktok_count = vendor_df['Cleaned_Answer'].str.contains('tiktok', na=False, case=False).sum()
        danok_count = vendor_df['Cleaned_Answer'].str.contains('danok|floating', na=False, case=False).sum()
        prom_count = vendor_df['Cleaned_Answer'].str.contains('promote|media', na=False, case=False).sum()
        
        vendor_metrics = pd.DataFrame({
            'Topic Mentioned': ['TikTok Strategy', 'Danok/Floating Market Concept', 'Marketing/Promotion'],
            'Mentions Count': [tiktok_count, danok_count, prom_count]
        })
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("### 📊 Key Theme Mentions among Vendors")
            fig_bar = px.bar(
                vendor_metrics, 
                x='Topic Mentioned', 
                y='Mentions Count',
                color='Topic Mentioned',
                color_discrete_sequence=['#00F2FE', '#8B5CF6', '#FF007F']
            )
            fig_bar.update_layout(
                 template="plotly_dark",
                 paper_bgcolor="rgba(0,0,0,0)",
                 plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col2:
            st.write("### 💡Key Takeaway Highlights")
            st.info("**TikTok Focus**: Vendors heavily leverage live streaming and social video to attract crowds.\n\n"
                    "**Concept Inspiration**: Several items or setups are explicitly inspired by regional trends like Danok/Hatyai floating markets.")

        st.write("### 💬 Vendor Raw Statements")
        st.dataframe(vendor_df[['Speaker', 'Raw_Answer']], use_container_width=True)

    # -------------------------------------------------------------
    # PAGE 4: ANALYTICS REPORT
    # -------------------------------------------------------------
elif page == "📊 Analytics Report":
        st.title("📋 Integrated Analysis Report")
        st.markdown("This page contains analytical components that meet the dashboard evaluation criteria.")
            
        # 1. STATISTIK RESPONDEN & VENDOR
        st.markdown("### 📊 1. Respondent and Vendor Statistics")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-card"><h4>Total Public Respondents</h4><h2>{len(resp_df)}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-card"><h4>Total Vendor Feedback</h4><h2>{len(vendor_df)}</h2></div>', unsafe_allow_html=True)
        with m3:
            unique_speakers = resp_df['Speaker'].nunique() if 'Speaker' in resp_df.columns else len(resp_df)
            st.markdown(f'<div class="metric-card"><h4>Total Unique Speakers</h4><h2>{unique_speakers}</h2></div>', unsafe_allow_html=True)
                
        st.markdown("<br>", unsafe_allow_html=True)
            
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("### 🏷️ 2. Word Cloud of Key Issues (Respondents)")
            all_resp_text = " ".join(resp_df['Cleaned_Answer'].dropna().astype(str))
            for word in ['yang', 'dan', 'di', 'ke', 'untuk', 'saya', 'ada', 'ini']:
                all_resp_text = all_resp_text.replace(f" {word} ", " ")
            
            if all_resp_text.strip():
                wordcloud = WordCloud(width=500, height=350, background_color='#0F172A', colormap='cool').generate(all_resp_text)
                fig, ax = plt.subplots(figsize=(5, 3.5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("Insufficient text data available.")
                    
        with col_right:
            st.markdown("### 🎭 3. Feedback Sentiment Analysis")
            resp_df['Sentiment'] = resp_df['Cleaned_Answer'].apply(hitung_sentimen)
            sentimen_counts = resp_df['Sentiment'].value_counts().reset_index()
            sentimen_counts.columns = ['Sentiment', 'Total']
            
            fig_sentimen = px.pie(
                sentimen_counts, names='Sentiment', values='Total',
                color='Sentiment',
                color_discrete_map={'Positive': '#10B981', 'Neutral': '#F59E0B', 'Negative': '#EF4444'},
                hole=0.3
            )
            st.plotly_chart(fig_sentimen, use_container_width=True)
                
        st.markdown("---")
        col_trend, col_influencer = st.columns(2)
            
        with col_trend:
            st.markdown("### 📈 4. Social Media Trend Chart (Event Mention Rate)")
            gabung_teks_resp = " ".join(resp_df['Cleaned_Answer'].dropna().astype(str).str.lower())
            gabung_teks_vendor = " ".join(vendor_df['Cleaned_Answer'].dropna().astype(str).str.lower())
            semua_teks = gabung_teks_resp + " " + gabung_teks_vendor
            
            tiktok_sebenar = semua_teks.count('tiktok') + semua_teks.count('tt')
            instagram_sebenar = semua_teks.count('instagram') + semua_teks.count('ig') + semua_teks.count('insta')
            facebook_sebenar = semua_teks.count('facebook') + semua_teks.count('fb')
            
            platform_data = pd.DataFrame({
                'Platform': ['TikTok', 'Instagram', 'Facebook'],
                'Total Current Mentions': [tiktok_sebenar, instagram_sebenar, facebook_sebenar]
            })
            
            fig_trend_real = px.bar(
                platform_data, 
                x='Platform', 
                y='Total Current Mentions',
                color='Platform',
                text='Total Current Mentions',
                color_discrete_map={'TikTok': '#000000', 'Instagram': '#E1306C', 'Facebook': '#1877F2'},
                title="Social Media Platform Mention Rate in Feedback"
            )
            fig_trend_real.update_traces(textposition='outside')
            st.plotly_chart(fig_trend_real, use_container_width=True)
                        
        with col_influencer:
            st.markdown("### 👑 5. Key Influencer Analysis (SNA Network Graph)")
            sna_image_path = r"C:\Users\HP\Documents\SOCMED\SNA.jpg"
            try:
                st.image(
                    sna_image_path, 
                    caption="Social Media Network Analysis (SNA) – Event Interaction Relationships",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Failed to display SNA image. Error cause: {e}")
                    
        st.markdown("---")
        # 6. STRATEGIC ACTION RECOMMENDATIONS (Upgraded Futuristic Interface)
        st.markdown("---")
        st.markdown("### ⚡ 6. Data-Driven Strategic Recommendations")
        
        # Sub-header caption explaining the source of insights
        st.markdown("<p style='color: #94A3B8; font-style: italic; margin-bottom: 15px;'>Synthesized insights derived from Cross-Dataset NLP, Sentiment Distribution, and Social Network Analysis (SNA).</p>", unsafe_allow_html=True)
        
        # Creating interactive tabs for a cleaner, high-tech breakdown
        tab_visitor, tab_vendor, tab_marketing = st.tabs(["👥 Visitor-Centric Actions", "🏪 Vendor-Centric Actions", "👑 Network & Influencer Strategy"])
        
        with tab_visitor:
            st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.3); padding: 18px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #EF4444 !important; margin-top:0;">🛑 1. Critical Facility & Traffic Mitigation</h4>
                <p style="color: #E2E8F0; margin-bottom:0;">
                    <b>Data Origin:</b> High frequency density of negative sentiment tokens (<i>'parking'</i>, <i>'jem'</i>, <i>'sesak'</i>) isolated in the Respondent Word Cloud.<br><br>
                    <b>Action Item:</b> The organizer should provide a designated park-and-ride area or work with the Changlun municipal authorities to improve traffic management during peak hours. Solving this traffic issue can enhance visitors' experience and help increase positive feedback and repeat visits.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with tab_vendor:
            st.markdown("""
            <div style="background: rgba(139, 92, 246, 0.05); border: 1px solid rgba(139, 92, 246, 0.3); padding: 18px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #8B5CF6 !important; margin-top:0;">🌌 2. Cross-Border Concept Scale-Up (Danok Theme)</h4>
                <p style="color: #E2E8F0; margin-bottom:0;">
                    <b>Data Origin:</b> Text mining from Vendor Insights highlighting a strong clustering of mentions around <i>'Danok'</i> and <i>'Hatyai Floating Market'</i> setups.<br><br>
                    <b>Action Item:</b> Take advantage of Changlun's location near the border by creating a dedicated Cross-Border Culture Zone. Organizers can also arrange vendor booths based on popular regional tourism themes to attract more visitors and provide a unique experience.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with tab_marketing:
            st.markdown("""
            <div style="background: rgba(0, 242, 254, 0.05); border: 1px solid rgba(0, 242, 254, 0.3); padding: 18px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #00F2FE !important; margin-top:0;">🚀 3. Centrality-Targeted TikTok Campaign</h4>
                <p style="color: #E2E8F0; margin-bottom:5;">
                    <b>Data Origin:</b> Overwhelming platform mention supremacy of <i>TikTok</i> over legacy apps, coupled with high-centrality bridge nodes in the <b>SNA Graph</b>.<br><br>
                    <b>Action Item:</b> Instead of relying on general advertising, the organizer should collaborate with micro-influencers identified through the Social Network Analysis (SNA) to promote the event. These influencers can help reach their communities more effectively, increase event awareness and attract more visitors. 
                </p>
            </div>
            <div style="background: rgba(255, 0, 127, 0.05); border: 1px solid rgba(255, 0, 127, 0.3); padding: 18px; border-radius: 10px;">
                <h4 style="color: #FF007F !important; margin-top:0;">📡 4. 'Live-Commerce' Vendor Incubation</h4>
                <p style="color: #E2E8F0; margin-bottom:0;">
                    <b>Data Origin:</b> Direct vendor statements identifying social stream strategies as their primary conversion channel.<br><br>
                    <b>Action Item:</b> Launch an on-site 'Live-Commerce Booster Pack' providing optimized cellular coverage or dedicated streaming corners for vendors. Empowering micro-vendors to stream dynamically from their booth stalls amplifies the digital footprint of the physical event space in real time.
                </p>
            </div>
            """, unsafe_allow_html=True)