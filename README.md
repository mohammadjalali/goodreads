## Goodreads sample APIs

This is just a sample project for goodreads APIs.

For running the project, install docker and docker-compose, and then run the commands below.

```bash
cp .env.sample .env && cd .scripts && chmode +x entrypoint.sh load_fixtures.sh && cd .. && docker compose up --build
```

You can see the apis and use them from [swagger](http://localhost:8000/api/schema/swagger-ui/)
or [redoc](http://localhost:8000/api/schema/redoc/).

If you like to have some data, you can load the fixtures. You must go to the
`goodreads-backend` container, cd to the `.scripts` directory, and run the `load_fixtures.sh`.

```bash
1. docker exec -it goodreads-backend sh
2. cd .scripts
3. ./load_fixtures.sh
```
