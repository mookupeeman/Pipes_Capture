import streamlit as st
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import base64

def main():
    st.title("Mobile Camera Capture")

    # Full-screen camera input using HTML and JavaScript
    st.markdown(
        """
        <style>
        #videoElement {
            width: 100vw;
            height: 100vh;
            object-fit: cover;
        }
        </style>

        <video id="videoElement" autoplay></video>
        <button id="capture">Capture</button>

        <script>
        (function() {
            const videoElement = document.getElementById('videoElement');
            const captureButton = document.getElementById('capture');

            navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
                .then(stream => {
                    videoElement.srcObject = stream;
                });

            captureButton.addEventListener('click', () => {
                const canvas = document.createElement('canvas');
                canvas.width = videoElement.videoWidth;
                canvas.height = videoElement.videoHeight;
                const context = canvas.getContext('2d');
                context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

                const dataURL = canvas.toDataURL('image/jpeg');
                const img = document.createElement('img');
                img.src = dataURL;
                document.body.appendChild(img);

                window.streamlitPythonCallback(dataURL);
            });
        })();
        </script>
        """,
        unsafe_allow_html=True
    )

    # Listen to the captured image
    captured_image = st.experimental_js_listen("window.streamlitPythonCallback")

    if captured_image:
        # Decode the base64 image
        image = Image.open(BytesIO(base64.b64decode(captured_image.split(",")[1])))

        # Convert PIL Image to numpy array
        img_array = np.array(image)

        # Convert the image from RGB to BGR (OpenCV uses BGR)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # Get image dimensions
        height, width = img_array.shape[:2]

        rect_width = int(width * 0.8)
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
