# DSBA 6156: Applied Machine Learning

![](https://img.shields.io/github/last-commit/kmcleste/dsba-6156)

Shared repository for Applied Machine Learning Group 2 Final Project.

## Getting Started

Make sure to read through our [Contribution Guidelines](https://github.com/kmcleste/dsba-6156/blob/main/CONTRIBUTING.md) for instructions on environment setup and creating your first commit.

## Usage

Below are instructions for running the project locally and within a [Docker](https://www.docker.com/) container.

### Local

To start the FastAPI service, run the following from the base directory of the repo:

```bash
make fastapi
```

Once the service has finished initializing, you can head on over to [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive Swagger documentation.

![](images/swagger_example.png)

To start the Streamlit service, open another terminal and run:

```bash
make streamlit
```

Once the Streamlit service has started, you can view the web app by going to [127.0.0.1:8501](http://127.0.0.1:8501) in your browser.

### Docker

To start the services in Docker, run the following:

```bash
docker-compose up
```

Once the services have finished initializing, you can head on over to [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and [127.0.0.1:8501](http://127.0.0.1:8501) to view the Swagger documentation and Streamlit app, respectively.

To start the services independent of one another, you can run each command in a separate terminal:

```bash
make docker-run-ui
make docker-run-api
```

To build the images locally, run:

```bash
# build both images
make docker-build

# build individually
make docker-build-ui
make docker-build-api

# build using docker compose
docker-compose -f docker-compose-dev.yml build

# build and run
docker-compose -f docker-compose-dev.yml up --build
```

Note: If the docker images do not already exist on your system, they will be built automatically. This process can take some time.

## License

[MIT](https://choosealicense.com/licenses/mit/)
