from typing import Optional
from azureml.core import Model
from azureml.core import Workspace


def retrieve_model(workspace: Workspace, model_name: str, model_version: Optional[int] = None):
    aml_model = Model(workspace=workspace, name=model_name, version=model_version)
    model_path = aml_model.download(target_dir=f"./{model_name}/{model_version}", exist_ok=True)
    return model_path


if __name__ == '__main__':
    ws = Workspace.get(subscription_id='091ac194-317f-4880-9f66-a9c23f42cb60', resource_group='dev', name='ecb-dev')
    model_path = retrieve_model(workspace=ws, model_name='led-large-16384-arxiv')
    print(model_path)

