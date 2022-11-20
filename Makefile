pip-install:
	python3 -m pip install -r requirements.txt
	pre-commit install

docker-build-ui:
	docker build -t search-ui:latest -f build/docker/ui/Dockerfile .

docker-build-api:
	docker build -t search-api:latest -f build/docker/api/Dockerfile .

docker-build: docker-build-ui docker-build-api

black:
	black .

bandit:
	bandit -r src/

fastapi:
	uvicorn main:app --reload --reload-dir src/api --app-dir src/api

streamlit:
	streamlit run src/ui/01_🏠_Home.py
