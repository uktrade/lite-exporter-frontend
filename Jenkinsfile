pipeline {
  agent {
    node {
      label 'docker.ci.uktrade.io'
    }
  }

  stages {
    stage('prep') {
      steps {
        script {
          deleteDir()
          checkout scm
          deployer = docker.image("joyzoursky/python-chromedriver:3.7-selenium")
          deployer.pull()
        }
      }
    }

    stage('running selenium tests') {
      steps {
        script {
          deployer.inside {
            sh 'echo running'
            sh 'ls'
            sh 'python --version'
            sh 'python test.py'
            println "Result: Done"
          }
        }
      }
    }
  }
}
