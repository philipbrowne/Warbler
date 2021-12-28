FROM debian:buster-slim
RUN apt-get update -y 
RUN apt-get install --no-install-recommends -y apache2 libapache2-mod-wsgi-py3 wget python3-pip
RUN a2enmod wsgi
RUN adduser --system --group --disabled-login user ; cd /home/user
RUN wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py' ; python3 get-pip.py --disable-pip-version-check --no-cache-dir
COPY requirements.txt /var/www/app/requirements.txt
RUN pip install -r /var/www/app/requirements.txt
COPY apache2.conf /var/www/app/apache2.conf
RUN cat /var/www/app/apache2.conf > /etc/apache2/apache2.conf
RUN apt-get clean
RUN mkdir /logs
COPY . /var/www/app
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND", "-f", "/etc/apache2/apache2.conf"]