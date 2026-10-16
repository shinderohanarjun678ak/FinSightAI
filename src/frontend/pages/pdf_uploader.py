import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="PDF Uploader Dashboard", layout="centered")

# Main Dashboard Content
st.title("📄 PDF Uploader Page")
st.markdown("Upload your payment transaction statements below.")
st.write("") 

# Google Pay (GPay) Uploader
with st.container():
    st.subheader("GPay")
    gpay_file = st.file_uploader("Upload GPay PDF Statement", type=["pdf"], key="gpay_upload")
    if gpay_file:
        st.success(f"Successfully uploaded: {gpay_file.name}")

st.divider()

# PhonePe Uploader
with st.container():
    st.subheader("PhonePe")
    phonepe_file = st.file_uploader("Upload PhonePe PDF Statement", type=["pdf"], key="phonepe_upload")
    if phonepe_file:
        st.success(f"Successfully uploaded: {phonepe_file.name}")

st.divider()

# Paytm Uploader
with st.container():
    st.subheader("Paytm")
    paytm_file = st.file_uploader("Upload Paytm PDF Statement", type=["pdf"], key="paytm_upload")
    if paytm_file:
        st.success(f"Successfully uploaded: {paytm_file.name}")

st.divider() # Adds a nice visual line before the button

# --- PROCEED BUTTON LOGIC (Must be at the very bottom, completely unindented) ---
if st.button("Proceed", type="primary", use_container_width=True):
    # Check which files were actually uploaded
    uploaded_platforms = []
    if gpay_file: uploaded_platforms.append("GPay")
    if phonepe_file: uploaded_platforms.append("PhonePe")
    if paytm_file: uploaded_platforms.append("Paytm")
    
    # Verify at least one file is uploaded
    if len(uploaded_platforms) > 0:
        st.balloons() 
        st.success(f"🚀 Proceeding to extract data from: {', '.join(uploaded_platforms)}")
    else:
        st.warning("⚠️ Please upload at least one PDF statement before proceeding.")