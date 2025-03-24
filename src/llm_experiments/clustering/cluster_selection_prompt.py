PROMPT = """You are powering an API making clustering decisions.

The type of cluster is: {cluster_description}

Here are the existing cluster names:

{clusters}

You have a new item to cluster:

- {item}

Respond with EITHER the JSON {{"name": "existing cluster name"}} to assign the item to an cluster, OR the JSON {{"new": "<name>"}} to create a new cluster named <name> if a good fit does not exist within the existing ones."""


EMPTY = """You are powering an API making clustering decisions.

The type of cluster is: {cluster_description}

No clusters exist yet. 

Please provide a suggested cluster name for the first item:

- {item}

Respond with the JSON {{"name": "new cluster name"}} to create this first cluster."""


SPLIT = """You are powering an API making clustering decisions.

The type of cluster is: {cluster_description}

Your job is to SPLIT the cluster {cluster_name} into two new cluster.

The items in cluster {cluster_name} are:

{items}

Respond with the JSON [{"new": "name1"}, {"new": "name2"}] to create two new clusters named name1 and name2."""