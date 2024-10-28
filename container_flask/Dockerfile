FROM amazonlinux:2023

COPY ./app /app

WORKDIR /app

RUN yum install python pip -y

RUN pip install flask

CMD python /app/app.py




# FROM amazonlinux:2023

# EXPOSE 80
# RUN yum update -y
# RUN yum install -y python3-flask
# COPY ./app /app
# WORKDIR /app

# CMD ["/usr/bin/python3", "/app/main.py"]