import os
import subprocess
from common_module.in_out import OutputModule

class BlackDomain(OutputModule):

    def __init__(self, data_list):
        super().__init__(data_list)
        self.data_set = []
        self.domain_set_ns = []
        self.domain = ""
        self.ipv4_set = []
        self.ipv6_set = []

    def ns_lookup(self):
        for domain in self.data:
            command = "nslookup " + domain
            sysMsg = subprocess.getstatusoutput(command)
            self.data_set = sysMsg[1]
            self.data_set = self.data_set.replace("    ", " ")
            self.data_set = self.data_set.replace("  ", " ")
            self.data_set = self.data_set.replace("\n", " ")
            self.data_set = self.data_set.replace("\t", " ")
            self.data_set = self.data_set.split(" ")
            self.data_set = [v for v in self.data_set if v]

    def slicing_domain(self):
        idx = 0
        for i in range(len(self.data_set)):
            if self.data_set[i] == "이름:":  # 이름값 담기
                idx = i
                break
        idx += 1
        length = len(self.data_set)
        self.domain = self.data_set[idx]  # 이름변수 담기

        for i in range(idx + 2, length):  # ip담기 (ipv4, ipv6구분)
            if self.data_set[i] == 'Alias:' or self.data_set[i] == 'Aliases:': break
            if '.' not in self.data_set[i]:
                self.ipv6_set.append(self.data_set[i])
            else:
                self.ipv4_set.append(self.data_set[i])
        self.ipv4_set = ",".join(self.ipv4_set)  # 문자열로 변환
        self.ipv6_set = ",".join(self.ipv6_set)
        print(self.ipv6_set)
        print(self.ipv4_set)

    def make_report_domain(self, dir, fname):
        with open(f"{dir}/{fname}_{self.date}.csv", 'w', encoding='utf-8-sig') as f:
            f.write("ZONE,도메인 객체 이름,도메인 네임,IPv4,IPv6,설명\n")  # 맨위에 목록 작성
            f.write(f"E,{self.domain}_공격차단")
            f.write(f',{self.domain},"{self.ipv4_set}",{self.ipv6_set},{self.date2}_악성메일유포차단\n')
