from typing import Optional
from os import path
import os
import logging
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration
from azureml.core import Model
from azureml.core import Workspace

my_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
logger = logging.getLogger(__name__)

default_model_name = 'led-large-16384-arxiv'
default_subscription = '091ac194-317f-4880-9f66-a9c23f42cb60'
default_resource_group = 'dev'
default_ml_workspace = 'ecb-dev'
default_model_version = None


def download_model_from_workspace(workspace: Workspace, model_name: str, target_dir: str, model_version: Optional[int] = None):
    aml_model = Model(workspace=workspace, name=model_name, version=model_version)
    model_path = aml_model.download(target_dir=target_dir, exist_ok=True)
    return model_path


def model_cache_empty(cache_folder: str) -> bool:
    return not path.exists(cache_folder)


def read_config() -> dict:
    return {
        "model_name": os.environ.get('MODEL_NAME') if os.environ.get('MODEL_NAME') else default_model_name,
        "subscription": os.environ.get('SUBSCRIPTION') if os.environ.get('SUBSCRIPTION') else default_subscription,
        "resource_group": os.environ.get('RESOURCE_GROUP') if os.environ.get('RESOURCE_GROUP') else default_resource_group,
        "workspace": os.environ.get('ML_WORKSPACE') if os.environ.get('ML_WORKSPACE') else default_ml_workspace,
        'model_version': os.environ.get('MODEL_VERSION') if os.environ.get('MODEL_VERSION') else default_model_version
    }


def fetch_model():
    download_path = path.join('.', 'cache')
    cfg = read_config()
    model_version = cfg.get('model_version')
    target_dir = path.join(download_path, cfg['model_name'], model_version if model_version is not None else 'None')

    downloaded_model_path = path.join(target_dir, cfg.get('model_name'))
    if model_cache_empty(downloaded_model_path):
        ws = Workspace.get(subscription_id=cfg.get('subscription'),
                           resource_group=cfg.get('resource_group'),
                           name=cfg.get('workspace'))
        logger.info(f' Loading model from ml registry: ${ws.name}')
        download_model_from_workspace(workspace=ws, model_name=cfg.get('model_name'), target_dir=target_dir)
        logger.info(f' Loaded model from ml registry and stored it: ${downloaded_model_path}')
    else:
        logger.info('Loading model from local cache')

    model = LEDForConditionalGeneration.from_pretrained(downloaded_model_path)
    model.to(my_device)
    tokenizer = LEDTokenizer.from_pretrained(downloaded_model_path)
    return model, tokenizer




