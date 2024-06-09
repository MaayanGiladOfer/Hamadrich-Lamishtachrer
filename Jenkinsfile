pipeline {
    agent any
    tools {
        maven 'maven' // Use the name you provided in the Global Tool Configuration
        terraform 'terraform'
    }
    environment {
        DOCKER_REGISTRY = "hub.docker.com"
        DOCKER_IMAGE = "${env.DOCKER_REGISTRY}/manofer/hamadrich-lamishtachrer:0.1.${env.BUILD_NUMBER}"
        KUBECONFIG_LOCAL = "/home/maayan/.kube/config"
        KUBECONFIG_AWS = ""  
    }
    stages {
        stage('Clone Repository') {
            steps {
                script {
                        git url: 'https://github.com/MaayanGiladOfer/Hamadrich-Lamishtachrer.git', branch: 'development'
                }
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
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'docker-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
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
