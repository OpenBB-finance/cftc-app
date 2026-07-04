FROM python:3.10-slim-bookworm

RUN useradd -m -s /bin/bash openbb

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir openbb-cftc openbb-core openbb-platform-api

COPY start.py .
COPY static ./static
COPY system_settings.json /home/openbb/.openbb_platform/system_settings.json
RUN chown -R openbb:openbb /home/openbb/.openbb_platform

USER openbb
ENV HOME=/home/openbb

EXPOSE 7750

ENTRYPOINT ["python", "start.py"]
