FROM python:3.11

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the scripts to the folder
COPY . /app
EXPOSE 5000
CMD ["python", "sunfish_api/app.py"]
