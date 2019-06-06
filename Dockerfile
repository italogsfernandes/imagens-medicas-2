From python:3.6COPY . .RUN pip install -r requirements.txt
CMD ["python", "./my_script.py"]
