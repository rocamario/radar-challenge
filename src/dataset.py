import os
from user_session import UserSession
import gdown
import zipfile
import streamlit as st

class Dataset:
    def __init__(self, directory='data'):
        self.directory = directory

        if not os.path.exists(directory):
            print("Downloading data from Google Drive...")
            self._download_data()

        self.session_ids = []
        self.sessions = {}

    def _download_data(self):
        file_id = st.secrets["drive"]["file_id"]
        url = f"https://drive.google.com/uc?id={file_id}"
        output = "data.zip"
        gdown.download(url, output, quiet=False)
        with zipfile.ZipFile(output, 'r') as zip_ref:
            zip_ref.extractall(self.directory)
