import streamlit as st
import time
import os
import numpy as np
from PIL import Image
import pandas as pd
import plotly.express as px

# Import the custom modules
from model import SkinDiseaseModel
from advisory import SkinAdvisoryEngine
from doctor import DoctorRecommendationEngine
from utils import make_gradcam_heatmap, overlay_gradcam
from report import create_pdf_report
from chatbot import MedicalChatbot

# 1. Page Configuration
st.set_page_config(
    page_title="SkinCare AI Pro | Diagnosis & Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Language Toggle
    lang_choice = st.radio("Select Language / भाषा चुनें", ["English", "हिंदी"])
    lang_code = 'hi' if lang_choice == "हिंदी" else 'en'
    
    # Settings
    user_location = st.text_input("🌍 Location (For Nearby Doctors)", "Mumbai, MH")
    gemini_api_key = st.text_input("🔑 Gemini API Key (Chatbot)", type="password", help="Get your API key from Google AI Studio")
    
    st.markdown("---")
    st.info("🧠 Model Info: MobileNetV2 (HAM10000)\n\n📈 XAI: Grad-CAM Activated")

# Initialize engines once (cached using Streamlit)
@st.cache_resource
def load_engines():
    inference_engine = SkinDiseaseModel()
    advisory_engine = SkinAdvisoryEngine()
    doctor_engine = DoctorRecommendationEngine()
    return inference_engine, advisory_engine, doctor_engine

inference_eng, advisory_eng, doctor_eng = load_engines()

# Initialize Chatbot based on Sidebar API Key
chatbot = MedicalChatbot(api_key=gemini_api_key)

# Translations Dictionary for UI Elements
ui_text = {
    'title': {"en": "🩺 AI-Based Skin Disease Diagnosis Pro", "hi": "🩺 एआई आधारित त्वचा रोग जांच प्रो"},
    'desc': {"en": "Upload a clear, close-up image of a skin lesion. This system provides Grad-CAM analysis, risk estimation, PDF reports, and AI chatbot assistance.", "hi": "त्वचा के घाव/दाग की साफ फोटो अपलोड करें। यह सिस्टम बीमारी की जांच, संभावित खतरा, पीडीएफ रिपोर्ट, और एआई चैटबॉट (AI Chatbot) की सुविधा देता है।"},
    'disclaimer': {"en": "Disclaimer: This tool provides preliminary analysis only. It is NOT a replacement for a professional medical diagnosis.", "hi": "चेतावनी: यह उपकरण केवल प्रारंभिक जांच के लिए है। यह पेशेवर चिकित्सा सलाह का विकल्प नहीं है।"},
    'upload': {"en": "Upload Skin Image (JPG/PNG)", "hi": "स्किन की फोटो अपलोड करें (JPG/PNG)"},
    'btn_analyze': {"en": "🔍 Analyze Image", "hi": "🔍 फोटो की जाँच करें"},
    'analyzing': {"en": "Analyzing image... (Generating Heatmaps)", "hi": "फोटो की जाँच हो रही है... (हीटमैप बन रहा है)"},
    'results': {"en": "Analysis Results", "hi": "जाँच के परिणाम"},
    'high_alert': {"en": "🚨 HIGH RISK DETECTED: Consult a dermatologist immediately!", "hi": "🚨 भारी जोखिम (HIGH RISK): तुरंत एक त्वचा विशेषज्ञ (Dermatologist) से मिलें!"},
    'precautions': {"en": "Recommended Precautions", "hi": "सुझाई गई सावधानियां (Precautions)"},
    'doctors': {"en": f"📍 Nearby Dermatologists in {user_location}", "hi": f"📍 {user_location} में आस-पास के त्वचा विशेषज्ञ"},
    'download': {"en": "📄 Download Medical Report (PDF)", "hi": "📄 मेडिकल रिपोर्ट डाउनलोड करें (PDF)"},
    'chat_title': {"en": "💬 AI Medical Assistant", "hi": "💬 एआई मेडिकल असिस्टेंट (Chatbot)"},
    'chat_prompt': {"en": "Ask me anything about your analysis...", "hi": "जांच के बारे में कुछ भी पूछें..."}
}

# 3. Main Title & Description
st.title(ui_text['title'][lang_code])
st.markdown(f"**{ui_text['desc'][lang_code]}**")
st.warning(ui_text['disclaimer'][lang_code])

# Chatbot Session State Init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_data" not in st.session_state:
    st.session_state.context_data = None

# Ensure temp directory for PDF parsing exists
os.makedirs("temp", exist_ok=True)

# 4. Upload Section
uploaded_file = st.file_uploader(ui_text['upload'][lang_code], type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Three column layout: Image, GradCAM
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Original Image" if lang_code == "en" else "अपलोड की गई फोटो")
        try:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            analyze_button = st.button(ui_text['btn_analyze'][lang_code], type="primary", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            analyze_button = False
            
    if analyze_button:
        with st.spinner(ui_text['analyzing'][lang_code]):
            # Mock delay for UX
            time.sleep(1) 
            
            # --- A. Inference ---
            try:
                results, preprocessed_array = inference_eng.predict(image, top_k=3)
                top_pred_class = results[0]['class']
                top_confidence = results[0]['confidence']
            except Exception as e:
                st.error(f"Prediction Error: {e}")
                results = [{"class": "Unknown", "confidence": 0.0}]
                preprocessed_array = None
                top_pred_class, top_confidence = "Unknown", 0.0
            
            # --- B. Grad-CAM XAI ---
            if preprocessed_array is not None and inference_eng.is_loaded:
                heatmap = make_gradcam_heatmap(preprocessed_array, inference_eng.model)
                superimposed_img = overlay_gradcam(image, heatmap)
            else:
                superimposed_img = np.array(image.convert('RGB')) # mock fallback
            
            with col2:
                st.subheader("XAI Heatmap (Grad-CAM)" if lang_code == "en" else "एआई हीटमैप (प्रभावित क्षेत्र)")
                st.image(superimposed_img, use_column_width=True)
            
            # Save Temp Images for PDF
            img_path, heat_path = "temp/upl.jpg", "temp/heat.jpg"
            image.convert("RGB").save(img_path)
            Image.fromarray(superimposed_img).save(heat_path)
            
            # --- C. Advisory Data ---
            info = advisory_eng.analyze(top_pred_class, top_confidence, lang=lang_code)
            st.session_state.context_data = info # Save context for chatbot
            
            st.markdown("---")
            st.subheader(ui_text['results'][lang_code])
            
            # Smart Alert System
            if info['severity'] in ['High']:
                st.error(ui_text['high_alert'][lang_code], icon="🚨")
            
            # Metrics
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Predicted Disease", str(info['name']))
            mcol2.metric("Confidence Score", f"{top_confidence:.1f}%")
            
            sev_color = "inverse" if info['severity'] == "High" else "normal"
            mcol3.metric("Severity Level", str(info['severity']), delta_color=sev_color)
            
            st.markdown(f"**Risk Level:** `{info['risk_level']}`")
            st.info(f"**Description:** {info['description']}")
            
            # --- D. Confidence Visualization (Plotly) ---
            df_preds = pd.DataFrame(results)
            # rename for plot
            df_preds.rename(columns={"class": "Disease", "confidence": "Confidence (%)"}, inplace=True)
            fig = px.bar(df_preds, x="Confidence (%)", y="Disease", orientation='h', 
                         title="Top 3 Predictions Confidence" if lang_code == "en" else "संभावित बीमारियों का ग्राफ",
                         color="Confidence (%)", color_continuous_scale="Reds")
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Precautions
            st.markdown(f"### 🛑 {ui_text['precautions'][lang_code]}")
            for prec in info['precautions']:
                st.markdown(f"- {prec}")
                
            st.markdown("---")
            
            # --- E. Doctor & PDF Report ---
            doc_col, pdf_col = st.columns([2, 1])
            with doc_col:
                st.subheader(ui_text['doctors'][lang_code])
                doctors = doctor_eng.search_nearby_doctors(user_location)
                    
                if doctors:
                    for doc in doctors:
                        with st.container(border=True):
                            st.markdown(f"**👩‍⚕️ {doc['name']}** - ⭐ {doc['rating']}/5.0")
                            st.write(f"🗺️ Address: {doc['address']} ({doc['distance_km']} km away)")
                else:
                    st.warning("No specialists found nearby.")
            
            with pdf_col:
                st.subheader("Report" if lang_code == "en" else "रिपोर्ट")
                try:
                    pdf_path = create_pdf_report(
                        img_path, heat_path, results, info, doctors, user_location
                    )
                    with open(pdf_path, "rb") as pdf_file:
                        PDFbyte = pdf_file.read()

                    st.download_button(
                        label=ui_text['download'][lang_code],
                        data=PDFbyte,
                        file_name="Medical_Report.pdf",
                        mime='application/octet-stream',
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")

# --- F. Chatbot System ---
if st.session_state.context_data is not None:
    st.markdown("---")
    st.subheader(ui_text['chat_title'][lang_code])
    
    if not chatbot.is_ready():
        st.warning("⚠️ Enter your Gemini API Key in the sidebar to chat with the Medical Assistant.")
    else:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input(ui_text['chat_prompt'][lang_code]):
            # Display user message in chat message container
            st.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.spinner("Thinking..." if lang_code == "en" else "सोच रहा है..."):
                    response = chatbot.generate_response(prompt, st.session_state.context_data)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
