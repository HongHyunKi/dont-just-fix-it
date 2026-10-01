def total_for_ids(rows, ids):
    return sum(next(row["value"] for row in rows if row["id"] == key) for key in ids)
