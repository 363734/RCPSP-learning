# Representation of an RCPSP instance

from typing import List
import pickle

from script.Instances.PrecedenceGraph import Graph


def load_rcpsp(filename: str):
    with open(filename, 'rb') as file:
        instance = pickle.load(file)
        return instance


def save_rcpsp(filename: str, instance):
    with open(filename, "wb") as file:
        pickle.dump(instance, file, pickle.HIGHEST_PROTOCOL)


class RCPSP:
    def __init__(self, nb_jobs: int, successors: List[List[int]], duration: List[int], usage: List[List[int]],
                 resource: List[int]):
        self.nb_jobs: int = nb_jobs  # nb of tasks to plan (with dummy task included)
        self.successors: List[List[int]] = successors  # for each task, list of tasks executed after it
        self.duration: List[int] = duration  # for each task, time for the tasks
        self.usage: List[List[int]] = usage  # for each task, for each resource, usage of the resource by the task
        self.resource: List[int] = resource  # for each resource, max capacity
        self.nb_resources = len(resource)  # nb of available resource

        self.graph = Graph()  # precedence graph
        for j in range(self.nb_jobs):
            self.graph.add_node(j, self.duration[j])
        for j in range(self.nb_jobs):
            for s in self.successors[j]:
                self.graph.add(j, s)

        self.all_succ = [self.graph.get(i).idxs_s_all for i in range(self.nb_jobs)]
        self.all_prec = [self.graph.get(i).idxs_p_all for i in range(self.nb_jobs)]
        self.earliest_latest_time = [(self.graph.get(i).earliest_time, self.graph.get(i).latest_time) for i in
                                     range(self.nb_jobs)]

        self.min_horizon = self.earliest_latest_time[0][1]  # smallest horizon allowed by the data (LB)

    def __str__(self):
        strg = "nbJobs {}\n".format(self.nb_jobs)
        strg += "ressources : \n"
        for i in range(len(self.resource)):
            strg += "   R {} : {}\n".format(i + 1, self.resource[i])
        strg += "tasks : \n"
        for i in range(self.nb_jobs):
            strg += "   J {} : \n".format(i + 1)
            strg += "      duration : {}\n".format(self.duration[i])
            strg += "      usage    : {}\n".format(self.usage[i])
            strg += "      succ     : {}\n".format(self.successors[i])
        return strg
