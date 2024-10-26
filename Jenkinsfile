pipeline {
    agent any
    environment {
        TURBOSCRIBE_USERNAME = credentials('turboscribe-credentials', 'username')
        TURBOSCRIBE_PASSWORD = credentials('turboscribe-credentials', 'password')
    }
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                sh '. venv/bin/activate && flake8 turboscribe/'
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest --maxfail=1 --disable-warnings'
            }
        }
        stage('Build Docs') {
            when {
                branch 'main'
            }
            steps {
                sh '. venv/bin/activate && make -C docs clean html'
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
