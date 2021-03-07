# Chimaera
KG+NLP+LISP+Prolog+ANN+Hook=Junk

## 模块1. Py2Neo & Neo4J：
用知识图谱（KG）存储有限状态机（FSM）

用节点存储状态标志符号（SFS），用关系存储状态转移函数符号（STFS）

在此基础上利用一系列工具操作、解析节点-关系信息

## 模块2. NLTK
用于使用自然语言命令行进行交互，创建和删除SFS、STFS，仅支持英文

对简化的自然语言进行词性标注，提取文本中由SFS-STFS-SFS构成的三元组（Triplet）

关系动词的时态会在这个阶段强制转换为第三人称单数，对应KG接口的STFS参数字符串也应为第三人称单数的动词

人称代词的时态会强制转为主格，对应CYPHER中变量的代词代换规则

## 模块3. Hy：
从以KG中获取已存在的SFS、STFS，并将其DAG子图解析为广义表（GList），限制DAG图是为了避免存在回路形成递归

得到GList后，用Hy编写状态标志程序（SFP）、状态转移函数程序（STFP），嵌入到GList当中作为实际运行程序

利用Hy的宏（defmacro）动态更新SFP、STFP实现元编程

## 模块4. Pengines & SWI-Prolog：
连接SWI-Prolog，利用基于Prolog实现的推理引擎对SFS-STFS进行推理（STFS查找与填补）

由于Prolog对大小写敏感，因此所有STFS从KG中获取后都需要进行小写化，而SFS都只采用数字id而非名称字符串

反过来这也要求KG中出现的STFS也必须均为可用固定程序从小写字符串转换过来的形式

## 模块5. TensorFlow & Numpy：
利用ANN进行SFS分类和STFS预测（非一阶逻辑可推导的情形，不适用于Prolog推理引擎）

将Triplet转化为有向图的邻接矩阵作为ANN的输入和标签，对模型进行训练，得到可实现上述目的的ANN的权重数据

## 模块6. Ctypes & Win32API
用于与其它内存空间中的进程交互，获取函数指针或是数据，以嵌入到SFP、STFP当中

1.调用kernel32.dll，使用其开放的API读写进程中指定内存数据：

查找进程->确定进程主模块->

根据主模块信息确定内存地址区间->

内存区间内搜索与匹配->改写&监听变量

2.对指定函数进行代理（Hook），读写入参和返回值：

查找进程->确定需要代理的模块->

根据模块路径找到dll->用dumpbin获取函数名->

根据函数名找到函数地址->查找进程内存中指向此地址的数据->

替换为含有原函数调用语句的代理函数

## 名词解释：
KG（Knowledge Graph）：

包含有状态机的状态标志和状态转移函数的图数据库

SF（State Flags）：

图数据库中的一个节点，对应状态机中的一个状态标志，含有一个数据库唯一标识id、分类标签及SFS

STF（State Transition Functions）：

图数据库中的一个关系，对应状态机中的一个状态转移函数，含有其起始SF的id、终点SF的id及STFS

SFS（State Flags Symbols）：

为了方便在其它工具中处理SF，用一个图中唯一的名称字符串来表示SF

STFS（State Transition Functions Symbols)：

为了方便在其它工具中处理STF，用一个仅含大写英文+下划线构成的第三人称单数动词短语字符串来表示STF

SFP（State Flags Programs）：

SF在Hy脚本当中所对应的程序（方法集合），每个SF对应的SFP有相同的方法签名，但实现和运行逻辑均有不同

STFP（State Transition Functions Programs）：

STF在Hy脚本当中所对应的程序（方法集合），每个STF对应的STFP有相同的方法签名，但实现和运行逻辑均有不同）