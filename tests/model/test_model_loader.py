from summarizer.model.model_loader import ModelManager


def test_that_read_config_yields_default_config():
    from summarizer.model.model_loader import ModelSettings

    default_settings = ModelSettings().dict()

    result_cfg = ModelManager.read_config()
    for k, v in result_cfg.items():
        assert default_settings[k] == v

