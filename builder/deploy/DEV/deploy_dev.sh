#!/bin/bash 
directory="$(dirname "$(realpath "$BASH_SOURCE")")"

source ${directory}/environment_variable.conf

builder_container()
{
    echo '------------------------------------------------'
    echo 'Install database'
    echo '------------------------------------------------'
    cd ${directory}/../../container/database/DEV
    docker image build --force-rm -t sofia-core-db-dev .
    docker container run --name SOFIA-CORE-DB-DEV -p 9001:5432 \
        -e POSTGRES_PASSWORD=${DB_PASSWORD} -d sofia-core-db-dev

    echo '------------------------------------------------'
    echo 'Install App'
    echo '------------------------------------------------'
    cd ${directory}/../../container/app/DEV
    docker image build --force-rm -t sofia-core-dev .
    docker container run --name SOFIA-CORE-DEV --link SOFIA-CORE-DB-DEV \
        -e DB_ENGINE=${DB_ENGINE} -e DB_NAME=${DB_NAME} \
        -e DB_USER=${DB_USER} -e DB_PASSWORD=${DB_PASSWORD} \
        -e DB_HOST=${DB_HOST} -e DB_PORT=${DB_PORT} \
        -p 9002:80 -d sofia-core-dev

    echo '------------------------------------------------'
    echo 'Run Migrations App'
    echo '------------------------------------------------'
    docker container exec -it SOFIA-CORE-DEV /bin/bash -c 'python3 manage.py makemigrations api --check'
    docker container exec -it SOFIA-CORE-DEV /bin/bash -c 'python3 manage.py migrate api'
}

echo '================================================'
echo 'Option select:'
echo '================================================'
option_list=("[1]Status" "[2]Build" "[3]Restart Database" "[4]Backup Database" "[5]Restore Database" "[6]Restart App" "[7]Quit")
select option in "${option_list[@]}"
do
    case $option in
        "[1]Status")
            echo '================================================'
            echo '------------------------------------------------'
            echo 'Status for docker images and containers'
            echo '------------------------------------------------'
            echo 'Images'
            echo '------------------------------------------------'
            docker image list
            echo '------------------------------------------------'
            echo 'Containers'
            echo '------------------------------------------------'
            docker container list -a --size
            echo '================================================'
            ;;
        "[2]Build")
            echo '================================================'
            echo '------------------------------------------------'
            echo 'Container build'
            echo '------------------------------------------------'
            total=$(docker container list --filter 'name=SOFIA-CORE' -a | wc -l)
            if [ "$total" -gt 1 ]
            then
                echo '------------------------------------------------'
                echo 'System already created!'
                echo '------------------------------------------------'
                docker container list -a
            else
                builder_container
            fi
            echo '================================================'
            ;;
        "[3]Restart Database")
            echo '------------------------------------------------'
            echo 'Container database restart'
            echo '------------------------------------------------'
            total=$(docker container list --filter 'name=SOFIA-CORE-DB' -a | wc -l)
            if [ "$total" -le 1 ]
            then
                echo '------------------------------------------------'
                echo 'Database dont exist!'
                echo '------------------------------------------------'
            else
                docker container restart SOFIA-CORE-DB-DEV
            fi
            echo '================================================'
            ;;
        "[4]Backup Database")
            echo '------------------------------------------------'
            echo 'Backup database from "'${DB_NAME}'"'
            echo '------------------------------------------------'
            docker container exec -it SOFIA-CORE-DB-DEV /usr/bin/pg_dumpall --host localhost --username "${DB_USER}" -W --verbose --quote-all-identifiers > $(date +"%d-%m-%Y_%H-%M-%S")_db.dump
            ;;
        "[5]Restore Database")
            # # Restore
            # cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE
            ;;
        "[6]Restart App")
            echo 'Container app restart'
            total=$(docker container list --filter 'name=SOFIA-CORE' -a | wc -l)
            if [ "$total" -le 1 ]
            then
                echo '------------------------------------------------'
                echo 'App dont exist!'
                echo '------------------------------------------------'
            else
                docker container restart SOFIA-CORE-DEV
            fi
            echo '================================================'
            ;;
        "[7]Quit")
            break
            ;;
        *)
            echo '================================================'
            echo '------------------------------------------------'
            echo 'Invalid option'
            echo '------------------------------------------------'
            echo '================================================'
            ;;
    esac
done
