# DSBA 6156: Applied Machine Learning

![](https://img.shields.io/github/last-commit/kmcleste/dsba-6156)

Shared repository for Applied Machine Learning Group 2 Final Project.

## Installation

- pip

    ```bash
    make pip-install
    ```

## Docker

We have included some helper functions to build and run the docker image for you. Run the following:

```bash
make docker-build
make docker-run
```

Once the build is complete, docker should spin up a new container which hosts our Streamlit site. You can access the site by going to [localhost:8501](https://localhost:8501) in your browser.

## Usage

![](images/swagger_example.png)

## License

[MIT](https://choosealicense.com/licenses/mit/)
