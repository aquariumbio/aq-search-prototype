FROM jupyter/scipy-notebook:latest as notebook-base

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
