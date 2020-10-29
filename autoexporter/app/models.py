import os
import shutil
import werkzeug
import logging
from flask_login import UserMixin
import app.config

import time
import random # TODO TEMP

projects = []

class User(UserMixin):
    def __init__(self):
        # TEMP generate here the login pwd hash
        self.pwdhash = werkzeug.security.generate_password_hash('password42')
        self.id = 42
        
    def check_password(self, pwd):
        return werkzeug.security.check_password_hash(self.pwdhash, pwd)
        
class Project():
    def __init__(self, id, status):
        self.id = werkzeug.utils.secure_filename(id)
        self.name = self.id
        self.status = None
        self.setStatus(status)
        
    @staticmethod
    def get(id):
        for p in projects:
            if p.getId() == id:
                return p
        return None
        
    def getId(self):
        return self.id
        
    def getName(self):
        return self.name
        
    def getStatus(self):
        return self.status
        
    def getProgress(self):
        return random.random()
        
    def getDir(self, status = None):
        if status == None:
            status = self.status
        return os.path.join(app.config.dirConfig[status], self.id)
        
    def setStatus(self, status):
        if self.status != None and self.status != status:
            oldPath = self.getDir()
            newPath = self.getDir(status)
            if not os.path.isdir(oldPath):
                raise Exception('Project id ' + self.id + ' not found')
            if os.path.isdir(newPath):
                raise Exception('Project id ' + self.id + ' conflict')
            shutil.move(oldPath, newPath)
            logging.info('Project id ' + self.id + ' status change: ' + str(self.status) + ' -> ' + str(status))
        self.status = status
        if self.status == app.config.STATUS_QUEUED:
            # TODO extract .mlt filename now
            self.name = 'TODO: Extract name'
        
    def delete(self):
        shutil.rmtree(self.getDir())
        projects.remove(self)
        logging.info('Project id ' + self.id + ' deleted')
        
    def run(self):
        logging.info('Project id ' + self.id + ' running...')
        self.setStatus(app.config.STATUS_WORKING)
        time.sleep(30)
        self.setStatus(app.config.STATUS_SUCCESS)
