from common_module.in_out import OutputModule

class BlackIP(OutputModule):

    def __init__(self, data_list):
        self.data = data_list
        super(OutputModule, self).__init__()

    def make_report_ip(self, dir, fname):
        with open(f"{dir}/{fname}_{self.date}.csv", 'w', encoding='utf-8-sig') as f:
            f.write("출발지 주소,출발지 포트,목적지 주소,목적지 포트,프로토콜,설명\n")  # 맨위에 목록 작성
            for i in self.data:  # 데이터 줄마다 작성하기
                f.write(i)
                f.write(",ANY,ANY,ANY,ANY")
                f.write(f",EXT_Attack_{self.date}_{i}\n")
            for i in self.data:  # 데이터 줄마다 작성하기
                f.write("ANY,ANY")
                f.write(f",{i},ANY,ANY")
                f.write(f",EXT_Attack_{self.date}_{i}\n")