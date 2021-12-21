pipeline {
    agent { docker { image 'python-black' } }
    stages {
        stage('build') {
            steps {
                sh 'python -V'
                sh 'python -m black bandcamp.py'
            }
        }
    }
}