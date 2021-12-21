pipeline {
    agent { docker { image 'python-black:v1' } }
    stages {
        stage('build') {
            steps {
                sh 'python -V'
                sh 'python -m black bandcamp.py'
            }
        }
    }
}