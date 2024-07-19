
FROM python:3.9-slim

#repo de travail
WORKDIR /app

COPY . .

EXPOSE 8501

CMD [ "streamlit" , "run", "web.py"]
#v