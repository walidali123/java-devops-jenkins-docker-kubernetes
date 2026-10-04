# DevOps Deployment & Infrastructure

## Overview

This case study documents the build and deployment configuration of [java-maven-app](https://github.com/walidali123/java-maven-app), reviewed across all seven remote branch tips on 4 October 2026. The primary example is `java-maven-app-complete-pipeline-ecr-eks`: a Jenkins pipeline combining Maven packaging, Docker image publication to Amazon ECR, and Kubernetes manifest application.

The application is a small Java/Spring Boot web application. This portfolio focuses on its DevOps configuration and does not claim application authorship. Diagrams represent checked-in commands and intended runtime relationships; they are not screenshots or proof of a live production deployment.

The repository also contains separate EC2, Terraform, Docker Compose, shared-library, and Ansible experiments. They are not merged into a fictional single architecture. See [EVIDENCE.md](EVIDENCE.md) for the complete branch audit, source links, prerequisites, and limitations; see [UPWORK.md](UPWORK.md) for portfolio copy.

## Architecture

![Java delivery architecture](01-devops-architecture.png)

The primary pipeline packages the Java application, builds its container image, authenticates to Amazon ECR, publishes a versioned tag, substitutes image/application values into Kubernetes templates, and applies those templates. The cluster pulls the referenced image using a named image-pull Secret supplied outside this repository.

The manifest defines one application replica and a Service on port 80 targeting container port 8080. No Service type is specified, so the definition is for an internal ClusterIP Service. No public ingress, load balancer, proxy, or HTTPS route is configured. The branch name mentions EKS, but neither EKS provisioning nor cluster identity is established by the checked-in files; this case study therefore describes a Kubernetes target rather than a verified EKS environment.

After the apply commands, the pipeline commits project changes and pushes to a GitLab `jenkins-jobs` branch. The GitHub repository supplied for review and the GitLab writeback destination are different source-control endpoints.

## CI/CD

![Jenkins pipeline](02-cicd-pipeline.png)

The primary Jenkinsfile contains five stages:

1. **Increment version:** invokes Maven version-update commands, reads the project version, and derives a Docker image tag from that version plus the Jenkins build number.
2. **Build app:** executes `mvn clean package`. The source includes one basic JUnit test of `Application.getStatus()`; testing is part of packaging, not a separate pipeline stage.
3. **Build image:** builds the Docker image, uses Jenkins-bound registry credentials for `docker login --password-stdin`, and pushes the tag to ECR.
4. **Deploy:** uses `envsubst` and `kubectl apply` for the Deployment and Service.
5. **Commit version update:** commits project files and pushes to the configured GitLab branch.

Jenkins setup, checkout/job configuration, webhook wiring, tool installation, registry provisioning, valid credentials, and cluster access are external prerequisites. The source commands are present; their successful execution was not verified during this audit. There is no rollout wait, post-deployment HTTP check, rollback procedure, or Jenkins test-report publication step.

## Infrastructure

![Infrastructure variants](03-infrastructure.png)

**Kubernetes variant:** the Deployment specifies one container using an ECR image, a named image-pull Secret, `imagePullPolicy: Always`, and container port 8080. Its Service selects the application's labels. The manifests include no probes, persistent volumes, resource requests/limits, Ingress, or cluster-provisioning resources.

**Independent EC2/Compose variant:** `feature-sshagent-terraform-jenkins-integeration` contains Terraform definitions for a VPC, subnet, internet gateway, default route table, default security group, and Amazon Linux EC2 instance. User data installs Docker and Docker Compose. A Compose file defines the Java container and a PostgreSQL container, publishing ports 8080 and 5432. No explicit Compose networks or volumes are declared; no application datasource connection to PostgreSQL is configured. The database is therefore shown as a separate service, without an invented application-to-database data-flow arrow.

The EC2 pipeline calls external shared-library functions and expects Terraform files under `terraform/`, while those files are stored at the branch root. It also reads Terraform output without `-raw`. Those integration details need validation before this branch can support an end-to-end execution claim. The commented S3 backend is not presented as active remote-state storage.

**Supplemental examples:** `master` includes an Ansible playbook for downloading Nexus, creating its runtime user, assigning ownership, starting it, and inspecting process/network output. It is not integrated into the primary pipeline, and no inventory is supplied. Shared-library branches reference external build/publish helpers; their implementations are outside the reviewed repository.

## Deployment Flow

![Deployment flow](04-deployment-flow.png)

A Jenkins job run begins the configured flow. Version update and Maven packaging precede Docker build/publication. The Deployment template references the resulting image tag, while the Service template defines internal routing. `kubectl apply` submits those resources to an externally configured cluster; Kubernetes is expected to reconcile the desired state.

The pipeline then performs Git writeback without waiting for rollout completion. This establishes a configured release sequence, not evidence that a container became healthy or that a public production application was available. There is no checked-in push trigger, so the diagrams do not claim that every GitHub push automatically initiates this flow.

## Security

![Credential and access configuration](05-security.png)

The primary Jenkinsfile references credentials for ECR authentication, AWS environment bindings, and Git authentication. Its Docker login uses `--password-stdin`. The Kubernetes Deployment references an image-pull Secret but does not define or create that Secret. The EC2 Terraform security group restricts SSH to configured CIDR inputs, allows public application access on TCP 8080, and allows outbound traffic.

These are configuration elements, not proof of a hardened production environment. The branch examples disable SSH host-key verification, interpolate credentials into shell commands/Git URLs, and include a literal database password in Compose. Values, account identifiers, hosts, IP addresses, credential IDs, and personal filesystem details are omitted from portfolio diagrams and text. No TLS, RBAC policy, NetworkPolicy, container security context, secrets rotation, or vulnerability-scanning workflow is implemented in the reviewed files.

## Technologies

**Primary case study:** Jenkins, Groovy, Apache Maven, Docker, Amazon ECR, Kubernetes, Git, Bash/shell, `envsubst`, Java 8, Spring Boot, and JUnit.

**Separate branch examples:** Terraform, AWS VPC/network resources, Amazon EC2, Amazon Linux, Docker Compose, Docker Hub, PostgreSQL, SSH/SCP, Ansible, Sonatype Nexus, and external Jenkins Shared Library integration.

Application startup logging uses SLF4J. A Logstash Logback encoder dependency exists, but no configured log-shipping destination, centralized logging stack, monitoring system, or dashboard is supplied. Nginx occurs only as the image in a separate Kubernetes deployment demo; it is not a configured reverse proxy for this application.

## DevOps Responsibilities

The repository demonstrates configuration work in these areas:

- Jenkins stages for packaging, container publication, deployment commands, and version writeback.
- Java JAR containerization and version-based Docker image tags.
- Kubernetes Deployment and internal Service templates with environment substitution.
- Credential bindings and a private-image pull Secret reference.
- Terraform network/EC2 definitions and startup automation in a separate branch.
- SSH/Compose deployment commands and supplemental Ansible Nexus setup.

This review does not establish who authored each part. Publish personal responsibility claims only for work actually performed by the portfolio owner; no application-development claim is included.

## Project Results

- A five-stage Jenkins configuration defines the primary build-to-deployment sequence.
- Container packaging and Kubernetes templates connect the application artifact to a declared runtime image and internal service route.
- Separate infrastructure definitions document an EC2/Compose alternative, with its integration limitations recorded.
- A committed Surefire report in the Terraform branch records one test with zero failures/errors. It is historical build output, not a fresh test result or deployment-health validation, and is not evidence for the ECR branch run.
- No live deployment, cloud-resource existence, public availability, production security, or performance metric was verified. Maven, Jenkins, Docker, Terraform, and cloud deployment were not executed in this review.

## Assets

All five visuals are available as 1920 × 1080 PNGs and editable SVGs. [UPWORK.md](UPWORK.md) contains the title, overview, responsibilities, features, results, and suggested skills. [EVIDENCE.md](EVIDENCE.md) contains the audit. [source/generate_visuals.py](source/generate_visuals.py) reproduces the diagrams using Python and Inkscape.
