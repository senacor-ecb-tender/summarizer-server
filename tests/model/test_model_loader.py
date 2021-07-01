from summarizer.model.model_loader import ModelManager


def test_that_read_config_yields_default_config():
    from summarizer.model.model_loader import default_model_version, default_model_name, default_resource_group, \
        default_subscription, default_ml_workspace
    result_cfg = ModelManager.read_config()
    assert result_cfg['model_name'] == default_model_name
    assert result_cfg['subscription'] == default_subscription
    assert result_cfg['resource_group'] == default_resource_group
    assert result_cfg['workspace'] == default_ml_workspace
    assert result_cfg['model_version'] == default_model_version
