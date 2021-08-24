FROM python:3.9
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
WORKDIR /link_cutter_app
COPY . .
CMD python flask_app.py