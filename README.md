# Flask App on Azure

A lightweight Flask application with a modern landing page, ready to be containerized and deployed to Azure Container Registry (ACR) and Azure Container Instances (ACI).

## Tech Stack

- Python 3.12
- Flask 3.0.3
- Docker
- Azure Container Registry (ACR)
- Azure Container Instances (ACI)
- Azure DevOps Pipelines
- HTML5 + CSS3

## Project Structure

```text
FlaskApp-ACR-ACI/
├── app.py
├── requirements.txt
├── Dockerfile
├── templates/
│   └── index.html
├── README.md
└── azure-pipelines.yml
```

## End-to-End Deployment Walkthrough

### 1. Start Docker Desktop

Start Docker Desktop and wait until it reports that the Docker Engine is running. Open a terminal or PowerShell window and check the tools:

```powershell
docker --version
docker buildx version
az version
```

### 2. Create the Azure Container Registry

In the Azure portal, open **Container registries** and select **Create**. Create the registry with the name `atulkamble` in your subscription and resource group. Its login server should be:

```text
atulkamble.azurecr.io
```

If you specifically need registry username/password authentication, open the registry's **Settings > Access keys** and enable **Admin user**. Admin credentials are secrets: do not paste them into source files, README files, pipeline YAML, or chat. Prefer Microsoft Entra authentication (`az acr login`) or a managed identity/service connection where supported, and disable the admin user when it is no longer needed.

Sign in and authenticate Docker to ACR:

```powershell
az login
az acr login --name atulkamble
```

### 3. Get the Application Source

For a new checkout:

```powershell
git clone https://github.com/atulkamble/FlaskApp-ACR-ACI.git
cd FlaskApp-ACR-ACI
code .
```

For an existing checkout, update it instead:

```powershell
cd FlaskApp-ACR-ACI
git pull
code .
```

### 4. Run the Flask App Locally

Create and activate a virtual environment, install the dependencies, and start the app:

```powershell
python -m venv .venv
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then, on either platform:

```powershell
pip install -r requirements.txt
python app.py
```

Open the landing page at [http://localhost:5000](http://localhost:5000). The health endpoint is [http://localhost:5000/health](http://localhost:5000/health).

### 5. Build and Push a Multi-Platform Image

Build for AMD64 and ARM64 and push directly to ACR:

```powershell
docker buildx build --platform linux/amd64,linux/arm64 -t atulkamble.azurecr.io/cloudnautic/flaskapp:latest --push .
```

Pull and inspect the pushed image:

```powershell
docker pull atulkamble.azurecr.io/cloudnautic/flaskapp:latest
docker images
```

Run it locally:

```powershell
docker run -d --name flaskapp -p 5000:5000 atulkamble.azurecr.io/cloudnautic/flaskapp:latest
docker container ls
```

Open [http://localhost:5000](http://localhost:5000). To view the container output, use the container name or ID returned by `docker run`:

```powershell
docker logs flaskapp
```

Stop, list, and restart the container as needed:

```powershell
docker container stop flaskapp
docker container ls
docker ps -a
docker container start flaskapp
```

### 6. Deploy the Image to Azure Container Instances

In the Azure portal:

1. Open **Container instances** and select **Create**.
2. Choose the subscription, resource group, and container name.
3. For **Image source**, select **Azure Container Registry**, then select `atulkamble`, the `cloudnautic/flaskapp` image, and the `latest` tag.
4. Configure the container to use Linux and add a TCP port mapping for port `5000`. Enable a public IP if the app should be reachable from the internet.
5. Review and create the container instance, then wait for deployment to complete.
6. Open the instance's **Overview** page and use its assigned IP address with port `5000`. The address shared for this deployment is [http://130.107.46.213:5000](http://130.107.46.213:5000).

The public IP can change when an instance is recreated. If that link stops working, use the current IP shown in the Azure portal.

> **Image name note:** The manual commands above publish `cloudnautic/flaskapp`. The Azure DevOps pipeline below currently publishes `cloudnautic/pythonapp`; update its `imageName` variable if the pipeline should publish the same `flaskapp` image.

## Prerequisites

- Docker Desktop running
- Azure CLI installed and authenticated
- Access to an Azure subscription
- Git installed

```bash
docker --version
docker buildx version
az --version
python --version
```

## Local Development

```bash
git clone https://github.com/atulkamble/FlaskApp-ACR-ACI.git
cd FlaskApp-ACR-ACI
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:5000
```

## Application Endpoints

- `/` - Modern landing page
- `/health` - Health check endpoint returning JSON status

## Docker Build

### Single Platform (AMD64)

```bash
docker buildx build \
  --platform linux/amd64 \
  -t atulkamble.azurecr.io/cloudnautic/flaskapp:latest \
  --load .
```

### Multi-Platform (AMD64 + ARM64)

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t atulkamble.azurecr.io/cloudnautic/flaskapp:latest \
  --push .
```

## Azure Login and ACR Setup

```bash
az login
az acr login --name atulkamble
```

Registry:

```text
atulkamble.azurecr.io
```

## Verify Image in Azure Container Registry

```bash
az acr repository list --name atulkamble --output table
az acr repository show-tags \
  --name atulkamble \
  --repository cloudnautic/flaskapp \
  --output table
```

## Run Docker Image Locally

```bash
docker pull atulkamble.azurecr.io/cloudnautic/flaskapp:latest
docker run -d \
  --name flaskapp \
  -p 5000:5000 \
  atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

Check:

```bash
docker ps
curl http://localhost:5000
```

## Azure DevOps Pipeline

Azure DevOps can be configured to build and push the container image to ACR on every push to the main branch.

```yaml
trigger:
  - main

pool:
  vmImage: "ubuntu-latest"

variables:
  imageName: "cloudnautic/pythonapp"
  serviceConnection: "acr-connection"

steps:
  - task: Docker@2
    displayName: "Build and Push Docker Image to ACR"
    inputs:
      containerRegistry: "$(serviceConnection)"
      repository: "$(imageName)"
      command: "buildAndPush"
      Dockerfile: "**/Dockerfile"
      tags: |
        $(Build.BuildId)
        latest
```

### Service Connection Setup

In Azure DevOps:

- Project Settings
- Service Connections
- New Service Connection
- Docker Registry
- Azure Container Registry

Use a Docker Registry service connection, not an Azure Resource Manager (ARM) connection, for `Docker@2`.

## Azure Container Instances (ACI)

This project is designed to work with Azure Container Instances for quick deployment of the containerized app.

Typical flow:

```text
Source code
  ↓
Dockerfile
  ↓
Docker build
  ↓
ACR push
  ↓
ACI deploy
  ↓
Public endpoint
```

## Notes

- Do not hardcode credentials into pipeline YAML files.
- Use Azure DevOps service connections for secure authentication.
- Keep Docker Desktop running while developing locally.

## License

This project is provided as a learning and deployment template for Azure container workloads.

Read-only template containing:

* Application
* Runtime
* Libraries
* Dependencies

Example

```bash
nginx:latest
python:3.12
ubuntu:24.04
```

---

## Docker Container

A running instance of an image.

Example

```bash
docker run nginx
```

---

## Docker Engine

The software responsible for:

* Building images
* Running containers
* Managing images
* Managing networks
* Managing volumes

---

# Dockerfile Overview

A Dockerfile contains instructions used to build a Docker image.

Example

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]
```

---

## Important Dockerfile Instructions

| Instruction | Purpose               |
| ----------- | --------------------- |
| FROM        | Base Image            |
| WORKDIR     | Working directory     |
| COPY        | Copy files            |
| RUN         | Install dependencies  |
| EXPOSE      | Application Port      |
| CMD         | Default command       |
| ENTRYPOINT  | Fixed startup command |

---

# Practical 1 – Deploy Hello World using Azure Container Instances

## Step 1

Open Azure Portal

```
Search
```

```
Container Instances
```

---

## Step 2

Click

```
Create
```

---

## Step 3

Configure

Image

```
Hello World
```

---

## Step 4

Networking

```
Protocol

TCP

Port

80
```

---

## Step 5

Keep remaining settings as Default

```
Next
Next
Review + Create
Create
```

---

## Step 6

Deployment completes

Copy

```
Public IP Address
```

Example

```
http://4.188.98.244/
```

Open it in the browser.

---

# Practical 2 – Azure Container Registry (ACR)

## Step 1 – Login to Azure

```bash
az login
```

Select the required Azure Subscription.

---

## Step 2 – Login to Azure Container Registry

Example Registry

```
atulkamble
```

Command

```bash
az acr login --name atulkamble
```

---

## Step 3 – Enable Admin User

Azure Portal

```
Azure Container Registry
        │
Settings
        │
Access Keys
        │
Enable
Admin User
```

Use the generated:

* Username
* Password

---

## Step 4 – Login using Docker

```bash
docker login atulkamble.azurecr.io
```

Enter

```
Username

Password
```

---

## Step 5 – Clone Sample Project

```bash
git clone https://github.com/atulkamble/FlaskApp-ACR-ACI.git
```

Move into project

```bash
cd FlaskApp-ACR-ACI
```

Open VS Code

```bash
code .
```

---

# Build Docker Image

```bash
docker buildx build \
--platform linux/amd64,linux/arm64 \
-t atulkamble.azurecr.io/cloudnautic/flaskapp:latest \
--load .
```

Verify

```bash
docker images
```

---

# Run Container Locally

```bash
docker run -d -p 5000:5000 \
atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

Verify

```bash
docker container ls
```

Open

```
http://localhost:5000
```

---

# Push Image to Azure Container Registry

```bash
docker push atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

---

# Pull Image from Azure Container Registry

```bash
docker pull atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

---

# Run Pulled Image

```bash
docker run -d -p 5000:5000 \
atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

Open

```
http://localhost:5000
```

---

# Practical 3 – Deploy Custom Image to Azure Container Instances

## Step 1

Azure Portal

```
Search

Container Instances
```

---

## Step 2

Create

---

## Step 3

Select Image Source

```
Azure Container Registry
```

Image

```
atulkamble.azurecr.io/cloudnautic/flaskapp:latest
```

---

## Step 4

Networking

```
TCP

5000
```

---

## Step 5

Keep Defaults

```
Next

Next

Review + Create

Create
```

---

## Step 6

After Deployment

Copy

```
Public IP Address
```

Example

```
http://135.235.236.121:5000/
```

Open in Browser.

---

# Required Ubuntu Packages (Optional)

```bash
sudo apt update

sudo apt install git docker.io -y

sudo systemctl start docker

sudo systemctl enable docker

sudo usermod -aG docker $USER

newgrp docker

sudo apt install docker-buildx -y
```

---

# Complete Workflow

```text
Python Application
        │
        ▼
Dockerfile
        │
        ▼
docker build
        │
        ▼
Docker Image
        │
        ▼
Local Testing
        │
        ▼
docker push
        │
        ▼
Azure Container Registry (ACR)
        │
        ▼
Azure Container Instance (ACI)
        │
        ▼
Public IP
        │
        ▼
Browser
```

---

# Architecture Diagram

```text
                Developer Machine
+----------------------------------------------+
|                                              |
|   Source Code                                |
|        │                                     |
|        ▼                                     |
|   Dockerfile                                 |
|        │                                     |
|        ▼                                     |
| docker build                                 |
|        │                                     |
|        ▼                                     |
| Docker Image                                 |
|        │                                     |
| docker push                                  |
+--------│-------------------------------------+
         │
         ▼
+-------------------------------+
| Azure Container Registry      |
| (Private Docker Repository)   |
+-------------------------------+
         │
         │ Pull Image
         ▼
+-------------------------------+
| Azure Container Instance      |
| Linux Container               |
| Port 5000                     |
+-------------------------------+
         │
         ▼
     Public IP Address
         │
         ▼
      Web Browser
```

---

# Important Commands

```bash
az login

az acr login --name <registry-name>

docker login <registry-name>.azurecr.io

docker images

docker container ls

docker buildx build --platform linux/amd64,linux/arm64 -t <image> --load .

docker push <image>

docker pull <image>

docker run -d -p 5000:5000 <image>
```

---

# Interview Questions

1. What is Azure Container Instances (ACI)?
2. Is ACI PaaS or IaaS?
3. What is Azure Container Registry (ACR)?
4. Difference between Docker Hub and ACR?
5. Why do we use Docker Buildx?
6. What is the purpose of `EXPOSE` in a Dockerfile?
7. Difference between `CMD` and `ENTRYPOINT`?
8. Can ACI pull images directly from ACR?
9. Why enable the Admin User in ACR?
10. What are the advantages of ACI over Virtual Machines?

---

# Key Points to Remember

* **ACI is a PaaS service** for running containers without managing VMs.
* **ACR is Azure's private Docker image registry.**
* Always **test the image locally** before pushing it to ACR.
* Use **`docker push`** to upload images and **`docker pull`** to download them.
* Expose the correct application port (e.g., **5000** for Flask, **80** for Nginx).
* Use **Buildx** to build **multi-platform images** (`linux/amd64`, `linux/arm64`).
* ACI can deploy images directly from **Azure Container Registry** with minimal configuration.
* ACI is ideal for **development, testing, batch jobs, APIs, and short-lived workloads**.
