FROM python:3.13

COPY requirements.txt ./
RUN python -m pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./main.py

CMD ["python", "/main.py"]