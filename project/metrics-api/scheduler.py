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
    # Prometheus 쿼리 → CPU 가장 낮은 노드 선택
    return "node3:9100"
def generate_dynamic_config():
    best_node = get_best_node()
    return f"""
http:
  routers:
    dynamic-router:
      rule: "Host(`whoami.local`)"
      service: dynamic-service
  services:
    dynamic-service:
      loadBalancer:
        servers:
          - url: "http://{best_node}"
