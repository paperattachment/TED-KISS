准备Neu-IR的训练、测试文件
输入文件：
1 TED_xml 存放路径：1xml/ 
2 evalData.txt 问题-正确答案 文件；格式：query_id 0 answer_id 1
3 __AllQueriesMultiLine0131.xml 查询xml文件
4 4SeaResCombine.txt 基于no_description_speaker索引通过QL方法检索得到的：query_id-1000个answer_id文件
5 100_no_answer_queryids.txt galago检索结果的前100个答案中不包含正确答案的query_id

输出文件：
train：作为Neu-IR的train file
test1：作为Neu-IR的test file