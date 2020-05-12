bench1=1112MultiInvoc
mkdir -p ./data/${bench1}/

for size in default
do
    for app in fop
#   for app in batik
    do
        for i in `seq 1 1000` 
        do
            echo ${i} >> ./data/${bench1}/${app}_${size}_150
            java -jar ./dacapo-9.12-bach.jar -s ${size} -n 150 ${app} 2>> ./data/${bench1}/${app}_${size}_150
        done
    done
done
for size in default
do
#   for app in luindex lusearch xalan avrora h2 
    for app in h2
    do
        for i in `seq 1 1000` 
        do
            echo ${i} >> ./data/${bench1}/${app}_${size}_50
            java -jar ./dacapo-9.12-bach.jar -s ${size} -n 50 ${app} 2>> ./data/${bench1}/${app}_${size}_50
        done
    done
done
