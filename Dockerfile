# Building the main container
FROM python:3.7
# 0.9.1.post1
WORKDIR /tmp
COPY requirements.txt .
RUN apt-get update
RUN pip install --no-cache -r requirements.txt
COPY crtx_backend/uwsgi.ini /etc/uwsgi/
COPY crtx_backend/supervisord.conf /etc/supervisor/conf.d/

WORKDIR /app
ADD crtx_backend/*.py /app/
EXPOSE 9090
EXPOSE 8080
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

#WORKDIR /label-studio
#RUN apt-get update
#RUN apt-get install git-all


#RUN git clone https://github.com/heartexlabs/label-studio-ml-backend
#RUN cd label-studio-ml-backend
#RUN pip install -U -e .
# RUN mkdir /label-studio/data
# COPY conf/crtx_config.xml /label-studio/conf/crtx_config.xml
# ENV LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
# ENV INIT_COMMAND=--init --force --input-path=/label-studio/data/deepfashion/Sheer_Pleated-Front_Blouse --label-config=/label-studio/conf/crtx_config.xml --input-format=image-dir
# ENV LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/label-studio/data
# ENV LOCAL_FILES_DOCUMENT_ROOT=/label-studio/data
# ENV LOCAL_FILES_DOCUMENT_ROOT=/home/mi/carrillo/SynologyDrive/arbeit/crtx/label-studio/small_example_project/data/deepfashion/Sheer_Pleated-Front_Blouse
# ENV LOCAL_FILES_DOCUMENT_ROOT=/home/user
# ENV LOCAL_FILES_DOCUMENT_ROOT=/mnt/ameli/SynologyDrive/arbeit/crtx/label-studio/small_example_project/myfiles
# RUN label-studio start --username "admin@crtx.com" --password "12345678" --user-token "admin"
#https://labelstud.io/guide/start.html