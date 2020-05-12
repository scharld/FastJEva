#! /bin/bash
#project path
PKG=/home/sch/

#tools & resources
DATA=${PKG}/
SOURCES=${PKG}/src

#JAVA
JAVA=/home/sch/jdk8u-dev/build/linux-x86_64-normal-server-slowdebug/jdk/
MY_JAVA=${JAVA}/bin/

#Benchmarks
BENCHMARK=/home/jxf/benchmark/dacapo09/benchmarks/
DACAPO9=/home/sch/dacapo-9.12.jar
DACAPO_HPC_CACHE=${BENCHMARK}/dacapo-Normal_WithHpc.jar
DACAPO_HPC_DROP=${BENCHMARK}/dacapo-DropCache_WithHpc.jar
DACAPO_SLEEP=${BENCHMARK}/dacapo-OnlySleep.jar
DACAPO_DROP=${BENCHMARK}/dacapo-OnlyDrop.jar

itr=1
nitr=300
run=startup
sz=default

mkdir /home/sch/result/${run}/
#mkdir /home/sch/result/${run}/normal
#mkdir /home/sch/result/${run}/dropcache

#for app in xalan luindex #lusearch pmd sunflow batik avrora fop
#do
    #cd ${DATA}/result
#    echo ${app}
   # for i in `seq $itr`
   # do
#       echo "normal test starting"
#        java -Xmx16384m -jar ${DACAPO_DROP} -s $sz -n $nitr $app 1>Monitor 2>>TimeLog
      #  echo java -Xmx16384m -jar ${DACAPO9} -s $sz -n $nitr $app
#        mv ./TimeLog /home/sch/result/${run}/${app}_drop_TimeLog
        #mv ./Monitor ${DATA}/result/${run}/normal/${app}_Monitor
#        echo "normal test finish"

 #       echo "dropcache test starting"
 #       java -Xmx16384m -jar ${DACAPO_SLEEP} -s $sz -n $nitr $app 1>Monitor 2>TimeLog
 #       mv ./TimeLog ${DATA}/result/${run}/${app}_sleep__TimeLog
        #mv ./Monitor ${DATA}/result/${run}/dropcache/${app}_Monitor
 #       echo "dropcache test finish"
   # done

#done

for app in lusearch pmd sunflow batik avrora fop h2 jython tradesoap tradebeans 
do
    #cd ${DATA}/result
    echo ${app}
    for i in `seq $itr`
    do
#	echo "normal test starting"
	java -Xmx16384m -XX:+PrintCompilation -jar ${DACAPO9} -s $sz -n $nitr $app 1>TimeLog 2>&1
#	echo java -Xmx16384m -jar ${DACAPO9} -s $sz -n $nitr $app
	mv ./TimeLog /home/sch/result/${run}/${app}_TimeLog${i}
        #mv ./Monitor ${DATA}/result/${run}/normal/${app}_Monitor
        echo "${app} finish"

#	echo "dropcache test starting"
#	java -Xmx16384m -jar ${DACAPO_HPC_DROP} -s $sz -n $nitr $app 1>Monitor 2>TimeLog
#       mv ./TimeLog ${DATA}/result/${run}/dropcache/${app}_TimeLog${i}
	#mv ./Monitor ${DATA}/result/${run}/dropcache/${app}_Monitor
#	echo "dropcache test finish"
    done

done

