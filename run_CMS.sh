bench1=1804012CMSMultiFromNode22
Dacapo=//home/jxf/dacapo-9.12-bach.jar
mkdir -p /home/jxf/data/${bench1}/

#iterCMS=(100 100 50 50 100 120 100 100 50 120 80 80)
#iterPar=(200 100 50 100 100 50 150 50 100)
iterNewPar=(150 100 60 50 150 100 150 100 50 120 60 60)
#iterSerial=(50 150 150 100 100 100 200 150 50 100)
apps=(fop pmd sunflow luindex lusearch jython batik avrora xalan tradebeans tradesoap h2)
for ((i=170; i<200;i++))
do
echo $i
for size in default
do
    echo ${apps[j]}
    for ((j=0;j<${#apps[@]};j++))
    do
        java -XX:+UseParNewGC -jar ${Dacapo} -s ${size} -n ${iterNewPar[j]} ${apps[j]} 1>/home/jxf/data/${bench1}/${apps[j]}_${size}_NewPar${i} 2>&1
    done
done
done
