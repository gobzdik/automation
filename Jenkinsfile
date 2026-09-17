pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.62.0-jammy'
            args '-u root'
        }
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Код получен'
                sh 'rm -rf reports/ result.xml screenshots.tar.gz allure-results allure-report'
            }
        }

        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh 'pytest suites/ -v --junitxml=result.xml --alluredir=allure-results'
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
            archiveArtifacts artifacts: 'result.xml', allowEmptyArchive: true

            sh 'tar -czf results.tar.gz reports/ || true'
            archiveArtifacts artifacts: 'results.tar.gz', allowEmptyArchive: true

            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
        }
    }
}