FROM python:3.6
ENV PYTHONUNBUFFERED 1

#spark
RUN wget http://apache.mirror.anlx.net/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
RUN tar -xzf spark-2.4.0-bin-hadoop2.7.tgz -C /usr/local/
ENV SPARK_HOME /usr/local/spark-2.4.0-bin-hadoop2.7
ENV PATH $PATH:$SPARK_HOME/bin
# ENV PYSPARK_SUBMIT_ARGS = "--packages=org.apache.hadoop:hadoop-aws:2.7.3 pyspark-shell"

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk8-installer;

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code
EXPOSE 8100

