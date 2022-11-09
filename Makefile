pip-install:
	python3 -m pip install -r build/requirements.txt
	pre-commit install

ui-build:
	docker build -t ui:latest -f build/docker/ui/Dockerfile .

api-build:
	docker build -t api:latest -f build/docker/api/Dockerfile .

docker: ui-build api-build

black:
	black .

bandit:
	bandit -r src/

fastapi:
	uvicorn main:app --reload --app-dir src/api

streamlit:
	streamlit run src/ui/01_🏠_Home.py
