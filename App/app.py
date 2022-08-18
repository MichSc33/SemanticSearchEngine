import dashboard_text2image
import dashboard_image2image
import dashboard_featurefinder

import streamlit as st

PAGES = {
    "Retrieve Images given Text": dashboard_text2image,
    "Retrieve Images given Image": dashboard_image2image,
    "Find Feature in Image": dashboard_featurefinder,
}

st.sidebar.title("Semantic Search Engine for Attic Vase paintings")
st.sidebar.image("./App/vases_thumbnail.jpeg")
st.sidebar.markdown("""
    Test Project
""")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
