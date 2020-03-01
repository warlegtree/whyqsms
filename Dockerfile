#NCP sms
#Version 1.0

# Base images
FROM ubuntu:xenial


#MAINTAINER
MAINTAINER ezngzen

#Config pip.conf
RUN mkdir /root/.pip/
ADD pip.conf /root/.pip/
ADD sources.list /etc/apt/

#install python3
RUN apt-get update
RUN apt-get install cron python3 python3-pip vim -y

#install python module
RUN pip3 install  requests aliyun-python-sdk-core

#make phone dir
RUN mkdir /home/phone
#add the program
ADD smsyq.py /home
RUN chmod +x /home/smsyq.py
ADD smsyq /etc/cron.d/
RUN chmod 0644 /etc/cron.d/smsyq
RUN crontab /etc/cron.d/smsyq
RUN touch /var/log/cron.log
CMD ["cron", "-f"]


