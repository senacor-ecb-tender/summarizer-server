import json
from summarizer.model.model_loader import MODEL_LOADER_CONFIG_JSON
from os import path
import os
import uuid
from summarizer.model.model_loader import ModelManager


def test_that_read_config_from_file_works():
    expected_config = {'key_1': 'value_1', 'key2': 'value_2'}

    # TODO: this needs to go into some sort of before/after methods
    # prepare
    base_dir = str(uuid.uuid4())
    os.mkdir(base_dir)
    with open(path.join(base_dir, MODEL_LOADER_CONFIG_JSON), 'w') as f:
        json.dump(expected_config, f)

    result_cfg = ModelManager.read_config(base_dir)
    assert result_cfg == expected_config

    _tear_down(base_dir)


def test_that_read_config_yields_default_config():
    # prepare
    base_dir = str(uuid.uuid4())

    from summarizer.model.model_loader import default_model_version, default_model_name, default_resource_group, \
        default_subscription, default_ml_workspace
    result_cfg = ModelManager.read_config(base_dir)
    assert result_cfg['model_name'] == default_model_name
    assert result_cfg['subscription'] == default_subscription
    assert result_cfg['resource_group'] == default_resource_group
    assert result_cfg['workspace'] == default_ml_workspace
    assert result_cfg['model_version'] == default_model_version

    _tear_down(base_dir)


def _tear_down(base_dir):
    os.remove(path.join(base_dir, MODEL_LOADER_CONFIG_JSON))
    os.rmdir(base_dir)
