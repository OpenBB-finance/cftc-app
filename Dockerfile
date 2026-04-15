FROM python:3.10-slim-bookworm

WORKDIR /app

COPY *.whl .

RUN pip install *.whl && rm -f *.whl

ENV OPENBB_API_AUTH=false

EXPOSE 7750

ENTRYPOINT ["openbb-api", "--host", "0.0.0.0", "--port", "7750"]
