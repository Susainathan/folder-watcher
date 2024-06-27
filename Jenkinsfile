pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/Susainathan/folder-watcher.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    try {
                        sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install bandit semgrep
                        '''
                    } catch (Exception e) {
                        error "Installing dependencies failed: ${e.message}"
                    }
                }
            }
        }
        // stage('Run Security Checks') {
        //     steps {
        //         script {
        //             try {
        //                 sh '''
        //                 . venv/bin/activate
        //                 python security_check.py
        //                 '''
        //             } catch (Exception e) {
        //                 error "Security check failed: ${e.message}"
        //             }
        //         }
        //     }
        // }
        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('MySonar') {
                    sh '''
                            docker run --rm \
                              -v "$WORKSPACE:/usr/src" \
                              --network host \
                              -v "$WORKSPACE/.git:/usr/src/.git" \
                              sonarsource/sonar-scanner-cli:latest \
                              sonar-scanner \
                                -Dsonar.projectKey=first \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=http://localhost:9001 \
                                -Dsonar.login=sqp_ef3b30ddc87e7e3f82473ad4208624f3bbc881d4 \
                                -Dsonar.python.version=3.x
                            '''
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
