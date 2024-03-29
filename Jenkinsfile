pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
        stage('Test') {
            steps {
                dir ('lib') {
                    git branch: "mod/2101", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('mongo_lib') {
                    git branch: "mod/422", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/mongo-lib.git"
                }
                dir ('mongo_lib/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                dir ('rabbit_lib') {
                    git branch: "mod/221", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/rabbitmq-lib.git"
                }
                dir ('checklog') {
                    git branch: "mod/402", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/check-log.git"
                }
                dir ('checklog/lib') {
                    git branch: "mod/294", credentialsId: "2cfb403c-be21-4fac-94d7-c8cd5c531feb", url: "https://gitlab.code.dicelab.net/JAC-IDM/python-lib.git"
                }
                sh """
                virtualenv test_env
                source test_env/bin/activate
                pip2 install mock==2.0.0 --user
                pip2 install pika==1.2.0 --user
                pip2 install psutil==5.4.3 --user
                pip2 install pymongo==3.8.0 --user
                /usr/bin/python2 ./test/unit/pulled_search/checks_dirs.py
                /usr/bin/python2 ./test/unit/pulled_search/cleanup_files.py
                /usr/bin/python2 ./test/unit/pulled_search/config_override.py
                /usr/bin/python2 ./test/unit/pulled_search/file_input.py
                /usr/bin/python2 ./test/unit/pulled_search/get_archive_files.py
                /usr/bin/python2 ./test/unit/pulled_search/help_message.py
                /usr/bin/python2 ./test/unit/pulled_search/insert_data.py
                /usr/bin/python2 ./test/unit/pulled_search/insert_mongo.py
                /usr/bin/python2 ./test/unit/pulled_search/is_base64.py
                /usr/bin/python2 ./test/unit/pulled_search/load_processed.py
                /usr/bin/python2 ./test/unit/pulled_search/main.py
                /usr/bin/python2 ./test/unit/pulled_search/mvalidate_dirs.py
                /usr/bin/python2 ./test/unit/pulled_search/non_processed.py
                /usr/bin/python2 ./test/unit/pulled_search/parse_data.py
                /usr/bin/python2 ./test/unit/pulled_search/process_docid.py
                /usr/bin/python2 ./test/unit/pulled_search/process_failed.py
                /usr/bin/python2 ./test/unit/pulled_search/process_files.py
                /usr/bin/python2 ./test/unit/pulled_search/process_insert.py
                /usr/bin/python2 ./test/unit/pulled_search/process_json.py
                /usr/bin/python2 ./test/unit/pulled_search/recall_search.py
                /usr/bin/python2 ./test/unit/pulled_search/recall_search2.py
                /usr/bin/python2 ./test/unit/pulled_search/remove_processed.py
                /usr/bin/python2 ./test/unit/pulled_search/run_program.py
                /usr/bin/python2 ./test/unit/pulled_search/search_docid.py
                /usr/bin/python2 ./test/unit/pulled_search/update_processed.py
                /usr/bin/python2 ./test/unit/pulled_search/validate_dirs.py
                /usr/bin/python2 ./test/unit/pulled_search/write_summary.py
                deactivate
                rm -rf test_env
                """
            }
        }
        stage('SonarQube analysis') {
            steps {
                sh './test/unit/sonarqube_code_coverage.sh'
                sh 'rm -rf lib'
                sh 'rm -rf checklog'
                sh 'rm -rf rabbit_lib'
                sh 'rm -rf mongo_lib'
                script {
                    scannerHome = tool 'sonar-scanner';
                }
                withSonarQubeEnv('Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.JACIDM.properties"
                }
            
            }
        }
        stage('Artifactory upload') {
            steps {
                script {
                    server = Artifactory.server('Artifactory')
                    server.credentialsId = 'art-svc-highpoint-dev'
                    uploadSpec = """{
                        "files": [
                            {
                                "pattern": "./*.py",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/pulled-search/"
                            },
                            {
                                "pattern": "./*.txt",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/pulled-search/"
                            },
                            {
                                "pattern": "./*.md",
                                "recursive": false,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/pulled-search/"
                            },
                            {
                                "pattern": "*.TEMPLATE",
                                "recursive": true,
                                "excludePatterns": [],
                                "target": "pypi-proj-local/highpoint/pulled-search/config/"
                            }
                        ]
                    }"""
                    server.upload(uploadSpec)
                }
            }
        }
    }
    post {
        always {
            cleanWs disableDeferredWipeout: true
        }
    }
}
