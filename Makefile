poetry-install:
	poetry install
	poetry run pre-commit install
	poetry shell

pip-install:
	python3 -m pip install -r build/requirements.txt
	pre-commit install

poetry-requirements:
	poetry export --with dev --without-hashes --format=requirements.txt > build/requirements.txt

poetry-update-from-pip:
	poetry add $( cat build/requirements.txt)

pip-requirements:
	pip freeze > build/requirements.txt

streamlit:
	poetry run streamlit run src/01_Home.py

docker-build:
	docker build -t streamlit:latest -f build/docker/Dockerfile .

docker-run:
	docker run -p 8501:8501 streamlit:latest

black:
	poetry run black .

bandit:
	poetry run bandit -r src/
