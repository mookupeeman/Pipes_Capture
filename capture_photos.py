import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Google Drive API settings
# SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SERVICE_ACCOUNT_FILE = 'capture-image-pipes-88a9648d1cc4.json'  # Path to your service account key file

# def authenticate_google_drive():
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     service = build('drive', 'v3', credentials=credentials)
#     return service

# def upload_to_drive(service, file_name, file_data, folder_id):
#     file_metadata = {
#         'name': file_name,
#         'parents': [folder_id]
#     }
#     media = MediaIoBaseUpload(file_data, mimetype='image/jpeg')
#     file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#     return file.get('id')

def main():
    st.title("Mobile Camera Capture")

    # Custom CSS for fullscreen camera input
    st.markdown(
        """
        <style>
        .css-1r7b0x2 {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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

        # Convert image to JPEG and prepare it for upload
        buffered = BytesIO()
        Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)).save(buffered, format="JPEG")
        buffered.seek(0)

        # # Authenticate and upload to Google Drive
        # service = authenticate_google_drive()
        # folder_id = '1CcmHTorJysPzSj1ghEPjO2oOnRrK_BuI'  # Replace with your Google Drive folder ID
        # file_name = f'captured_image_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
        # file_id = upload_to_drive(service, file_name, buffered, folder_id)

        # st.success(f"Image uploaded to Google Drive with file ID: {file_id}")

        # Create a download button for the original image
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/jpg;base64,{img_str}" download="captured_image.jpg">Download Captured Image</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
