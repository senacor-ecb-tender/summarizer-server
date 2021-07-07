FROM node:12-alpine as builder

WORKDIR /frontend

COPY frontend/ .
RUN cp local_docker_compose_quasar.conf.js quasar.conf.js
RUN yarn global add @quasar/cli
RUN yarn install --prefer-offline
RUN yarn run build

FROM continuumio/miniconda3:4.9.2-alpine

WORKDIR /

COPY environment.yml .
COPY backend/summarizer /summarizer
COPY --from=builder /frontend/dist/spa /templates
COPY backend/templates /templates

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
CMD ["summarizer.main:app", "--host", "0.0.0.0", "--port", "8000"]