MCP-IQA-Server Documentation
============================

Welcome to MCP-IQA-Server's documentation. This server provides an implementation of the Model Context Protocol (MCP) for Image Quality Assessment.

Features
--------

- Multiple image quality indicators (Traditional, No-Reference, Perceptual)
- Mean Opinion Score (MOS) prediction using deep learning
- High-performance batch processing
- GPU acceleration support
- Docker deployment support
- Prometheus metrics integration
- Comprehensive API for image quality analysis

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api
   examples
   deployment
   contributing

Installation
-----------

You can install MCP-IQA-Server using pip:

.. code-block:: bash

   pip install mcp-iqa-server

For development installation:

.. code-block:: bash

   git clone https://github.com/yourusername/mcp-iqa-server.git
   cd mcp-iqa-server
   pip install -e ".[dev]"

Quick Start
----------

Here's a simple example of using the server:

.. code-block:: python

   from iqa_server.client import IQAClient
   
   # Create a client
   client = IQAClient("localhost:50051")
   
   # Analyze image quality
   result = client.analyze_image("path/to/image.jpg")
   print(f"Image quality score: {result.quality_score}")

For more examples, see the :doc:`examples` section.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`