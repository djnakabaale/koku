#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
from itertools import cycle

from faker import Faker
from model_bakery.recipe import foreign_key
from model_bakery.recipe import Recipe
from model_bakery.recipe import seq

from api.report.test.util.constants import AWS_CONSTANTS
from api.report.test.util.constants import AWS_GEOG
from api.report.test.util.constants import AZURE_CONSTANTS
from api.report.test.util.constants import GCP_CONSTANTS
from api.report.test.util.constants import OCP_CONSTANTS


fake = Faker()

billing_source = Recipe("ProviderBillingSource", data_source={})
provider = Recipe("Provider", billing_source=foreign_key(billing_source))

aws_daily_summary = Recipe(
    "AWSCostEntryLineItemDailySummary",
    product_code=cycle(AWS_CONSTANTS["product_codes"]),
    product_family=cycle(AWS_CONSTANTS["product_families"]),
    instance_type=cycle(AWS_CONSTANTS["instance_types"]),
    resource_count=cycle(AWS_CONSTANTS["resource_counts"]),
    resource_ids=cycle(AWS_CONSTANTS["resource_ids"]),
    unit=cycle(AWS_CONSTANTS["units"]),
    region=cycle(AWS_GEOG["regions"]),
    availability_zone=cycle(AWS_GEOG["availability_zones"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=AWS_CONSTANTS.length,
)

azure_daily_summary = Recipe(
    "AzureCostEntryLineItemDailySummary",
    service_name=cycle(AZURE_CONSTANTS["service_names"]),
    instance_type=cycle(AZURE_CONSTANTS["instance_types"]),
    instance_ids=cycle(AZURE_CONSTANTS["instance_ids"]),
    instance_count=cycle(AZURE_CONSTANTS["instance_counts"]),
    unit_of_measure=cycle(AZURE_CONSTANTS["units_of_measure"]),
    resource_location="US East",
    _fill_optional=True,
    _bulk_create=True,
    _quantity=AZURE_CONSTANTS.length,
)

gcp_daily_summary = Recipe(
    "GCPCostEntryLineItemDailySummary",
    service_id=cycle(GCP_CONSTANTS["service_ids"]),
    service_alias=cycle(GCP_CONSTANTS["service_aliases"]),
    sku_id=cycle(GCP_CONSTANTS["service_ids"]),
    sku_alias=cycle(GCP_CONSTANTS["sku_aliases"]),
    unit=cycle(GCP_CONSTANTS["units"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=GCP_CONSTANTS.length,
)

ocp_usage_pod = Recipe(  # Pod data_source
    "OCPUsageLineItemDailySummary",
    data_source="Pod",
    node=seq("node_"),
    resource_id=seq("i-0000000"),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
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
    pod_labels=cycle(OCP_CONSTANTS["pod_labels"]),
    _fill_optional=False,
    _bulk_create=True,
    _quantity=OCP_CONSTANTS.length,
)

ocp_usage_storage = Recipe(  # Storage data_source
    "OCPUsageLineItemDailySummary",
    data_source="Storage",
    node=seq("node_"),
    resource_id=seq("i-0000000"),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
    persistentvolumeclaim=seq("pvc_"),
    persistentvolume=seq("volume_"),
    storageclass=cycle(OCP_CONSTANTS["storage_classes"]),
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
    volume_labels=cycle(OCP_CONSTANTS["pvc_labels"]),
    _fill_optional=False,
    _bulk_create=True,
    _quantity=OCP_CONSTANTS.length,
)

ocp_on_aws_daily_summary = Recipe(
    "OCPAWSCostLineItemDailySummary",
    node=seq("node_", start=100),
    resource_id=seq("i-0000", increment_by=111, start=111),
    namespace=cycle([ns] for ns in OCP_CONSTANTS["namespaces"]),
    product_code=cycle(AWS_CONSTANTS["product_codes"]),
    product_family=cycle(AWS_CONSTANTS["product_families"]),
    unit=cycle(AWS_CONSTANTS["units"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AWS_CONSTANTS.length, 9),
)

ocp_on_aws_project_daily_summary_pod = Recipe(  # Pod data_source
    "OCPAWSCostLineItemProjectDailySummary",
    data_source="Pod",
    node=seq("node_", start=100),
    resource_id=seq("i-0000", increment_by=111, start=111),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
    persistentvolumeclaim=None,
    persistentvolume=None,
    storageclass=None,
    product_code=cycle(AWS_CONSTANTS["product_codes"]),
    product_family=cycle(AWS_CONSTANTS["product_families"]),
    unit=cycle(AWS_CONSTANTS["units"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AWS_CONSTANTS.length, 9),
)

ocp_on_aws_project_daily_summary_storage = Recipe(  # Storage data_source
    "OCPAWSCostLineItemProjectDailySummary",
    data_source="Storage",
    node=seq("node_", start=100),
    resource_id=seq("i-0000", increment_by=111, start=111),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
    persistentvolumeclaim=seq("pvc_", start=100),
    persistentvolume=seq("volume_", start=100),
    storageclass=cycle(OCP_CONSTANTS["storage_classes"]),
    product_code=cycle(AWS_CONSTANTS["product_codes"]),
    product_family=cycle(AWS_CONSTANTS["product_families"]),
    unit=cycle(AWS_CONSTANTS["units"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AWS_CONSTANTS.length, 9),
)

ocp_on_azure_daily_summary = Recipe(
    "OCPAzureCostLineItemDailySummary",
    node=seq("node_", start=1000),
    resource_id=seq("i-000", increment_by=1111, start=1111),
    namespace=cycle([ns] for ns in OCP_CONSTANTS["namespaces"]),
    service_name=cycle(AZURE_CONSTANTS["service_names"]),
    instance_type=cycle(AZURE_CONSTANTS["instance_types"]),
    resource_location="US East",
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AZURE_CONSTANTS.length, 9),
)

ocp_on_azure_project_daily_summary_pod = Recipe(  # Pod data_source
    "OCPAzureCostLineItemProjectDailySummary",
    data_source="Pod",
    node=seq("node_", start=1000),
    resource_id=seq("i-000", increment_by=1111, start=1111),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
    persistentvolumeclaim=None,
    persistentvolume=None,
    storageclass=None,
    service_name=cycle(AZURE_CONSTANTS["service_names"]),
    instance_type=cycle(AZURE_CONSTANTS["instance_types"]),
    unit_of_measure=cycle(AZURE_CONSTANTS["units_of_measure"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AZURE_CONSTANTS.length, 9),
)

ocp_on_azure_project_daily_summary_storage = Recipe(  # Storage data_source
    "OCPAzureCostLineItemProjectDailySummary",
    data_source="Storage",
    node=seq("node_", start=100),
    resource_id=seq("i-000", increment_by=1111, start=1111),
    namespace=cycle(OCP_CONSTANTS["namespaces"]),
    persistentvolumeclaim=seq("pvc_", start=1000),
    persistentvolume=seq("volume_", start=1000),
    storageclass=cycle(OCP_CONSTANTS["storage_classes"]),
    service_name=cycle(AZURE_CONSTANTS["service_names"]),
    instance_type=cycle(AZURE_CONSTANTS["instance_types"]),
    unit_of_measure=cycle(AZURE_CONSTANTS["units_of_measure"]),
    _fill_optional=True,
    _bulk_create=True,
    _quantity=min(AZURE_CONSTANTS.length, 9),
)
