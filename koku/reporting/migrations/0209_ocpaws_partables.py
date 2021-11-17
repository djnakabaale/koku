# Generated by Django 3.1.13 on 2021-11-17 20:32
import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations
from django.db import models

from koku.database import set_partition_mode
from koku.database import unset_partition_mode


class Migration(migrations.Migration):

    dependencies = [("api", "0050_exchangerates"), ("reporting", "0208_savingsplan_markup_fields")]

    operations = [
        migrations.RunPython(code=set_partition_mode, reverse_code=unset_partition_mode),
        migrations.CreateModel(
            name="OCPAWSStorageSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_storage_summary_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSNetworkSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_network_summary_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSDatabaseSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_database_summary_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSCostSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_cost_summary_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSCostSummaryByServiceP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("product_code", models.CharField(max_length=50)),
                ("product_family", models.CharField(max_length=150, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_cost_summary_by_service_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSCostSummaryByRegionP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("region", models.CharField(max_length=50, null=True)),
                ("availability_zone", models.CharField(max_length=50, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_cost_summary_by_region_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSCostSummaryByAccountP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_cost_summary_by_account_p"},
        ),
        migrations.CreateModel(
            name="OCPAWSComputeSummaryP",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("usage_start", models.DateField()),
                ("usage_end", models.DateField()),
                ("cluster_id", models.CharField(max_length=50, null=True)),
                ("cluster_alias", models.CharField(max_length=256, null=True)),
                ("usage_account_id", models.CharField(max_length=50)),
                ("instance_type", models.CharField(max_length=50, null=True)),
                ("resource_id", models.CharField(max_length=253, null=True)),
                ("usage_amount", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("unit", models.CharField(max_length=63, null=True)),
                ("unblended_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("markup_cost", models.DecimalField(decimal_places=9, max_digits=24, null=True)),
                ("currency_code", models.CharField(max_length=10)),
                (
                    "account_alias",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
                    ),
                ),
                (
                    "source_uuid",
                    models.ForeignKey(
                        db_column="source_uuid",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.provider",
                    ),
                ),
            ],
            options={"db_table": "reporting_ocpaws_compute_summary_p"},
        ),
        migrations.AddIndex(
            model_name="ocpawsstoragesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpawsstorsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawsstoragesummaryp",
            index=models.Index(fields=["usage_account_id"], name="ocpawsstorsumm_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawsnetworksummaryp",
            index=models.Index(fields=["usage_start"], name="ocpawsnetsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawsnetworksummaryp",
            index=models.Index(fields=["usage_account_id"], name="ocpawsnetsumm_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawsdatabasesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpawsdbsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawsdatabasesummaryp",
            index=models.Index(fields=["usage_account_id"], name="ocpawsdbsumm_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummaryp",
            index=models.Index(fields=["usage_start"], name="ocpawscostsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyservicep",
            index=models.Index(fields=["usage_start"], name="ocpawscost_serv_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyservicep",
            index=models.Index(fields=["usage_account_id"], name="ocpawscostsumm_serv_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyservicep",
            index=models.Index(fields=["product_code"], name="ocpawscostsumm_serv_p_code"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyregionp",
            index=models.Index(fields=["usage_start"], name="ocpawscostsumm_reg_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyregionp",
            index=models.Index(fields=["usage_account_id"], name="ocpawscostsumm_reg_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyregionp",
            index=models.Index(fields=["region"], name="ocpawscostsumm_reg_region"),
        ),
        migrations.AddIndex(
            model_name="ocpawscostsummarybyaccountp",
            index=models.Index(fields=["usage_start"], name="ocpawscost_acct_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawscomputesummaryp",
            index=models.Index(fields=["usage_start"], name="ocpawscompsumm_usage_start"),
        ),
        migrations.AddIndex(
            model_name="ocpawscomputesummaryp",
            index=models.Index(fields=["usage_account_id"], name="ocpawscompsumm_usage_acct"),
        ),
        migrations.AddIndex(
            model_name="ocpawscomputesummaryp",
            index=models.Index(fields=["instance_type"], name="ocpawscompsumm_inst_type"),
        ),
        migrations.RunPython(code=unset_partition_mode, reverse_code=set_partition_mode),
    ]
