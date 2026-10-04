# Jenkins CI/CD for Java: Docker, Amazon ECR & Kubernetes

## Short overview

This DevOps case study presents a repository-defined Jenkins pipeline for a Java/Spring Boot application. The configuration updates the Maven project version, packages the application with a JUnit test, builds and publishes a tagged Docker image to Amazon ECR, and applies parameterized Kubernetes Deployment and Service manifests. Separate branches demonstrate Terraform infrastructure definitions and Docker Compose deployment commands for Amazon EC2. The scope is build and deployment engineering; live production operation and application authorship are not claimed.

## Responsibilities represented by the repository

- Jenkins pipeline configuration for Maven packaging, Docker image publication, Kubernetes manifest application, and Git version writeback.
- Container packaging of a Java application using a Java 8 runtime image and an executable JAR.
- Image tagging with the application version and Jenkins build number in the ECR pipeline variant.
- Environment-based substitution of application and image values into Kubernetes manifests.
- Kubernetes configuration for a single-replica Deployment and an internal Service forwarding port 80 to container port 8080.
- Jenkins credential bindings for registry, AWS, and Git integration; an image-pull Secret reference in the Deployment.
- A separate Terraform/EC2 variant defining network resources, a security group, an instance, Docker installation user data, and SSH/Compose deployment commands.

## Technologies / skills

Jenkins, CI/CD, Docker, Apache Maven, Kubernetes, Amazon ECR, Amazon EC2, Terraform, Docker Compose, Git, Bash, Groovy, Linux.

Application context: Java 8 and Spring Boot. Supplemental branch configuration: PostgreSQL, Ansible, Sonatype Nexus, and Jenkins Shared Libraries.

## Key DevOps features

- **Versioned delivery:** the ECR variant ties the image tag to the Maven project version and Jenkins build number.
- **Build and test lifecycle:** `mvn clean package` runs Maven packaging; the repository includes a basic JUnit test of an application method. This is not a service-health or end-to-end test.
- **Declarative runtime configuration:** Kubernetes Deployment and Service templates receive image and application values through `envsubst` before `kubectl apply`.
- **Alternative deployment approach:** an independent branch contains Terraform AWS definitions and a two-service Compose stack. It is presented separately from the Kubernetes path.

## Results supported by repository evidence

- A checked-in five-stage Jenkins configuration covers version update, application packaging, image publication, Kubernetes apply, and Git writeback.
- A Dockerfile and matching manifest variables define how the packaged application is delivered to a Kubernetes target.
- Terraform and deployment scripts document an alternative EC2/Compose approach; the branch contains a directory mismatch that requires resolution before an end-to-end run.
- No uptime, deployment-speed, availability, or production-security metrics are claimed. Successful live Jenkins, ECR, Kubernetes, and EC2 execution was not verified in this review.

## Recommended Upwork skill tags

Use the closest available tags to: Jenkins, CI/CD, Docker, Kubernetes, Terraform, Amazon Web Services, Amazon EC2, Git, Linux, and Bash. Maven and Amazon ECR can appear in the project description if the platform does not offer matching tags.

## Attribution

These statements describe configuration found in the repository, not independently verified personal authorship. Before publishing first-person responsibilities, retain only work the portfolio owner actually performed. The application is context for the DevOps case study, not an application-development claim.
