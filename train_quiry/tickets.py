
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

    
    
