FROM python:3.11-alpine as requirements-builder

RUN mkdir build/
WORKDIR /build/

COPY Pipfile Pipfile.lock /build/

RUN pip install pipenv
RUN pipenv requirements > requirements.txt


FROM python:3.11-alpine

RUN mkdir /app
WORKDIR /app/

COPY --from=requirements-builder /build/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY employment_exchange employment_exchange
COPY migrations migrations

WORKDIR /app/employment_exchange
# COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]