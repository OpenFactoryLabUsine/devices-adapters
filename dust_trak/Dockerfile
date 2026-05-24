FROM python:3.12-slim

WORKDIR /app

COPY opcua_base/ ./opcua_base/
COPY dust_trak/ ./dust_trak/

RUN pip install --no-cache-dir -r dust_trak/requirements.txt

ENV VIRTUAL_DEVICE=true

CMD ["python", "-m", "dust_trak.server"]