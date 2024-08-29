FROM python:3.8

WORKDIR /workspace

ADD requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt

ADD app.py /workspace/

ENV HOME=/workspace

EXPOSE 80

CMD [ "python3" , "/workspace/app.py" ]