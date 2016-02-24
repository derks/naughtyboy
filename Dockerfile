FROM python:3.5

MAINTAINER BJ Dierkes <derks@datafolklabs.com> 

ADD . /app/
RUN pip install -r /app/requirements.txt
CMD python /app/naughtyboy.py run /app/commands.yml --with-prep
