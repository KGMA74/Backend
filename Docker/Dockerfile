FROM python:3.11-slim

WORKDIR /Backend

COPY ./ .
RUN python3 -m env /opt/env && \
    /opt/env/bin/pip install --upgrade pip && \
    /opt/env/bin/pip install -r requirements.txt && \
    chmod +x /