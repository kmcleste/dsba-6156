pip-install:
	python3 -m pip install -r build/requirements.txt
	pre-commit install

pip-reqs:
	pip freeze > build/requirements.txt

streamlit:
	poetry run streamlit run src/01_Home.py

docker-build:
	docker build -t streamlit:latest -f build/docker/Dockerfile .

docker-run:
	docker run -p 8501:8501 streamlit:latest

black:
	black .

bandit:
	bandit -r src/

fastapi:
	uvicorn main:app --reload --app-dir src/api
