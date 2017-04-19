#!/bin/bash

outputFile="$(mktemp)"
customTmp="$(mktemp)"

log() {
  echo "$1" >> $outputFile
}

redact() {
  sed -i 's/$1=.*/$1=REDACTED/g' $2
}

#Find the ActiveMQ paths
amq=$(ps aux | grep activemq | grep -v grep)
amqConf=$(echo $amq | grep -o 'activemq.conf=\(/[a-zA-Z0-9\.\-]*\)*' | cut -f 2 -d "=")

#Find the config files
amqXml=$amqConf/activemq.xml
amqUsers=$amqConf/users.properties
amqGroups=$amqConf/groups.properties

#Find the Opencast paths
oc=$(ps aux | grep opencast | grep -v grep)
ocConf=$(echo $oc | grep -o 'karaf.etc=\(/[a-zA-Z0-9\.\-]*\)*' | cut -f 2 -d "=")
ocData=$(echo $oc | grep -o 'karaf.data=\(/[a-zA-Z0-9\.\-]*\)*' | cut -f 2 -d "=")

#Find the config files
ocCustom=$ocConf/custom.properties
ocOrgFile=$ocConf/org.opencastproject.organization-mh_default_org.cfg
ocLogFile=$ocConf/org.ops4j.pax.logging.cfg
currentLog=$(grep '^log4j.appender.out.file' $ocLogFile | cut -f 2 -d "=")
isKarafData=$(echo $currentLog | grep -o "karaf.data")
if [ -n "$isKarafData" ]; then
  currentLog="$ocData/log/opencast.log"
fi

echo "Log file can be found at $outputFile"
log "Detecting file locations..."
log "ActiveMQ config XML is at: $amqXml"
log "ActiveMQ users config is at: $amqUsers"
log "ActiveMQ groups config is at: $amqGroups"

log "Opencast custom.properties is at: $ocCustom"
log "Opencast organization config is at: $ocOrgFile"
log "Opencast logging config is at: $ocLogFile"
log "Opencast logfile is at: $currentLog"

#is oc running?
if [ -n "$oc" ]; then
  log "Opencast is running"
else
  log "Opencast is NOT running"
fi

#Gather ActiveMQ auth settings
ocAmqHost=$(grep '^activemq.broker.url' $ocCustom | cut -f 2 -d "=" | sed 's/.*tcp:\/\/\(.*\):\(.*\)\?.*/\1/')
ocAmqUser=$(grep '^activemq.broker.username' $ocCustom | cut -f 2 -d "=")
ocAmqPass=$(grep '^activemq.broker.password' $ocCustom | cut -f 2 -d "=")

#If amq is local in oc conf...
isLocal=$(echo $ocAmqHost | grep -o $HOSTNAME)
if [ -n $isLocal ]; then
  log "Opencast thinks ActiveMQ is running locally..."
  #Is amq running?
  if [ -n "$amq" ]; then
    log "and ActiveMQ is running locally"
  else
    log "but ActiveMQ is not running locally"
  fi

  #If both of the Opencast AMQ auth settings are are set
  if [ -n "$ocAmqUser" -a -n "$ocAmqPass" ]; then
    amqUserPass=$(grep "$ocAmqUser:$ocAmqPass" $amqUsers)
    amqUserGroup=$(grep $ocAmqUser $amqGroups | cut -f 1 -d "=")

    #TODO: Make this check better
    amqXmlGroup=$(grep 'authorizationEntry topic' $amqXml  | grep -o 'read="\w*"' | head -n 1 | cut -f 2 -d "=" | sed 's/"//g')
    #Does amqUserGroup match amqXmlGroup
    if [ "$amqUesrGroup" -ne "$amqXmlGroup" ]; then
      log "ActiveMQ user authentication settings do not match!"
    fi
  fi
else
  log "Opencast thinks ActiveMQ is running remotely."
fi

#try to log into amq
echo "TODO: Log into ActiveMQ"

#Attempt to log into mysql
ocSqlHost=$(grep '^org.opencastproject.db.jdbc.url' $ocCustom | cut -f 2 -d "=" | sed 's/.*mysql:\/\/\(.*\)\/.*/\1/')
ocSqlUser=$(grep '^org.opencastproject.db.jdbc.user' $ocCustom | cut -f 2 -d "=")
ocSqlPass=$(grep '^org.opencastproject.db.jdbc.pass' $ocCustom | cut -f 2 -d "=")

if [ -n "$ocSqlHost" ]; then
  log "\nSQL Grants:"
  if [ -n "$ocSqlPass" ]; then
	  mysql -u$ocSqlUser -p$ocSqlPass -h $ocSqlHost -e 'SHOW GRANTS FOR CURRENT_USER;' | sed 's/PASSWORD .*/REDACTED/g' >> $outputFile
  else
	  mysql -u$ocSqlUser -h $ocSqlHost -e 'SHOW GRANTS FOR CURRENT_USER;' | sed 's/PASSWORD .*/REDACTED/g' >> $outputFile
  fi
else
  log "Using internal H2 DB"
fi

#sanitize custom.properties
cp $ocCustom $customTmp
redact org.opencastproject.security.admin.user $customTmp
redact org.opencastproject.security.admin.pass $customTmp
redact org.opencastproject.security.digest.user $customTmp
redact org.opencastproject.security.digest.pass $customTmp
redact org.opencastproject.db.jdbc.user $customTmp
redact org.opencastproject.db.jdbc.pass $customTmp
redact activemq.broker.username $customTmp
redact activemq.broker.password $customTmp
redact karaf.shutdown.command $customTmp

#Cat the redacted custom.properties file to the output file
log "\ncustom.properties"
cat $customTmp >> $outputFile

log "\nLast 500 lines of the logfile"
tail -n 500 $currentLog >> $outputFile
 
log "\nMemory Stats"
free -m >> $outputFile

log "\nDisk Stats"
df -h >> $outputFile

log "\nNetstat"
netstat -tulpen >> $outputFile

