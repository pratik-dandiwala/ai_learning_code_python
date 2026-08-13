# pick a base image (e.g., `python:3.11`)
FROM python:3.12-slim

# set the working folder inside the container
WORKDIR /app

#copy your project files into the container
COPY requirements.txt .

# install dependencies (e.g., `pip install -r requirements.txt`)
RUN pip install --no-cache-dir -r requirements.txt

# copy the app code
COPY . .

#declare the port your app runs on
EXPOSE 8000

# the command that starts your app when the container runs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


