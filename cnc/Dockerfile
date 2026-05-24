FROM python:3.12-slim

WORKDIR /app

COPY opcua_base/ ./opcua_base/
COPY cnc/ ./cnc/

RUN pip install --no-cache-dir -r cnc/requirements.txt

CMD ["python", "-m", "cnc.opcua_server"]