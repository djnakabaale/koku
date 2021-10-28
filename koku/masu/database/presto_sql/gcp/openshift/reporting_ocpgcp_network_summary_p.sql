-- Clear out old entries first
DELETE FROM postgres.{{schema | sqlsafe}}.reporting_ocpgcp_network_summary_p
WHERE usage_start >= date('{{start_date | sqlsafe}}')
    AND usage_start <= date('{{end_date | sqlsafe}}')
    AND invoice_month = '{{year | sqlsafe}}{{month | sqlsafe}}'
;

-- Populate the daily aggregate line item data
INSERT INTO postgres.{{schema | sqlsafe}}.reporting_ocpgcp_network_summary_p (
    uuid,
    cluster_id,
    cluster_alias,
    usage_start,
    usage_end,
    account_id,
    service_id,
    service_alias,
    unblended_cost,
    markup_cost,
    currency,
    source_uuid,
    credit_amount,
    invoice_month
)
    SELECT uuid(),
        cluster_id,
        cluster_alias,
        usage_start,
        usage_end,
        account_id,
        service_id,
        service_alias,
        sum(unblended_cost) as unblended_cost,
        sum(markup_cost) as markup_cost,
        max(currency) as currency,
        source_uuid,
        sum(credit_amount) as credit_amount,
        invoice_month
    FROM postgres.{{schema | sqlsafe}}.reporting_ocpgcpcostlineitem_daily_summary
    -- Get data for this month or last month
    WHERE service_alias LIKE '%%Network%%'
        OR service_alias LIKE '%%VPC%%'
        OR service_alias LIKE '%%Firewall%%'
        OR service_alias LIKE '%%Route%%'
        OR service_alias LIKE '%%IP%%'
        OR service_alias LIKE '%%DNS%%'
        OR service_alias LIKE '%%CDN%%'
        OR service_alias LIKE '%%NAT%%'
        OR service_alias LIKE '%%Traffic Director%%'
        OR service_alias LIKE '%%Service Discovery%%'
        OR service_alias LIKE '%%Cloud Domains%%'
        OR service_alias LIKE '%%Private Service Connect%%'
        OR service_alias LIKE '%%Cloud Armor%%'
        AND usage_start >= date('{{start_date | sqlsafe}}')
        AND usage_start <= date('{{end_date | sqlsafe}}')
        AND invoice_month = '{{year | sqlsafe}}{{month | sqlsafe}}'
    GROUP BY cluster_id,
        cluster_alias,
        usage_start,
        usage_end,
        account_id,
        service_id,
        service_alias,
        source_uuid,
        invoice_month
;
