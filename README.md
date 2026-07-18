# Azure Container Instances (ACI) & Azure Container Registry (ACR) Project

## Learning Objectives

After completing this module, you will be able to:

* Understand Azure Container Instances (ACI)
* Understand Azure Container Registry (ACR)
* Build Docker images using a Dockerfile
* Push container images to Azure Container Registry
* Deploy containers directly into Azure Container Instances
* Access applications using a Public IP Address

---

# Theory

## What is Azure Container Instances (ACI)?

Azure Container Instances (ACI) is a **Platform as a Service (PaaS)** offering that allows you to run Docker containers without managing virtual machines or Kubernetes clusters.

### Features

* No VM management
* Fast deployment (seconds)
* Public or Private IP
* Linux and Windows containers
* Pay only while the container is running

---

## What is Azure Container Registry (ACR)?

Azure Container Registry is Microsoft's private Docker Registry.

It stores container images securely inside Azure.

### Similar To

| Public Registry     | Private Registry         |
| ------------------- | ------------------------ |
| Docker Hub          | Azure Container Registry |
| Public Images       | Private Images           |
| Internet Accessible | Secure Azure Access      |

---

# Container Architecture

```text
Application Source Code
        │
        ▼
 Dockerfile
        │
        ▼
Docker Build
        │
        ▼
Docker Image
        │
        ▼
Docker Run
        │
        ▼
Docker Container
        │
        ▼
Port Binding
        │
        ▼
Browser
```

Example

```text
nginx Image
      │
docker run
      │
Container
      │
Port Mapping
80:80
      │
Browser
```

Command

```bash
docker run -d -p 80:80 nginx:latest
```

---

# Docker Components

## Docker Image

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
