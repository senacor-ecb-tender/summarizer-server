FROM ezbpitch.azurecr.io/base-images/ecb-conda-base-image:0.0.1

WORKDIR /

COPY environment.yml .
COPY summarizer .
COPY templates /templates
COPY cache /cache


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