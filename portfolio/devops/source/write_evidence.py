from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True)
branches=[b.removeprefix('origin/') for b in git('for-each-ref','--format=%(refname:short)','refs/remotes/origin').splitlines() if b!='origin']
shas={b:git('rev-parse','origin/'+b).strip() for b in branches}
primary='java-maven-app-complete-pipeline-ecr-eks'
feature='feature-sshagent-terraform-jenkins-integeration'
def link(b,f,start=1,end=None):
    frag=f'#L{start}'+(f'-L{end}' if end else '')
    return f'[{b} / {f}](https://github.com/walidali123/java-maven-app/blob/{shas[b]}/{f}{frag})'
def locate(b,f,needle):
    lines=git('show',f'origin/{b}:{f}').splitlines()
    n=next(i+1 for i,line in enumerate(lines) if needle in line)
    return link(b,f,n)

rows=[
('Java web application',primary,'src/main/java/com/example/Application.java','@SpringBootApplication','Spring Boot entry point; startup logging and getStatus method. Static index.html is present. No datasource configuration or DB client dependency found.'),
('Maven packaging + basic test',primary,'Jenkinsfile',"mvn clean package",'Packaging command is active; pom.xml contains Spring Boot repackage and JUnit dependencies. AppTest checks a Java method, not an HTTP endpoint. No run performed.'),
('Version update and build-number tag',primary,'Jenkinsfile',"stage('increment version')",'Maven version-update command, pom version parsing, and IMAGE_NAME assignment are active. Command/tool compatibility was not executed.'),
('Java Docker image',primary,'Dockerfile','FROM','Java 8 JRE Alpine base, port 8080, copied target JAR, java -jar command. No multi-stage build, HEALTHCHECK, or USER instruction.'),
('ECR publication',primary,'Jenkinsfile','docker push','An ECR registry URL and docker build/login/push commands are present. Registry and credentials must already exist; no ECR provisioning included.'),
('Kubernetes apply',primary,'Jenkinsfile','envsubst < kubernetes/deployment.yaml','Environment substitution pipes templates to kubectl apply. AWS credential bindings do not establish cluster identity, kubeconfig, or EKS provisioning.'),
('Deployment desired state',primary,'kubernetes/deployment.yaml','replicas:','One replica, image variables, labels, Always pull policy, port 8080, and pull-Secret name reference. No probes, resource limits, volumes, or securityContext.'),
('Internal Service routing',primary,'kubernetes/service.yaml','targetPort:','Port 80 targets 8080 using application labels. No type is specified (ClusterIP default). No external client path configured.'),
('GitLab writeback',primary,'Jenkinsfile',"stage('commit version update')",'Git add/commit and push to a GitLab jenkins-jobs branch are active; no claim that changes are pushed to the supplied GitHub branch.'),
('Credential bindings',primary,'Jenkinsfile','withCredentials','References Jenkins credentials; registry login uses password-stdin. No secret values copied. Git URL and shell interpolation remain limitations.'),
('Terraform AWS resources',feature,'main.tf','resource "aws_vpc"','VPC, subnet, IGW, default route table, default SG, AMI data source, EC2 instance, user data, and public-IP output. S3 backend is commented, not active.'),
('EC2 startup automation',feature,'entry-script.sh','sudo yum','Installs/starts Docker, adjusts Docker group membership, and downloads Docker Compose. Not verified on a live host.'),
('SSH/SCP deployment configuration',feature,'Jenkinsfile',"stage('deploy')",'Copies a script and Compose file, then invokes the script through SSH agent credentials. Host-key verification is disabled; credentials passed as shell arguments.'),
('Terraform invocation mismatch',feature,'Jenkinsfile',"dir('terraform')",'Pipeline expects terraform/ but main.tf, variables.tf, lock file, and entry script are at branch root. Output is read without -raw. External library helpers are absent.'),
('Compose services and port mappings',feature,'docker-compose.yaml','services:','Java image supplied by IMAGE and postgres:13 with published 8080/5432 ports. No explicit networks, volumes, probes, or application datasource wiring.'),
('Remote Compose startup',feature,'server-cmds.sh','docker-compose','Sets IMAGE, authenticates to Docker Hub, and starts Compose detached. Success echo does not prove service health. Database password value omitted.'),
('SSH firewall configuration',feature,'main.tf','cidr_blocks = [var.my_ip, var.jenkins_ip]','SSH restricted to configured CIDRs; TCP 8080 is public; outbound traffic allowed. No IP/CIDR values reproduced.'),
('Shared-library integration','Jenkins-shared-lib','Jenkinsfile','library identifier:','External library reference and buildJar/buildImage/dockerLogin/dockerPush calls. Helper implementations are not present. Local deployApp only echoes.'),
('Nginx Kubernetes demo','deploy-on-k8s','Jenkinsfile','kubectl create deployment','Creates an nginx Deployment; build stages only echo. Not a reverse-proxy configuration or Java application deployment.'),
('Main branch SSH example','main','Jenkinsfile','docker run','Active remote docker run of a fixed existing image, with host 3080 mapped to container 80. Build helper calls are commented and no Dockerfile is present in this branch.'),
('Supplemental Ansible Nexus playbook','master','ansible-deploy-nexus.yaml','Download and unpack nexus installer','Installs prerequisites, downloads/unpacks Nexus, creates a user, assigns ownership, starts Nexus and checks processes/ports. Inventory and pipeline invocation are absent.'),
('Master Compose integration limits','master','Jenkinsfile','buildJar()','Build helpers are called while shared-library import is commented; remote Compose image uses a different fixed tag. Do not claim complete functioning automation.'),
('Jenkins training variants','jenkins-jobs','Jenkinsfile-kubernetes/Jenkinsfile','envsubst','Nested ECR/Kubernetes example plus version-increment, simple-pipeline, and syntax examples. Root build/push active, deploy commented. Syntax example calls missing buildApp/testApp helpers; simple example loads a root script.groovy that is absent.'),
('Historical unit-test output',feature,'target/surefire-reports/AppTest.txt','Tests run:','Committed output records one test and no failures/errors. It was not regenerated here, and does not validate a live deployment or the primary branch.'),
]

text='''# Repository Evidence & Branch Audit

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
'''
summaries={
'main':'SSH docker-run example; build calls commented; no Dockerfile. Local deploy helper is an echo.',
'master':'Docker/Compose + SSH commands and independent Ansible Nexus playbook; external build helpers unresolved and image tags inconsistent.',
'Jenkins-shared-lib':'External shared-library build/image publication calls; local deploy helper is a placeholder. No helper implementations in this repository.',
'deploy-on-k8s':'Build/image stages are echoes; active kubectl command creates nginx demo Deployment. Does not deploy the Java image.',
feature:'Terraform AWS network/EC2 definitions, Docker user data, shared-library calls, SSH/Compose and PostgreSQL. Root vs terraform/ path mismatch; external helpers and credentials required.',
primary:'Primary five-stage version/package/image-publish/Kubernetes-apply/Git-writeback configuration. Existing cluster/registry required; no EKS provisioning or live run evidence.',
'jenkins-jobs':'Root Maven + Docker Hub publication example; commented deployment. Nested ECR/Kubernetes, versioning, simple and syntax examples have differing helper/target assumptions.',
}
for b in branches:text+=f'| `{b}` | `{shas[b]}` | {summaries[b]} |\n'
text+='\n## Feature evidence\n\n| Feature | Immutable source reference | Supported interpretation |\n|---|---|---|\n'
for title,b,f,needle,desc in rows:text+=f'| {title} | {locate(b,f,needle)} | {desc} |\n'
text+='''
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
'''
for b in branches:
    text+=f'\n### `{b}`\n\n```text\n'+git('ls-tree','-r','--name-only','origin/'+b)+'```\n'
(OUT/'EVIDENCE.md').write_text(text)
print('Evidence audit written for',len(branches),'branches and',len(rows),'feature references')
