FROM python:3.12-slim
RUN mkdir /jwtpt
WORKDIR /jwtpt
COPY requirements.txt .
RUN pip install -U -r requirements.txt
COPY . .
RUN chmod a+x docker/*.sh

