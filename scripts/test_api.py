"""Test API script"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import httpx


def test_health(base_url: str):
    """Test health endpoint"""
    response = httpx.get(f"{base_url}/api/v1/health")
    print("Health check:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return response.status_code == 200


def test_qa(base_url: str, query: str):
    """Test QA endpoint"""
    print(f"\nQuestion: {query}")

    response = httpx.post(
        f"{base_url}/api/v1/qa",
        json={"query": query},
        timeout=30.0,
    )

    data = response.json()
    print("\nAnswer:")
    print(data["data"]["answer"])
    print("\nSources:")
    for source in data["data"]["sources"]:
        print(f"  - {source['title']} (score: {source['relevance_score']})")

    return response.status_code == 200


def test_retrieve(base_url: str, query: str, top_k: int = 5):
    """Test retrieve endpoint"""
    print(f"\nRetrieve: {query}")

    response = httpx.post(
        f"{base_url}/api/v1/retrieve",
        json={"query": query, "top_k": top_k},
        timeout=10.0,
    )

    data = response.json()
    print(f"\nFound {data['data']['total']} results:")
    for result in data["data"]["results"]:
        print(f"  - [{result['doc_title']}] {result['section_title']}")
        print(f"    Score: {result['final_score']:.3f}")

    return response.status_code == 200


def main():
    parser = argparse.ArgumentParser(description="Test MS-RAG API")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of API server",
    )
    parser.add_argument(
        "--query",
        default="模型训练很慢，怎么定位问题？",
        help="Query to test",
    )
    parser.add_argument(
        "--endpoint",
        choices=["health", "qa", "retrieve", "all"],
        default="all",
        help="Which endpoint to test",
    )

    args = parser.parse_args()

    print(f"Testing API at {args.url}")

    if args.endpoint in ["health", "all"]:
        test_health(args.url)

    if args.endpoint in ["qa", "all"]:
        test_qa(args.url, args.query)

    if args.endpoint in ["retrieve", "all"]:
        test_retrieve(args.url, args.query)


if __name__ == "__main__":
    main()