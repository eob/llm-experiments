import json
from typing import List
import pathlib
from llm_experiments.clustering.cluster_selection_prompt import PROMPT, EMPTY, SPLIT
from llm_experiments.llm import generate 


class ClusterParams:    
    ideal_cluster_size: int
    cluster_description: str

    def __init__(self, cluster_description, ideal_cluster_size: int):
        self.cluster_description = cluster_description
        self.ideal_cluster_size = ideal_cluster_size


class Item:
    data: any

    def __init__(self, data: any):
        self.data = data

    def llm_description(self) -> str:
        return f"{self.data}"
    
    def __str__(self):
        return f"{self.data}"
    
    def __repr__(self):
        return f"{self.data}"


class Cluster:
    name: str
    items: List[Item]

    def __init__(self, name: str):
        self.name = name
        self.items = []

    def llm_description(self) -> str:
        return f"{self.name}"

    def add(self, item: Item):
        self.items.append(item)

    def __str__(self):
        return f"{self.name}: {len(self.items)}"
    
    def __repr__(self):
        return f"{self.name}: {len(self.items)}"
    
    def split(self, cluster_description: str) -> List["Cluster"]:
        prompt = SPLIT.format(cluster_name=self.name, items="\n".join([f"- {i}" for i in self.items]), cluster_description=cluster_description)
        response = generate(
            prompt=prompt,
            json_response=True,
            cache=True
        ).strip()
        
        new_clusters = []
        for j in json.loads(response):
            if name := j.get("name", j.get("new")):
                new_cluster = Cluster(name)
                new_clusters.append(new_cluster)

        return new_clusters


class RebalancingClusterer:
    cluster_params: ClusterParams
    clusters: List[Cluster]

    def __init__(self, cluster_params: ClusterParams):
        self.cluster_params = cluster_params
        self.clusters = []

    def assign_clusters(self, item: Item) -> str:
        available_clusters = "\n".join([f"- {c.llm_description()}" for c in self.clusters])
        prompt = PROMPT.format(cluster_description=self.cluster_params.cluster_description, clusters=available_clusters, item=item.llm_description()) if len(self.clusters) > 0 else EMPTY.format(cluster_description=self.cluster_params.cluster_description, item=item.llm_description())
        response = generate(
            prompt=prompt,
            json_response=True,
            cache=True
        ).strip()
        print(response)
        j = json.loads(response)
        name = j.get("name", j.get("new"))
        return name        

    def add(self, item: Item):
        cluster = self.assign_clusters(item)
        for c in self.clusters:
            if c.name == cluster:
                c.add(item)
                # Sort the clusters by size
                self.clusters.sort(key=lambda c: len(c.items), reverse=True)
                return
          
        # The LLM proposed a new cluster; add it to our list.
        new_cluster = Cluster(cluster)
        new_cluster.add(item)
        self.clusters.append(new_cluster)

        # Sort the clusters by size
        self.clusters.sort(key=lambda c: len(c.items), reverse=True)

    def possibly_rebalance(self):
        return
    
    def __str__(self):
        # Print a bullet list of each cluster, with count, in decreasing order of size
        return "\n".join([f"{c}" for c in self.clusters])

    def __repr__(self):
        return self.__str__()


def main():
    # Get the filesystem path of this python file
    print()

    # Open the file dataset_1.txt in the same folder as this file and read in each line.
    dataset = pathlib.Path(__file__).parent.resolve() / "dataset_1.txt"

    with open(dataset) as f:
        lines = f.readlines()
        items = [Item(line.strip()) for line in lines]

    # Create a new RebalancingClusterer with an ideal cluster size of 10.
    params = ClusterParams("College Majors", 10)
    clusterer = RebalancingClusterer(params)

    for item in items:
        clusterer.add(item)
    
    print(clusterer)


if __name__ == "__main__":
    main()

