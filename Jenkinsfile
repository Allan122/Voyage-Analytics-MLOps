pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                git 'https://github.com/Allan122/Voyage-Analytics-MLOps.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t voyage_mlops_app:latest .'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yml'
            }
        }
    }
}