from pathlib import Path
from html import escape
import subprocess

OUT = Path(__file__).resolve().parents[1]
INK = '#142a43'
MUTED = '#536579'
BLUE = '#2468df'
TEAL = '#087f82'
LINE = '#dbe5ef'

class Diagram:
    def __init__(self, number, title, subtitle, scope):
        self.parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">',
          '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#2468df"/></marker></defs>']
        self.rect(0,0,1920,1080,'#f7f9fc',0)
        self.rect(70,58,8,102,BLUE,3)
        self.text(102,75,'DEVOPS PORTFOLIO  /  JAVA MAVEN APPLICATION',20,BLUE,True)
        self.text(102,126,title,42,INK,True)
        self.text(102,175,subtitle,24,MUTED)
        self.text(1818,87,f'{number:02d}',32,BLUE,True,anchor='end')
        self.rect(90,205,1740,48,'#eaf1ff',9)
        self.text(110,236,scope,20,BLUE)
        self.rect(90,984,1740,2,LINE,0)
        self.text(90,1024,'Repository configuration • Reviewed 04 Oct 2026 • No live deployment verification',18,MUTED)
        self.text(1830,1024,'walidali123 / java-maven-app',18,MUTED,anchor='end')

    def rect(self,x,y,w,h,fill='#ffffff',r=18,stroke=None):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="2"' if stroke else '')+'/>')

    def text(self,x,y,s,size=24,color=INK,bold=False,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(s)}</text>')

    def card(self,x,y,w,h,kicker,title,lines,color=BLUE):
        self.rect(x,y,w,h,stroke=LINE)
        self.rect(x+22,y+24,5,31,color,2)
        self.text(x+42,y+47,kicker,18,color,True)
        self.text(x+25,y+90,title,29,INK,True)
        for i,s in enumerate(lines):self.text(x+25,y+130+i*32,s,22,MUTED)

    def arrow(self,points,label=None,lx=None,ly=None,dash=False):
        pts=' '.join(f'{x},{y}' for x,y in points)
        self.parts.append(f'<polyline points="{pts}" fill="none" stroke="{BLUE}" stroke-width="3" marker-end="url(#arrow)"'+(' stroke-dasharray="9 7"' if dash else '')+'/>')
        if label:self.text(lx,ly,label,18,BLUE)

    def note(self,x,y,w,title,lines):
        self.rect(x,y,w,65+len(lines)*30,'#eef3f8',12)
        self.text(x+22,y+34,title,21,INK,True)
        for i,s in enumerate(lines):self.text(x+22,y+65+i*30,s,20,MUTED)

    def save(self,name):
        p=OUT/(name+'.svg')
        p.write_text('\n'.join(self.parts+['</svg>']))
        subprocess.run(['inkscape',str(p),'--export-type=png',f'--export-filename={OUT/(name+".png")}'],check=True,capture_output=True)

d=Diagram(1,'Java delivery architecture','Versioned container delivery to a configured Kubernetes target.',
 'PRIMARY VARIANT  •  java-maven-app-complete-pipeline-ecr-eks  •  EKS provisioning is not included')
d.card(90,305,440,200,'SOURCE','GitHub repository',['Java / Spring Boot application','Maven project + Jenkinsfile'])
d.card(740,305,440,200,'AUTOMATION','Jenkins',['Version update + Maven package','Docker build + publish + apply'])
d.card(1390,305,440,200,'IMAGE REGISTRY','Amazon ECR',['Version + Jenkins build-number tag','Registry authentication configured'])
d.arrow([(530,405),(740,405)],'job source',573,386)
d.arrow([(1180,405),(1390,405)],'publish image',1213,386)
d.card(90,610,440,200,'VERSION WRITEBACK','GitLab repository',['Commit updated project files','Push to jenkins-jobs branch'])
d.arrow([(830,505),(830,553),(310,553),(310,610)],'commit version update',345,541)
d.rect(740,580,1090,340,'#eef5ff',18,LINE)
d.text(768,620,'KUBERNETES TARGET  •  externally configured cluster',22,BLUE,True)
d.card(765,670,430,205,'INTERNAL TRAFFIC','Service · port 80',['Selector matches application labels','Forwards to container port 8080'])
d.card(1375,670,430,205,'APPLICATION','Deployment · 1 replica',['Java 8 runtime + packaged JAR','imagePullSecrets reference'])
d.arrow([(1195,765),(1375,765)],'HTTP',1250,746)
d.arrow([(1610,505),(1610,670)],'image pull',1630,567)
d.arrow([(970,505),(970,580)],'kubectl apply',991,552)
d.text(90,910,'No public ingress, reverse proxy, database, or TLS is configured in this variant.',22,MUTED)
d.save('01-devops-architecture')

d=Diagram(2,'Jenkins CI/CD pipeline','Five configured stages, with tests included in Maven packaging.',
 'PRIMARY VARIANT  •  Jenkinsfile stages  •  Pipeline execution evidence was not supplied')
cards=[(90,315,'01  VERSION','Increment version',['Maven version-update command','Tag = version + build number']),
 (680,315,'02  BUILD','Package application',['mvn clean package','JUnit test in Maven lifecycle']),
 (1270,315,'03  CONTAINER','Build & publish',['Docker build from packaged JAR','Push tagged image to Amazon ECR']),
 (1270,650,'04  DEPLOY','Apply manifests',['envsubst resolves image variables','kubectl apply: Deployment + Service']),
 (680,650,'05  WRITEBACK','Commit version update',['Commit updated files in Git','Push to GitLab jenkins-jobs'])]
for x,y,k,t,ls in cards:d.card(x,y,560,225,k,t,ls)
d.arrow([(650,427),(680,427)])
d.arrow([(1240,427),(1270,427)])
d.arrow([(1550,540),(1550,650)])
d.arrow([(1270,762),(1240,762)])
d.note(90,650,560,'What this configuration establishes',['Build, publication, and apply commands','No standalone test stage or rollout check','Webhook setup is external to this repo'])
d.text(90,946,'Evidence: Jenkinsfile · pom.xml · Dockerfile · src/test/java/AppTest.java',20,MUTED)
d.save('02-cicd-pipeline')

d=Diagram(3,'Infrastructure: two separate variants','Kubernetes application manifests and an independent EC2 / Compose configuration.',
 'BRANCH SCOPES  •  ECR / Kubernetes and Terraform / EC2 are alternatives, not one combined environment')
d.rect(90,290,840,590,'#eef5ff',18,LINE)
d.text(118,337,'A  /  KUBERNETES TARGET',25,BLUE,True)
d.text(118,375,'Cluster supplied outside the repository',22,MUTED)
d.card(120,415,780,185,'SERVICE','Internal application access',['Service port 80 → application port 8080','No LoadBalancer or Ingress definition'])
d.arrow([(510,600),(510,640)])
d.card(120,640,780,185,'DEPLOYMENT','Java application · 1 replica',['ECR image + imagePullSecrets reference','No probes, PVCs, or resource limits defined'])
d.rect(990,290,840,590,'#edf7f5',18,LINE)
d.text(1018,337,'B  /  TERRAFORM + EC2',25,TEAL,True)
d.text(1018,375,'VPC · subnet · internet gateway · routes · security group',21,MUTED)
d.card(1020,415,780,185,'HOST CONFIGURATION','Amazon Linux EC2',['User data installs Docker and Docker Compose','Public address + SSH key-pair reference'],TEAL)
d.arrow([(1410,600),(1410,640)])
d.card(1020,640,780,185,'COMPOSE SERVICES','Java application + PostgreSQL',['Published ports: application 8080 / database 5432','No named volume or application DB connection'],TEAL)
d.text(90,922,'EC2 variant: Terraform files are at repo root; Jenkins expects a terraform/ directory.',22,MUTED)
d.text(90,953,'These are checked-in definitions; running infrastructure and production readiness are not verified.',20,MUTED)
d.save('03-infrastructure')

d=Diagram(4,'How a release is configured to move','A tagged artifact links the build to the Kubernetes deployment manifest.',
 'PRIMARY VARIANT  •  Release flow begins when the Jenkins job runs  •  Push-trigger wiring is not checked in')
d.card(90,315,500,215,'01  INPUT','Jenkins job starts',['Source checked out by job configuration','Pipeline reads the Maven project'])
d.card(710,315,500,215,'02  ARTIFACT','Build versioned image',['Update project version + package JAR','Docker tag includes Jenkins build number'])
d.card(1330,315,500,215,'03  DELIVERY','Publish to Amazon ECR',['Registry login uses Jenkins credentials','docker push publishes the tagged image'])
d.arrow([(590,425),(710,425)])
d.arrow([(1210,425),(1330,425)])
d.card(1330,650,500,225,'04  CONFIGURATION','Render and apply',['envsubst inserts application and image','kubectl applies Deployment + Service'])
d.card(710,650,500,225,'05  TARGET STATE','Kubernetes desired state',['Deployment references the new image','Service routes to application port 8080'])
d.card(90,650,500,225,'06  SOURCE RECORD','Write version back',['Git commit after apply commands','Push goes to a GitLab branch'])
d.arrow([(1580,530),(1580,650)])
d.arrow([(1330,762),(1210,762)])
d.arrow([(710,762),(590,762)])
d.text(90,944,'The pipeline does not wait for rollout completion or execute a post-deployment health check.',22,MUTED)
d.save('04-deployment-flow')

d=Diagram(5,'Credential & access configuration','Repository-supported controls, shown with their operational limits.',
 'CONFIGURATION REVIEW  •  Credential bindings and firewall rules exist  •  No claim of a hardened production system')
d.card(90,305,550,245,'ECR / KUBERNETES VARIANT','Jenkins credential bindings',['Registry, AWS, and Git credentials','Referenced by credential IDs','Registry login uses password-stdin'])
d.card(685,305,550,245,'ECR / KUBERNETES VARIANT','Private-image pull reference',['Deployment names an imagePullSecret','The Secret object is not in this repo','Cluster access is an external prerequisite'])
d.card(1280,305,550,245,'TERRAFORM / EC2 VARIANT','Security-group rules',['SSH allowed from configured CIDRs','Application TCP 8080 open publicly','Outbound traffic allowed'],TEAL)
d.note(90,610,840,'Security boundaries to keep visible',['Kubernetes Service defaults to internal ClusterIP access.','No TLS / HTTPS, Ingress, RBAC, or securityContext defined.','No secret values or network addresses appear in these assets.'])
d.note(990,610,840,'Limitations of the checked-in deployment examples',['SSH commands disable host-key verification.','Compose includes a literal database password; value omitted.','Git credentials are interpolated into a remote URL.'])
d.text(90,891,'Credential references show intended integration; secret provisioning and safe runtime handling need validation.',21,MUTED)
d.text(90,944,'Evidence: Jenkinsfile · kubernetes/deployment.yaml · main.tf · docker-compose.yaml · server-cmds.sh',20,MUTED)
d.save('05-security')

print('Generated five PNGs and five editable SVGs at', OUT)
