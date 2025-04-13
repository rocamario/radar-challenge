import glob
import os

from user_session import UserSession

class Dataset:
    def __init__(self, directory='data'):
        self.directory = directory

        self.session_ids = []
        self.sessions = {}

    def load(self):
        self.session_ids = [sid[:-5] for sid in os.listdir(self.directory)]
        for sid in self.session_ids:
            s = UserSession(user_id=sid, directory=self.directory)
            s.load()
            self.sessions[sid] = s
