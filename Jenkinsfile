pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}/two-tier-flask-app"
        COMPOSE_FILE = "${PROJECT_DIR}/docker-compose.yml"
    }

    stages {

        stage('Pulizia ambiente') {
            steps {
                echo 'Pulizia ambiente esistente del progetto...'
                sh '''
                # Stoppo e rimuovo SOLO i container di questo progetto, usando docker-compose down
                if [ -f ${COMPOSE_FILE} ]; then
                    docker-compose -f ${COMPOSE_FILE} down
                fi

                # Non tocco gli altri container, né le immagini globali!
                '''
            }
        }

        stage('Clona repository') {
            steps {
                echo 'Pulizia vecchia cartella di progetto (se esiste)...'
                sh '''
                # Rimuovo la directory solo di questa repo
                rm -rf ${PROJECT_DIR}

                # Ora clono ex novo
                git clone -b master https://github.com/Ciro-Gallucci/two-tier-flask-app.git ${PROJECT_DIR}
                '''
            }
        }

        stage('Build immagine Flask') {
            steps {
                echo 'Costruisco immagine Flask...'
                dir("${PROJECT_DIR}") {
                    sh '''
                    docker build -t flaskapp:latest .
                    '''
                }
            }
        }

        stage('Avvio docker-compose') {
            steps {
                echo 'Avvio dei servizi con Docker Compose...'
                sh '''
                docker-compose -f ${COMPOSE_FILE} up -d --build
                '''
            }
        }

        stage('Check servizi') {
            steps {
                echo 'Verifica stato container...'
                sh 'docker ps'
            }
        }

    }

    post {
        success {
            echo 'Applicazione Flask su localhost avviata con successo!'
            echo 'Visita: http://localhost:5500'
        }
        failure {
            echo 'Errore nella pipeline!'
        }
    }
}
