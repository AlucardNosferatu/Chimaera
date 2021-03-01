# Chimaera
GNN+KG+Datalog+LISP=Junk

# Blather
## Python：
胶水语言，业务逻辑实现层，可读可维护，没啥好说的

## Py2Neo：
用来访问Neo4J数据库的接口，通过这玩意获取三元组和图结构数据

## TensorFlow：
炼丹，用GCN或其它GNN来做实体分类（Entities Classification）和关系预测（Links Prediction），没啥好说的

## Pengines：
连接SWI-Prolog，利用基于Prolog实现的推理引擎进行推理和回溯

由于坑爹的Prolog大小写不同有语法上的歧义，因此所有字符串从KG中获取后都需要进行小写化

反过来KG中出现的字符串也必须均为大写或小写或任意一种可依照固定程序从小写字符串转换过来的形式

## Hy（或者其它LISP方言接口）：
LISP方言编写工具类，在Hy堆栈上动态更新自身运行逻辑实现元编程（Meta-Programming）
