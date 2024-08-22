import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2
import numpy as np
from datetime import datetime
import base64

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.rect_width = 200
        self.rect_height = 200
        self.last_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Store the last frame
        self.last_frame = img.copy()

        # Draw centered rectangle on the frame
        frame_height, frame_width = img.shape[:2]
        top_left = (frame_width // 2 - self.rect_width // 2, frame_height // 2 - self.rect_height // 2)
        bottom_right = (frame_width // 2 + self.rect_width // 2, frame_height // 2 + self.rect_height // 2)
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

        return img

def main():
    st.title("Mobile Camera Capture")

    webrtc_ctx = webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )

    if st.button("Capture Photo"):
        if webrtc_ctx.video_transformer:
            if webrtc_ctx.video_transformer.last_frame is not None:
                img = webrtc_ctx.video_transformer.last_frame

                # Convert the image to JPEG
                _, buffer = cv2.imencode('.jpg', img)

                # Convert to base64 for download
                b64_image = base64.b64encode(buffer).decode('utf-8')

                # Create download link
                href = f'<a href="data:image/jpeg;base64,{b64_image}" download="captured_image.jpg">Click here to download the captured image</a>'
                st.markdown(href, unsafe_allow_html=True)

                # Display the captured image
                st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Captured Photo")
            else:
                st.error("No frame available. Please make sure your camera is working and visible in the stream.")

if __name__ == "__main__":
    main()
