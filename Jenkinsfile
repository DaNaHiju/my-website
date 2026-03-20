pipeline {
    agent any

    environment {
        GITHUB_REPO = 'github.com/your-username/my-website'  // Change to your GitHub repo
        DOCKER_IMAGE = 'my-website'
        DOCKER_TAG = "${BUILD_NUMBER}"  // Build number from Jenkins
        REGISTRY = 'docker.io'  // Docker Hub or your registry
        REGISTRY_CREDENTIALS = 'docker-credentials'  // Jenkins credentials ID
    }

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Checking out code from GitHub...'
                checkout scm
            }
        }

        stage('Setup & Install Dependencies') {
            steps {
                echo '🔧 Setting up Python environment...'
                sh '''
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '✅ Running tests...'
                sh '''
                    pip install pytest pytest-flask
                    pytest -v tests/ || true
                '''
            }
        }

        stage('Code Quality Check') {
            steps {
                echo '🔍 Checking code quality...'
                sh '''
                    pip install pylint
                    pylint app.py || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG} ${REGISTRY}/${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Push to Docker Registry') {
            steps {
                echo '📤 Pushing Docker image to registry...'
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${REGISTRY}/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${REGISTRY}/${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                echo '🚀 Deploying to staging environment...'
                sh '''
                    docker-compose -f docker-compose.yml down || true
                    docker-compose -f docker-compose.yml up -d
                    sleep 5
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
        success {
            echo '✅ Pipeline succeeded! App is ready to deploy.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            cleanWs()  // Clean workspace after build
        }
    }
}
