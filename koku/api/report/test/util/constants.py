#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
# AWS_INSTANCE_TYPES = ("db.t3.medium", "db.r5.2xlarge", "m5.large", "r4.large", "t2.micro", None)
# AWS_PRODUCT_CODES = ("AmazonRDS", "AmazonElastiCache", "AmazonS3", "AmazonVPC", "AmazonEC2")
# AWS_REGIONS = (
#     ("us-east-1", "us-east-1a"),
#     ("us-west-2", "us-west-2a"),
#     ("eu-west-1", "eu-west-1c"),
#     ("ap-southeast-2", "ap-southeast-2b"),
#     ("af-south-1", "af-south-1a"),
# )
AWS_REGIONS = ("us-east-1", "us-west-2", "eu-west-1", "ap-southeast-2", "af-south-1")
AWS_AVAILABILITY_ZONES = ("us-east-1a", "us-west-2a", "eu-west-1c", "ap-southeast-2b", "af-south-1a")
# Product Code, Product Family, Instances, Units
AWS_PRODUCT_CODES = ("AmazonRDS", "AmazonRDS", "AmazonS3", "AmazonVPC", "AmazonEC2", "AmazonEC2", "AmazonEC2")
AWS_PRODUCT_FAMILIES = (
    "Database Instance",
    "Database Instance",
    "Storage Snapshot",
    "Cloud Connectivity",
    "Compute Instance",
    "Compute Instance",
    "Compute Instance",
)
AWS_INSTANCE_TYPES = ("db.t3.medium", "db.r5.2xlarge", None, None, "m5.large", "r4.large", "t2.micro")
AWS_RESOURCE_COUNTS = (1, 1, 0, 0, 1, 1, 1)
AWS_INSTANCE_IDS = ("i-11111111", "i-22222222", None, None, "i-33333333", "i-44444444", "i-55555555")
AWS_UNITS = ("Hrs", "Hrs", "GB-Mo", "Hrs", "Hrs", "Hrs", "Hrs")
# AWS_SERVICES = (
#     (
#         "AmazonRDS",
#         "Database Instance",
#         {"type": "db.t3.medium", "id": "i-11111111"},
#         "Hrs",
#     ),
#     (
#         "AmazonRDS",
#         "Database Instance",
#         {"type": "db.r5.2xlarge", "id": "i-22222222"},
#         "Hrs",
#     ),
#     ("AmazonS3", "Storage Snapshot", {"type": None, "id": None}, "GB-Mo"),
#     ("AmazonVPC", "Cloud Connectivity", {"type": None, "id": None}, "Hrs"),
#     ("AmazonEC2", "Compute Instance", {"type": "m5.large", "id": "i-33333333"}, "Hrs"),
#     ("AmazonEC2", "Compute Instance", {"type": "r4.large", "id": "i-44444444"}, "Hrs"),
#     ("AmazonEC2", "Compute Instance", {"type": "t2.micro", "id": "i-55555555"}, "Hrs"),
# )

AZURE_SERVICES = (
    ("SQL Database", {"type": None, "id": None}, "Hrs"),
    ("Virtual Machines", {"type": "Standard_A0", "id": "id1"}, "Hrs"),
    ("Virtual Machines", {"type": "Standard_B2s", "id": "id2"}, "Hrs"),
    ("Virtual Network", {"type": None, "id": None}, ""),
    ("DNS", {"type": None, "id": None}, ""),
    ("Load Balancer", {"type": None, "id": None}, ""),
    ("General Block Blob", {"type": None, "id": None}, "GB-Mo"),
    ("Blob Storage", {"type": None, "id": None}, "GB-Mo"),
    ("Standard SSD Managed Disks", {"type": None, "id": None}, "GB-Mo"),
)

GCP_INSTANCE_TYPES = ()
GCP_SERVICES = (
    ("6F81-5844-456A", "Compute Engine", "Instance Core running", "hour"),
    ("1111-581D-38E5", "SQL Database", "Storage PD Snapshot", "gibibyte month"),
    ("95FF-2EF5-5EA1", "Cloud Storage", "Standard Storage US Regional", "gibibyte month"),
    ("12B3-1234-JK3C", "Network", "ManagedZone", "seconds"),
    ("23C3-JS3K-SDL3", "VPC", "ManagedZone", "seconds"),
)

OCP_DATA_SOURCES = ("Pod", "Storage")
OCP_NAMESPACES = ("default", "koku", "koku-dev", "koku-stage", "koku-perf", "koku-prod")
# Node tuple ex ((node name, resource id, cpu, memory, volume tuple))

OCP_NODES = (
    ("node_1", "i-00000001", 4, 16, {"app": "mobile", "disabled": "Danilov"}),
    ("node_2", "i-00000002", 8, 32, {"app": "banking", "disabled": "Villabate"}),
    ("node_3", "i-00000003", 8, 32, {"app": "weather", "disabled": "Elbeuf"}),
    ("node_4", "i-00000004", 4, 16, {"app": "messaging", "disabled": "Pekanbaru"}),
    ("node_5", "i-00000005", 8, 32, {"app": "social", "disabled": "Castelfranco_Emilia"}),
    ("node_6", "i-00000006", 8, 32, {"app": "gaming", "disabled": "Teluk_Intan"}),
)
OCP_STORAGE_CLASSES = ("bronze", "silver", "gold", "platinum", "adamantium", "vibranium")
OCP_POD_LABELS = (
    {"app": "mobile", "disabled": "Danilov"},
    {"app": "banking", "disabled": "Villabate"},
    {"app": "weather", "disabled": "Elbeuf"},
    {"app": "messaging", "disabled": "Pekanbaru"},
    {"app": "social", "disabled": "Castelfranco_Emilia"},
    {"app": "gaming", "disabled": "Teluk_Intan"},
)
OCP_PVCS = (
    ("pvc_1", "volume_1", "bronze", 512, {"app": "mobile", "disabled": "Danilov", "storageclass": "Ruby"}),
    ("pvc_2", "volume_2", "silver", 128, {"app": "banking", "disabled": "Villabate", "storageclass": "Saphire"}),
    ("pvc_3", "volume_3", "gold", 256, {"app": "weather", "disabled": "Elbeuf", "storageclass": "Pearl"}),
    ("pvc_4", "volume_4", "platinum", 1024, {"app": "messaging", "disabled": "Pekanbaru", "storageclass": "Diamond"}),
    ("pvc_5", "volume_5", "adamantium", 512, {"app": "social", "disabled": "Castel_Emili", "storageclass": "Emerald"}),
    ("pvc_6", "volume_6", "vibranium", 1024, {"app": "mobile", "disabled": "Teluk_Intan", "storageclass": "Garnet"}),
)
OCP_PVC_LABELS = (
    {"app": "mobile", "disabled": "Danilov", "storageclass": "Ruby"},
    {"app": "banking", "disabled": "Villabate", "storageclass": "Saphire"},
    {"app": "weather", "disabled": "Elbeuf", "storageclass": "Pearl"},
    {"app": "messaging", "disabled": "Pekanbaru", "storageclass": "Diamond"},
    {"app": "social", "disabled": "Castel_Emili", "storageclass": "Emerald"},
    {"app": "gaming", "disabled": "Teluk_Intan", "storageclass": "Garnet"},
)
