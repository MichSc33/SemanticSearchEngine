import matplotlib.pyplot as plt
import nmslib
import numpy as np
import os
import streamlit as st

from PIL import Image
from transformers import CLIPProcessor, FlaxCLIPModel

import utils

BASELINE_MODEL = "openai/clip-vit-base-patch32"
MODEL_PATH = "flax-community/clip-rsicd-v2"
IMAGE_VECTOR_FILE = "./App/vectors/test-bs128x8-lr5e-6-adam-ckpt-1.tsv"
IMAGES_DIR = "./App/images"
CAPTIONS_FILE = os.path.join(IMAGES_DIR, "test-captions.json")

def app():
    filenames, index = utils.load_index(IMAGE_VECTOR_FILE)
    model, processor = utils.load_model(MODEL_PATH, BASELINE_MODEL)
    image2caption = utils.load_captions(CAPTIONS_FILE)

    st.title("Retrieve Images given Text")
    st.markdown("""
        Test
    """)
    suggested_query = [
        "Ares",
        "Artemis and Apollon",
        "Persephone",
        "exekias",
        "Aphrodite",
        "Hercules",
        "Donkey"
    ]
    st.text("Some suggested queries to start you off with...")
    col0, col1, col2, col3, col4, col5, col6 = st.beta_columns(7)
        # [1, 1.1, 1.3, 1.1, 1, 1, 1])
    suggest_idx = -1
    with col0:
        if st.button(suggested_query[0]):
            suggest_idx = 0
    with col1:
        if st.button(suggested_query[1]):
            suggest_idx = 1
    with col2:
        if st.button(suggested_query[2]):
            suggest_idx = 2
    with col3:
        if st.button(suggested_query[3]):
            suggest_idx = 3
    with col4:
        if st.button(suggested_query[4]):
            suggest_idx = 4
    with col5:
        if st.button(suggested_query[5]):
            suggest_idx = 5
    with col6:
        if st.button(suggested_query[6]):
            suggest_idx = 6
    query = st.text_input("OR enter a text Query:")
    query = suggested_query[suggest_idx] if suggest_idx > -1 else query

    if st.button("Query") or suggest_idx > -1:
        inputs = processor(text=[query], images=None, return_tensors="jax", padding=True)
        query_vec = model.get_text_features(**inputs)
        query_vec = np.asarray(query_vec)
        ids, distances = index.knnQuery(query_vec, k=10)
        result_filenames = [filenames[id] for id in ids]
        for rank, (result_filename, score) in enumerate(zip(result_filenames, distances)):
            caption = "{:s} (score: {:.3f})".format(result_filename, 1.0 - score)
            col1, col2, col3 = st.beta_columns([2, 10, 10])
            col1.markdown("{:d}.".format(rank + 1))
            col2.image(Image.open(os.path.join(IMAGES_DIR, result_filename)),
                       caption=caption)
            caption_text = []
            for caption in image2caption[result_filename]:
                caption_text.append("* {:s}\n".format(caption))
            col3.markdown("".join(caption_text))                       
            st.markdown("---")
        suggest_idx = -1
