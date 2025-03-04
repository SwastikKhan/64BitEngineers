import streamlit as st

# Set Page Configuration
st.set_page_config(page_title="Medical Imaging AI Assistant", layout="wide")

# Sidebar: Patient Details & History
st.sidebar.header("🩺 Patient Information")
st.sidebar.text_input("Patient Name")
st.sidebar.text_input("Age")
st.sidebar.text_input("Gender")
st.sidebar.text_area("Medical History", placeholder="Enter previous diagnoses, allergies, past reports...")
st.sidebar.subheader("📁 Uploaded Reports")
st.sidebar.write("List of uploaded medical reports will appear here.")

# Main Layout: Upload & Analysis Section
col1, col2 = st.columns([1.2, 1])

with col1:
    st.header("📤 Upload Medical Report")
    uploaded_file = st.file_uploader("Upload X-ray, MRI, CT scan (PNG, JPG, PDF, DICOM)", 
                                     type=["png", "jpg", "jpeg", "pdf", "dcm"])
    
    if uploaded_file:
        st.success("✅ File uploaded successfully")
        st.image(uploaded_file, caption="Uploaded Scan", use_column_width=True)  # Display uploaded image
    
    st.subheader("📑 Uploaded Reports")
    st.write("Here, users can see a list of all uploaded reports.")  # Placeholder for file list

with col2:
    st.header("🧠 AI-Based Report Analysis")
    st.info("AI-detected anomalies will be displayed here with confidence scores.")  # Placeholder for AI results
    
    # Critical Alert Section
    st.warning("🚨 Emergency alert will be triggered if critical conditions are detected.")

    # Recommendations
    st.subheader("🍎 Personalized Insights")
    st.write("- Suggested dietary changes based on medical history")
    st.write("- Health & lifestyle improvement tips")

# Footer
st.markdown("---")
st.markdown("© 2025 Medical Imaging AI Assistant | Privacy Policy | Contact Support")
