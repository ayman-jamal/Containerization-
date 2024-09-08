FROM python

WORKDIR /auth

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . . 

CMD ["python","auth.py"]

