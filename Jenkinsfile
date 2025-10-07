pipeline {
    agent any

    environment {
        IMAGE_NAME = "bha02/myapp"
        IMAGE_TAG  = "${GIT_COMMIT.take(7)}"
        SSH_TARGET = "ubuntu@13.127.199.194"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ./profile-app"
                    sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh "echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker push ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                sshagent (credentials: ['deploy-ssh-key']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${SSH_TARGET} '
                    cd /home/ec2-user &&
                    docker compose pull app || true &&
                    docker compose up -d app
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "App deployed successfully!"
        }
        failure {
            echo "Deployment failed!"
        }
    }
}
