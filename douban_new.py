import requests
from bs4 import BeautifulSoup
import re
number = 1
def getHtmlText(url):
    try:
        r =requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        print("Error")
        return ''

def avg(html,num):

    soup = BeautifulSoup(html,'html.parser')
    #初始化
    sum = 0
    global number
    str1 = ""
    user = []
    comment = []
    score = []

    #用这样的方式会导致用户名和评论或者分数对应不上
    #user = soup.find_all('span', 'comment-info')
    #comment = soup.find_all('p', 'comment-content')
    #pattern_s = re.compile('allstar(\d+)')  
    #p = re.findall(pattern_s, html)
    #print(len(user),len(comment),len(p))
    #user_comment_score = zip(user[:num], p[:num], comment[:num])

    #改进
    #先找用户名、评论和评分的综合体
    all = soup.find_all('div','comment')
    #print(len(all))
    #定义规则
    pattern_s = re.compile('allstar(\d+)')
    
    for item in all[0:num]:#别忘了加入数量控制，如果少于一页中的数量

        #测试
        #a = item.find('span', 'comment-info')
        #print(a.a.string)

        #用户名和评论
        user.append(item.find('span', 'comment-info').a.string)
        comment.append(item.find('p', 'comment-content').string)

        #print(item.find('span', 'comment-info').span['class'][1])
        #item.find('span', 'user-stars')['class'][1])可以替换上句，因为不用飞要找到span的父节点在span.span[][]，直接找儿子span 

        m = item.find('span', 'user-stars')  # user-stars是截取的是属性中的一部分，不用全部属性
        #可能存在不评分的情况
        if m != None:
            #print(m)
            score.append(''.join(re.findall(pattern_s, m['class'][1])))#使用join去掉[]
        else:
            score.append("0")
        #测试
        #print(len(score))
        #print(score)

    user_comment_score = zip(user, score, comment)

    #测试.join（string的方法）
    #user_comment = zip(user, comment)
    #for item in user_comment:
        #print(type(item[0].a.string))
        #nstring = item[0].a.string + item[1].string
        #str = str.join(nstring)
        #str = str.join('\n')
        #str = str +“第“ + str(number) + "位：”+ item[0].a.string + ':' + item[1].string + '\n'#一开始忘了.a了导致一直出现NonrTyp错误
        #number += 1
    
    #测试
    #for p_item in p[:num]:下面注释是错误的
        #下一行自己定义的变量不要是str，不然语句中又使用了系统内置str会导致str is not callable
        #str1 = str1 + "第" + str(number) + "位：" + user_comment_score[number][0].a.string + " " + "评分是：" + p_item + "评论是：" + user_comment_score[number][1].string + '\n'
    
    #保存到字符串
    for a,b,c in user_comment_score:
        sum += int(b)
        str1 = str1 + "第" + str(number) + "个是:" + a + " 评分是：" + b + " 评论是：" + c + '\n'
        number += 1
    #写入文件
    with open('./666你绝对没见过的文件夹名字.text', 'a+') as f:
        f.write(str1)
    return sum
    
def main():
    url = "https://book.douban.com/subject/1856285/comments"
    sum = 0
    print('请输入要抓取的短评的个数：')
    num = int(input())
    for i in range(num//20+1):
        html = getHtmlText(url)
        num_item = num - i*20
        print("第{}次后剩余{}".format(i,num_item))
        if num_item >= 20:
            sum += avg(html,20)
            url = url + '/hot?p=' + str(i+2)
        else:
            sum += avg(html,num%20)
            url = url + '/hot?p=' + str(i+2)
    if num%20: 
        print("第{}次后剩余0".format(num//20+1))
    print("总评分是：{}，平均评分是：{}".format(sum,sum/num))
    print("评论保存在了本路径下，文件名是：666你绝对没见过的文件夹名字.text")

main()


