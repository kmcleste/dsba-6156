pip-install:
	python3 -m pip install -r requirements.txt
	pre-commit install

docker-build-ui:
	docker build -t search-ui:latest -f build/docker/ui/Dockerfile .

docker-build-api:
	docker build -t search-api:latest -f build/docker/api/Dockerfile .

docker-build: ui-build api-build

docker-run-ui:
	docker run -p 8501:8501 search-ui:latest

docker-run-api:
	docker run -p 8000:8000 -e API_BASE_URL=http://search-api:8000 search-api:latest

black:
	black .

bandit:
	bandit -r src/

fastapi:
	uvicorn main:app --reload --reload-dir src/api --app-dir src/api

streamlit:
	streamlit run src/ui/01_🏠_Home.py
