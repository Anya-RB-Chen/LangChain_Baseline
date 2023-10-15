import os
import sys
import json

CONFIG_FILE = "config.json"

class Config:
    """
        This class is for loading the configuration file.
    """
    def __init__(self):
        self.config = self.load_config(CONFIG_FILE)
        self.openai_config = self.config["openai_api"]
        self.ringley_config = self.config["ringley_api"]

    def load_config(self, CONFIG_FILE):
        """
            INPUT: None
            OUTPUT: config: dict
        """
        with open(CONFIG_FILE) as f:
            self.config = json.loads(f.read())
        return self.config

    def get_config(self):
        """
            INPUT: None
            OUTPUT: config: dict
        """
        return self.config
    
    def show_config(self):
        """
            INPUT: None
            OUTPUT: None
        """
        print(self.config)

    def change_data_dir(self, dir):
        """
            INPUT: dir: str
            OUTPUT: None
        """
        self.config["data_dir"] = dir
        self.save_config(CONFIG_FILE, self.config)

    def save_config(self, CONFIG_FILE, config):
        """
            INPUT: CONFIG_FILE: str, config: dict
            OUTPUT: None
        """
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def get_openai_key(self):
        """
            INPUT: None
            OUTPUT: OPENAI_API_KEY: str
        """
        return self.openai_config["OPENAI_API_KEY"]
    
    def get_ringley_key_value(self):
        """
            INPUT: None
            OUTPUT: RINGLEY_API_KEY: str
        """
        return self.ringley_config["key"], self.ringley_config["value"]
    
    def get_db_dir(self):
        """
            INPUT: None
            OUTPUT: path: str
        """
        return self.config["db_dir"]
    
    def get_data_dir(self):
        """
            INPUT: None
            OUTPUT: path: str
        """
        return self.config["data_dir"]
    
    def get_update_data_dir(self):
        """
            INPUT: None
            OUTPUT: path: str
        """
        return self.config["update_data_dir"]
    
    def get_vector_dir(self):
        """
            INPUT: None
            OUTPUT: path: str
        """
        return self.config["vector_dir"]
    
    def get_model_name(self):
        """
            INPUT: None
            OUTPUT: model_name: str
        """
        return self.config["model"]
    
    def connect_OPENAI(self):
        """
            INPUT: key: str
            OUTPUT: None
        """
        os.environ["OPENAI_API_KEY"] = self.get_openai_key()

