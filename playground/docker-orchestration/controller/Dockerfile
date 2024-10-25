FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
COPY controller.py .
RUN pip install -r requirements.txt
CMD ["python", "controller.py"]