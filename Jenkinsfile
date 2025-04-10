pipeline {
    agent any

    environment {
        REGISTRY = '199900000'  // Docker Hub username
        IMAGE_NAME = 'scalling'     // Docker image name
        IMAGE_TAG = 'lat'       // Version tag
        DOCKER_CREDENTIALS = 'gatepass_dockerhub'  // Jenkins credential ID for Docker login
        SONARQUBE_CREDENTIALS = 'gatepass_sonarqube'  // Jenkins credential ID for SonarQube
        SONARQUBE_URL = "http://sonar:9000"  // SonarQube server URL
        PROJECT_KEY = "gatepassvms"  // Unique key for your SonarQube project
        EMAIL_RECIPIENTS = 'teklemariamshewamnil@gmail.com'
        DOTNET_TOOLS_PATH = "$HOME/.dotnet/tools" // Path for .NET global tools
       
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'git@github.com:michaelnig1133/scaling_script.git'
            }
        }

        stage('build) {
              steps{
                  script {
                      sh '''
                        echo "Building Docker image..."
                        docker compose up -d
                      '''
                  }
              }
        }

      
       
        // stage('Build and Push Docker Image') {
        //     steps {
        //         script {
        //             withDockerRegistry([credentialsId: env.DOCKER_CREDENTIALS, url: 'https://index.docker.io/v1/']) {
        //                 sh '''#!/bin/bash
        //                     echo "Building Docker image..."
        //                     docker compose build

        //                     // echo "Tagging image..."
        //                     // docker tag scalling $REGISTRY/$IMAGE_NAME:$IMAGE_TAG

        //                     // echo "Pushing image to Docker Hub..."
        //                     // docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
        //                 '''
        //             }
        //         }
        //     }
        // }

        // stage('Deploy Application') {
        //     steps {
        //         script {
        //             sh '''#!/bin/bash
        //                 echo "Stopping existing container..."
        //                 docker compose down

        //                 echo "Deploying new version..."
        //                 docker compose up -d
        //             '''
        //         }
        //     }
        // }
    }

    post {
        success {
            echo 'Deployment Successful!'
            emailext(
                subject: "Deployment Successful - GatePass App",
                body: "The GatePass application has been successfully deployed.",
                to: "$EMAIL_RECIPIENTS",
                 attachLog: true
            )
        }
        failure {
            echo 'Deployment Failed. Check logs.'
            emailext(
                subject: "Deployment Failed - GatePass App",
                body: "The deployment has failed. Please check the Jenkins logs for details.",
                to: "$EMAIL_RECIPIENTS",
                attachLog: true
            )
        }
    }
}
