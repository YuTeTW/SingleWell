#
FROM python:3.9

#
WORKDIR /SWserver

#
COPY ./requirements.txt /SWserver/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /SWserver/requirements.txt

#
COPY ./app /SWserver/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

