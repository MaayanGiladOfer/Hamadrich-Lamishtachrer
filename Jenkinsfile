pipeline {
    agent any
    environment {
        DOCKER_REGISTRY = "your-docker-registry"
        DOCKER_IMAGE = "${env.DOCKER_REGISTRY}/your-app:${env.BUILD_NUMBER}"
        KUBECONFIG_LOCAL = "/path/to/oracle/kubeconfig"
    }
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://your-git-repo.git'
            }
        }
        stage('Build and Test') {
            steps {
                sh 'mvn clean package'
                sh 'mvn test'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-credentials') {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }
        stage('Deploy to AWS') {
            when {
                branch 'aws-branch' // Adjust as necessary
            }
            steps {
                script {
                    withEnv(["KUBECONFIG=${KUBECONFIG_AWS}"]) {
                        sh """
                        sed -i 's|image:.*|image: ${DOCKER_IMAGE}|g' aws/path/to/terraform/manifest.yaml
                        cd aws
                        terraform init
                        terraform apply -auto-approve
                        """
                    }
                }
            }
        }
        stage('Deploy to Oracle') {
            when {
                branch 'oracle-branch' // Adjust as necessary
            }
            steps {
                script {
                    withEnv(["KUBECONFIG=${KUBECONFIG_LOCAL}"]) {
                        sh """
                        sed -i 's|image:.*|image: ${DOCKER_IMAGE}|g' oracle/path/to/terraform/manifest.yaml
                        cd oracle
                        terraform init
                        terraform apply -auto-approve
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}