FROM python:3.12

WORKDIR /restapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /restapi_app/

CMD ["python", "./main.py"]