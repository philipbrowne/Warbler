pipeline {
   agent any
   stages{
      stage ('Assemble Container') {
         steps{
            sh "docker-compose up -d"
            echo "Docker Containers Running"
            echo "Seeding Database"
            sh 'docker exec -i warblerpipeline_web_1 bash -c "cd /var/www/app && python3 seed.py"'
            }
      }
      stage ('Run Tests') {
         steps{
            sh 'docker exec -i warblerpipeline_web_1 bash -c "cd /var/www/app && python3 -m unittest"'
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