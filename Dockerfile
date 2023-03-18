FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
COPY initialization.py ./

RUN pip install -r requirements.txt

COPY . .

RUN python initialization.py

EXPOSE 5000
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]