import streamlit as st
import cv2
import tempfile
import os
import zipfile
from io import BytesIO

st.set_page_config(page_title="Last 10 Frames Extractor", layout="wide")

st.title("🎬 Last 10 Frames Extractor")
st.write("Upload a video file to extract and download its last 10 frames.")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with st.spinner("Processing video..."):
        # Save uploaded video to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") 
        tfile.write(uploaded_file.read())
        tfile.close()
        
        # Open the video with OpenCV
        cap = cv2.VideoCapture(tfile.name)
        
        if not cap.isOpened():
            st.error("Error opening video file. Please try a different format.")
        else:
            # Get total number of frames
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            st.info(f"Total frames in video: **{total_frames}**")
            
            if total_frames < 10:
                st.warning("Video has less than 10 frames. Extracting all available frames.")
                start_frame = 0
                frames_to_extract = total_frames
            else:
                start_frame = total_frames - 10
                frames_to_extract = 10
                
            # Set the video position to the starting frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
            
            frames = []
            for i in range(frames_to_extract):
                ret, frame = cap.read()
                if ret:
                    # Convert BGR to RGB for Streamlit display
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frames.append((start_frame + i, frame_rgb))
                else:
                    break
                    
            cap.release()
            
            if len(frames) > 0:
                st.success(f"Successfully extracted {len(frames)} frames!")
                
                # Display the frames in a grid (2 rows of 5)
                cols = st.columns(5)
                
                for idx, (frame_num, frame_data) in enumerate(frames):
                    col = cols[idx % 5]
                    with col:
                        st.image(frame_data, caption=f"Frame {frame_num}", width="stretch")
                        
                        frame_bgr = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)
                        success, buffer = cv2.imencode(".jpg", frame_bgr)
                        if success:
                            st.download_button(
                                label="⬇️ Download",
                                data=buffer.tobytes(),
                                file_name=f"frame_{frame_num}.jpg",
                                mime="image/jpeg",
                                width="stretch",
                                key=f"dl_btn_{frame_num}"
                            )

                # Prepare zip file for download
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for frame_num, frame_data in frames:
                        # Convert back to BGR for saving with cv2.imencode
                        frame_bgr = cv2.cvtColor(frame_data, cv2.COLOR_RGB2BGR)
                        success, buffer = cv2.imencode(".jpg", frame_bgr)
                        if success:
                            zip_file.writestr(f"frame_{frame_num}.jpg", buffer.tobytes())
                            
                st.write("---")
                # Provide download button for the zip file
                st.download_button(
                    label="⬇️ Download Frames as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="last_10_frames.zip",
                    mime="application/zip",
                    width="stretch"
                )
            else:
                st.error("Failed to extract frames.")
            
        # Clean up temporary file
        try:
            os.unlink(tfile.name)
        except Exception as e:
            pass
