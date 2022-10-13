import re  # 导包
import time
dic = []  # 创建字典列表


def init():

    with open(r"D:\Python\Python code\homework\chineseDic.txt", encoding="gbk") as dic_input:
        for word in dic_input:
            word=re.sub('([^\u4e00-\u9fa5])','',word)  # 只留下汉字
            dic.append(word.strip())


# 正向最大匹配算法
def FMM(raw_sentence, word_dic):
    # 统计词典中最长的词
    max_length = max(len(word) for word in dic)
    sentence = raw_sentence.strip()   # 移除字符串内的空格
    # 统计序列长度
    words_length = len(sentence)
    # 存储切分好的词语
    cut_word = []
    while words_length > 0:
        max_cut_length = min(max_length, words_length)
        # 创建待分序列
        sub = sentence[0 : max_cut_length]
        # 进行一轮分词，在左侧切出一个词
        while max_cut_length > 0:
            if sub in dic:  # 若待切分的词在词典中，则将其加入已分列表，跳出循环
                cut_word.append(sub)
                break
            elif max_cut_length == 1:   # 剩下单个字,将其切分，并跳出循环
                cut_word.append(sub)
                break
            else:     # 都不符合则从右侧去掉一个词，重新分词
                max_cut_length = max_cut_length - 1
                sub = sub[0 : max_cut_length]
        # 将切掉的单词删去
        sentence = sentence[max_cut_length:]
        words_length = words_length - max_cut_length
    words = "/".join(cut_word)
    return words


# 反向最大匹配算法
def RMM(raw_sentence, word_dic):
    # 统计词典种最长的词
    max_length = max(len(word) for word in dic)
    sentence = raw_sentence.strip()   # 移除字符串内的空格
    # 统计序列长度
    words_length = len(sentence)
    # 存储切分好的词语
    cut_word = []
    while words_length > 0:
        max_cut_length = min(max_length, words_length)
        # 创建待分序列
        sub = sentence[words_length-max_cut_length : words_length]
        # 进行一轮分词，在右侧切出一个词
        while max_cut_length > 0:
            if sub in dic:  # 若待切分的词在词典中，则将其加入已分列表，跳出循环
                cut_word.append(sub[::-1])
                break
            elif max_cut_length == 1:   # 剩下单个字,将其切分，并跳出循环
                cut_word.append(sub)
                break
            else:     # 都不符合则从左侧去掉一个词，重新分词
                max_cut_length = max_cut_length - 1
                sub = sub[1:]
        # 将切掉的单词删去
        sentence = sentence[0:words_length - max_cut_length]
        words_length = words_length - max_cut_length
    words = "/".join(cut_word)
    return words[::-1]


# 双向最大匹配算法
def BMM(raw_sentence, word_dic):
    bmm_word_list = FMM(raw_sentence, word_dic)
    fmm_word_list = RMM(raw_sentence, word_dic)
    bmm_size = len(bmm_word_list)
    fmm_size = len(fmm_word_list)

    # 分词结果数不同
    if bmm_size != fmm_size:
        if bmm_size < fmm_size:
            return bmm_word_list
        else:
            return fmm_size
    else:
        Fsingle = 0
        Bsingle = 0
        isSame = True
        for i in range(bmm_size):
            # 分词结果不同
            if bmm_word_list[i] != fmm_word_list[i]:
                isSame = False
            # 统计单个词的数量
            if len(bmm_word_list[i]) == 1:
                Bsingle += 1
            if len(fmm_word_list[i]) == 1:
                Fsingle += 1
        if isSame == True:
            return bmm_word_list
        # 分词结果不同选词数少的一个
        else:
            if Fsingle >= Bsingle:
                return bmm_word_list
            else:
                return fmm_word_list


def main():

    init()
    while True:  # 无限输入进行测试
        print("请输入您要分词的序列：")
        input_str = input()
        if not input_str:
            break
        start1 = time.time()
        result1 = FMM(input_str, dic)  # 正向分词结果
        end1 = time.time()
        start2 = time.time()
        result2 = RMM(input_str, dic)  # 反向分词结果
        end2 = time.time()
        start3 = time.time()
        result3 = BMM(input_str, dic)  # 双向分词结果
        end3 = time.time()
        print("正向分词结果：")
        print(result1)
        print("正向分词所需时间为：")
        print(end1 - start1)
        print("反向分词结果：")
        print(result2)
        print("反向分词所需时间为：")
        print(end2 - start2)
        print("双向分词结果：")
        print(result3)
        print("双向分词所需时间为：")
        print(end3 - start3)


if __name__ == '__main__':
    main()
