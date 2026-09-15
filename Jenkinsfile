pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.62.0-jammy'
            args '-u root'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен'
                sh 'rm -rf reports/ result.xml'
            }
        }
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run tests') {
            steps {
                sh 'pytest suites/ -v --junitxml=result.xml'
            }
        }
        stage('Publish results') {
            steps {
                junit 'result.xml'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'result.xml, reports/**', allowEmptyArchive: true
        }
    }
}