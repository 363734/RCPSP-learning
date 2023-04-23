# helper to gather stats about a graph (helps avoiding recomputation)

from script.Instances.RCPSPinstance import RCPSP
from typing import List
import pandas

dict_stat_graph = {}


def get_stat(instance: RCPSP):
    if instance not in dict_stat_graph:
        dict_stat_graph[RCPSP] = RCPSPstats(instance)
    return dict_stat_graph[RCPSP]


def lazy_property(fn):
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property


class RCPSPstats:
    def __init__(self, instance: RCPSP):
        self.instance = instance  # RCPSP instance based on

    # usage_proportion[j][r] is the proportion of ressource r the job j is using
    @lazy_property
    def usage_proportion(self) -> List[List[float]]:
        return [[self.instance.usage[j][r] / self.instance.resource[r] for r in range(self.instance.nb_resources)]
                for j in range(self.instance.nb_jobs)]

    # usage_proportion_all[j] is the proportion of ressource the job j is using (e.g. 1 ressource among 4 available = 25%)
    @lazy_property
    def usage_proportion_all(self) -> List[float]:
        return [len([i for i in j if i > 0])/len(j) for j in self.usage_proportion]

    # create a dict with multiple features
    @lazy_property
    def features(self):
        features = {"job_id": [0] * self.instance.nb_jobs,
                    "precedent_percentage": [0.0] * self.instance.nb_jobs,
                    "successor_percentage": [0.0] * self.instance.nb_jobs,
                    "prec_and_succ_percentage": [0.0] * self.instance.nb_jobs,
                    "critical_path": [0.0] * self.instance.nb_jobs,
                    "usage_max": [0.0] * self.instance.nb_jobs,
                    "resource_used": [0.0] * self.instance.nb_jobs,
                    "energy": [0.0] * self.instance.nb_jobs}
        for i in range(self.instance.nb_jobs):
            features["job_id"][i] = i + 1
            features["precedent_percentage"][i] = len(self.instance.all_prec[i])
            features["precedent_percentage"][i] /= (self.instance.nb_jobs - 1)
            features["successor_percentage"][i] = len(self.instance.all_succ[i])
            features["successor_percentage"][i] /= (self.instance.nb_jobs - 1)
            features["prec_and_succ_percentage"][i] = features["precedent_percentage"][i] + \
                                                      features["successor_percentage"][i]
            features["usage_max"][i] = max(self.usage_proportion[i])
            features["resource_used"][i] = len(
                [i for i in self.instance.usage[i] if i != 0]) * 1.0 / self.instance.nb_resources
            features["energy"][i] = sum(self.instance.usage[i])
            features["energy"][i] *= self.instance.duration[i]
            features["energy"][i] /= self.mean_energy
        return features

    # use of pandas to summarize the features
    def summarize_features(self):
        features = self.features
        df = pandas.DataFrame(data=features)
        with pandas.option_context('display.max_columns', 40):
            print(str(df.describe(include='all')))

    # energy_per_resource_per_job[j][r] is the energy (duration times usage of ressource) of resource r for job j
    @lazy_property
    def energy_per_resource_per_job(self):
        return [[self.instance.usage[i][j] * self.instance.duration[i] for j in range(self.instance.nb_resources)] for i
                in range(self.instance.nb_jobs)]

    # energy_per_job[j] is the sum of the energies for each resource for a given job j
    @lazy_property
    def energy_per_job(self):
        return [sum(self.energy_per_resource_per_job[i]) for i in range(self.instance.nb_jobs)]

    # energy_per_resource[r] is the sum of the energies for each job for a given resource r
    @lazy_property
    def energy_per_resource(self):
        return [sum([self.energy_per_resource_per_job[i][r] for i in range(self.instance.nb_jobs)]) for r in
                range(self.instance.nb_resources)]

    # total energy of the instance
    @lazy_property
    def total_energy(self):
        return sum(self.energy_per_job)

    @lazy_property
    def mean_energy(self):
        return self.total_energy / self.instance.nb_jobs
