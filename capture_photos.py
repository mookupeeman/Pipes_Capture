import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

def main():
    st.title("Mobile Camera Capture")

    # Use Streamlit's camera input
    img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # Read the image file buffer with PIL
        image = Image.open(img_file_buffer)

        # Convert PIL Image to numpy array
        img_array = np.array(image)

        # Convert the image from RGB to BGR (OpenCV uses BGR)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Get image dimensions
        height, width = img_array.shape[:2]

        # Define rectangle dimensions
        rect_width = int(width*0.8)
        rect_height = int(height * 0.8)

        # Calculate rectangle coordinates
        top_left = (width // 2 - rect_width // 2, height // 2 - rect_height // 2)
        bottom_right = (width // 2 + rect_width // 2, height // 2 + rect_height // 2)

        # Draw rectangle on the image
        cv2.rectangle(img_array, top_left, bottom_right, (0, 255, 0), 2)

        # Convert back to RGB for displaying
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

        # Display the image with the rectangle
        st.image(img_rgb, caption="Captured Photo with Rectangle", use_column_width=True)

        # Create a download button for the original image
        buffered = BytesIO()
        Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)).save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/jpg;base64,{img_str}" download="captured_image.jpg">Download Captured Image</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
