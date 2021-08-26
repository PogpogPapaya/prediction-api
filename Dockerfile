FROM python:3.9.6-bullseye

WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
# RUN pip3 install --no-cache-dir Pillow
# RUN pip3 install --no-cache-dir fastapi
# RUN pip3 install --no-cache-dir keras
# RUN pip3 install --no-cache-dir tensorflow
COPY ./model-large.h5 ./
COPY ./server.py ./

CMD [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000" ]