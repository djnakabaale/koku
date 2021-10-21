# Generated by Django 3.1.13 on 2021-10-11 10:24
import uuid

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
import django.db.models.deletion
from django.db import migrations
from django.db import models

from koku.database import set_partition_mode
from koku.database import unset_partition_mode


class Migration(migrations.Migration):

    dependencies = [("reporting", "0197_usersettings")]

    operations = [
        migrations.RunPython(code=set_partition_mode, reverse_code=unset_partition_mode),
        migrations.CreateModel(
            name="OCPGCPCostLineItemDailySummary",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                (
                    "namespace",
                    django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=253), size=None),
                ),
                ("node", models.CharField(max_length=253, null=True)),
                ("resource_id", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("project_id", models.CharField(max_length=256)),
                ("project_name", models.CharField(max_length=256)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("region", models.TextField(null=True)),
                ("tags", models.JSONField(null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("unit", models.TextField(null=True)),
                ("shared_projects", models.IntegerField(default=1)),
                ("project_costs", models.JSONField(null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcpcostlineitem_daily_summary"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcpcostlineitem_daily_summary ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostSummaryByAccountP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_cost_summary_by_account_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_cost_summary_by_account_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostSummaryByGCPProjectP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("project_id", models.CharField(max_length=256)),
                ("project_name", models.CharField(max_length=256)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("unit", models.TextField(null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_cost_summary_by_gcp_project_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_cost_summary_by_gcp_project_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostSummaryByRegionP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("region", models.TextField(null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_cost_summary_by_region_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_cost_summary_by_region_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostSummaryByServiceP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_cost_summary_by_service_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_cost_summary_by_service_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostSummaryP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_cost_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_cost_summary_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPComputeSummaryP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("instance_id", models.CharField(max_length=50, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_compute_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_compute_summary_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPDatabaseSummaryP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_database_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_database_summary_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPNetworkSummaryP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_network_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_network_summary_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPStorageSummaryP",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("node", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=17, null=True)),
                ("currency", models.TextField(null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcp_storage_summary_p"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcp_storage_summary_p ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPCostLineItemProjectDailySummary",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("data_source", models.CharField(max_length=64, null=True)),
                ("namespace", models.CharField(max_length=253)),
                ("node", models.CharField(max_length=253, null=True)),
                ("persistentvolumeclaim", models.CharField(max_length=253, null=True)),
                ("persistentvolume", models.CharField(max_length=253, null=True)),
                ("storageclass", models.CharField(max_length=50, null=True)),
                ("pod_labels", models.JSONField(null=True)),
                ("resource_id", models.CharField(max_length=253, null=True)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("account_id", models.CharField(max_length=20)),
                ("project_id", models.CharField(max_length=256)),
                ("project_name", models.CharField(max_length=256)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                ("service_id", models.CharField(max_length=256, null=True)),
                ("service_alias", models.CharField(blank=True, max_length=256, null=True)),
                ("sku_id", models.CharField(max_length=256, null=True)),
                ("sku_alias", models.CharField(max_length=256, null=True)),
                ("region", models.TextField(null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ("currency", models.CharField(max_length=10, null=True)),
                ("invoice_month", models.CharField(blank=True, max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ("project_markup_cost", models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ("pod_cost", models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ("tags", models.JSONField(null=True)),
                ("source_uuid", models.UUIDField(null=True)),
                ("credit_amount", models.DecimalField(blank=True, decimal_places=9, max_digits=24, null=True)),
            ],
            options={"db_table": "reporting_ocpgcpcostlineitem_project_daily_summary"},
        ),
        migrations.RunSQL(
            sql="ALTER TABLE reporting_ocpgcpcostlineitem_project_daily_summary ALTER COLUMN uuid SET DEFAULT uuid_generate_v4()",
            reverse_sql="select 1",
        ),
        migrations.CreateModel(
            name="OCPGCPTagsSummary",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("key", models.CharField(max_length=253)),
                ("values", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ("account_id", models.TextField()),
                ("project_id", models.TextField()),
                ("project_name", models.TextField()),
                ("namespace", models.TextField()),
                ("node", models.TextField(null=True)),
            ],
            options={"db_table": "reporting_ocpgcptags_summary"},
        ),
        migrations.CreateModel(
            name="OCPGCPTagsValues",
            fields=[
                ("uuid", models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ("key", models.TextField()),
                ("value", models.TextField()),
                ("account_ids", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ("project_ids", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ("project_names", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ("cluster_ids", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                (
                    "cluster_aliases",
                    django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
                ),
                ("namespaces", django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                (
                    "nodes",
                    django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), null=True, size=None),
                ),
            ],
            options={"db_table": "reporting_ocpgcptags_values"},
        ),
        migrations.AddIndex(
            model_name="ocpgcptagsvalues", index=models.Index(fields=["key"], name="ocp_gcp_tags_value_key_idx")
        ),
        migrations.AlterUniqueTogether(name="ocpgcptagsvalues", unique_together={("key", "value")}),
        migrations.AddField(
            model_name="ocpgcptagssummary",
            name="cost_entry_bill",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reporting.gcpcostentrybill"),
        ),
        migrations.AddField(
            model_name="ocpgcptagssummary",
            name="report_period",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"),
        ),
        migrations.AddField(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            name="cost_entry_bill",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reporting.gcpcostentrybill"),
        ),
        migrations.AddField(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostsummarybyaccountp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostsummarybygcpprojectp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostsummarybyregionp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostsummarybyservicep",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostsummaryp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcomputesummaryp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpdatabasesummaryp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpnetworksummaryp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpstoragesummaryp",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AddField(
            model_name="ocpgcpcostlineitemdailysummary",
            name="cost_entry_bill",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="reporting.gcpcostentrybill"),
        ),
        migrations.AddField(
            model_name="ocpgcpcostlineitemdailysummary",
            name="report_period",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="reporting.ocpusagereportperiod"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ocpgcptagssummary",
            unique_together={
                (
                    "key",
                    "cost_entry_bill",
                    "account_id",
                    "project_id",
                    "project_name",
                    "report_period",
                    "namespace",
                    "node",
                )
            },
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["usage_start"], name="ocpgcp_proj_usage_start_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["namespace"], name="ocpgcp_proj_namespace_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["node"], name="ocpgcp_proj_node_idx", opclasses=["varchar_pattern_ops"]),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["resource_id"], name="ocpgcp_proj_resource_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=django.contrib.postgres.indexes.GinIndex(fields=["tags"], name="ocpgcp_proj_tags_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["project_id"], name="ocpgcp_proj_id_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["project_name"], name="ocpgcp_proj_name_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["service_id"], name="ocpgcp_proj_service_id_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemprojectdailysummary",
            index=models.Index(fields=["service_alias"], name="ocpgcp_proj_service_alias_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["usage_start"], name="ocpgcp_usage_start_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["namespace"], name="ocpgcp_namespace_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["node"], name="ocpgcp_node_idx", opclasses=["varchar_pattern_ops"]),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["resource_id"], name="ocpgcp_resource_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=django.contrib.postgres.indexes.GinIndex(fields=["tags"], name="ocpgcp_tags_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["project_id"], name="ocpgcp_id_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["project_name"], name="ocpgcp_name_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["service_id"], name="ocpgcp_service_id_idx"),
        ),
        migrations.AddIndex(
            model_name="ocpgcpcostlineitemdailysummary",
            index=models.Index(fields=["service_alias"], name="ocpgcp_service_alias_idx"),
        ),
        migrations.RunPython(code=unset_partition_mode, reverse_code=set_partition_mode),
    ]
