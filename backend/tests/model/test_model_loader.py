from model.model_loader import ModelManager
from model.model_loader import ModelSettings
import pathlib


def test_that_read_config_yields_default_config():
    default_settings = ModelSettings().dict()

    result_cfg = ModelManager.read_config().dict()
    for k, v in result_cfg.items():
        assert default_settings[k] == v


def test_that_loading_from_azureml_registry_is_correctly_configured(mocker):
    m = ModelManager.instance()

    auth = mocker.patch.object(m, "build_service_principal")
    workspace = mocker.patch("summarizer.model.model_loader.Workspace", spec=True)
    model = mocker.patch("summarizer.model.model_loader.Model")
    model.configure_mock(**{"name.return_value": "my_model"})

    target_dir = pathlib.Path(__file__).parent / "some_cache"
    cfg = ModelSettings()

    m._fetch_from_azureml_registry(target_dir, cfg)

    auth.assert_called_once()
    workspace.get.assert_called_once()
    model.assert_called_once()
