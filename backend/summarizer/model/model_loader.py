import logging
import os
import pathlib

import torch
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.model import Model
from pydantic import BaseSettings
from transformers import LEDTokenizer, LEDForConditionalGeneration

from ..utils.tracing import traced

MODEL_LOADER_CONFIG_JSON = 'model_loader_config.json'
CACHE = 'cache'

my_device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
logger = logging.getLogger(__name__)


class ModelSettings(BaseSettings):
    model_name: str = 'led-large-16384-arxiv'
    subscription: str = '091ac194-317f-4880-9f66-a9c23f42cb60'
    resource_group: str = 'dev'
    ml_workspace: str = 'ecb-dev'
    model_version: str = 'None'


class ModelManager:
    _instance = None

    model: LEDForConditionalGeneration = None
    tokenizer: LEDTokenizer = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            logger.info('Creating new instance')
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance

    @staticmethod
    @traced
    def read_config() -> ModelSettings:
        """
        This functions assembles a config dictionary of values required to connect to an Azure ML Workspace. The fct
        attempts to read the config from environment values first, and finally falls back to hard
        coded default values.

        :return: a dictionary holding the values for ML model name, Azure subscription, Azure resource group, ML Workspace
        and model version.
        """
        return ModelSettings()

    # this can be improved
    # https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate
    @staticmethod
    def build_service_principal() -> ServicePrincipalAuthentication:
        return ServicePrincipalAuthentication(
            tenant_id=os.environ.get('TENANT_ID'),
            service_principal_id=os.environ.get('CLIENT_ID'),
            service_principal_password=os.environ.get('CLIENT_SECRET')
        )

    @traced
    def fetch_model(self, cfg: dict = None):
        """ Load the configured model either from cache directory or from ml model registry

        :param cfg: ModelSettings containing the name and version of the model.
        """
        download_path = pathlib.Path(CACHE)

        if cfg is None:
            cfg = self.read_config()

        version = cfg.model_version if cfg.model_version is not None else 'None'

        target_dir = download_path / cfg.model_name / version
        downloaded_model_path = target_dir / cfg.model_name

        if not downloaded_model_path.exists() or cfg.model_version is None:
            logger.info('Loading model from Azure ML registry')
            self._fetch_from_azureml_registry(target_dir, cfg)
        else:
            logger.info('Loading model from local cache')

        self.model = LEDForConditionalGeneration.from_pretrained(downloaded_model_path)
        self.model.to(my_device)
        self.tokenizer = LEDTokenizer.from_pretrained(downloaded_model_path)

    @traced
    def _fetch_from_azureml_registry(self, target_dir: pathlib.Path, cfg):
        auth = self.build_service_principal()

        ws = Workspace.get(subscription_id=cfg.subscription,
                           resource_group=cfg.resource_group,
                           name=cfg.ml_workspace,
                           auth=auth
                           )

        aml_model = Model(workspace=ws, name=cfg.model_name, version=cfg.model_version)
        model_path = aml_model.download(target_dir=str(target_dir), exist_ok=True)

        logger.info(f'Loaded model {aml_model.name} to {model_path}')


model_mgr = ModelManager.instance()
