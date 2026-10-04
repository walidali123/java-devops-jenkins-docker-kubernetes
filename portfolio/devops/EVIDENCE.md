# Repository Evidence & Branch Audit

Reviewed: 4 October 2026. Method: full Git clone, inventory of all seven remote branch tips, inspection of source files and configuration (including nested pipeline examples), and static cross-checks. Application and infrastructure files were not modified. External shared-library repositories, Jenkins installations, registries, and cloud resources were not inspected. No deployment, build, or infrastructure mutation was performed.

## Evidence levels

- **Defined:** a file or active command is present. This demonstrates configuration, not successful execution.
- **Referenced externally:** a credential, shared-library helper, cluster, registry, or host is expected outside this repository.
- **Historical artifact:** committed output can record a previous event but cannot validate the present configuration or a current deployment.
- **Absent / placeholder:** omitted from capability claims. README prose is not treated as stronger evidence than executable configuration.

All branch names and commit hashes below identify the exact tips reviewed. Historical versions reachable in Git are not treated as additional current implementations.

## Branch matrix

| Branch | Commit | Actual scope and material limits |
|---|---|---|
| `Jenkins-shared-lib` | `e6e4a37a00aaa50a7cfec06d0b6a805bf9b1c3bf` | External shared-library build/image publication calls; local deploy helper is a placeholder. No helper implementations in this repository. |
| `deploy-on-k8s` | `d4827bd2c28b536eb7fdd8a8a5825b9cc7ad24c3` | Build/image stages are echoes; active kubectl command creates nginx demo Deployment. Does not deploy the Java image. |
| `feature-sshagent-terraform-jenkins-integeration` | `0a1819f24b52d1df8bb11771600f4ba53618528d` | Terraform AWS network/EC2 definitions, Docker user data, shared-library calls, SSH/Compose and PostgreSQL. Root vs terraform/ path mismatch; external helpers and credentials required. |
| `java-maven-app-complete-pipeline-ecr-eks` | `f90bd2087e284c70b8f5be50627ab4bda713785e` | Primary five-stage version/package/image-publish/Kubernetes-apply/Git-writeback configuration. Existing cluster/registry required; no EKS provisioning or live run evidence. |
| `jenkins-jobs` | `5e3bbca3e83824f2b8921b38a76301c2549ee27d` | Root Maven + Docker Hub publication example; commented deployment. Nested ECR/Kubernetes, versioning, simple and syntax examples have differing helper/target assumptions. |
| `main` | `7be9aeb5da64f0d0d8fa07fe78b038cf9452a165` | SSH docker-run example; build calls commented; no Dockerfile. Local deploy helper is an echo. |
| `master` | `64e2a41aa509dd0ce3c4d6f9cb07dea9766bb03e` | Docker/Compose + SSH commands and independent Ansible Nexus playbook; external build helpers unresolved and image tags inconsistent. |

## Feature evidence

| Feature | Immutable source reference | Supported interpretation |
|---|---|---|
| Java web application | [java-maven-app-complete-pipeline-ecr-eks / src/main/java/com/example/Application.java](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/src/main/java/com/example/Application.java#L9) | Spring Boot entry point; startup logging and getStatus method. Static index.html is present. No datasource configuration or DB client dependency found. |
| Maven packaging + basic test | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L31) | Packaging command is active; pom.xml contains Spring Boot repackage and JUnit dependencies. AppTest checks a Java method, not an HTTP endpoint. No run performed. |
| Version update and build-number tag | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L13) | Maven version-update command, pom version parsing, and IMAGE_NAME assignment are active. Command/tool compatibility was not executed. |
| Java Docker image | [java-maven-app-complete-pipeline-ecr-eks / Dockerfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Dockerfile#L1) | Java 8 JRE Alpine base, port 8080, copied target JAR, java -jar command. No multi-stage build, HEALTHCHECK, or USER instruction. |
| ECR publication | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L42) | An ECR registry URL and docker build/login/push commands are present. Registry and credentials must already exist; no ECR provisioning included. |
| Kubernetes apply | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L56) | Environment substitution pipes templates to kubectl apply. AWS credential bindings do not establish cluster identity, kubeconfig, or EKS provisioning. |
| Deployment desired state | [java-maven-app-complete-pipeline-ecr-eks / kubernetes/deployment.yaml](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/kubernetes/deployment.yaml#L8) | One replica, image variables, labels, Always pull policy, port 8080, and pull-Secret name reference. No probes, resource limits, volumes, or securityContext. |
| Internal Service routing | [java-maven-app-complete-pipeline-ecr-eks / kubernetes/service.yaml](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/kubernetes/service.yaml#L11) | Port 80 targets 8080 using application labels. No type is specified (ClusterIP default). No external client path configured. |
| GitLab writeback | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L61) | Git add/commit and push to a GitLab jenkins-jobs branch are active; no claim that changes are pushed to the supplied GitHub branch. |
| Credential bindings | [java-maven-app-complete-pipeline-ecr-eks / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/f90bd2087e284c70b8f5be50627ab4bda713785e/Jenkinsfile#L39) | References Jenkins credentials; registry login uses password-stdin. No secret values copied. Git URL and shell interpolation remain limitations. |
| Terraform AWS resources | [feature-sshagent-terraform-jenkins-integeration / main.tf](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/main.tf#L14) | VPC, subnet, IGW, default route table, default SG, AMI data source, EC2 instance, user data, and public-IP output. S3 backend is commented, not active. |
| EC2 startup automation | [feature-sshagent-terraform-jenkins-integeration / entry-script.sh](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/entry-script.sh#L2) | Installs/starts Docker, adjusts Docker group membership, and downloads Docker Compose. Not verified on a live host. |
| SSH/SCP deployment configuration | [feature-sshagent-terraform-jenkins-integeration / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/Jenkinsfile#L56) | Copies a script and Compose file, then invokes the script through SSH agent credentials. Host-key verification is disabled; credentials passed as shell arguments. |
| Terraform invocation mismatch | [feature-sshagent-terraform-jenkins-integeration / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/Jenkinsfile#L45) | Pipeline expects terraform/ but main.tf, variables.tf, lock file, and entry script are at branch root. Output is read without -raw. External library helpers are absent. |
| Compose services and port mappings | [feature-sshagent-terraform-jenkins-integeration / docker-compose.yaml](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/docker-compose.yaml#L2) | Java image supplied by IMAGE and postgres:13 with published 8080/5432 ports. No explicit networks, volumes, probes, or application datasource wiring. |
| Remote Compose startup | [feature-sshagent-terraform-jenkins-integeration / server-cmds.sh](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/server-cmds.sh#L7) | Sets IMAGE, authenticates to Docker Hub, and starts Compose detached. Success echo does not prove service health. Database password value omitted. |
| SSH firewall configuration | [feature-sshagent-terraform-jenkins-integeration / main.tf](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/main.tf#L56) | SSH restricted to configured CIDRs; TCP 8080 is public; outbound traffic allowed. No IP/CIDR values reproduced. |
| Shared-library integration | [Jenkins-shared-lib / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/e6e4a37a00aaa50a7cfec06d0b6a805bf9b1c3bf/Jenkinsfile#L3) | External library reference and buildJar/buildImage/dockerLogin/dockerPush calls. Helper implementations are not present. Local deployApp only echoes. |
| Nginx Kubernetes demo | [deploy-on-k8s / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/d4827bd2c28b536eb7fdd8a8a5825b9cc7ad24c3/Jenkinsfile#L28) | Creates an nginx Deployment; build stages only echo. Not a reverse-proxy configuration or Java application deployment. |
| Main branch SSH example | [main / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/7be9aeb5da64f0d0d8fa07fe78b038cf9452a165/Jenkinsfile#L32) | Active remote docker run of a fixed existing image, with host 3080 mapped to container 80. Build helper calls are commented and no Dockerfile is present in this branch. |
| Supplemental Ansible Nexus playbook | [master / ansible-deploy-nexus.yaml](https://github.com/walidali123/java-maven-app/blob/64e2a41aa509dd0ce3c4d6f9cb07dea9766bb03e/ansible-deploy-nexus.yaml#L22) | Installs prerequisites, downloads/unpacks Nexus, creates a user, assigns ownership, starts Nexus and checks processes/ports. Inventory and pipeline invocation are absent. |
| Master Compose integration limits | [master / Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/64e2a41aa509dd0ce3c4d6f9cb07dea9766bb03e/Jenkinsfile#L23) | Build helpers are called while shared-library import is commented; remote Compose image uses a different fixed tag. Do not claim complete functioning automation. |
| Jenkins training variants | [jenkins-jobs / Jenkinsfile-kubernetes/Jenkinsfile](https://github.com/walidali123/java-maven-app/blob/5e3bbca3e83824f2b8921b38a76301c2549ee27d/Jenkinsfile-kubernetes/Jenkinsfile#L55) | Nested ECR/Kubernetes example plus version-increment, simple-pipeline, and syntax examples. Root build/push active, deploy commented. Syntax example calls missing buildApp/testApp helpers; simple example loads a root script.groovy that is absent. |
| Historical unit-test output | [feature-sshagent-terraform-jenkins-integeration / target/surefire-reports/AppTest.txt](https://github.com/walidali123/java-maven-app/blob/0a1819f24b52d1df8bb11771600f4ba53618528d/target/surefire-reports/AppTest.txt#L4) | Committed output records one test and no failures/errors. It was not regenerated here, and does not validate a live deployment or the primary branch. |

## Requested categories that are absent or limited

| Category | Finding across inspected branches |
|---|---|
| GitHub Actions | No `.github/workflows` configuration. Pipelines are Jenkins/Groovy. |
| Automatic source-push trigger | README suggests manual run or webhook setup; no webhook/job configuration checked in. |
| Nginx / reverse proxy | Only an nginx-image Kubernetes demo command. No Nginx configuration, app proxy, or ingress controller definition. |
| HTTPS / SSL | No certificates, TLS configuration, certificate automation, or HTTPS exposure. |
| Database | PostgreSQL containers appear in Compose variants. No Java-to-PostgreSQL configuration or persistence volumes. |
| Health checks | No Docker HEALTHCHECK, Compose healthcheck, Kubernetes readiness/liveness/startup probes, or rollout wait. getStatus is an ordinary Java method, not a mapped endpoint. |
| Logging | Startup `log.info` and Logstash Logback encoder dependency. No logback configuration, destination, log aggregation, or retention policy. |
| Monitoring | No metrics collector, exporter, dashboard, alerting, or monitoring manifests. README mention of watching Jenkins output is not monitoring implementation. |
| Networking | Kubernetes Service selectors/ports; Compose published ports with implicit default network; Terraform VPC/subnet/IGW/routes/SG. No explicit Compose isolation or NetworkPolicy. |
| Storage | No named volumes, PVCs, persistent volume definitions, database backups, or active remote-state backend. EC2 default root disk is not a custom persistence design. |
| Cloud | EC2/network resources explicitly defined; ECR registry explicitly referenced. EKS is only suggested by a branch name; no cluster resource or verified cluster context. |
| Production outcomes | No successful live release, public access, availability metric, throughput metric, zero-downtime outcome, or production-hardening proof. |
| Personal role | Git configuration and files do not independently establish which work the portfolio owner performed. No first-person authorship claim or application-development credit asserted. |

## Static validation and execution limits

The two Kubernetes YAML files in the primary branch parse as Deployment and Service definitions. Their labels/selectors agree; Service targetPort and containerPort are both 8080; the pipeline assigns the image/application variables consumed by these manifests. Five stage definitions are present in the primary Jenkinsfile.

This does not validate Groovy execution, Jenkins plugins/tools, ECR authentication freshness, Maven plugin resolution/compiler compatibility, external shared-library behavior, Terraform provider execution, kubeconfig, IAM permissions, image-pull Secret contents, or container startup. Maven, Docker, Jenkins, Terraform, and cloud deployment were not executed. A new run is required before claiming end-to-end success.

The checked-in examples use legacy runtime/tool versions. The case study presents them as repository evidence, not as a current production recommendation. No changes were made to remediate them under this documentation-only request.

## Full file inventory by branch

Paths are listed for reproducibility; no secret contents, account numbers, IP values, credential values/IDs, or private host names are copied. Build artifacts in the Terraform branch are inventoried as artifacts, not implementation evidence.

### `Jenkins-shared-lib`

```text
.gitignore
Dockerfile
Jenkinsfile
README.md
pom.xml
script.groovy
src/main/java/com/example/Application.java
```

### `deploy-on-k8s`

```text
.gitignore
Jenkinsfile
README.md
pom.xml
script.groovy
src/main/java/com/example/Application.java
src/main/resources/static/index.html
```

### `feature-sshagent-terraform-jenkins-integeration`

```text
.gitignore
.terraform.lock.hcl
Dockerfile
Jenkinsfile
README.md
docker-compose.yaml
entry-script.sh
main.tf
pom.xml
server-cmds.sh
src/main/java/com/example/Application.java
src/test/java/AppTest.java
target/java-maven-app-1.0-SNAPSHOT.jar
target/maven-archiver/pom.properties
target/maven-status/maven-compiler-plugin/compile/default-compile/createdFiles.lst
target/maven-status/maven-compiler-plugin/compile/default-compile/inputFiles.lst
target/maven-status/maven-compiler-plugin/testCompile/default-testCompile/createdFiles.lst
target/maven-status/maven-compiler-plugin/testCompile/default-testCompile/inputFiles.lst
target/surefire-reports/AppTest.txt
target/surefire-reports/TEST-AppTest.xml
target/test-classes/AppTest.class
variables.tf
```

### `java-maven-app-complete-pipeline-ecr-eks`

```text
.gitignore
Dockerfile
Jenkinsfile
README.md
kubernetes/deployment.yaml
kubernetes/service.yaml
pom.xml
src/main/java/com/example/Application.java
src/main/resources/static/index.html
src/test/java/AppTest.java
```

### `jenkins-jobs`

```text
.gitignore
Dockerfile
Jenkinsfile
Jenkinsfile-kubernetes/.gitkeep
Jenkinsfile-kubernetes/Jenkinsfile
Jenkinsfile-simple-pipeline/.gitkeep
Jenkinsfile-simple-pipeline/Jenkinsfile
Jenkinsfile-simple-pipeline/script.groovy
Jenkinsfile-syntax/.gitkeep
Jenkinsfile-syntax/Jenkinsfile
Jenkinsfile-syntax/script.groovy
Jenkinsfile-version-increment/.gitkeep
Jenkinsfile-version-increment/Jenkinsfile
Jenkinsfile-version-increment/README.md
README.md
docker-compose.yaml
freestyle-build.sh
kubernetes/deployment.yaml
kubernetes/service.yaml
pom.xml
src/main/java/com/example/Application.java
src/test/java/AppTest.java
```

### `main`

```text
.gitignore
Jenkinsfile
pom.xml
script.groovy
src/main/java/com/example/Application.java
src/main/resources/static/index.html
```

### `master`

```text
.gitignore
Dockerfile
Jenkinsfile
ansible-deploy-nexus.yaml
docker-compose.yaml
pom.xml
server-cmds.sh
src/main/java/com/example/Application.java
src/main/resources/static/index.html
src/test/java/AppTest.java
tmpfile.txt
```
