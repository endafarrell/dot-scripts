#!/bin/bash

ps -ef | grep catalina | awk '{print $2}' | xargs kill -9
rm -rf /usr/local/apache-tomcat-6.0.18/webapps/kv*
rm -rf /usr/local/apache-tomcat-6.0.18/work/*
rm -rf /usr/local/apache-tomcat-6.0.18/logs/*
cp /Workspace/kv2-webapp/target/kv.war /usr/local/apache-tomcat-6.0.18/webapps/
/usr/local/apache-tomcat-6.0.18/bin/startup.sh
