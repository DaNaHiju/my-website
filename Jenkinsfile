pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'my-website'
        DOCKER_TAG = "${BUILD_NUMBER}"
        REGISTRY = 'docker.io'
        REGISTRY_CREDENTIALS = 'docker-credentials'
        DOCKER_HUB_USERNAME = credentials('${REGISTRY_CREDENTIALS}')
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image for testing...'
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Run Tests in Docker') {
            steps {
                echo '✅ Running tests in Docker container...'
                sh '''
                    docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        sh -c "pip install pytest pytest-flask && pytest -v tests/"
                '''
            }
        }

        stage('Code Quality Check') {
            steps {
                echo '🔍 Checking code quality...'
                sh '''
                    docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} \
                        sh -c "pip install pylint && pylint app.py || true"
                '''
            }
        }

        stage('Push to Docker Registry') {
            steps {
                echo '📤 Pushing Docker image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_USER}/${DOCKER_IMAGE}:latest
                        docker push ${DOCKER_USER}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_USER}/${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy Locally for Testing') {
            steps {
                echo '🚀 Deploying Docker container...'
                sh '''
                    docker stop my-website-container || true
                    docker rm my-website-container || true
                    docker run -d -p 5000:5000 --name my-website-container ${DOCKER_IMAGE}:${DOCKER_TAG}
                    sleep 3
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo '🏥 Performing health check...'
                sh '''
                    curl -f http://localhost:5000/health || exit 1
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Cleaning up test container...'
            sh '''
                docker stop my-website-container || true
                docker rm my-website-container || true
            '''
            cleanWs()
        }
        success {
            echo '✅ Pipeline succeeded! App is ready to deploy.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
    }
}
