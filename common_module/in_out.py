import datetime

class InputModule():
    def __init__(self, inputdata):
        self.data = inputdata
        self.data_set = []
        self.input_data()

    def input_data(self):
        self.data=self.data.replace("\n","")
        self.data=self.data.replace(" ","")
        self.data_set = self.data.split(",")

class OutputModule():

    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d_%H%M%S")

    def __init__(self, data_list):
        self.data = data_list
