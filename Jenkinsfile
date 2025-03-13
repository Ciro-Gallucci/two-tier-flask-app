pipeline {
    agent any

    environment {
        PROJECT_DIR = "${WORKSPACE}/two-tier-flask-app"
        COMPOSE_FILE = "${PROJECT_DIR}/docker-compose.yml"
        VENV_DIR = "/var/jenkins_home/workspace/appdemo-new/venv"  // Directory per l'ambiente virtuale    
        SEMGREP_RULES = "p/ci" // Regole predefinite per CI/CD, puoi personalizzarle
        SEMGREP_REPORT_NAME = "semgrep-report.json"  // Nome del report per Semgrep
        BANDIT_REPORT_NAME = "bandit-report.xml"  // Nome del report per Bandit
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
                echo 'Creazione dell\'ambiente virtuale e installazione di Bandit e Semgrep...'
                sh 'python3 -m venv $VENV_DIR'
                sh '$VENV_DIR/bin/pip install --upgrade pip bandit semgrep'
            }
        }

        stage('Esegui Bandit') {
            steps {
                script {
                    // Esegui Bandit solo nella cartella del progetto, escludendo l'ambiente virtuale
                    echo "Eseguo Bandit nella cartella del progetto..."
                    sh(returnStatus: true, script: 'cd ${PROJECT_DIR} && ${VENV_DIR}/bin/bandit -r . -f xml -o ${PROJECT_DIR}/bandit-report.xml')
                    echo "Analisi Bandit completata. Puoi controllare bandit-report.xml per i dettagli."
                    
                    // Verifica che il file sia stato creato nella cartella giusta
                    sh 'ls -l ${PROJECT_DIR}/bandit-report.xml'
                }
            }
        }

        stage('Esegui Semgrep') {
            steps {
                script {
                    echo "Eseguo Semgrep nella cartella del progetto..."
                    sh(returnStatus: true, script: 'cd ${PROJECT_DIR} && ${VENV_DIR}/bin/semgrep --config=${SEMGREP_RULES} --json > ${PROJECT_DIR}/${SEMGREP_REPORT_NAME}')
                    echo "Analisi Semgrep completata. Puoi controllare ${SEMGREP_REPORT_NAME} per i dettagli."
                    
                    // Verifica che il file del report di Semgrep sia stato creato
                    sh 'ls -l ${PROJECT_DIR}/${SEMGREP_REPORT_NAME}'
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
            echo 'Archivia i report Bandit e Semgrep...'
            archiveArtifacts artifacts: 'two-tier-flask-app/bandit-report.xml, two-tier-flask-app/semgrep-report.json', fingerprint: true
        }
    }
}
