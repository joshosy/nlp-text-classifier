import logging
import yaml
import sys
import os
import glob
import pandas as pd

def load_config(config:dict=None) -> dict:
    with open(os.path.join(sys.path[0], 'default_config.yml')) as f:
        default_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    
    if config is None:
        return default_config
    else:
        return collect_default_config(config, default_config)

def collect_default_config(config:dict, default_config:dict) -> dict:
    '''
    Starting with a default config as base, updates with new arguments from a config file
    '''
    for k in default_config:
        if k in config:
            if isinstance(config[k], dict) and isinstance(default_config[k], dict):
                collect_default_config(config[k], default_config[k])
        else:
            config[k] = default_config[k]
    return config

def set_basic_logging(filename:str) -> None:
    logging.basicConfig(filename=filename, filemode='w', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s [%(filename)s:%(lineno)d] %(message)s')
    return


def combine_csv(file_dir, output_fname:str):
    csv_filenames = [f for f in glob.glob(f'{file_dir}/*.csv')]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f, header=None, names=['text','url']) for f in csv_filenames])
    combined_csv.to_csv(output_fname, index=False, encoding='utf-8')
    return