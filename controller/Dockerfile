FROM python:3.9

RUN pip install -U pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]