import logging

from django.db import connection
from django.db import models

# import os


CANCEL = "cancel"
TERMINATE = "terminate"


LOG = logging.getLogger(__name__)


# @models.Field.register_lookup
# class IsDistinctFrom(models.Lookup):
#     lookup_name = "is_distinct_from"

#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params

#         return f"{lhs} IS DISTINCT FROM {rhs}", params


# @models.Field.register_lookup
# class IsNotDistinctFrom(models.Lookup):
#     lookup_name = "is_not_distinct_from"

#     def as_sql(self, compiler, connection):
#         lhs, lhs_params = self.process_lhs(compiler, connection)
#         rhs, rhs_params = self.process_rhs(compiler, connection)
#         params = lhs_params + rhs_params

#         return f"{lhs} IS NOT DISTINCT FROM {rhs}", params


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
        db_table = "public.pg_stat_statements"

    user = models.ForeignKey("PGRole", db_column="userid", on_delete=models.DO_NOTHING)
    db = models.ForeignKey("PGDatabase", db_column="dbid", on_delete=models.DO_NOTHING)
    queryid = models.BigIntegerField(primary_key=True)
    query = models.TextField(null=True)
    calls = models.BigIntegerField(null=True)
    total_time = models.DecimalField(null=True)
    min_time = models.DecimalField(null=True)
    max_time = models.DecimalField(null=True)
    mean_time = models.DecimalField(null=True)
    stdev_time = models.DecimalField(null=True)
    rows = models.BigIntegerField(null=True)
    shared_blocks_hit = models.BigIntegerField(null=True)
    shared_blocks_read = models.BigIntegerField(null=True)
    shared_blocks_dirtied = models.BigIntegerField(null=True)
    shared_blocks_written = models.BigIntegerField(null=True)
    local_blocks_hit = models.BigIntegerField(null=True)
    local_blocks_read = models.BigIntegerField(null=True)
    local_blocks_dirtied = models.BigIntegerField(null=True)
    local_blocks_written = models.BigIntegerField(null=True)
    temp_blocks_read = models.BigIntegerField(null=True)
    temp_blocks_written = models.BigIntegerField(null=True)
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


class PGNamespace(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_namespace'

    oid = models.IntegerField(primary_key=True)
    nspname = models.TextField()


class PGClass(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_class'

    oid = models.IntegerField(primary_key=True)
    relname = models.TextField()
    relnamespace = models.ForeignKey("PGNamespace", db_column="relnamespace", on_delete=models.DO_NOTHING)
    relkind = models.CharField()
    relispartition = models.BooleanField()
    relhasrules = models.BooleanField()
    relhastriggers = models.BooleanField()
    relpages = models.IntegerField()
    reltuples = models.DecimalField()


class PGLocks(models.Model):
    class Meta:
        managed = False
        db_table = 'pg_catalog"."pg_locks'

    locktype = models.TextField()
    database = models.IntegerField()
    relation = models.ForeignKey("PGClass", db_column="relation", on_delete=models.DO_NOTHING, null=True)
    page = models.IntegerField(null=True)
    tuple = models.SmallIntegerField(null=True)
    virtualxid = models.TextField(null=True)
    classid = models.IntegerField(null=True)
    objid = models.IntegerField(null=True)
    objsubid = models.IntegerField(null=True)
    virtualtransaction = models.TextField(null=True)
    pid = models.ForeignKey("PGStatStatements", db_column="pid", primary_key=True, on_delete=models.DO_NOTHING)
    mode = models.TextField()
    granted = models.BooleanField()
    fastpath = models.BooleanField()


def manipulate_backend(backend_op, pids):
    def quoteall(iterable):
        return (f"'{val}'" for val in iterable)

    allowed_ops = ("cancel", "terminate")
    if backend_op not in allowed_ops:
        raise ValueError(f"backend_op '{backend_op}' not one of {', '.join(quoteall(allowed_ops))}")

    processed = []
    with connection.cursor() as cur:
        for pid in pids:
            cur.execute(f"select pg_catalog.pg_{backend_op}_backend(%s) ;", (pid,))
            res = cur.fetchone()
            processed.append((pid, res[0]))

    return processed


def cancel_backend(pids):
    return manipulate_backend(CANCEL, pids)


def terminate_backend(pids):
    return manipulate_backend(TERMINATE, pids)


class BlockingProcesses:
    def __init__(self, blocked_pid, blocked_locktype, blocked_query, blocking_pid, blocking_locktype, blocking_query):
        self.blocked_pid = blocked_pid
        self.blocked_locktype = blocked_locktype
        self.blocked_query = blocked_query
        self.blocking_pid = blocking_pid
        self.blocking_locktype = blocking_locktype
        self.blocking_query = blocking_query

    def __str__(self):
        # txt = f"Blocked Pid {self.blocked_pid} Locktype {self.blocked_locktype}
        # Query {self.blocked_query[:50]}{os.linesep}"
        # txt2 = f"Blocked by Pid {self.blocking_pid} Locktype {self.blocking_locktype}
        # Query {self.blocking_query[:50]}"
        txt = "eek"
        txt2 = "eek2"
        return txt + txt2

    def __repr__(self):
        return str(self)


def get_blocked_process_info():
    def blocking_match(p1, p2):
        return (
            p1.locktype == p2.locktype
            and p1.database == p2.database
            and p1.relation.oid == p2.relation.oid
            and p1.page == p2.page
            and p1.tuple == p2.tuple
            and p1.virtualxid == p2.virtualxid
            and p1.transactionid == p2.transactionid
            and p1.classid == p2.classid
            and p1.objid == p2.objid
            and p1.objsubid == p2.objsubid
            and p1.pid.pid != p2.pid.pid
        )

    blocked = PGLocks.objects.all().select_related("relation").select_related("pid")
    blocking_info = []
    blkg_seen = set()
    for blok in blocked:
        for blkg_ix, blkg in enumerate(blocked):
            if blkg_ix in blkg_seen:
                continue
            if blocking_match(blok, blkg):
                blkg_seen.add(blkg_ix)
                blocking_info.append(
                    BlockingProcesses(blok.pid.pid, blok.locktype, blok.query, blkg.pid.pid, blkg.locktype, blkg.query)
                )

    return blocking_info


# SELECT blocked_locks.pid     AS blocked_pid,
#          blocked_activity.usename  AS blocked_user,
#          blocking_locks.pid     AS blocking_pid,
#          blocking_activity.usename AS blocking_user,
#          blocked_activity.query    AS blocked_statement,
#          blocking_activity.query   AS current_statement_in_blocking_process
#    FROM  pg_catalog.pg_locks         blocked_locks
#     JOIN pg_catalog.pg_stat_activity blocked_activity  ON blocked_activity.pid = blocked_locks.pid
#     JOIN pg_catalog.pg_locks         blocking_locks
#         ON blocking_locks.locktype = blocked_locks.locktype
#         AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
#         AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
#         AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
#         AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
#         AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
#         AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
#         AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
#         AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
#         AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
#         AND blocking_locks.pid != blocked_locks.pid

#     JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
#    WHERE NOT blocked_locks.granted;

# table=SomeModel._meta.db_table
# join_column_1=SomeModel._meta.get_field('field1').column
# join_column_2=SomeModel._meta.get_field('field2').column
# join_queryset=SomeModel.objects.filter()
# # Force evaluation of query
# querystr=join_queryset.query.__str__()
# # Add promote=True and nullable=True for left outer join
# rh_alias=join_queryset.query.join((table,table,join_column_1,join_column_2))
# # Add the second conditional and columns
# join_queryset=join_queryset.extra(select=dict(rhs_col1='%s.%s' % (rhs,join_column_2)),
#     where=['%s.%s = %s.%s' % (table,join_column_2,rh_alias,join_column_1)])
