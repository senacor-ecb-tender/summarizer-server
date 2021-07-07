# ECB Tender PoC: summarizer-server

This service creates summaries of given texts from European Central Bank. The API is implemented in Python using FastAPI. 
The Frontend is implemented in Vue.js and built with Yarn/Quasar.  

# Folder structure
The repository has the following folder structure: 

| Directory    | Content                                                                          |
|--------------|----------------------------------------------------------------------------------|
| .github      | contains Github actions workflow definitions                                     |
| scripts      | contains a run scripts to render K8s deployment descriptors with env variables   |
| frontend     | contains VueJS frontend code                                                     |
| backend      | contains API code implemented in Python                                          |
| deployment   | contains Kubernetes deployment descriptors using place holders for env variables |
| notebooks    | contains the Jupyter notebook for training the machine-learning model            |

The root folder contains the conda environment definition in the following file: 

``environment.yml``

The root folder also contains the docker file and a docker-compose file to build & start the docker container. See 
below for instructions to run summarizer-server on a local machine. 

# Deployment on AKS

The frontend is currently deployed as a Azure static web app with the following URL:

``https://mango-stone-032a68f03.azurestaticapps.net/``

The backend is deployed as a combination of service & deployment on a Kubernetes cluster on 
Azure Kubernetes Service (AKS). The deployment is fully automated and integrated via Github Actions

# Installation on a local machine

We require a linux server, e.g. RedHat Enterprise Linux(RHEL 8) with a working internet connection and docker as well 
as docker-compose installed. For instructions to install docker ce as well as docker-compose on a RHEL server read 
[here](https://computingforgeeks.com/install-docker-and-docker-compose-on-rhel-8-centos-8/). 

The `docker-compose.yml` file in this repo builds the frontend as well as the backend into one docker image. During the 
build process a conda environment is created. The conda environment is specified by the above mentioned `environment.yml`. 
In case a direct internet access is not possible, a private conda channel and PyPi repository need to be specified, which 
hold the packages specified in the environment. 

Furthermore, the ml model needs to be provided in form of a directory `cache` (can have an arbitrary name but must be 
mounted into the docker container under `/cache`). We provide the fine tuned model as deployed in the PoC installation on 
the DVD. Copy this cache directory somewhere accessible on a local disk and replace the string `CACHEDIR` in the docker-compose 
file with the absolute path of the cache directory. 

Alternatively, the PoC service will attempt to pull the specified model from the Azure ML Workspace using the credentials 
of a service principal(SP). The credentials to this SP are specified in the docker-compose file using the variables 
`TENANT_ID`, `CLIENT_ID` and `CLIENT_SECRET` (see the PoC word documentation for credential values). In order for the api 
service to load a model from the Azure ML Workspace a working internet connection to MS Azure is required.

To build and run the service locally execute the following commands in the root directory of this repo:

```$docker-compose up```

## Hardware & Software Requirements

We require a standard server machine equipped with 
- a CPU of either Intel Intel Core™ i7-6700 or better or AMD Ryzen processor family
- 32 GB of Ram
- 50 GB of free hard disk space. 

We require a RHEL installation, a non-root user with docker and docker-compose installed. The non-root user needs to 
be in the docker group. 

## Detailed Installation Instructions

1. Install RHEL on the server. 
2. Add a user to the system. 
3. Install docker-ce and docker-compose following these [instructions](https://computingforgeeks.com/install-docker-and-docker-compose-on-rhel-8-centos-8/)
4. Create a directory Workspace in the users home dir: ``/home/USER/Workspace``.
5. Create a directory cache/ in the Workspace dir: ``/home/USER/Workspace/cache``.
6. Create a directory led-ecb-lm-arxiv-sum/ in the Workspace dir: ``/home/USER/Workspace/cache/led-ecb-lm-arxiv-sum``.
7. Create a directory 10/ in the led-ecb-lm-arxiv-sum dir: ``/home/USER/Workspace/cache/led-ecb-lm-arxiv-sum/10``.
8. Create a directory led-ecb-lm-arxiv-sum/ in the led-ecb-lm-arxiv-sum/10/ dir: ``/home/USER/Workspace/cache/led-ecb-lm-arxiv-sum/10/led-ecb-lm-arxiv-sum``.
9. Copy the model artefacts into ``/home/USER/Workspace/cache/led-ecb-lm-arxiv-sum/10/led-ecb-lm-arxiv-sum/``.
10. Copy the directory summarizer-server/ from the DVD into the Workspace dir: ``/home/USER/Workspace/summarizer-server``.
11. Open a bash console and change into the directory ``/home/USER/Workspace/summarizer-server``.
12. Edit the file docker-compose.yml and replace the string CACHEDIR with ``/home/USER/Workspace/cache/``.
13. Build the docker image with the command ``docker-compose build``. (This takes a few minutes)
14. Start the docker image using the command ``docker-compose up``. 
15. Open a browser and access the IP and port 8000 of the RHEL machine (or localhost on that machine): ``http://localhost:8000/``.
