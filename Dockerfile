FROM continuumio/miniconda3:4.9.2-alpine

WORKDIR /

COPY environment.yml .
COPY summarizer .
COPY templates /templates
RUN ls

RUN conda env create -f environment.yml

RUN echo "conda activate ecb" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

ARG NAME=n/a
ARG CREATED=n/a
ARG SOURCE=n/a
ARG REVISION=n/a

ENV REVISION=${REVISION}

LABEL org.opencontainers.image.name="${NAME}"
LABEL org.opencontainers.image.created="${CREATED}"
LABEL org.opencontainers.image.source="${SOURCE}"
LABEL org.opencontainers.image.revision="${REVISION}"

EXPOSE 8000
ENTRYPOINT ["/opt/conda/envs/ecb/bin/uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]