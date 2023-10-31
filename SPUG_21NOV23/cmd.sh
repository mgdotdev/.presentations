
build() {
    docker compose build --parallel --no-cache
    docker build -f .docker/Dockerfile.testing -t demo-testing .
}

test() {
    docker run -d -ti \
        -v $PWD:/home/user/code \
        --name demo-testing-1 \
        demo-testing bash
    docker network connect demo-public demo-testing-1
    docker exec -it demo-testing-1 bash
    docker kill demo-testing-1 &> /dev/null
    docker rm demo-testing-1 &> /dev/null
}

# main
case $1 in
    "build"|"b") build $@ ;;
    "test"|"t") test $@ ;;
esac
