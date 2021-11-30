# Generated by Django 3.1.13 on 2021-11-30 16:13
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("reporting", "0209_gcp_partables")]

    operations = [
        migrations.AddField(
            model_name="awscomputesummaryp",
            name="account_alias",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="reporting.awsaccountalias"
            ),
        ),
        migrations.AddField(
            model_name="awscomputesummaryp",
            name="usage_account_id",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
