pipeline {
    agent any
    environment {
        VENV_DIR = "venv"
        BRANCH_NAME = "${env.BRANCH_NAME}"
    }
    stages {
        stage('Setup') {
            steps {
                sh 'python3 -m venv ${VENV_DIR}'
                sh '. ${VENV_DIR}/bin/activate && pip install -r requirements.txt'
            }
        }
        stage('Lint') {
            steps {
                sh '. ${VENV_DIR}/bin/activate && flake8 turboscribe/'
            }
        }
        stage('Test') {
            steps {
                sh '. ${VENV_DIR}/bin/activate && pytest --maxfail=1 --disable-warnings'
            }
        }
        stage('Build Docs') {
            when {
                branch 'main' // Only build docs for main branch
            }
            steps {
                sh '. ${VENV_DIR}/bin/activate && make -C docs clean html'
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