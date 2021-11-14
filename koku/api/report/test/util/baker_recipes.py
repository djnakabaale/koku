#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
from itertools import cycle

from faker import Faker
from model_bakery.recipe import foreign_key
from model_bakery.recipe import Recipe

from api.report.test.util import constants


fake = Faker()

billing_source = Recipe("ProviderBillingSource", data_source={})
provider = Recipe("Provider", billing_source=foreign_key(billing_source))

aws_daily_summary = Recipe(
    "AWSCostEntryLineItemDailySummary",
    product_code=cycle(constants.AWS_PRODUCT_CODES),
    product_family=cycle(constants.AWS_PRODUCT_FAMILIES),
    instance_type=cycle(constants.AWS_INSTANCE_TYPES),
    resource_count=cycle(constants.AWS_RESOURCE_COUNTS),
    resource_ids=cycle(constants.AWS_INSTANCE_IDS),
    unit=cycle(constants.AWS_UNITS),
    region=cycle(constants.AWS_REGIONS),
    availability_zone=cycle(constants.AWS_AVAILABILITY_ZONES),
    _fill_optional=True,
)

ocp_usage_pod = Recipe(  # Pod data_source
    "OCPUsageLineItemDailySummary",
    data_source="Pod",
    pod_limit_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    pod_usage_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    pod_request_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    pod_limit_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    pod_usage_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    pod_request_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_cpu_cores=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_memory_gigabytes=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    cluster_capacity_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    cluster_capacity_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
)

ocp_usage_storage = Recipe(  # Storage data_source
    "OCPUsageLineItemDailySummary",
    data_source="Storage",
    persistentvolumeclaim_capacity_gigabyte=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    persistentvolumeclaim_capacity_gigabyte_months=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    volume_request_storage_gigabyte_months=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    persistentvolumeclaim_usage_gigabyte_months=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_cpu_cores=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_memory_gigabytes=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    node_capacity_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    cluster_capacity_cpu_core_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
    cluster_capacity_memory_gigabyte_hours=fake.pydecimal(left_digits=5, right_digits=5, positive=True),
)

ocp_on_azure_pod = Recipe("OCPAzureCostLineItemDailySummary", data_source="Pod")  # Pod data_source
