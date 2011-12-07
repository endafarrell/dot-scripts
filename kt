#!/bin/bash

/usr/local/apache-tomcat-7.0.2/bin/shutdown.sh
sleep 3
ps -ef | grep 'org.apache.catalina.startup.Bootstrap start' | grep -v apache-tomcat-solr | grep -v grep | awk '{print $2}' | xargs kill -9

