from common_module.in_out import OutputModule

class BlackNetwork(OutputModule):

    def __init__(self, data_list):
        self.data = data_list
        self.data_slice = []
        super(OutputModule, self).__init__()

    def slicing_net(self):
        for i in self.data:
            cnt = 0
            # data[i] = 111.111/24
            for j in i:
                cnt += 1
                if j =="/":
                    break
            self.data_slice.append([i[:cnt-1], i[cnt:]])

    def make_report_network(self, dir, fname):
        with open(f"{dir}/{fname}_{self.date}.csv", 'w', encoding='utf-8-sig') as f:
            f.write("ZONE,네트워크 이름,IP,설명\n")  # 맨위에 목록 작성
            for i in self.data_slice:  # 데이터 줄마다 작성하기
                f.write(f"E,EXT_Attack_{self.date}_{i[0]}_{i[1]}")
                f.write(f",{i[0]}/{i[1]},EXT_Attack_{self.date}_{i[0]}_{i[1]}\n")