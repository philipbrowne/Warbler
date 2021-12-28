pipeline {
   agent any
   stages{
      stage ('Assemble Container') {
         steps{
            sh "docker-compose up -d"
            echo "Docker Containers Running"
            sh "docker ps"
            sh 'echo "Running First Unit Test"'
            sh "docker-compose run web python3 -m /var/www/app/test_message_model.py"
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