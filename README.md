# 🎬 Last 10 Frames Extractor

A simple Streamlit web application that allows users to upload a video file and easily extract and download its last 10 frames as individual images or as a bundled ZIP file.

## ☁️ Run in the Cloud

The easiest way to use the app is to run it directly in your browser without having to install anything!

👉 **[Access the App Here](https://last10frames.streamlit.app/)**

---

## 💻 Run Locally

If you prefer to run the application on your own machine, follow these steps:

### Prerequisites

Make sure you have Python installed. You will also need the following Python packages:
- `streamlit`
- `opencv-python`

### Installation

1. Clone or download this project to your computer.
2. Open your terminal or command prompt and navigate to the project folder.
3. Install the required dependencies by running:
   ```bash
   pip install streamlit opencv-python
   ```

### Running the Application

#### Using the Batch File (Windows only)
You can simply double-click the `run_app.bat` file. This will automatically open a command prompt and launch the local Streamlit server.

#### Using the Terminal (All Platforms)
Run the following command in your terminal:
```bash
python -m streamlit run app.py
```

The application will automatically open in your default web browser (usually at `http://localhost:8501`).
