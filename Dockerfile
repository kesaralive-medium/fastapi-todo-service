FROM python:3.10

ENV PYTHONUNBUFFERED True
ENV TZ=Asia/Kolkata

RUN rm /etc/localtime && ln -s /usr/share/zoneinfo/$TZ /etc/localtime

RUN mkdir /app

COPY ./ /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV ATLAS_URI=""
ENV DB_NAME=""

RUN pip3 install poetry==1.5.1
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


#CMD exec uvicorn "app.main:start" --host 0.0.0.0 --port 8000 --workers 2 --factory
#CMD ["/app/.venv/bin/uvicorn", "app.main:start", "--host", "0.0.0.0", "--port","8090", "--workers", "2", "--factory"]
CMD ["poetry","run","start"]