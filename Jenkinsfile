pipeline {
    agent any

    stages {

        stage('Checkout'){
            steps{
                checkout scm
            }
        }

        stage('Install Dependencies'){
            steps{
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Test'){
            steps {
                sh 'pytest'
            }
        }

        stage('Build Docker Image'){
            steps{
                sh '''
                    export PATH=$PATH:$HOME/.local/bin:$(pwd)/docker
                    if ! command -v docker &> /dev/null; then
                        echo "Docker CLI not found. Downloading statically..."
                        curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-24.0.9.tgz
                        tar xzvf docker-24.0.9.tgz
                    fi
                    
                    if ! docker info > /dev/null 2>&1; then
                        echo "WARNING: Docker daemon is not accessible (unix:///var/run/docker.sock)."
                        echo "Skipping image build."
                        echo "true" > .skip_docker
                    else
                        docker build -t seatmeup:latest .
                        echo "false" > .skip_docker
                    fi
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps{
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]){
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push anantparab/flask-app:latest
                    '''
                }
            }
        }

    }

}