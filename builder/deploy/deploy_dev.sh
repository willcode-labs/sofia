#!/bin/bash 
directory="$(dirname "$(realpath "$BASH_SOURCE")")"

builder_container()
{
    database_password=$1
    echo '------------------------------------------------'
    echo 'Install database'
    echo '------------------------------------------------'
    cd ${directory}/../container/database/DEV
    docker build --force-rm -t sofia-core-db-dev .
    docker run --name SOFIA-CORE-DB-DEV -p 9001:5432 -e POSTGRES_PASSWORD=${database_password} -d sofia-core-db-dev

    echo '------------------------------------------------'
    echo 'Install App'
    echo '------------------------------------------------'
    cd ${directory}/../container/app/DEV
    docker build --force-rm -t sofia-core-dev .
    docker run --name SOFIA-CORE-DEV --link SOFIA-CORE-DB-DEV -p 9002:80 -d sofia-core-dev

    echo '------------------------------------------------'
    echo 'Run Migrations App'
    echo '------------------------------------------------'
    docker exec -it SOFIA-CORE-DEV /bin/bash -c 'python3 makemigrations api --check'
    docker exec -it SOFIA-CORE-DEV /bin/bash -c 'python3 migrate api'
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
                docker container ls -a
            else
                builder_container 1234567890
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
        *) echo 'Invalid option';;
    esac
done
