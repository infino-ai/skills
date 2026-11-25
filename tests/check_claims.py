"""Check the claims in search-with-infino's 'Mistakes to avoid' section against
the published Python package. Exits non-zero if any claim no longer holds."""
import sys, tempfile
import infino
import pyarrow as pa

failures = []


def claim(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'} {name} {detail}".rstrip())
    if not ok:
        failures.append(name)


def raises(fn):
    try:
        fn()
        return None
    except Exception as ex:  # noqa: BLE001
        return ex


schema = pa.schema([
    pa.field("doc_id", pa.large_utf8(), nullable=False),
    pa.field("tenant", pa.large_utf8(), nullable=False),
    pa.field("body", pa.large_utf8(), nullable=False),
    pa.field("embedding", pa.list_(pa.float32(), 16), nullable=False),
])
spec = infino.IndexSpec().fts("body").vector("embedding", 16, "cosine")
e = [1.0] + [0.0] * 15
row = lambda i, tenant, body: {"doc_id": i, "tenant": tenant, "body": body, "embedding": e}

with tempfile.TemporaryDirectory() as d:
    db = infino.connect(d)
    t = db.create_table("docs", schema, spec)
    t.append([row("1", "acme", "billing settings"), row("2", "other", "billing refunds")])

    claim("results default to _id and score",
          t.bm25_search("body", "billing", k=5).column_names == ["_id", "score"])
    claim("create_table fails when the table exists",
          raises(lambda: db.create_table("docs", schema, spec)) is not None)
    claim("open_table reopens it", db.open_table("docs").bm25_search("body", "billing", k=5).num_rows == 2)
    sql = "SELECT _id, score FROM bm25_search('docs', 'body', 'billing', 5) WHERE tenant = 'acme'"
    claim("bm25_search table function filters with WHERE", db.query_sql(sql).num_rows == 1)
    claim("a supplied _id is rejected",
          raises(lambda: t.append([{"_id": 5, **row("9", "a", "x")}])) is not None)
    claim("update and delete take a SQL predicate",
          t.delete("doc_id = '2'").matched == 1)

m = infino.connect("memory://")
mt = m.create_table("docs", schema, spec)
mt.append([row("1", "a", "x")])
claim("delete on memory:// is refused", raises(lambda: mt.delete("doc_id = '1'")) is not None)

with tempfile.TemporaryDirectory() as d:
    small = pa.schema([pa.field("embedding", pa.list_(pa.float32(), 8), nullable=False)])
    bad = raises(lambda: infino.connect(d).create_table(
        "v", small, infino.IndexSpec().vector("embedding", 8, "cosine")))
    claim("vector dim below 16 is rejected", bad is not None)

sys.exit(1 if failures else 0)
