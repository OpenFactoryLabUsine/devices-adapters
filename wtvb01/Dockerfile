FROM python:3.12-slim

WORKDIR /app

COPY opcua_base/ ./opcua_base/
COPY wtvb01/ ./wtvb01/

RUN pip install --no-cache-dir -r wtvb01/requirements.txt

ENV VIRTUAL_DEVICE=true

CMD ["python", "-m", "wtvb01.server"]