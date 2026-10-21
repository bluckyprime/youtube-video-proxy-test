
import hashlib
import streamlit as st

st.set_page_config(
    page_title="Video Data Relay Test",
    page_icon="📦",
    layout="centered",
)

st.title("📦 Video Data Relay Test")
st.write(
    "Test whether file bytes remain identical "
    "when uploaded to and downloaded from a server."
)

uploaded = st.file_uploader(
    "Upload a test file",
    type=None,
)

if uploaded is not None:
    data = uploaded.getvalue()
    digest = hashlib.sha256(data).hexdigest()

    st.subheader("Original file")
    st.write("Filename:", uploaded.name)
    st.write("Size:", f"{len(data):,} bytes")
    st.code(digest, language=None)

    st.download_button(
        label="Download identical file",
        data=data,
        file_name=f"copy_{uploaded.name}",
        mime="application/octet-stream",
        use_container_width=True,
    )

    st.info(
        "The download contains the same bytes "
        "as the uploaded file. No re-encoding is performed."
    )

    st.caption(
        "Compare the SHA-256 hash of the downloaded "
        "file with the original to verify integrity."
    )
