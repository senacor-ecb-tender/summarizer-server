FROM continuumio/miniconda3:4.9.2-alpine

WORKDIR /

COPY ../environment.yml .
RUN conda env create -f environment.yml

RUN echo "conda activate ecb" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

CMD ["ls", "-lisah"]