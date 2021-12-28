pipeline {
   agent any
   stages{
      stage ('Get Source') {
         steps{
            sh 'ls'
            echo "This is your project directory"
            }
         }
   // stage('Build Docker Image from Docker Compose') {
   //     // build the docker image from the source code using the BUILD_ID parameter in image name
   //       sh "docker-compose build"
   // }
   // stage("run docker container"){
   //      sh "docker-compose up"
   //  }
   }
}