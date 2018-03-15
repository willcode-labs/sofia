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
option_list=("[1]Status" "[2]Build" "[3]Restart Database" "[4]Restart App" "[5]Quit")
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
            echo 'Container database restart'
            # TODO
            ;;
        "[4]Restart App")
            echo 'Container app restart'
            # TODO
            ;;
        "[5]Quit")
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
