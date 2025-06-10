#!/usr/bin/env python3

import argparse
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import grpc

from iqa_server.server.handlers import create_image_quality_request
from iqa_server.core.config import load_config
from iqa_server.utils.performance import measure_latency, measure_memory
from iqa_server.utils.image_utils import load_image_batch
import iqa_server.server.mcp_server_pb2_grpc as pb2_grpc
import iqa_server.server.mcp_server_pb2 as pb2

def run_single_benchmark(client_stub, image_path, batch_size, num_iterations=100):
    """Run a single benchmark case."""
    images = load_image_batch(image_path, batch_size)
    request = create_image_quality_request(images)
    
    latencies = []
    memory_usages = []
    
    for _ in range(num_iterations):
        start_time = time.time()
        response = client_stub.AnalyzeImageQuality(request)
        latency = time.time() - start_time
        latencies.append(latency)
        
        memory_usage = measure_memory()
        memory_usages.append(memory_usage)
    
    return {
        'mean_latency': np.mean(latencies),
        'p95_latency': np.percentile(latencies, 95),
        'p99_latency': np.percentile(latencies, 99),
        'mean_memory': np.mean(memory_usages),
        'max_memory': max(memory_usages)
    }

def main():
    parser = argparse.ArgumentParser(description='Benchmark MCP-IQA-Server')
    parser.add_argument('--host', default='localhost:50051', help='Server address')
    parser.add_argument('--images-dir', type=str, required=True, help='Directory containing test images')
    parser.add_argument('--batch-sizes', type=int, nargs='+', default=[1, 4, 8, 16], help='Batch sizes to test')
    parser.add_argument('--output', type=str, default='benchmarks/results/benchmark_results.json',
                       help='Output file for results')
    args = parser.parse_args()

    # Setup gRPC channel
    channel = grpc.insecure_channel(args.host)
    stub = pb2_grpc.ImageQualityServiceStub(channel)
    
    results = {}
    images_dir = Path(args.images_dir)
    
    for batch_size in args.batch_sizes:
        print(f"Running benchmark with batch size {batch_size}...")
        results[f'batch_{batch_size}'] = run_single_benchmark(
            stub, 
            images_dir, 
            batch_size
        )
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate summary report
    df = pd.DataFrame(results).T
    print("\nBenchmark Results Summary:")
    print(df.to_string())
    
    # Save CSV report
    csv_path = output_path.with_suffix('.csv')
    df.to_csv(csv_path)
    print(f"\nDetailed results saved to: {output_path} and {csv_path}")

if __name__ == '__main__':
    main()