pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
        disableConcurrentBuilds()
    }

    triggers {
        // Trigger immediately on GitHub push webhook
        githubPush()
        // Automatic SCM polling fallback every 2 minutes (works even if Jenkins is on localhost)
        pollSCM('H/2 * * * *')
    }

    parameters {
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run Pytest automated testing suite')
        booleanParam(name: 'BUILD_DOCKER', defaultValue: true, description: 'Build and package Docker container image')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push built image to Docker Hub registry')
        booleanParam(name: 'TRIGGER_ANSIBLE', defaultValue: false, description: 'Execute Ansible deployment automation')
        string(name: 'IMAGE_NAME', defaultValue: 'fittrack-app', description: 'Docker Image Name')
        string(name: 'IMAGE_TAG', defaultValue: 'latest', description: 'Docker Image Tag')
        string(name: 'ANSIBLE_TARGET', defaultValue: 'local', description: 'Target Ansible inventory host group')
    }

    environment {
        PYTHON_APP_ENV = 'testing'
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_CREDS_ID = 'dockerhub-credentials'
        TEST_CONTAINER_NAME = "fittrack-test-${env.BUILD_NUMBER ?: 'smoke'}"
        CONTAINER_PORT = '5000'
    }

    stages {
        // Stage 1: Checkout Code from Source Control
        stage('1. Checkout Code') {
            steps {
                echo '=== Stage 1: Checking out source code from Git repository ==='
                checkout scm
            }
        }

        // Stage 2: Set up Python Environment
        stage('2. Setup Python') {
            steps {
                echo '=== Stage 2: Verifying Python installation & virtual environment ==='
                script {
                    if (isUnix()) {
                        sh '''
                            python3 --version || python --version
                            python3 -m venv .jenkins_venv || python -m venv .jenkins_venv
                        '''
                    } else {
                        bat '''
                            if exist "C:\\Users\\pavip\\anaconda3\\python.exe" set "PATH=C:\\Users\\pavip\\anaconda3;C:\\Users\\pavip\\anaconda3\\Scripts;%PATH%"
                            python --version
                            python -m venv .jenkins_venv
                        '''
                    }
                }
            }
        }

        // Stage 3: Install Project Dependencies
        stage('3. Install Dependencies') {
            steps {
                echo '=== Stage 3: Installing dependencies from requirements.txt ==='
                script {
                    if (isUnix()) {
                        sh '''
                            . .jenkins_venv/bin/activate
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                            if exist "C:\\Users\\pavip\\anaconda3\\python.exe" set "PATH=C:\\Users\\pavip\\anaconda3;C:\\Users\\pavip\\anaconda3\\Scripts;%PATH%"
                            call .jenkins_venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                            python -m pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        // Stage 4: Run Pytest Automated Testing
        stage('4. Run Pytest') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                echo '=== Stage 4: Running automated Pytest suite (Fail immediately on error) ==='
                script {
                    if (isUnix()) {
                        sh '''
                            . .jenkins_venv/bin/activate
                            pytest -v --junitxml=pytest-results.xml
                        '''
                    } else {
                        bat '''
                            if exist "C:\\Users\\pavip\\anaconda3\\python.exe" set "PATH=C:\\Users\\pavip\\anaconda3;C:\\Users\\pavip\\anaconda3\\Scripts;%PATH%"
                            call .jenkins_venv\\Scripts\\activate.bat
                            pytest -v --junitxml=pytest-results.xml
                        '''
                    }
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'pytest-results.xml'
                }
            }
        }

        // Stage 5: Application Syntax & Configuration Checks
        stage('5. Syntax & Config Checks') {
            steps {
                echo '=== Stage 5: Verifying syntax, schema scripts, and configuration ==='
                script {
                    if (isUnix()) {
                        sh '''
                            . .jenkins_venv/bin/activate
                            python -m py_compile app.py config.py database/db.py database/init_db.py services/analytics.py
                            echo "Application syntax validation passed."
                        '''
                    } else {
                        bat '''
                            if exist "C:\\Users\\pavip\\anaconda3\\python.exe" set "PATH=C:\\Users\\pavip\\anaconda3;C:\\Users\\pavip\\anaconda3\\Scripts;%PATH%"
                            call .jenkins_venv\\Scripts\\activate.bat
                            python -m py_compile app.py config.py database/db.py database/init_db.py services/analytics.py
                            echo Application syntax validation passed.
                        '''
                    }
                }
            }
        }

        // Stage 6: Build Docker Image
        stage('6. Build Docker Image') {
            when {
                expression { return params.BUILD_DOCKER }
            }
            steps {
                echo "=== Stage 6: Building Docker image ${params.IMAGE_NAME}:${params.IMAGE_TAG} ==="
                script {
                    if (isUnix()) {
                        sh """
                            docker build -t ${params.IMAGE_NAME}:${params.IMAGE_TAG} -t ${params.IMAGE_NAME}:latest .
                        """
                    } else {
                        bat """
                            docker build -t ${params.IMAGE_NAME}:${params.IMAGE_TAG} -t ${params.IMAGE_NAME}:latest .
                        """
                    }
                }
            }
        }

        // Stage 7: Container & Health-Check Validation
        stage('7. Health-Check Validation') {
            when {
                expression { return params.BUILD_DOCKER }
            }
            steps {
                echo '=== Stage 7: Starting ephemeral container and testing /api/health endpoint ==='
                script {
                    if (isUnix()) {
                        sh """
                            docker rm -f ${env.TEST_CONTAINER_NAME} || true
                            docker run -d --name ${env.TEST_CONTAINER_NAME} -p 5055:5000 ${params.IMAGE_NAME}:${params.IMAGE_TAG}
                            sleep 6
                            curl --fail --retry 5 --retry-delay 2 http://localhost:5055/api/health
                            docker rm -f ${env.TEST_CONTAINER_NAME}
                            echo "Container health check successfully validated."
                        """
                    } else {
                        bat """
                            docker rm -f ${env.TEST_CONTAINER_NAME} 2>nul || ver >nul
                            docker run -d --name ${env.TEST_CONTAINER_NAME} -p 5055:5000 ${params.IMAGE_NAME}:${params.IMAGE_TAG}
                            ping 127.0.0.1 -n 7 >nul
                            curl --fail --retry 5 --retry-delay 2 http://localhost:5055/api/health
                            docker rm -f ${env.TEST_CONTAINER_NAME}
                            echo Container health check successfully validated.
                        """
                    }
                }
            }
        }

        // Stage 8: Tag Docker Image
        stage('8. Tag Docker Image') {
            when {
                expression { return params.BUILD_DOCKER }
            }
            steps {
                echo '=== Stage 8: Tagging Docker image for release ==='
                script {
                    if (isUnix()) {
                        sh """
                            docker tag ${params.IMAGE_NAME}:${params.IMAGE_TAG} ${params.IMAGE_NAME}:build-${params.IMAGE_TAG}
                        """
                    } else {
                        bat """
                            docker tag ${params.IMAGE_NAME}:${params.IMAGE_TAG} ${params.IMAGE_NAME}:build-${params.IMAGE_TAG}
                        """
                    }
                }
            }
        }

        // Stage 9: Optionally Push to Docker Hub
        stage('9. Push Docker Image') {
            when {
                expression { return params.PUSH_IMAGE }
            }
            steps {
                echo '=== Stage 9: Authenticating and pushing Docker image to registry ==='
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    script {
                        if (isUnix()) {
                            sh """
                                echo "\$DOCKER_PASS" | docker login -u "\$DOCKER_USER" --password-stdin
                                docker tag ${params.IMAGE_NAME}:${params.IMAGE_TAG} \$DOCKER_USER/${params.IMAGE_NAME}:${params.IMAGE_TAG}
                                docker tag ${params.IMAGE_NAME}:latest \$DOCKER_USER/${params.IMAGE_NAME}:latest
                                docker push \$DOCKER_USER/${params.IMAGE_NAME}:${params.IMAGE_TAG}
                                docker push \$DOCKER_USER/${params.IMAGE_NAME}:latest
                                docker logout
                            """
                        } else {
                            bat """
                                echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                                docker tag ${params.IMAGE_NAME}:${params.IMAGE_TAG} %DOCKER_USER%/${params.IMAGE_NAME}:${params.IMAGE_TAG}
                                docker tag ${params.IMAGE_NAME}:latest %DOCKER_USER%/${params.IMAGE_NAME}:latest
                                docker push %DOCKER_USER%/${params.IMAGE_NAME}:${params.IMAGE_TAG}
                                docker push %DOCKER_USER%/${params.IMAGE_NAME}:latest
                                docker logout
                            """
                        }
                    }
                }
            }
        }

        // Stage 10: Trigger Ansible Deployment
        stage('10. Trigger Ansible Deployment') {
            when {
                expression { return params.TRIGGER_ANSIBLE }
            }
            steps {
                echo "=== Stage 10: Executing Ansible deployment on target host: ${params.ANSIBLE_TARGET} ==="
                script {
                    if (isUnix()) {
                        sh """
                            ansible-playbook -i ansible/inventory.ini ansible/playbook.yml \
                                --extra-vars "docker_image_tag=${params.IMAGE_TAG} target_hosts=${params.ANSIBLE_TARGET}"
                        """
                    } else {
                        bat """
                            ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --extra-vars "docker_image_tag=${params.IMAGE_TAG} target_hosts=${params.ANSIBLE_TARGET}"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo '=== Pipeline Execution Completed ==='
            script {
                if (isUnix()) {
                    sh """
                        docker rm -f ${env.TEST_CONTAINER_NAME} 2>/dev/null || true
                    """
                } else {
                    bat """
                        docker rm -f ${env.TEST_CONTAINER_NAME} 2>nul || ver >nul
                    """
                }
            }
        }
        success {
            echo 'FitTrack CI/CD pipeline completed successfully.'
        }
        failure {
            echo 'FitTrack CI/CD pipeline encountered an error. Check stage logs for details.'
        }
    }
}
