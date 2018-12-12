
import requests
from bs4 import BeautifulSoup,element

def get_daili():

    url_list = [
        'https://www.xicidaili.com/nt/1',
        'https://www.xicidaili.com/nt/2',
        'https://www.xicidaili.com/nn/1',
        'https://www.xicidaili.com/nn/2',
        'https://www.xicidaili.com/nn/3',
        'https://www.xicidaili.com/nn/4',
                ]

    # url = 'https://www.xicidaili.com/wt/'
    ip_list = []
    for url in url_list:
        list = _get_daili_by_url(url)
        ip_list = ip_list + list
    return ip_list



def _get_daili_by_url(url):
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection': 'Keep-Alive',
               'Host': 'zhannei.baidu.com',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    resp = requests.get(url, headers=headers)
    # print resp.content
    bs = BeautifulSoup(resp.content, 'html.parser')
    ip_list_table = bs.find('table', id='ip_list')
    header_row = ip_list_table.tr
    ip_list = []
    print header_row
    for ip_row in header_row.next_siblings:
        if ip_row is not None and isinstance(ip_row, element.Tag):
            # print ip_row,type(ip_row)
            tds = ip_row.find_all('td')
            ip_list.append({
                'ip': tds[1].get_text(),
                'port': tds[2].get_text()
            })
    return ip_list


if __name__ == '__main__':
    print get_daili()