ARG PYTHON_VERSION=3.9
ARG SHA256=c46b0ae5728c2247b99903098ade3176a58e274d9c7d2efeaaab3e0621a53935

FROM python:${PYTHON_VERSION}-slim AS build

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:${PYTHON_VERSION}-slim-bookworm AS prod

WORKDIR /app
COPY . /app

COPY --from=build /app/wheels /wheels
COPY --from=build /app/requirements.txt .

RUN pip install --no-cache /wheels/*

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
