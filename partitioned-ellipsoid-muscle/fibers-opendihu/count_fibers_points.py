import json

json_path = "fibers4.json"

with open(json_path, "r") as f:
    data = json.load(f)

fibers = []

# --------------------------------------------------
# Find fibers: lists of dicts with x/y/z keys
# --------------------------------------------------
def find_fibers(obj):
    if isinstance(obj, list):
        if (
            obj
            and isinstance(obj[0], dict)
            and {"x", "y", "z"} <= obj[0].keys()
        ):
            fibers.append(obj)
            return
        for v in obj:
            find_fibers(v)

    elif isinstance(obj, dict):
        for v in obj.values():
            find_fibers(v)

find_fibers(data)

# --------------------------------------------------
# Report
# --------------------------------------------------
print(f"Total fibers found: {len(fibers)}\n")

total_points = 0
for i, fiber in enumerate(fibers):
    n = len(fiber)
    total_points += n
    print(f"Fiber {i:4d}: {n} points")

print("\nSummary:")
print("--------")
print(f"Total fibers : {len(fibers)}")
print(f"Total points : {total_points}")
print(f"Min points   : {min(len(f) for f in fibers)}")
print(f"Max points   : {max(len(f) for f in fibers)}")
print(f"Avg points   : {total_points / len(fibers):.2f}")