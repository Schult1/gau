import pandas as pd
import numpy as np
import os

def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
