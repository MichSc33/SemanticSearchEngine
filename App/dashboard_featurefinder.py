import jax
import flax
import matplotlib.pyplot as plt
import nmslib
import numpy as np
import os
import requests
import streamlit as st

from tempfile import NamedTemporaryFile
from torchvision.transforms import Compose, Resize, ToPILImage
from transformers import CLIPProcessor, FlaxCLIPModel
from PIL import Image

import utils

BASELINE_MODEL = "openai/clip-vit-base-patch32"
MODEL_PATH = "flax-community/clip-rsicd-v2"

IMAGE_VECTOR_FILE = "./App/vectors/test-bs128x8-lr5e-6-adam-ckpt-1.tsv"

IMAGES_DIR = "./App/images"
DEMO_IMAGES_DIR = "./App/demo-images"


def split_image(X):
  num_rows = X.shape[0] // 224
  num_cols = X.shape[1] // 224
  Xc = X[0 : num_rows * 224, 0 : num_cols * 224, :]
  patches = []
  for j in range(num_rows):
    for i in range(num_cols):
      patches.append(Xc[j * 224 : (j + 1) * 224, 
                        i * 224 : (i + 1) * 224,
                        :])
  return num_rows, num_cols, patches


def get_patch_probabilities(patches, searched_feature, 
                            image_preprocesor,
                            model, processor):
  images = [image_preprocesor(patch) for patch in patches]
  text = "An aerial image of {:s}".format(searched_feature)
  inputs = processor(images=images,
                    text=text,
                    return_tensors="jax",
                    padding=True)
  outputs = model(**inputs)
  probs = jax.nn.softmax(outputs.logits_per_text, axis=-1)
  probs_np = np.asarray(probs)[0]
  return probs_np


def get_image_ranks(probs):
  temp = np.argsort(-probs)
  ranks = np.empty_like(temp)
  ranks[temp] = np.arange(len(probs))
  return ranks


def download_and_prepare_image(image_url):
    """
        Take input image and resize it to 672x896 
    """
    try:
        image_raw = requests.get(image_url, stream=True,).raw
        image = Image.open(image_raw).convert("RGB")
        width, height = image.size
        # print("WID,HGT:", width, height)
        if width < 224 or height < 224:
            return None
        # take the short edge and reduce to 672
        if width < height:
            resize_factor = 672 / width
            image = image.resize((672, int(height * resize_factor)))
            image = image.crop((0, 0, 672, 896))
        else:
            resize_factor = 672 / height
            image = image.resize((int(width * resize_factor), 896))
            image = image.crop((0, 0, 896, 672))
        return np.asarray(image)
    except Exception as e:
        # print(e)
        return None



def app():
    model, processor = utils.load_model(MODEL_PATH, BASELINE_MODEL)

    st.title("Find Features in Images")
    st.markdown("""
        This demo shows the ability of the model to find specific features
        (specified as text queries) in the image. As an example, say you wish to
        find the parts of the following image that contain a `beach`, `houses`, 
        or `ships`. We partition the image into tiles of (224, 224) and report
        how likely each of them are to contain each text features.
    """)
    st.image("./App/demo-images/st_tropez_1.png")
    st.image("./App/demo-images/st_tropez_2.png")
    st.markdown("""
        For this image and the queries listed above, our model reports that the
        two left tiles are most likely to contain a `beach`, the two top right 
        tiles are most likely to contain `houses`, and the two bottom right tiles
        are likely to contain `boats`.

        We have provided a few representative images from [Unsplash](https://unsplash.com/s/photos/aerial-view) 
        that you can experiment with. Use the image name to put in an initial feature
        to look for, this will show the original image, and you will get more ideas
        for features that you can ask the model to identify.
    """)
    image_file = st.selectbox(
        "Sample Image File",
        options=[
            "-- select one --",
            "St-Tropez-Port.jpg",
            "Acopulco-Bay.jpg",
            "Highway-through-Forest.jpg",
            "Forest-with-River.jpg",
            "Eagle-Bay-Coastline.jpg",
            "Multistoreyed-Buildings.jpg",
            "Street-View-Malayasia.jpg",
        ])
    image_url = st.text_input(
        "OR provide an image URL",
        value="https://static.eos.com/wp-content/uploads/2019/04/Main.jpg")
    searched_feature = st.text_input("Feature to find", value="beach")

    if st.button("Find"):
        if image_file.startswith("--"):
            image = download_and_prepare_image(image_url)
        else:
            image = plt.imread(os.path.join("./App/demo-images", image_file))

        if image is None:
            st.error("Image could not be downloaded, please try another one")
        else:
            st.image(image, caption="Input Image")
            st.markdown("---")
            num_rows, num_cols, patches = split_image(image)
            image_preprocessor = Compose([
                ToPILImage(),
                Resize(224)
            ])
            num_rows, num_cols, patches = split_image(image)
            patch_probs = get_patch_probabilities(
                patches,
                searched_feature,
                image_preprocessor,
                model,
                processor)
            patch_ranks = get_image_ranks(patch_probs)
            pid = 0
            for i in range(num_rows):
                cols = st.beta_columns(num_cols)
                for col in cols:
                    caption = "#{:d} p({:s})={:.3f}".format(
                        patch_ranks[pid] + 1, searched_feature, patch_probs[pid])
                    col.image(patches[pid], caption=caption)
                    pid += 1
