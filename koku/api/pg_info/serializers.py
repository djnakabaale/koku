from rest_framework import serializers

from koku.database import get_model


QUERY_MAX_LEN = 25000
NAME_MAX_LEN = 64


PGRole = get_model("PGRole")
PGDatabase = get_model("PGDatabase")
PGStatStatements = get_model("PGStatStatements")
PGStatActivity = get_model("PGStatActivity")


class PGRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGRole
        fields = ("oid", "username")

    oid = serializers.IntegerField()
    username = serializers.CharField(max_length=NAME_MAX_LEN, source="rolname")


class PGDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGDatabase
        fields = ("oid", "database")

    oid = serializers.IntegerField()
    database = serializers.CharField(max_length=NAME_MAX_LEN, source="datname")


class PGStatStatementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGStatStatements
        fields = tuple(f.name for f in PGStatStatements._meta.fields)

    user = PGRoleSerializer()
    db = PGDatabaseSerializer()
    queryid = serializers.IntegerField()
    query = serializers.CharField(max_length=QUERY_MAX_LEN)
    calls = serializers.IntegerField()
    total_time = serializers.DecimalField(20, 10, allow_null=True)
    min_time = serializers.DecimalField(20, 10, allow_null=True)
    max_time = serializers.DecimalField(20, 10, allow_null=True)
    mean_time = serializers.DecimalField(20, 10, allow_null=True)
    stddev_time = serializers.DecimalField(20, 10, allow_null=True)
    rows = serializers.IntegerField(allow_null=True)
    shared_blks_hit = serializers.IntegerField(allow_null=True)
    shared_blks_read = serializers.IntegerField(allow_null=True)
    shared_blks_dirtied = serializers.IntegerField(allow_null=True)
    shared_blks_written = serializers.IntegerField(allow_null=True)
    local_blks_hit = serializers.IntegerField(allow_null=True)
    local_blks_read = serializers.IntegerField(allow_null=True)
    local_blks_dirtied = serializers.IntegerField(allow_null=True)
    local_blks_written = serializers.IntegerField(allow_null=True)
    temp_blks_read = serializers.IntegerField(allow_null=True)
    temp_blks_written = serializers.IntegerField(allow_null=True)
    blk_read_time = serializers.DecimalField(20, 10, allow_null=True)
    blk_write_time = serializers.DecimalField(20, 10, allow_null=True)


class PGStatActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PGStatActivity
        fields = tuple(f.name for f in PGStatActivity._meta.fields)

    datid = serializers.IntegerField()
    datname = serializers.CharField(max_length=NAME_MAX_LEN)
    pid = serializers.IntegerField()
    usesysid = serializers.IntegerField()
    usename = serializers.CharField(max_length=NAME_MAX_LEN)
    application_name = serializers.CharField(max_length=NAME_MAX_LEN)
    client_addr = serializers.CharField(max_length=NAME_MAX_LEN)
    client_hostname = serializers.CharField(max_length=NAME_MAX_LEN)
    client_port = serializers.IntegerField()
    backend_start = serializers.DateTimeField()
    xact_start = serializers.DateTimeField()
    query_start = serializers.DateTimeField()
    state_change = serializers.DateTimeField()
    wait_event_type = serializers.CharField(max_length=NAME_MAX_LEN)
    wait_event = serializers.CharField(max_length=NAME_MAX_LEN)
    state = serializers.CharField(max_length=NAME_MAX_LEN)
    backend_xid = serializers.IntegerField()
    backend_xmin = serializers.IntegerField()
    query = serializers.CharField(max_length=QUERY_MAX_LEN)
    backend_type = serializers.CharField(max_length=QUERY_MAX_LEN)


class PGLocksSerializer(serializers.Serializer):
    class Meta:
        fields = (
            "blocked_pid",
            "blocked_locktype",
            "blocked_lockmode",
            "blocked_transaction_duration",
            "blocked_query_duration",
            "blocked_user",
            "blocked_relation",
            "blocking_pid",
            "blocking_locktype",
            "blocking_lockmode",
            "blocking_user",
            "blocked_statement",
            "current_statement_in_blocking_process",
        )

    blocked_pid = serializers.IntegerField()
    blocked_locktype = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_lockmode = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_transaction_duration = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_query_duration = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_user = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_relation = serializers.CharField(max_length=NAME_MAX_LEN)
    locking_pid = serializers.IntegerField()
    blocking_locktype = serializers.CharField(max_length=NAME_MAX_LEN)
    blocking_lockmode = serializers.CharField(max_length=NAME_MAX_LEN)
    blocking_user = serializers.CharField(max_length=NAME_MAX_LEN)
    blocked_statement = serializers.CharField(max_length=QUERY_MAX_LEN)
    current_statement_in_blocking_process = serializers.CharField(max_length=QUERY_MAX_LEN)
