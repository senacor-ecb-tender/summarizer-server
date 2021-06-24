from typing import Optional
from azureml.core import Model
from azureml.core import Workspace


def retrieve_model(workspace: Workspace, model_name: str, model_version: Optional[int] = None):
    aml_model = Model(workspace=workspace, name=model_name, version=model_version)
    model_path = aml_model.download(target_dir=f"./{model_name}/{model_version}", exist_ok=True)
    return model_path


if __name__ == '__main__':
    ws = Workspace.from_config()

    model = retrieve_model(workspace=ws, model_name='led-large-16384-arxiv')

