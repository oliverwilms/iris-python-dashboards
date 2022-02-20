FROM intersystemsdc/iris-community

USER root   

RUN apt-get update && apt-get install -y \
	nano \
	python3-pip \
	python3-venv

WORKDIR /opt/irisapp
RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/irisapp
USER ${ISC_PACKAGE_MGRUSER}

COPY . /opt/irisapp
COPY src/dash/assets /usr/irissys/bin/

RUN iris start IRIS \
	&& iris session IRIS < /opt/irisapp/iris.script \
    && iris stop IRIS quietly

ENV PYTHONPATH=/usr/irissys/bin/irispython
ENV SRC_PATH=/opt/irisapp
ENV IRISUSERNAME "SuperUser"
ENV IRISPASSWORD "SYS"
ENV IRISNAMESPACE "IRISAPP"

RUN pip3 install -r ${SRC_PATH}/src/dash/requirements.txt

# Install jupyter
RUN pip3 install jupyter
RUN mkdir /home/irisowner/.local/share/jupyter/kernels/irispython
COPY misc/kernels/irispython/* /home/irisowner/.local/share/jupyter/kernels/irispython/

# Install Native API
COPY misc/intersystems_irispython-3.2.0-py3-none-any.whl /usr/irissys/dev/python/intersystems_irispython-3.2.0-py3-none-any.whl
RUN pip3 install /usr/irissys/dev/python/intersystems_irispython-3.2.0-py3-none-any.whl

# WORKDIR ${SRC_PATH}/src/flask
# RUN $PYTHON_PATH -m gunicorn --bind "0.0.0.0:8080" wsgi:app