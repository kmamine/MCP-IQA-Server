Examples
========

This section provides examples of how to use MCP-IQA-Server in various scenarios.

Basic Usage
----------

Here's a simple example of using the server to analyze image quality:

.. literalinclude:: ../../examples/basic_usage.py
   :language: python
   :caption: basic_usage.py
   :linenos:

Batch Processing
--------------

For processing multiple images efficiently:

.. literalinclude:: ../../examples/batch_processing.py
   :language: python
   :caption: batch_processing.py
   :linenos:

Custom Metrics
------------

Implementing custom quality metrics:

.. literalinclude:: ../../examples/custom_metrics.py
   :language: python
   :caption: custom_metrics.py
   :linenos:

Docker Deployment
--------------

To run the server using Docker:

.. code-block:: bash

   # Build the Docker image
   docker build -t mcp-iqa-server -f docker/Dockerfile .

   # Run the server
   docker run -p 50051:50051 mcp-iqa-server

Using Docker Compose:

.. code-block:: bash

   docker-compose -f docker/docker-compose.yml up

GPU Support
---------

To enable GPU support:

1. Install NVIDIA drivers and CUDA toolkit
2. Run the GPU support installation script:

   .. code-block:: bash

      ./scripts/install_gpu_support.sh

3. Set the CUDA_VISIBLE_DEVICES environment variable:

   .. code-block:: bash

      export CUDA_VISIBLE_DEVICES=0

Performance Benchmarking
---------------------

To run performance benchmarks:

.. code-block:: bash

   python scripts/benchmark.py \
       --images-dir path/to/test/images \
       --batch-sizes 1 4 8 16 \
       --output benchmarks/results/benchmark_results.json