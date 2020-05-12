bench1=180423NoFullGCDefaultNode22
#Dacapo="dacapo-20171210.jar"
Dacapo="dacapo-NormalGC.jar"
mkdir -p ./data/${bench1}/

for size in default
do
    for i in `seq 1 1`
    do
        for app in fop pmd sunflow luindex lusearch jython batik avrora xalan tradebeans tradesoap h2
        do
#           echo ${i} >> ./data/${bench1}/${app}_${size}_150
            java -XX:+PrintGCDetails -jar ./${Dacapo} -s ${size} -n 300 ${app} &> ./data/${bench1}/${app}_${size}
#           java -XX:+PrintGCDetails -XX:+UseSerialGC -jar ./${Dacapo} -s ${size} -n 300 ${app} &> ./data/${bench1}/${app}_${size}_Serial
#           java -XX:+PrintGCDetails -XX:+UseParNewGC -jar ./${Dacapo} -s ${size} -n 300 ${app} &> ./data/${bench1}/${app}_${size}_NewPar
#           java -XX:+PrintGCDetails -XX:+UseParallelGC -jar ./${Dacapo} -s ${size} -n 300 ${app} &> ./data/${bench1}/${app}_${size}_Par
#           java -XX:+PrintGCDetails -XX:+UseConcMarkSweepGC -jar ./${Dacapo} -s ${size} -n 300 ${app} &> ./data/${bench1}/${app}_${size}_CMS
        done
    done
done
