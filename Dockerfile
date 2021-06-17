FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
COPY summarizer .

RUN conda env create -f environment.yml

RUN echo "conda activate ecb" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

CMD ["/opt/conda/envs/ecb/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]