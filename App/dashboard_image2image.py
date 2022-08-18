import matplotlib.pyplot as plt
import nmslib
import numpy as np
import os
import requests
import streamlit as st

from PIL import Image
from transformers import CLIPProcessor, FlaxCLIPModel

import utils

BASELINE_MODEL = "openai/clip-vit-base-patch32"
MODEL_PATH = "flax-community/clip-rsicd-v2"
IMAGE_VECTOR_FILE = "./App/vectors/test-bs128x8-lr5e-6-adam-ckpt-1.tsv"
IMAGES_DIR = "./App/images"
CAPTIONS_FILE = os.path.join(IMAGES_DIR, "test-captions.json")

@st.cache(allow_output_mutation=True)
def load_example_images():
    example_images = {}
    image_names = os.listdir(IMAGES_DIR)
    for image_name in image_names:
        if image_name.find("_") < 0:
            continue
        image_class = image_name.split("_")[0]
        if image_class in example_images.keys():
            example_images[image_class].append(image_name)
        else:
            example_images[image_class] = [image_name]
    example_image_list = sorted([v[np.random.randint(0, len(v))] 
                                for k, v in example_images.items()][0:10])
    return example_image_list


def get_image_thumbnail(image_filename):
    image = Image.open(os.path.join(IMAGES_DIR, image_filename))
    image = image.resize((100, 100))
    return image


def download_and_prepare_image(image_url):
    try:
        image_raw = requests.get(image_url, stream=True,).raw
        image = Image.open(image_raw).convert("RGB")
        width, height = image.size
        resize_mult = width / 224 if width < height else height / 224
        image = image.resize((int(width // resize_mult), 
                              int(height // resize_mult)))
        width, height = image.size
        left = int((width - 224) // 2)
        top = int((height - 224) // 2)
        right = int((width + 224) // 2)
        bottom = int((height + 224) // 2)
        image = image.crop((left, top, right, bottom))
        return image
    except Exception as e:
        return None

def app():
    filenames, index = utils.load_index(IMAGE_VECTOR_FILE)
    model, processor = utils.load_model(MODEL_PATH, BASELINE_MODEL)
    image2caption = utils.load_captions(CAPTIONS_FILE)

    example_image_list = load_example_images()

    st.title("Retrieve Images given Images")
    st.markdown("""
    Test
    """)

    suggest_idx = -1
    col0, col1, col2, col3, col4 = st.beta_columns(5)
    col0.image(get_image_thumbnail(example_image_list[0]))
    col1.image(get_image_thumbnail(example_image_list[1]))
    col2.image(get_image_thumbnail(example_image_list[2]))
    col3.image(get_image_thumbnail(example_image_list[3]))
    col4.image(get_image_thumbnail(example_image_list[4]))
    col0t, col1t, col2t, col3t, col4t = st.beta_columns(5)
    with col0t:
        if st.button("Image-1"):
            suggest_idx = 0
    with col1t:
        if st.button("Image-2"):
            suggest_idx = 1
    with col2t:
        if st.button("Image-3"):
            suggest_idx = 2
    with col3t:
        if st.button("Image-4"):
            suggest_idx = 3
    with col4t:
        if st.button("Image-5"):
            suggest_idx = 4
    col5, col6, col7, col8, col9 = st.beta_columns(5)
    col5.image(get_image_thumbnail(example_image_list[5]))
    col6.image(get_image_thumbnail(example_image_list[6]))
    col7.image(get_image_thumbnail(example_image_list[7]))
    col8.image(get_image_thumbnail(example_image_list[8]))
    col9.image(get_image_thumbnail(example_image_list[9]))
    col5t, col6t, col7t, col8t, col9t = st.beta_columns(5)
    with col5t:
        if st.button("Image-6"):
            suggest_idx = 5
    with col6t:
        if st.button("Image-7"):
            suggest_idx = 6
    with col7t:
        if st.button("Image-8"):
            suggest_idx = 7
    with col8t:
        if st.button("Image-9"):
            suggest_idx = 8
    with col9t:
        if st.button("Image-10"):
            suggest_idx = 9

    image_url = st.text_input(
        "OR provide an image URL",
        value="https://static.eos.com/wp-content/uploads/2019/04/Main.jpg")
    
    submit_button = st.button("Find Similar")
    
    if submit_button or suggest_idx > -1:
        image_name = None
        if suggest_idx > -1:
            image_name = example_image_list[suggest_idx]
            image = Image.fromarray(plt.imread(os.path.join(IMAGES_DIR, image_name)))
        else:
            image = download_and_prepare_image(image_url)
            st.image(image, caption="Input Image")
            st.markdown("---")

        if image is None:
            st.error("Image could not be downloaded, please try another one!")
        else:
            inputs = processor(images=image, return_tensors="jax", padding=True)
            query_vec = model.get_image_features(**inputs)
            query_vec = np.asarray(query_vec)
            ids, distances = index.knnQuery(query_vec, k=11)
            result_filenames = [filenames[id] for id in ids]
            rank = 0
            for result_filename, score in zip(result_filenames, distances):
                if image_name is not None and result_filename == image_name:
                    continue
                caption = "{:s} (score: {:.3f})".format(result_filename, 1.0 - score)
                col1, col2, col3 = st.beta_columns([2, 10, 10])
                col1.markdown("{:d}.".format(rank + 1))
                col2.image(Image.open(os.path.join(IMAGES_DIR, result_filename)),
                        caption=caption)
                caption_text = []
                for caption in image2caption[result_filename]:
                    caption_text.append("* {:s}\n".format(caption))
                col3.markdown("".join(caption_text))                       
                rank += 1
                st.markdown("---")
            suggest_idx = -1
