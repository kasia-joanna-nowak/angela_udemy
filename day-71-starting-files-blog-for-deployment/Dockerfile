FROM python:3.12

COPY requirements.txt .

RUN pip install -r requirements.txt
  
COPY . .

EXPOSE 5001

CMD ["Flask", "run", "--host=0.0.0.0", "--port=5001"]



