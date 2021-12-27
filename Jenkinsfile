node {
   stage('Get Source') {
      // copy source code from local file system and test
      // for a Dockerfile to build the Docker image
      git branch: 'main', 
      url: 'https://github.com/philipbrowne/Warbler.git'
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
   }
   stage('Build Docker Image from Docker Compose') {
       // build the docker image from the source code using the BUILD_ID parameter in image name
         sh "docker-compose build"
   }
   stage("run docker container"){
        sh "docker-compose up"
    }
}