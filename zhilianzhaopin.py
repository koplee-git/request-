import requests
import json
from urllib.parse import urlencode
from pyquery import PyQuery as pq
def start_url(jl, kw, num):
    base_url = "http://sou.zhaopin.com/jobs/searchresult.ashx?"
    query_url=urlencode({"jl":jl,"kw":kw,"p":num,"isadv":0})
    url = base_url + query_url
    urllst.append(url)
    return url
def get_next_index(url):
    response=requests.get(url)
    if response.status_code==200:
        html=response.text
        doc=pq(html)
        result=doc.find('.pagesDown')
        if result :
            url=result('.pagesDown-pos a').attr('href')
            if url:
                urllst.append(url)
                return get_next_index(url)
def pares_index(url): 
    response=requests.get(url)
    if response.status_code==200:
        html=response.text
        doc=pq(html)
        for item in doc('.newlist .zwmc a').items():
            yield item.attr('href')
def get_detail(url):
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        doc=pq(response.text)
        yield {
                    'job_salary':doc('.terminal-ul.clearfix li').eq(0)('strong').text(),
                    'job_station':doc('.terminal-ul.clearfix li').eq(1)('strong').text(),
                    'job_status':doc('.terminal-ul.clearfix li').eq(2)('strong').text(),
                    'job_experence':doc('.terminal-ul.clearfix li').eq(4)('strong').text(),
                    'job_degree':doc('.terminal-ul.clearfix li').eq(5)('strong').text(),
                    'job_name': doc('.inner-left h1').text(),
                    'job_company':doc('.inner-left h2').text(),
                    'job_description':doc('.tab-inner-cont').eq(0)('p').text(),
                    'company_description':doc('.tab-inner-cont').eq(1).text(),
                    'company_logo':doc('.img-border img').attr("src")
                    }
def write_json(item, name):
    with open(name+'.json','a',encoding='utf-8') as f:
        js=json.dumps(item,ensure_ascii=False)
        f.write(js)
        
def main(kw):
    jl="淄博"
    num=1
    i =0
    lst=[]
    url = start_url(jl,kw,num)
    print(url)
    get_next_index(url)
    for url in urllst:
        for url in pares_index(url):
            for item in get_detail(url):
                lst.append(item)
                i +=1
    print(lst[1])
    print(len(lst))
    write_json(lst,kw)
    print(kw,"相关工作岗位:",i)
if __name__ == "__main__":
    for kw in ['python','java','php','前端','android']:
        urllst=[]
        main(kw)
