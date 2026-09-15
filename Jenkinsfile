pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен'
            }
        }
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }
        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest suites/ -v --junitxml=result.xml
                '''
            }
        }
        stage('Publish results') {
            steps {
                junit 'result.xml'
            }
        }
    }
}