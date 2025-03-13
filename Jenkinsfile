pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}/two-tier-flask-app"
        COMPOSE_FILE = "${PROJECT_DIR}/docker-compose.yml"
        VENV_DIR = "/var/jenkins_home/workspace/appdemo-new/venv"  // Directory per l'ambiente virtuale    
    }

    stages {

        stage('Pulizia ambiente') {
            steps {
                echo 'Pulizia ambiente esistente del progetto...'
                // Stoppo e rimuovo SOLO i container di questo progetto, usando docker-compose down
                sh '''
                if [ -f ${COMPOSE_FILE} ]; then
                    docker-compose -f ${COMPOSE_FILE} down
                fi
                '''
            }
        }

        stage('Clona repository') {
            steps {
                echo 'Pulizia vecchia cartella di progetto (se esiste)...'
                
                // Rimuovo la directory solo di questa repo
                // Quindi  clono ex novo
                sh '''
                rm -rf ${PROJECT_DIR}
                git clone -b master https://github.com/Ciro-Gallucci/two-tier-flask-app.git ${PROJECT_DIR}
                '''
            }
        }

        stage('Imposta ambiente virtuale') {
            steps {
                echo 'Creazione dell\'ambiente virtuale e installazione di Bandit...'
                sh 'python3 -m venv $VENV_DIR'
                sh '$VENV_DIR/bin/pip install --upgrade pip bandit'
            }
        }

        stage('Esegui Bandit') {
            steps {
                script {
                    // Esegui Bandit e forza l'uscita con codice 0 anche se Bandit rileva problemi
                    // Questi verranno visualizzati nel report e non bloccheranno la pipe
                    sh(returnStatus: true, script: './venv/bin/bandit -r . -f xml -o bandit-report.xml') 
                    echo "Analisi Bandit completata. Puoi controllare bandit-report.xml per i dettagli."
                    // Aggiungi questa riga per vedere se il file e' stato creato
                    sh 'ls -l bandit-report.xml'
                }
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
                dir("${PROJECT_DIR}") {
                    sh '''
                    docker-compose -f ${COMPOSE_FILE} up -d --build
                    '''
                }
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
        always {
            echo 'Archivia il report Bandit...'
            archiveArtifacts artifacts: 'bandit-report.xml', fingerprint: true
        }
    }
}
