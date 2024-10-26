pipeline {
    agent any
    environment {
        TURBOSCRIBE_USERNAME = credentials('turboscribe-credentials', 'username')
        TURBOSCRIBE_PASSWORD = credentials('turboscribe-credentials', 'password')
        PROJECT_ROOT = "${WORKSPACE}"
    }
    stages {
        stage('Setup') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'turboscribe-credentials', usernameVariable: 'TURBOSCRIBE_USERNAME', passwordVariable: 'TURBOSCRIBE_PASSWORD')]) {
                        sh 'python3 -m venv venv'
                        sh '. venv/bin/activate && pip install -r requirements.txt'
                    }
                }
            }
        }
        stage('Lint') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'turboscribe-credentials', usernameVariable: 'TURBOSCRIBE_USERNAME', passwordVariable: 'TURBOSCRIBE_PASSWORD')]) {
                        sh '. venv/bin/activate && flake8 turboscribe/'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'turboscribe-credentials', usernameVariable: 'TURBOSCRIBE_USERNAME', passwordVariable: 'TURBOSCRIBE_PASSWORD')]) {
                        // Add PROJECT_ROOT to PYTHONPATH
                        sh '. venv/bin/activate && PYTHONPATH=$PROJECT_ROOT pytest --maxfail=1 --disable-warnings'
                    }
                }
            }
        }
        stage('Build Docs') {
            when {
                branch 'main'
            }
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'turboscribe-credentials', usernameVariable: 'TURBOSCRIBE_USERNAME', passwordVariable: 'TURBOSCRIBE_PASSWORD')]) {
                        sh '. venv/bin/activate && make -C docs clean html'
                    }
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'docs/build/html/**', allowEmptyArchive: true
            cleanWs()
        }
    }
}
