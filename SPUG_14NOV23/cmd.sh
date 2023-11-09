
build() {
    docker compose build --parallel --no-cache
}

test() {
    name="demo-testing-$2"
    instance="$name-1"
    exists=$(docker images --format "{{.Repository}}" | grep $name )
    [[ -z "$exists" || "$3" = "--build" ]] && {
        docker build \
            -f .docker/Dockerfile.testing \
            --build-arg FRAMEWORK=$2 \
            -t $name \
            . --no-cache
    }
    docker run -d -ti \
        -v $PWD/$2:/home/user/code/api \
        --name $instance \
        --env-file .env/redis.env \
        demo-testing-$2 bash
    docker network connect demo-network $instance
    docker exec -it $instance bash
    docker kill $instance &> /dev/null
    docker rm $instance &> /dev/null
}

restart() {
    docker compose down -t 0
    docker compose up -d
}

# main
case $1 in
    "build"|"b") build $@ ;;
    "test"|"t") test $@ ;;
    "restart") restart $@ ;;
esac
