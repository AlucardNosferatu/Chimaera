# Chimaera
GNN+KG+Datalog+LISP=Junk

## 模块1. Hy（或者其它LISP方言接口）：
LISP方言编写工具类，在Hy堆栈上动态更新自身运行逻辑实现元编程（Meta-Programming）

## 模块2. Jieba
超经典分词库，用于对最基本的自然语言进行词性标注，提取文本中关系三元组：

我爱Carol：我-爱-Carol

代词（名词）A-动词B-代词（名）C：A-B-C

我是你的爸爸：我-是（爸爸）-你

代词（名词）A-“是”-代词（名词）B-“的”-名词C：A-是（C）-B

用于使用自然语言命令行进行交互

## 模块3. Py2Neo：
用来访问Neo4J数据库的接口，通过这玩意获取三元组和图结构数据

## 模块4. Pengines：
连接SWI-Prolog，利用基于Prolog实现的推理引擎进行推理和回溯

由于坑爹的Prolog大小写不同有语法上的歧义，因此所有关系字符串从KG中获取后都需要进行小写化，而节点都只采用id进行推理

反过来KG中出现的关系字符串也必须均为大写或小写或任意一种可依照固定程序从小写字符串转换过来的形式

## 模块5. TensorFlow：
炼丹，用GCN或其它GNN来做实体分类（Entities Classification）和关系预测（Links Prediction），没啥好说的

## 模块6. MetaHook
利用操作系统的钩子或网络连接分析器获取数据