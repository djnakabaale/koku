import logging

from django.db import connection
from django.db import models
from psycopg2.extras import RealDictCursor


# Future!
# CANCEL = "cancel"
# TERMINATE = "terminate"


LOG = logging.getLogger(__name__)


class PGRole(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_roles'

    oid = models.IntegerField(primary_key=True)
    rolname = models.TextField(null=False)


class PGDatabase(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_database'

    oid = models.IntegerField(primary_key=True)
    datname = models.TextField(null=False)


class PGStatStatements(models.Model):
    class Meta:
        managed = False
        db_table = 'public"."pg_stat_statements'

    user = models.ForeignKey("PGRole", db_column="userid", on_delete=models.DO_NOTHING)
    db = models.ForeignKey("PGDatabase", db_column="dbid", on_delete=models.DO_NOTHING)
    queryid = models.BigIntegerField(primary_key=True)
    query = models.TextField(null=True)
    calls = models.BigIntegerField(null=True)
    total_time = models.DecimalField(null=True)
    min_time = models.DecimalField(null=True)
    max_time = models.DecimalField(null=True)
    mean_time = models.DecimalField(null=True)
    stddev_time = models.DecimalField(null=True)
    rows = models.BigIntegerField(null=True)
    shared_blks_hit = models.BigIntegerField(null=True)
    shared_blks_read = models.BigIntegerField(null=True)
    shared_blks_dirtied = models.BigIntegerField(null=True)
    shared_blks_written = models.BigIntegerField(null=True)
    local_blks_hit = models.BigIntegerField(null=True)
    local_blks_read = models.BigIntegerField(null=True)
    local_blks_dirtied = models.BigIntegerField(null=True)
    local_blks_written = models.BigIntegerField(null=True)
    temp_blks_read = models.BigIntegerField(null=True)
    temp_blks_written = models.BigIntegerField(null=True)
    blk_read_time = models.DecimalField(null=True)
    blk_write_time = models.DecimalField(null=True)


class PGStatActivity(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_stat_activity'

    datid = models.IntegerField()
    datname = models.TextField()
    pid = models.IntegerField(primary_key=True)
    usesysid = models.IntegerField()
    usename = models.TextField()
    application_name = models.TextField()
    client_addr = models.TextField()
    client_hostname = models.TextField()
    client_port = models.IntegerField()
    backend_start = models.DateTimeField()
    xact_start = models.DateTimeField()
    query_start = models.DateTimeField()
    state_change = models.DateTimeField()
    wait_event_type = models.TextField()
    wait_event = models.TextField()
    state = models.TextField()
    backend_xid = models.BigIntegerField()
    backend_xmin = models.BigIntegerField()
    query = models.TextField()
    backend_type = models.TextField()


# BEGIN Future! MUST BE AUDITABLE WITH REAL USERNAME
# def manipulate_backend(backend_op, pids):
#     def quoteall(iterable):
#         return (f"'{val}'" for val in iterable)

#     allowed_ops = ("cancel", "terminate")
#     if backend_op not in allowed_ops:
#         raise ValueError(f"backend_op '{backend_op}' not one of {', '.join(quoteall(allowed_ops))}")

#     processed = []
#     with connection.cursor() as cur:
#         for pid in pids:
#             cur.execute(f"select pg_catalog.pg_{backend_op}_backend(%s) ;", (pid,))
#             res = cur.fetchone()
#             processed.append((pid, res[0]))

#     return processed


# def cancel_backend(pids):
#     return manipulate_backend(CANCEL, pids)


# def terminate_backend(pids):
#     return manipulate_backend(TERMINATE, pids)
# END Future! MUST BE AUDITABLE WITH REAL USERNAME


def get_blocked_process_info():
    sql = """
WITH lock_relations AS (
SELECT DISTINCT
       lock.pid,
       lock.relation as relid,
       format('%I.%I', rel.relnamespace::regnamespace::text, rel.relname::text) as relation
  FROM pg_catalog.pg_locks AS lock
  JOIN pg_catalog.pg_class AS rel
    ON rel.oid = lock.relation
   AND rel.relkind = any('{p,r}'::text[])
 WHERE lock.relation is not null
),
monitor_locks as (
SELECT blocked_locks.pid            AS blocked_pid,
       blocked_locks.locktype       AS blocked_locktype,
       blocked_locks.mode           AS blocked_lockmode,
       age(blocked_activity.query_start)::text AS blocked_query_duration,
       blocked_activity.usename     AS blocked_user,
       blocking_locks.pid           AS blocking_pid,
       blocked_locks.locktype       AS blocking_locktype,
       blocked_locks.mode           AS blocking_lockmode,
       blocking_activity.usename    AS blocking_user,
       blocked_activity.query       AS blocked_statement,
       blocking_activity.query      AS current_statement_in_blocking_process
  FROM pg_catalog.pg_locks          AS blocked_locks
  JOIN pg_catalog.pg_stat_activity  AS blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
  JOIN pg_catalog.pg_locks          AS blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
   AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
   AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
   AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
   AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
   AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
   AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
   AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
   AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
   AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
   AND blocking_locks.pid != blocked_locks.pid
  JOIN pg_catalog.pg_stat_activity blocking_activity
    ON blocking_activity.pid = blocking_locks.pid
 WHERE NOT blocked_locks.granted
)
SELECT l.blocked_pid,
       l.blocked_locktype,
       l.blocked_lockmode,
       l.blocked_query_duration,
       l.blocked_user,
       coalesce(bk.relation, '<UNKNOWN>') AS blocked_relation,
       l.blocking_pid,
       l.blocking_locktype,
       l.blocking_lockmode,
       l.blocking_user,
       l.blocked_statement,
       l.current_statement_in_blocking_process
  FROM monitor_locks AS l
  LEFT
  JOIN lock_relations AS bk
    ON bk.pid = l.blocked_pid
 ORDER
    BY "blocked_relation",
       "blocking_pid";
"""
    res = []
    LOG.info("Getting blocked, blocking lock process information")
    LOG.debug("Using psycopg2.extras.RealDictCursor")
    with connection.connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        res = cur.fetchall()

    return res
