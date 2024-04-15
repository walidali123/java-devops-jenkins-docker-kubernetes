# Jenkins Pipeline with Terraform AWS Provisioning and Docker Deployment

This repository contains a Jenkins Pipeline script written in Groovy for building a Java application, creating a Docker image, provisioning an EC2 server using Terraform, and deploying the Docker image to the provisioned server.

## Prerequisites
- Jenkins installed and configured.
- Jenkins shared library plugin installed.
- Jenkins credentials set up for GitLab access (`walid-gitlab-credentials`), AWS access (`jenkins_aws_access_key_id` and `jenkins_aws_secret_access_key`), and Docker Hub access (`walid-docker-hub-repo`).
- Maven tool configured in Jenkins.
- AWS CLI installed and configured on the Jenkins server.
- Terraform installed on the Jenkins server.
- Docker installed on the Jenkins server.

## Usage
1. Configure the Jenkins pipeline job with this repository.
2. Ensure necessary credentials are configured in Jenkins.
3. Make sure Maven is installed and configured in Jenkins.
4. Make sure AWS CLI and Terraform are installed and configured on the Jenkins server.
5. Ensure Docker is installed on the Jenkins server.
6. Run the pipeline job in Jenkins.

## Pipeline Overview
1. **Build App Stage**: This stage builds the Java application JAR file.
2. **Build Image Stage**: This stage builds a Docker image using the JAR file and pushes it to Docker Hub.
3. **Provision Server Stage**: This stage provisions an EC2 server on AWS using Terraform.
4. **Deploy Stage**: This stage waits for the EC2 server to initialize, then deploys the Docker image to the provisioned server.

## Jenkins Shared Library
The pipeline script uses a shared library named `jenkins-shared-library` available at `https://gitlab.com/Walidfadel/jenkins-shared-library.git`.

## Terraform Configuration
The repository contains Terraform configurations for provisioning AWS infrastructure including VPC, Subnet, Internet Gateway, Route Table, Security Group, and EC2 instance.

## Directory Structure
- `terraform/`: Contains Terraform configuration files.
- `entry-script.sh`: Shell script to be executed on EC2 server startup.

## Notes
- Replace placeholders like `walidali123/my-repo:jma-3.0` with appropriate values.
- Modify Terraform configurations in `terraform/` directory according to your requirements.

