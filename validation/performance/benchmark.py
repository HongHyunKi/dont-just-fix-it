import json, platform, sys, time
from before import total_for_ids as before
from after import total_for_ids as after
rows = [{"id": i, "value": i % 7} for i in range(20000)]
ids = list(range(15000, 15500))
assert before(rows, ids) == after(rows, ids)
runs = {"before": [], "after": []}
for _ in range(5):
    for name, fn in [("before", before), ("after", after)]:
        start = time.perf_counter()
        fn(rows, ids)
        runs[name].append((time.perf_counter() - start) * 1000)
print(json.dumps({"synthetic_fixture": True, "unit": "ms", "rows": len(rows), "lookups": len(ids), "python": sys.version, "platform": platform.platform(), "runs": runs}, indent=2))
