import requests

PROMETHEUS_URL = "http://prometheus:9090"
QUERY = '100 * (1 - avg by (instance)(rate(node_cpu_seconds_total{mode="idle"}[20s])))'

def get_node_cpu_usage():
    try:
        res = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": QUERY})
        res.raise_for_status()
        result = res.json()["data"]["result"]

        usage = []
        for item in result:
            instance = item["metric"]["instance"]
            value = float(item["value"][1])  # CPU 사용률 (%)
            usage.append((instance, value))
        return usage
    except Exception as e:
        print(f"[ERROR] Prometheus 쿼리 실패: {e}")
        return []

def get_best_node():
    usage = get_node_cpu_usage()
    if not usage:
        return "localhost:80"  # fallback

    # 가장 CPU 사용률 낮은 노드 선택
    best_node = min(usage, key=lambda x: x[1])
    print(f"[INFO] Best node: {best_node[0]} (CPU: {best_node[1]:.2f}%)")
    return best_node[0]

def generate_dynamic_config():
    best_node = get_best_node()
    return f"""\
http:
  routers:
    dynamic-router:
      rule: "Host(`whoami.local`)"
      service: dynamic-service
  services:
    dynamic-service:
      loadBalancer:
        servers:
          - url: "http://{best_node}:8000"
"""
