FROM jupyter/scipy-notebook:latest as notebook-base

RUN python3 -m pip install PyMySQL
