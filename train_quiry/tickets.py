

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
from docopt import docopt
from prettytable import PrettyTable
from stations import stations
from colorama import init, Fore
import requests
import urllib3
urllib3.disable_warnings()

# header = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Connection': 'keep-alive',
#     'Cookie':'JSESSIONID=A9AE0B383F8F1BB150A9E99FC5D3162A; fp_ver=4.5.1; RAIL_EXPIRATION=1504288742858; RAIL_DEVICEID=G3PBmT-QYa5wK7Zx6fpMLX9kBK6lk2FaP51yEk9hsx2ykyWKabef4SWyQ8rSY1EZqOPRkMIbNojHN-Lp1pn605Qi4p-iYzNVtPLHStTmUnxnb6eF-YAif5vdy6BXj7UWRh7ost6U6se9IgW-7q6gCH1Ay-D2iSMP; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2017-08-30; _jc_save_toDate=2017-08-30; _jc_save_wfdc_flag=dc; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=367526154.24610.0000',
#     'Host':'kyfw.12306.cn',
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
#                   '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
# }

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split()
    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表, 包含可获得的火车班次, 每个
                                 火车班次是一个字典
        :param options: 查询的选项, 如高铁, 动车, etc...
        """
        self.available_trains = available_trains
        self.options = options

    def _get_duration(self, traininfo_list):
        duration = traininfo_list[10].replace(':', '小时') + '分'
        if duration.startswith('00'):  #判断字符串duration以00开头
            return duration[4:]
        if duration.startswith('0'):
            return duration[1:]
        return duration

    @property
    def trains(self):
        for raw_train in self.available_trains:
            traininfo_list = raw_train.split('|')
            train_no = traininfo_list[3]
            initial = train_no[0].lower
            # if not self.options or initial in self.options:
            if not self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.GREEN + traininfo_list[4] + Fore.RESET,
                               Fore.RED + traininfo_list[5] + Fore.RESET]),
                    '\n'.join([Fore.GREEN + traininfo_list[8] + Fore.RESET,
                               Fore.RED + traininfo_list[9] + Fore.RESET]),
                    self._get_duration(traininfo_list),
                    traininfo_list[31],  #一等座
                    traininfo_list[30],  #二等座
                    traininfo_list[23],  #软卧
                    traininfo_list[28],  #硬卧
                    traininfo_list[29],  #硬座
                    traininfo_list[26],  #无座
                ]
                yield train

    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # 构建URL
    # url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(
    #     date, from_station, to_station
    # )
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station
    )
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    # 添加verify=False参数不验证证书
    r = requests.get(url, verify=False)
    # r.encoding = "gbk"
    available_trains = r.json()['data']['result']
    TrainsCollection(available_trains, options).pretty_print()



if __name__ == '__main__':
    cli()
