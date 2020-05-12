介绍
FastJEva，这种框架不仅能够更加可信地划分一个JVM生命周期中的起始状态和稳定状态，更能够处理Java程序的不确定性问题，快速地进行程序性能评估。首先，FastJEva收集了多种JVM运行时的特征，并且通过齐性检验和线性拟合，对JVM生命周期中程序的起始状态和稳定状态进行了更可信的划分。其次， 为了提高性能评估的效率，FastJEva采用了一种基于bootstrap的抽样方法，稳定的区块Bootstrap（Stationary Block Bootstrap，SBB）帮助进行性能评估。该方可以在存在相关性的运行结果上进行重抽样，构建样本总体的近似分布，并基于这个样本空间来进行性能评估。这种方法可以被用于存在前后相关性的序列中的数据评估。根据实验结果，FastJEva可以将评估实验所需的程序运行次数从数千次降低到几十次，减少了64.42倍，并且得到的性能评估结果和通过之前的方法得出的结果相比偏差在随机误差范围内。
详细设计参考《A Framework for Efficient Evaluation of Parallel
Java Applications with Performance Variability》
2 软件包
整个包含了用来运行的脚本以及用来收集数据和进行性能评估的脚本，并附带了测试使用的数据。
名称	说明
run_multi.sh	用于运行多Invocation以及单Invocation的数据
run_CMS.sh	用于运行不同GC策略的数据
run_Tier1.sh	用于运行不同JIT策略的数据
run_printGC.sh	用于打印GC以及JIT的信息
PaperCV	用于计算变异系数
PaperACF.py	用于计算自相关系数
PaperDistribution.py	用于检验正态分布
PaperInfo.py	用于输出阶段判断信息并进行阶段判断
PaperSpeedUp.py	用于计算加速比
PaperInterval.py	用于计算置信区间
PaperCLT.py	用于计算满足CLT条件的Invocation数
Data	包含所有测试用的数据

2.各脚本说明
	run_multi.sh
该脚本用于运行单Invocation或者多Invocation的程序，每个Invocation会输出到不同的文件中。
	run_CMS.sh
该脚本用于运行不同的GC策略，现脚本下使用的是CMS策略，可以通过-XX：进行修改。
	run_Tier1.sh
该脚本用于运行不同的JIT策略，现脚本下使用的是TierOne策略，可以通过-XX：进行修改。
	run_printGC.sh
该脚本中可以执行四种GC策略并且打印出GC信息。此脚本使用的DaCapo与其他不同，需要使用软件包里带的dacapo-NormalGC.jar，取消Iteration间的Full GC。

	PaperACF.py
该文件读取180103Iter10kFromNode21 下的10k个Iteration大小的Invocation数据，并计算稳定状态下的ACF数据。
	PaperDistribution.py
	该文件分别读取单Invocation数据和多Invocation数据，分别画出数据分布图，检验正态分布性。图像输出在DATA_PREC+"/figure/distribution/ "下
	PaperInfo.py
	该文件分别读取GC信息和时间以及JIT信息，画图输出进行稳定状态判断时的时间，GC Freq，JIT Task， PCA和Fitting等并进行阶段判断。
	PaperCLT.py
	该文件读取数据，通过正态检验算法，判断CLT需要多少Invocation数据能够达到正态。
	PaperSpeedUp.py
该文件和PaperGCSpeedup.py以及PaperJITSpeedup.py一起都是用来计算加速比的脚本。该脚本分别计算了使用CLT方法和SBB检验下Node机器相对于205的加速比。同样，本脚本中也包含了测试不同大小origin sample的部分。
PaperGCSpeedup.py计算了默认方法相对于CMS的加速比，PaperJITSpeedup.py计算了默认相对于Tier1的加速比。
由于加速比是一点一点累加测试的，故而脚本中可以了手动设置初始值加快运行速度、
	PaperInterval.py
该文件读取数据，分别计算CLT方法和SBB方法下的置信区间。数值输出到屏幕上。

3 软件安装
运行上文中的脚本需要安装下列包：
Matplotlib 
statsmodels 
scipy 
numpy 
pandas
通过以下命令安装：	
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install -U statsmodels

之后直接Python + python脚本名即可使用。
