pipeline {
    agent any

    stages {
        stage('Install tools') {
            steps {
                 sh 'sudo apt-get update && sudo apt-get install -y python3-pip'
                 sh 'pip3 install pytest'
             }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/kdrzazga/empty-python-project.git']]])
            }
        }
        stage('Build') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Unit Test') {
            steps {
                sh 'pytest -m unit --junitxml=unittest-results.xml'
            }
            post {
                always {
                    junit 'unittest-results.xml'
                }
            }
        }
        stage('API Test') {
            steps {
                sh 'pytest -m api --junitxml=apitest-results.xml'
            }
            post {
                always {
                    junit 'apitest-results.xml'
                }
            }
        }
        stage('Web Test') {
            steps {
                sh 'pytest -m webtest --junitxml=webtest-results.xml'
            }
            post {
                always {
                    junit 'webtest-results.xml'
                }
            }
        }
        stage('Send Email') {
            steps {
                emailext (
                    subject: 'Test Report',
                    body: '''<html><body><p>Hi,</p><p>Please find attached the test report.</p></body></html>''',
                    to: 'zmwn@protonmail.com',
                    attachmentsPattern: '*test-results.xml',
                    mimeType: 'text/xml'
                )
            }
        }
    }
}