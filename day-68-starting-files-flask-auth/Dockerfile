FROM python:3.12

WORKDIR /flask-auth-app

COPY ./requirements.txt /flask-auth-app/
RUN pip install -r requirements.txt
COPY . . 
EXPOSE 5000
CMD ["python",  "0.0.0.0", "flask-auth-app"]