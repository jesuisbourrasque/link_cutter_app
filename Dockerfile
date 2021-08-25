FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /link_cutter_app
CMD python /link_cutter_app/flask_app.py