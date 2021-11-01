#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Test utilities."""
import json
import pkgutil
import random
from datetime import timedelta
from functools import partial

from django.test.utils import override_settings
from faker import Faker
from model_bakery import baker
from tenant_schemas.utils import schema_context

from api.models import Provider
from api.provider.models import ProviderBillingSource
from api.report.test.util import constants
from api.report.test.util.data_loader import DataLoader
from masu.database.aws_report_db_accessor import AWSReportDBAccessor
from masu.database.azure_report_db_accessor import AzureReportDBAccessor
from masu.database.gcp_report_db_accessor import GCPReportDBAccessor
from masu.database.ocp_report_db_accessor import OCPReportDBAccessor
from masu.processor.tasks import refresh_materialized_views
from masu.processor.tasks import update_cost_model_costs
from masu.util.aws.insert_aws_org_tree import InsertAwsOrgTree
from reporting.models import AWSAccountAlias
from reporting.models import AWSOrganizationalUnit


def aws_service_gen():
    account_alias = random.choice(list(AWSAccountAlias.objects.all()))
    service = random.choice(constants.AWS_SERVICES)
    return {
        "product_code": service[0],
        "product_family": service[2],
        "unit": service[4],
        "account_alias": account_alias,
    }


def azure_service_gen():
    # subscription_guid = random.choice(list(AWSOrganizationalUnit.objects.all()))
    service = random.choice(constants.AZURE_SERVICES)
    return {"service_name": service[0], "unit_of_measure": service[2] or None}


class ModelBakeryDataLoader(DataLoader):
    """Loads model bakery generated test data for different source types."""

    def __init__(self, schema, customer, num_days=10):
        super().__init__(schema, customer, num_days=num_days)
        self.faker = Faker()
        self.currency = "USD"  # self.faker.currency_code()
        self.num_tag_keys = 10
        self.tag_keys = [self.faker.slug() for _ in range(self.num_tag_keys)]
        self.tags = [{key: self.faker.slug()} for key in self.tag_keys] + [{"app": self.faker.slug()}]
        self.tag_test_tag_key = "app"
        self._populate_enabled_tag_key_table()
        self.namespaces = list(constants.OCP_NAMESPACES[:])
        random.shuffle(self.namespaces)

    def _get_bill_model(self, provider_type):
        """Return the correct model for a provider type."""
        if provider_type in (Provider.PROVIDER_AWS, Provider.PROVIDER_AWS_LOCAL):
            return "AWSCostEntryBill"
        elif provider_type in (Provider.PROVIDER_AZURE, Provider.PROVIDER_AZURE_LOCAL):
            return "AzureCostEntryBill"
        elif provider_type in (Provider.PROVIDER_GCP, Provider.PROVIDER_GCP_LOCAL):
            return "GCPCostEntryBill"
        if provider_type == Provider.PROVIDER_OCP:
            return "OCPUsageReportPeriod"

    def _get_cost_entry_model(self, provider_type):
        """Return the correct model for a provider type."""
        if provider_type in (Provider.PROVIDER_AWS, Provider.PROVIDER_AWS_LOCAL):
            return "AWSCostEntry"

    def _populate_enabled_tag_key_table(self):
        """Insert records for our tag keys."""
        for table_name in ("AWSEnabledTagKeys", "AzureEnabledTagKeys", "GCPEnabledTagKeys", "OCPEnabledTagKeys"):
            with schema_context(self.schema):
                baker.make(table_name, key=self.tag_test_tag_key)

    def create_provider(self, provider_type, credentials, billing_source, name, linked_openshift_provider=None):
        """Create a Provider record"""
        with override_settings(AUTO_DATA_INGEST=False):
            if provider_type == Provider.PROVIDER_OCP:
                billing_source, _ = ProviderBillingSource.objects.get_or_create(data_source={})
                provider = baker.make(
                    "Provider",
                    type=provider_type,
                    name=name,
                    authentication__credentials=credentials,
                    billing_source=billing_source,
                    customer=self.customer,
                )
            else:
                provider = baker.make(
                    "Provider",
                    type=provider_type,
                    name=name,
                    authentication__credentials=credentials,
                    billing_source__data_source=billing_source,
                    customer=self.customer,
                )

            if linked_openshift_provider:
                infra_map = baker.make(
                    "ProviderInfrastructureMap", infrastructure_type=provider_type, infrastructure_provider=provider
                )
                linked_openshift_provider.infrastructure = infra_map
                linked_openshift_provider.save()
            return provider

    def create_manifest(self, provider, bill_date, num_files=1):
        """Create a manifest for the provider."""
        manifest = baker.make(
            "CostUsageReportManifest",
            provider=provider,
            billing_period_start_datetime=bill_date,
            num_total_files=num_files,
            _fill_optional=True,
        )

        baker.make("CostUsageReportStatus", manifest=manifest, _fill_optional=True)

        return manifest

    def create_bill(self, provider_type, provider, bill_date, **kwargs):
        """Create a bill object for the provider"""
        with schema_context(self.schema):
            model_str = self._get_bill_model(provider_type)
            month_end = self.dh.month_end(bill_date)
            if provider_type != Provider.PROVIDER_OCP:
                return baker.make(
                    model_str,
                    provider=provider,
                    billing_period_start=bill_date,
                    billing_period_end=month_end,
                    _fill_optional=False,
                    **kwargs,
                )
            month_end = month_end + timedelta(days=1)
            return baker.make(
                model_str,
                provider=provider,
                report_period_start=bill_date,
                report_period_end=month_end,
                _fill_optional=False,
                **kwargs,
            )

    def create_cost_entry(self, provider_type, bill_date, bill):
        """Create a cost entry object for the provider"""
        with schema_context(self.schema):
            model_str = self._get_cost_entry_model(provider_type)
            month_end = self.dh.month_end(bill_date)
            baker.make(model_str, interval_start=bill_date, interval_end=month_end, bill=bill)

    def create_cost_model(self, provider):
        """Create a cost model and map entry."""
        cost_model_json = json.loads(
            pkgutil.get_data("api.report.test", "openshift_on_prem_cost_model.json").decode("utf8")
        )
        with schema_context(self.schema):
            cost_model = baker.make(
                "CostModel",
                name=cost_model_json.get("name"),
                description=cost_model_json.get("description"),
                rates=cost_model_json.get("rates"),
                distribution=cost_model_json.get("distribution"),
                source_type=provider.type,
                currency=self.currency,
                _fill_optional=True,
            )
            baker.make("CostModelMap", provider_uuid=provider.uuid, cost_model=cost_model)

    def load_aws_data(self, linked_openshift_provider=None, day_list=None):
        """Load AWS data for tests."""
        bills = []
        provider_type = Provider.PROVIDER_AWS_LOCAL
        role_arn = "arn:aws:iam::999999999999:role/CostManagement"
        credentials = {"role_arn": role_arn}
        billing_source = {"bucket": "test-bucket"}
        payer_account_id = "123456789"
        # create_supplemental_info = True

        provider = self.create_provider(
            provider_type, credentials, billing_source, "test-aws", linked_openshift_provider=linked_openshift_provider
        )

        if day_list:
            org_tree_obj = InsertAwsOrgTree(
                schema=self.schema, provider_uuid=provider.uuid, start_date=self.dates[0][0]
            )
            org_tree_obj.insert_tree(day_list=day_list)

        # with schema_context(self.schema):
        #     org_units = AWSOrganizationalUnit.objects.all()

        for start_date, end_date, bill_date in self.dates:
            self.create_manifest(provider, bill_date)
            bill = self.create_bill(provider_type, provider, bill_date, payer_account_id=payer_account_id)
            bills.append(bill)
            self.create_cost_entry(provider_type, bill_date, bill)
            with schema_context(self.schema):
                # if create_supplemental_info:
                #     alias = baker.make(
                #         "AWSAccountAlias", account_id=bill.payer_account_id, account_alias="Test Account"
                #     )
                #     create_supplemental_info = False
                days = (end_date - start_date).days
                for i in range(days):
                    for service in constants.AWS_SERVICES:
                        alias = random.choice(list(AWSAccountAlias.objects.all()))
                        org_units = AWSOrganizationalUnit.objects.filter(account_alias_id=alias.id)
                        instance = service[3]
                        region = random.choice(constants.AWS_REGIONS)
                        baker.make(
                            "AWSCostEntryLineItemDailySummary",
                            cost_entry_bill=bill,
                            usage_account_id=bill.payer_account_id,
                            account_alias=alias,
                            organizational_unit=random.choice(org_units),
                            currency_code=self.currency,
                            usage_start=start_date + timedelta(i),
                            usage_end=start_date + timedelta(i),
                            product_code=service[0],
                            product_family=service[2],
                            instance_type=instance.get("type"),
                            resource_count=1 if instance.get("id") else 0,
                            resource_ids=[instance.get("id")],
                            unit=service[4],
                            region=region[0],
                            availability_zone=region[1],
                            tags=random.choice(self.tags),
                            source_uuid=provider.uuid,
                            _fill_optional=True,
                        )
            AWSReportDBAccessor(self.schema).populate_tags_summary_table([bill.id], start_date, end_date)
        refresh_materialized_views(self.schema, provider_type, provider_uuid=provider.uuid, synchronous=True)

        return provider, bills

    def load_azure_data(self, linked_openshift_provider=None):
        """Load Azure data for tests."""
        bills = []
        provider_type = Provider.PROVIDER_AZURE_LOCAL
        credentials = {
            "subscription_id": "11111111-1111-1111-1111-11111111",
            "tenant_id": "22222222-2222-2222-2222-22222222",
            "client_id": "33333333-3333-3333-3333-33333333",
            "client_secret": "MyPassW0rd!",
        }
        billing_source = {"resource_group": "resourcegroup1", "storage_account": "storageaccount1"}

        provider = self.create_provider(
            provider_type,
            credentials,
            billing_source,
            "test-azure",
            linked_openshift_provider=linked_openshift_provider,
        )
        sub_guid = self.faker.uuid4()
        for start_date, end_date, bill_date in self.dates:
            self.create_manifest(provider, bill_date)
            bill = self.create_bill(provider_type, provider, bill_date)
            bills.append(bill)
            with schema_context(self.schema):
                days = (end_date - start_date).days
                for i in range(days):
                    for service in constants.AZURE_SERVICES:
                        instance = service[1]
                        baker.make(
                            "AzureCostEntryLineItemDailySummary",
                            cost_entry_bill=bill,
                            subscription_guid=sub_guid,
                            usage_start=start_date + timedelta(i),
                            usage_end=start_date + timedelta(i),
                            service_name=service[0],
                            instance_type=instance.get("type"),
                            instance_ids=[instance.get("id")],
                            instance_count=1 if instance.get("type") else 0,
                            unit_of_measure=service[2] or None,
                            resource_location="US East",
                            tags=random.choice(self.tags),
                            currency=self.currency,
                            source_uuid=provider.uuid,
                            _fill_optional=True,
                        )
            AzureReportDBAccessor(self.schema).populate_tags_summary_table([bill.id], start_date, end_date)
        refresh_materialized_views(self.schema, provider_type, provider_uuid=provider.uuid, synchronous=True)
        return provider, bills

    def load_gcp_data(self, linked_openshift_provider=None):
        """Load Azure data for tests."""
        bills = []
        provider_type = Provider.PROVIDER_GCP_LOCAL
        credentials = {"project_id": "test_project_id"}
        billing_source = {"table_id": "test_table_id", "dataset": "test_dataset"}
        account_id = "123456789"
        provider = self.create_provider(
            provider_type, credentials, billing_source, "test-gcp", linked_openshift_provider=linked_openshift_provider
        )
        projects = [(self.faker.slug(), self.faker.slug()) for _ in range(3)]
        for start_date, end_date, bill_date in self.dates:
            self.create_manifest(provider, bill_date)
            bill = self.create_bill(provider_type, provider, bill_date)
            bills.append(bill)
            with schema_context(self.schema):
                days = (end_date - start_date).days
                for i in range(days):
                    for project in projects:
                        for service in constants.GCP_SERVICES:
                            baker.make(
                                "GCPCostEntryLineItemDailySummary",
                                cost_entry_bill=bill,
                                invoice_month=bill_date.strftime("%Y%m"),
                                account_id=account_id,
                                project_id=project[0],
                                project_name=project[1],
                                usage_start=start_date + timedelta(i),
                                usage_end=start_date + timedelta(i),
                                service_id=service[0],
                                service_alias=service[1],
                                sku_id=service[0],
                                sku_alias=service[2],
                                unit=service[3],
                                tags=random.choice(self.tags),
                                currency=self.currency,
                                source_uuid=provider.uuid,
                                _fill_optional=True,
                            )
            GCPReportDBAccessor(self.schema).populate_tags_summary_table([bill.id], start_date, end_date)
        refresh_materialized_views(self.schema, provider_type, provider_uuid=provider.uuid, synchronous=True)
        return provider, bills

    def load_openshift_data(self, cluster_id, on_cloud=False):
        """Load OpenShift data for tests."""
        report_periods = []
        provider_type = Provider.PROVIDER_OCP
        credentials = {"cluster_id": cluster_id}
        billing_source = {}

        provider = self.create_provider(provider_type, credentials, billing_source, cluster_id)
        if not on_cloud:
            self.create_cost_model(provider)
        namespaces = {node[0]: self.namespaces[i] for i, node in enumerate(constants.OCP_NODES)}
        volumes = {node[0]: constants.OCP_PVCS[i] for i, node in enumerate(constants.OCP_NODES)}
        cluster_cpu_capacity = sum(node_tuple[2] for node_tuple in constants.OCP_NODES)
        cluster_memory_capacity = sum(node_tuple[3] for node_tuple in constants.OCP_NODES)
        for start_date, end_date, bill_date in self.dates:
            self.create_manifest(provider, bill_date)
            report_period = self.create_bill(
                provider_type, provider, bill_date, cluster_id=cluster_id, cluster_alias=cluster_id
            )
            report_periods.append(report_period)
            with schema_context(self.schema):
                days = (end_date - start_date).days
                for i in range(days):
                    for node_tuple in constants.OCP_NODES:
                        namespace = namespaces.get(node_tuple[0])
                        pvc_tuple = volumes.get(node_tuple[0])
                        for data_source in constants.OCP_DATA_SOURCES:
                            persistent_volume_claim = pvc_tuple[0] if data_source == "Storage" else None
                            persistent_volume = pvc_tuple[1] if data_source == "Storage" else None
                            storage_class = pvc_tuple[2] if data_source == "Storage" else None
                            volume_capcity = pvc_tuple[3]
                            infra_raw_cost = random.random() * 100 if on_cloud else None
                            project_infra_raw_cost = infra_raw_cost * random.random() if on_cloud else None
                            pod_limit_cpu = random.randint(1, node_tuple[2])
                            pod_limit_memory = random.randint(1, node_tuple[3])
                            baker.make(
                                "OCPUsageLineItemDailySummary",
                                report_period=report_period,
                                cluster_id=cluster_id,
                                cluster_alias=cluster_id,
                                node=node_tuple[0],
                                resource_id=node_tuple[1],
                                namespace=namespace,
                                data_source=data_source,
                                persistentvolumeclaim=persistent_volume_claim,
                                persistentvolume=persistent_volume,
                                storageclass=storage_class,
                                usage_start=start_date + timedelta(i),
                                usage_end=start_date + timedelta(i),
                                pod_labels=node_tuple[4] if data_source == "Pod" else None,
                                volume_labels=pvc_tuple[4] if data_source == "Storage" else None,
                                source_uuid=provider.uuid,
                                pod_limit_cpu_core_hours=pod_limit_cpu if data_source == "Pod" else None,
                                pod_usage_cpu_core_hours=pod_limit_cpu * random.random()
                                if data_source == "Pod"
                                else None,
                                pod_request_cpu_core_hours=pod_limit_cpu * random.random()
                                if data_source == "Pod"
                                else None,
                                pod_limit_memory_gigabyte_hours=pod_limit_memory if data_source == "Pod" else None,
                                pod_usage_memory_gigabyte_hours=pod_limit_memory * random.random()
                                if data_source == "Pod"
                                else None,
                                pod_request_memory_gigabyte_hours=pod_limit_memory * random.random()
                                if data_source == "Pod"
                                else None,
                                persistentvolumeclaim_capacity_gigabyte=volume_capcity
                                if data_source == "Storage"
                                else None,
                                persistentvolumeclaim_capacity_gigabyte_months=volume_capcity * 30
                                if data_source == "Storage"
                                else None,
                                volume_request_storage_gigabyte_months=volume_capcity * 30 * random.random()
                                if data_source == "Storage"
                                else None,
                                persistentvolumeclaim_usage_gigabyte_months=volume_capcity * 30 * random.random()
                                if data_source == "Storage"
                                else None,
                                node_capacity_cpu_cores=node_tuple[2],
                                node_capacity_cpu_core_hours=node_tuple[2] * 24,
                                node_capacity_memory_gigabytes=node_tuple[3],
                                node_capacity_memory_gigabyte_hours=node_tuple[3] * 24,
                                cluster_capacity_cpu_core_hours=cluster_cpu_capacity * 24,
                                cluster_capacity_memory_gigabyte_hours=cluster_memory_capacity * 24,
                                infrastructure_raw_cost=infra_raw_cost,
                                infrastructure_project_raw_cost=project_infra_raw_cost,
                                infrastructure_usage_cost=None,
                                infrastructure_monthly_cost=None,
                                infrastructure_monthly_cost_json=None,
                                supplementary_usage_cost=None,
                                supplementary_monthly_cost=None,
                                supplementary_monthly_cost_json=None,
                                infrastructure_project_monthly_cost=None,
                                supplementary_project_monthly_cost=None,
                                monthly_cost_type=None,
                                _fill_optional=True,
                            )
            OCPReportDBAccessor(self.schema).populate_pod_label_summary_table([report_period.id], start_date, end_date)
            OCPReportDBAccessor(self.schema).populate_volume_label_summary_table(
                [report_period.id], start_date, end_date
            )
            OCPReportDBAccessor(self.schema).update_line_item_daily_summary_with_enabled_tags(
                start_date, end_date, [report_period.id]
            )
            update_cost_model_costs(
                self.schema, provider.uuid, start_date, end_date, tracing_id="12345", synchronous=True
            )
        refresh_materialized_views(self.schema, provider_type, provider_uuid=provider.uuid, synchronous=True)
        return provider, report_periods

    def load_openshift_on_cloud_data(self, provider_type, cluster_id, bills, report_periods):
        """Load OCP on AWS Daily Summary table."""
        unique_fields = {}
        service_gen = lambda *args, **kwargs: {}  # noqa: E731
        if provider_type in (Provider.PROVIDER_AWS, Provider.PROVIDER_AWS_LOCAL):
            daily_summary_table = "OCPAWSCostLineItemDailySummary"
            project_summary_table = "OCPAWSCostLineItemProjectDailySummary"
            update_method = partial(AWSReportDBAccessor(self.schema).populate_ocp_on_aws_tags_summary_table)
            unique_fields = {"currency_code": self.currency}
            service_gen = aws_service_gen
        elif provider_type in (Provider.PROVIDER_AZURE, Provider.PROVIDER_AZURE_LOCAL):
            daily_summary_table = "OCPAzureCostLineItemDailySummary"
            project_summary_table = "OCPAzureCostLineItemProjectDailySummary"
            update_method = partial(AzureReportDBAccessor(self.schema).populate_ocp_on_azure_tags_summary_table)
            unique_fields = {"currency": self.currency, "subscription_guid": self.faker.uuid4()}
            service_gen = azure_service_gen

        provider = Provider.objects.filter(type=provider_type).first()
        namespaces = {node[0]: self.faker.slug() for node in constants.OCP_NODES}
        volumes = {node[0]: constants.OCP_PVCS[i] for i, node in enumerate(constants.OCP_NODES)}
        for dates, bill, report_period in zip(self.dates, bills, report_periods):
            start_date = dates[0]
            end_date = dates[1]
            with schema_context(self.schema):
                days = (end_date - start_date).days
                for i in range(days):
                    for node_tuple in constants.OCP_NODES:
                        namespace = namespaces.get(node_tuple[0])
                        pvc_tuple = volumes.get(node_tuple[0])
                        for data_source in constants.OCP_DATA_SOURCES:
                            persistent_volume_claim = pvc_tuple[0] if data_source == "Storage" else None
                            persistent_volume = pvc_tuple[1] if data_source == "Storage" else None
                            storage_class = pvc_tuple[2] if data_source == "Storage" else None
                            unique_fields.update(**service_gen())
                            baker.make(
                                daily_summary_table,
                                report_period=report_period,
                                cluster_id=cluster_id,
                                cluster_alias=cluster_id,
                                node=node_tuple[0],
                                resource_id=node_tuple[1],
                                usage_start=start_date + timedelta(i),
                                usage_end=start_date + timedelta(i),
                                cost_entry_bill=bill,
                                namespace=[namespace],
                                tags=random.choice(self.tags),
                                source_uuid=provider.uuid,
                                **unique_fields,
                                _fill_optional=True,
                            )
                            baker.make(
                                project_summary_table,
                                report_period=report_period,
                                cluster_id=cluster_id,
                                cluster_alias=cluster_id,
                                node=node_tuple[0],
                                resource_id=node_tuple[1],
                                usage_start=start_date + timedelta(i),
                                usage_end=start_date + timedelta(i),
                                pod_labels=random.choice(self.tags),
                                cost_entry_bill=bill,
                                namespace=namespace,
                                data_source=data_source,
                                persistentvolumeclaim=persistent_volume_claim,
                                persistentvolume=persistent_volume,
                                storageclass=storage_class,
                                tags=random.choice(self.tags),
                                source_uuid=provider.uuid,
                                **unique_fields,
                                _fill_optional=True,
                            )
            update_method([bill.id], start_date, end_date)

        refresh_materialized_views(self.schema, provider_type, provider_uuid=provider.uuid, synchronous=True)
