import cv2
import numpy as np
import os
import streamlit as st
from datetime import datetime
from config_loader import load_config
config = load_config('config.yml')


def read_and_save_input_image(uploaded_file):
    global config
    image_dir = config['image_dir']
    curr_time = datetime.now()
    try:
        if uploaded_file is not None:
            # convert image from np array to bytes
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)

            # Decode the byte array into an OpenCV image
            image = cv2.imdecode(file_bytes, 1)
            curr_time = datetime.now()
            
            # save image using current time 
            save_folder = image_dir + "/" + curr_time.strftime('%Y-%m-%d')
            os.makedirs(save_folder,exist_ok=True)
            image_path = save_folder + "/" + curr_time.strftime("%Y-%m-%d_%H%M%S")+".jpg"
            # save image
            cv2.imwrite(image_path,image)
                
            # Display the image
            st.image(image, caption="Uploaded Image.", use_column_width=True)

            # Optionally, you can add any further processing or saving of the image
            st.write("Image uploaded successfully!")
            return image_path

        else:
            st.write("Please upload an image.")
            return None
    except:
        return None