import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import ssl


def get_request_url(url, enc='utf-8'):
    req = urllib.request.Request(url)

    try:
        ssl._create_default_https_context = ssl._create_unverified_context

        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')

            return ret

    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


def CheogajipAddress(result):
    for page_idx in range(0, 125):  # 마지막 페이지까지
        Cheogajip_URL = (
            'http://www.cheogajip.co.kr/bbs/board.php?bo_table=store&page=%s' % str(page_idx + 1)
        )
        print(Cheogajip_URL)

        response = urllib.request.urlopen(Cheogajip_URL)
        soupData = BeautifulSoup(response, 'html.parser')
        tbody_tag = soupData.find('tbody')

        for store_tr in tbody_tag.find_all('tr'):
            tr_tag = list(store_tr.strings)
            store_name = tr_tag[1]
            store_address = tr_tag[3]
            store_sido_gu = store_address.split()[:2]
            store_phone = tr_tag[5]
            result.append([store_name] + store_sido_gu + [store_address, store_phone])

def cswin_Cheogajip():
    result = []

    print('CHEOGAJIP ADDRESS CRAWLING START')
    CheogajipAddress(result)
    cheogajip_table = pd.DataFrame(
        result,
        columns=('store', 'sido', 'gungu', 'store_address', 'store_phone'),
    )
    cheogajip_table.to_csv('./cheogajip.csv', encoding='cp949', mode='w', index=True)
    del result[:]

    print('FINISHED')


if __name__ == '__main__':
    cswin_Cheogajip()


