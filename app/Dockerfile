FROM python:3.9
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl
COPY . .
CMD ["python3", "app.py"]  