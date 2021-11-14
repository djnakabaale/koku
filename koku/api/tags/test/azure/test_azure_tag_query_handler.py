#
# Copyright 2021 Red Hat Inc.
# SPDX-License-Identifier: Apache-2.0
#
"""Test the Report Queries."""
from unittest.mock import patch

from tenant_schemas.utils import tenant_context

from api.functions import JSONBObjectKeys
from api.iam.test.iam_test_case import IamTestCase
from api.tags.azure.queries import AzureTagQueryHandler
from api.tags.azure.view import AzureTagView
from reporting.models import AzureCostEntryLineItemDailySummary
from reporting.models import AzureTagsSummary
from reporting.provider.azure.models import AzureTagsValues


class AzureTagMergingQueryHandlerTest(IamTestCase):
    """Tests for the AzureTagQueryHandler."""

    def test_merge_tags(self):
        """Test the _merge_tags functionality."""
        url = "?filter[time_scope_units]=month&filter[time_scope_value]=-1&filter[resolution]=monthly"
        query_params = self.mocked_query_params(url, AzureTagView)

        tagHandler = AzureTagQueryHandler(query_params)

        # Test no source type
        final = []
        source = {}
        qs1 = [("ms-resource-usage", ["azure-cloud-shell"]), ("project", ["p1", "p2"]), ("cost", ["management"])]
        tag_keys = tagHandler._convert_to_dict(qs1)
        expected_dikt = {
            "ms-resource-usage": {"key": "ms-resource-usage", "values": ["azure-cloud-shell"]},
            "project": {"key": "project", "values": ["p1", "p2"]},
            "cost": {"key": "cost", "values": ["management"]},
        }
        self.assertEqual(tag_keys, expected_dikt)

        expected_1 = [
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"]},
            {"key": "project", "values": ["p1", "p2"]},
            {"key": "cost", "values": ["management"]},
        ]
        tagHandler.append_to_final_data_without_type(final, tag_keys)
        self.assertEqual(final, expected_1)

        # Test with source type
        final = []
        source = {"type": "storage"}
        tagHandler.append_to_final_data_with_type(final, tag_keys, source)
        expected_2 = [
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"], "type": "storage"},
            {"key": "project", "values": ["p1", "p2"], "type": "storage"},
            {"key": "cost", "values": ["management"], "type": "storage"},
        ]
        self.assertEqual(final, expected_2)

        final = []
        tagHandler.append_to_final_data_without_type(final, tag_keys)
        tagHandler.append_to_final_data_with_type(final, tag_keys, source)

        expected_3 = [
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"]},
            {"key": "project", "values": ["p1", "p2"]},
            {"key": "cost", "values": ["management"]},
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"], "type": "storage"},
            {"key": "project", "values": ["p1", "p2"], "type": "storage"},
            {"key": "cost", "values": ["management"], "type": "storage"},
        ]
        self.assertEqual(final, expected_3)

        qs2 = [("ms-resource-usage", ["azure-cloud-shell2"]), ("project", ["p1", "p3"])]
        tag_keys2 = tagHandler._convert_to_dict(qs2)
        expected_tag_keys2 = {
            "ms-resource-usage": {"key": "ms-resource-usage", "values": ["azure-cloud-shell2"]},
            "project": {"key": "project", "values": ["p1", "p3"]},
        }
        self.assertEqual(tag_keys2, expected_tag_keys2)

        tagHandler.append_to_final_data_without_type(final, tag_keys2)
        expected_4 = [
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell", "azure-cloud-shell2"]},
            {"key": "project", "values": ["p1", "p2", "p1", "p3"]},
            {"key": "cost", "values": ["management"]},
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"], "type": "storage"},
            {"key": "project", "values": ["p1", "p2"], "type": "storage"},
            {"key": "cost", "values": ["management"], "type": "storage"},
        ]
        self.assertEqual(final, expected_4)

        with patch("api.tags.azure.queries.AzureTagQueryHandler.order_direction", return_value="not-default"):
            final = tagHandler.deduplicate_and_sort(final)
        expected_5 = [
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell", "azure-cloud-shell2"]},
            {"key": "project", "values": ["p1", "p2", "p3"]},
            {"key": "cost", "values": ["management"]},
            {"key": "ms-resource-usage", "values": ["azure-cloud-shell"], "type": "storage"},
            {"key": "project", "values": ["p1", "p2"], "type": "storage"},
            {"key": "cost", "values": ["management"], "type": "storage"},
        ]

        self.assertEqual(final, expected_5)


class AzureTagQueryHandlerTest(IamTestCase):
    """Tests for the Azure report query handler."""

    def setUp(self):
        """Set up the customer view tests."""
        super().setUp()

    def test_execute_query_no_query_parameters(self):
        """Test that the execute query runs properly with no query."""
        url = "?"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "day")
        self.assertEqual(handler.time_scope_value, -10)

    def test_execute_query_10_day_parameters(self):
        """Test that the execute query runs properly with 10 day query."""
        url = "?filter[time_scope_units]=day&filter[time_scope_value]=-10&filter[resolution]=daily"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "day")
        self.assertEqual(handler.time_scope_value, -10)

    def test_execute_query_30_day_parameters(self):
        """Test that the execute query runs properly with 30 day query."""
        url = "?filter[time_scope_units]=day&filter[time_scope_value]=-30&filter[resolution]=daily"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "day")
        self.assertEqual(handler.time_scope_value, -30)

    def test_execute_query_10_day_parameters_only_keys(self):
        """Test that the execute query runs properly with 10 day query."""
        url = "?filter[time_scope_units]=day&filter[time_scope_value]=-10&filter[resolution]=daily&key_only=True"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "day")
        self.assertEqual(handler.time_scope_value, -10)

    def test_execute_query_month_parameters(self):
        """Test that the execute query runs properly with single month query."""
        url = "?filter[resolution]=monthly&filter[time_scope_value]=-1&filter[time_scope_units]=month"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "month")
        self.assertEqual(handler.time_scope_value, -1)

    def test_execute_query_two_month_parameters(self):
        """Test that the execute query runs properly with two month query."""
        url = "?filter[time_scope_units]=month&filter[time_scope_value]=-2&filter[resolution]=monthly"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "month")
        self.assertEqual(handler.time_scope_value, -2)

    def test_execute_query_for_project(self):
        """Test that the execute query runs properly with project query."""
        subscription_guid = None
        with tenant_context(self.tenant):
            obj = AzureCostEntryLineItemDailySummary.objects.values("subscription_guid").first()
            subscription_guid = obj.get("subscription_guid")

        url = f"?filter[time_scope_units]=day&filter[time_scope_value]=-10&filter[resolution]=daily&filter[subscription_guid]={subscription_guid}"  # noqa: E501
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        query_output = handler.execute_query()
        self.assertIsNotNone(query_output.get("data"))
        self.assertEqual(handler.time_scope_units, "day")
        self.assertEqual(handler.time_scope_value, -10)

    def test_get_tag_keys_filter_true(self):
        """Test that not all tag keys are returned with a filter."""
        url = "?filter[time_scope_units]=month&filter[time_scope_value]=-2&filter[resolution]=monthly"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)

        tag_keys = set()
        with tenant_context(self.tenant):
            tags = (
                AzureCostEntryLineItemDailySummary.objects.annotate(tag_keys=JSONBObjectKeys("tags"))
                .values("tags")
                .distinct()
                .all()
            )

            for tag in tags:
                for key in tag.get("tags").keys():
                    tag_keys.add(key)

        result = handler.get_tag_keys(filters=False)
        self.assertEqual(sorted(result), sorted(list(tag_keys)))

    def test_get_tag_keys_filter_false(self):
        """Test that all tag keys are returned with no filter."""
        url = "?filter[time_scope_units]=month&filter[time_scope_value]=-2&filter[resolution]=monthly"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)

        tag_keys = set()
        with tenant_context(self.tenant):
            tags = (
                AzureCostEntryLineItemDailySummary.objects.annotate(tag_keys=JSONBObjectKeys("tags"))
                .values("tags")
                .distinct()
                .all()
            )

            for tag in tags:
                for key in tag.get("tags").keys():
                    tag_keys.add(key)

        result = handler.get_tag_keys(filters=False)
        self.assertEqual(sorted(result), sorted(list(tag_keys)))

    def test_get_tags_for_key_filter(self):
        """Test that get tags runs properly with key query."""
        key = "app"
        url = f"?filter[key]={key}"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        with tenant_context(self.tenant):
            tags = AzureTagsSummary.objects.filter(key__exact=key).values("values").distinct().all()
            tag_values = tags[0].get("values")
        expected = {"key": key, "values": tag_values}
        result = handler.get_tags()
        self.assertEqual(result[0].get("key"), expected.get("key"))
        self.assertEqual(sorted(result[0].get("values") or [0]), sorted(expected.get("values") or [1]))

    def test_get_tag_values_for_value_filter(self):
        """Test that get tag values runs properly with value query."""
        key = "app"
        with tenant_context(self.tenant):
            tag = AzureTagsValues.objects.filter(key__exact=key).values("value").first()
        value = tag.get("value")
        url = f"?filter[value]={value}"
        query_params = self.mocked_query_params(url, AzureTagView)
        handler = AzureTagQueryHandler(query_params)
        handler.key = key
        with tenant_context(self.tenant):
            tags = AzureTagsValues.objects.filter(key__exact=key, value=value).values("value").distinct().all()
            tag_values = [tag.get("value") for tag in tags]
        expected = {"key": key, "values": tag_values}
        result = handler.get_tag_values()
        self.assertEqual(result[0].get("key"), expected.get("key"))
        self.assertEqual(sorted(result[0].get("values") or [0]), sorted(expected.get("values") or [1]))

    def test_get_tag_values_for_value_filter_partial_match(self):
        """Test that the execute query runs properly with value query."""
        key = "app"
        with tenant_context(self.tenant):
            tag = AzureTagsValues.objects.filter(key__exact=key).values("value").first()
        value = tag.get("value")[0]  # get first letter of value
        url = f"/{key}/?filter[value]={value}"
        query_params = self.mocked_query_params(url, AzureTagView)
        # the mocked query parameters dont include the key from the url so it needs to be added
        query_params.kwargs = {"key": key}
        handler = AzureTagQueryHandler(query_params)
        with tenant_context(self.tenant):
            tags = (
                AzureTagsValues.objects.filter(key__exact=key, value__icontains=value).values("value").distinct().all()
            )
            tag_values = [tag.get("value") for tag in tags]
        expected = {"key": key, "values": tag_values}
        result = handler.get_tag_values()
        self.assertEqual(result[0].get("key"), expected.get("key"))
        self.assertEqual(sorted(result[0].get("values") or [0]), sorted(expected.get("values") or [1]))
