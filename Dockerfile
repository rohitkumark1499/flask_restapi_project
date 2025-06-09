# FROM python:3.11
# EXPOSE 5000
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY . .
# CMD ["flask","run","--host","0.0.0.0"]

FROM python:3.11
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]