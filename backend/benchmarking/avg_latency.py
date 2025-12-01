from warm_cold_test import warm_cold_runs

def avg_latency():
    result = warm_cold_runs(runs=10)
    avg = sum(result["times_ms"]) / len(result["times_ms"])
    return {
        "avg_latency_ms": avg,
        "all_runs_ms": result["times_ms"]
    }

if __name__ == "__main__":
    print(avg_latency())
