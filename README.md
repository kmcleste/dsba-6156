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

We have included some helper functions to build and run the docker image for you. Run the following:

```bash
make docker-build
make docker-run
```

Once the service has finished initializing, you can head on over to [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive Swagger documentation.

## License

[MIT](https://choosealicense.com/licenses/mit/)
