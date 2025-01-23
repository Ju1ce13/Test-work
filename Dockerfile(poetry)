FROM python:3.12-slim
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
EXPOSE 8080
CMD ["poetry", "run", "python", "app.py"]