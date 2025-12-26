.PHONY: run test lint

run:
uvicorn app.main:app --reload

test:
pytest -q
