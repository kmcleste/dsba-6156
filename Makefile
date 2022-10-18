pip-install:
	python3 -m pip install -r build/requirements.txt
	pre-commit install

pip-reqs:
	pip freeze > build/requirements.txt

streamlit:
	poetry run streamlit run src/ui/streamlit_app.py

docker-build:
	docker build -t search:latest -f build/docker/Dockerfile .

docker-run:
	docker run -p 8000:8000 search:latest

black:
	black .

bandit:
	bandit -r src/

fastapi:
	uvicorn main:app --reload --app-dir src/api
