default: debug

debug:
	uvicorn main:app --reload

load_data:
	python3 -m scripts.load_data

rm_revisions:
	rm -rf alembic/versions/*

gen_revision:
	alembic revision --autogenerate -m "init migration"

upgrade:
	alembic upgrade head

.PHONY: default load_data gen_revision rm_revisions upgrade debug
