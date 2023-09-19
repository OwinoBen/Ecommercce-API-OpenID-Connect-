FROM python:3.9.6-alpine
WORKDIR /savannah_api_test

#setting environment variables
ENV PYTHONDONTWRITEBYTECODE 1 #Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1 #Prevents Python from buffering stdout and stderr

#install postress conntion ddriver dependancies (psycopg)
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install all the dependancies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# coppy entrypoint to the plattform
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /savannah_api_test/entrypoint.sh
RUN chmod +x /savannah_api_test/entrypoint.sh

# Add project files to docker

COPY . .

# start entrypoint

ENTRYPOINT ["/savannah_api_test/entrypoint.sh"]