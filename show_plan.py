import json

def display_query_plan_results(plan_data, literals, metrics , query , cache_hits_of_current_query):
    """
    Pretty prints query plans (outer + inner), literals, and cache metrics.
    """
    print("\n" + "=" * 80)
    print(" # QUERY PLAN RESULTS for : " , query)
    print("=" * 80)

    # --- Handle outer and inner plans ---
    if isinstance(plan_data, dict):
        for k, v in plan_data.items():
            if k == "Inner Query Plans : ":
                print("\n Inner Query Plans:")
                for subq, subplan in v.items():
                    print(f"\n   Subquery: {subq}")
                    try:
                        print(json.dumps(json.loads(subplan), indent=6))
                    except Exception:
                        print("    (Invalid JSON format)")
            else:
                print(f"\n Outer Query: {k}")
                try:
                    print(json.dumps(json.loads(v), indent=6))
                except Exception:
                    print("    (Invalid JSON format)")
    else:
        # Single plan (no nested dicts)
        try:
            print(json.dumps(json.loads(plan_data), indent=6))
        except Exception:
            print(plan_data)

    # --- Print literals ---
    print("\n" + "-" * 80)
    print("# Extracted Literals:")
    print("   ", literals if literals else "None")

    # --- Print cache metrics ---
    print("Cache hits for current query : " , cache_hits_of_current_query)
    print("\n" + "-" * 80)
    print("# Cache Metrics:")
    for key, val in metrics.items():
        print(f"   {key.capitalize():<10}: {val}")

    print("=" * 80 + "\n")
