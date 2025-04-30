# Dockerfile
FROM python:3.11-slim-bullseye

WORKDIR /st_sstedoldi_cv

COPY requirements.txt /st_sstedoldi_cv/

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /st_sstedoldi_cv/

EXPOSE 8501

CMD ["streamlit","run", "app.py"]