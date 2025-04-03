import requests

PROMETHEUS_URL = "http://prometheus:9090"
QUERY = '100 - avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100'

def get_node_cpu_usage():
    res = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": QUERY})
    res.raise_for_status()
    result = res.json()["data"]["result"]

    usage = []
    for item in result:
        instance = item["metric"]["instance"]
        value = float(item["value"][1])
        usage.append((instance, value))
    return usage

def get_best_node():
    usage = get_node_cpu_usage()
    # CPU 사용률이 가장 낮은 노드를 선택
    best_node = min(usage, key=lambda x: x[1])
    return best_node[0]  # IP:port 형식