def total_for_ids(rows, ids):
    by_id = {row["id"]: row["value"] for row in rows}
    return sum(by_id[key] for key in ids)
