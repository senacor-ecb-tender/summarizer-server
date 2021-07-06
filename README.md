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
