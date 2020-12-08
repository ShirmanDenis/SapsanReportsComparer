import requests as client
import matplotlib.pyplot as plt
import matplotlib.dates as md
import json
from datetime import datetime
from matplotlib.pyplot import Axes
from enum import Enum
class Mode(Enum):
    File = 1
    Api = 2
class Session_type(Enum):
    YandexTank = 1
    Sapsan = 2
class SapsanResult:
    def __init__(self, session, session_type: Session_type, mode: Mode = Mode.Api):
        self.__sapsan_api_url = "https://sapsan.skbkontur.ru/api"
        self.json = []
        if (mode == Mode.Api):
            self.json = self.__download(session)
        else:
            self.json = self.__readJson(session)
        self.type = session_type

    def __readJson(self, filepath):
        with open(filepath) as file:
            return json.load(file)

    def __download(self, session):
        json_response = client.get(self.__sapsan_api_url + "/session/report/" + session).json()
        return json_response

    def __get_session_type(self, session):
        json_response = client.get(self.__sapsan_api_url + "/session/" + session).json()
        return json_response["Type"]

    def __extract_graphs(self, dashboardName: str, chartName: str, system: bool = False):
        graphs = []
        main_view = (self.json["View"], self.json["View"]["Metrics"])[system]
        for chart in main_view[dashboardName]:
            if (chart["Name"] == chartName):
                for graph in chart["Graphs"]:
                    points = [point["Data"] for point in graph["Points"]]
                    x = [datetime.utcfromtimestamp(point["Timestamp"] / 1000) for point in graph["Points"]]
                    name = graph["Name"]
                    graphs.append((name, x, points))
                break
        return graphs

    def get_http_codes(self):
        return self.__extract_graphs("Charts", ("HTTP Codes","HTTP Codes over time")[self.type == 1])
    def get_avg_latency(self):
        return self.__extract_graphs("Charts", ("Average Latency, ms","Average response time")[self.type == 1])
    def get_percentiles(self):
        # sapsan sessions have separate chart for each operation :(
        return self.__extract_graphs("Charts", ("Percentiles over time"))
    def get_agents_cpu_usage(self):
        if self.type == 1:
            raise Exception("Not supported for YT session type.")
        return self.__extract_graphs("AgentsSysMetrics", "Agent CPU usage", True)
    def get_agents_memory_usage(self):
        if self.type == 1:
            raise Exception("Not supported for YT session type.")
        return self.__extract_graphs("AgentsSysMetrics", "Agent Memory", True)

def __plot_points(graphs, plt: Axes):
    formatter = md.DateFormatter("%H:%M:%S")
    plt.xaxis.set_major_formatter(formatter)
    for name, x, y in graphs:
        plt.plot(x, y, label=name)
    plt.legend()

def draw(s1: SapsanResult, s2: SapsanResult):
    if (s1.type != s2.type):
        raise Exception("Must be equal types.")
    _, axs = plt.subplots(3, 2)
    codes_1 = s1.get_http_codes()
    codes_2 = s2.get_http_codes()
    lat_1 = s1.get_avg_latency()
    lat_2 = s2.get_avg_latency()
    # drawing
    __plot_points(codes_1, axs[0, 0])
    __plot_points(codes_2, axs[0, 1])
    __plot_points(lat_1, axs[1, 0])
    __plot_points(lat_2, axs[1, 1])
    if (s1.type == 1):
        quantiles_1 = s1.get_percentiles()
        quantiles_2 = s2.get_percentiles()
        __plot_points(quantiles_1, axs[2, 0])
        __plot_points(quantiles_2, axs[2, 1])
    else:
        agent_cpu1 = s1.get_agents_cpu_usage()
        agent_cpu2 = s2.get_agents_cpu_usage()
        __plot_points(agent_cpu1, axs[2, 0])
        __plot_points(agent_cpu2, axs[2, 1])
    plt.show()