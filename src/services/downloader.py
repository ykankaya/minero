from __future__ import print_function
import requests
import zipfile
import tarfile
import warnings
from threading import Thread
from sys import stdout
from os import makedirs
import os
from os.path import dirname
from os.path import exists


class Downloader:
    CHUNK_SIZE = 32768

    def __init__(self, *args, **kwargs):
        self.status = None
        self.content_size = None
        self.current_percentage = None
        self.error = None
        self.is_progress = False
        self.thread = None
        self.path = kwargs['path'] if 'path' in kwargs else None
        self.url = kwargs['url'] if 'url' in kwargs else None
        self.overwrite = kwargs['overwrite'] if 'overwrite' in kwargs else None

    def download(self):
        self.thread = Thread(target = self.download_in_background)
        self.thread.start()

    def is_downloaded(self):
        return os.path.exists(self.path)

    def stop(self):
        self.status = "Stopping"

    def wait(self):
        self.thread.join()

    def download_in_background(self):
        if self.is_progress:
            return;

        try:
            self.is_progress = True
            self.status = "Downloading"
            self.content_size = None
            self.current_percentage = None

            self.ensure_path()

            if not exists(self.path) or self.overwrite:
                session = requests.Session()
                response = session.get(self.url, params={}, stream=True, verify=False)
                self.save_response_content(response)
        
            if self.status == "Stopped" or self.status == "Error":
                self.is_progress = False
                return;
        
            self.on_downloaded()
        
            if self.status == "Stopped" or self.status == "Error":
                self.is_progress = False
                return;

            self.is_progress = False
            self.status = "Completed"

        except Exception as e:
            self.is_progress = False
            self.status = 'Error'
            self.error = 'Error: ' + str(e)
            return

    def ensure_path(self):
       destination_directory = dirname(self.path)
       if not exists(destination_directory):
          makedirs(destination_directory)

    def save_response_content(self, response):
        self.content_size = int(response.headers['content-length'])
        self.current_size = 0
        with open(self.path, 'wb') as f:
            for chunk in response.iter_content(Downloader.CHUNK_SIZE):
                if self.status == 'Stopping':
                    self.status = "Stopped"
                    return
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    self.current_size += Downloader.CHUNK_SIZE
                    self.current_percentage = int((self.current_size / self.content_size) * 100)
                    print(self.current_percentage)
        self.status = "Downloaded"

    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    def sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return '{:.1f} {}{}'.format(num, unit, suffix)
            num /= 1024.0
        return '{:.1f} {}{}'.format(num, 'Yi', suffix)

    def on_downloaded(self):
        pass