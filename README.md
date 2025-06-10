# IQA Server for AI Agents 
### An MCP server for Image Quality Assessment

This repository contains a Model Context Protocol (MCP) server that provides access to Image Quality Assessment (IQA) models through the PyIQA library. It allows AI agents to discover and get information about various IQA metrics, including Full Reference (FR), No Reference (NR), and task-specific methods.

## Features

- Access to a comprehensive database of IQA models
- Support for multiple types of IQA metrics:
  - Full Reference (FR) methods
  - No Reference (NR) methods
  - Task-specific methods (Color, Face, Underwater)
- Model search and discovery capabilities
- Detailed model information and usage examples
- MCP-compliant API for seamless integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mcp-iqa-server.git
cd mcp-iqa-server
```

2. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage

Start the server:
```bash
python iqa_server.py
```

The server will start and listen for MCP commands on stdin/stdout.

## Available Resources

- `iqa://models/all` - Complete list of all available IQA models
- `iqa://models/fr` - List of Full Reference (FR) IQA models
- `iqa://models/nr` - List of No Reference (NR) IQA models
- `iqa://models/specific` - List of task-specific IQA models

## Available Tools

1. `search_models` - Search for IQA models by name, type, or category
2. `get_model_info` - Get detailed information about a specific IQA model
3. `list_model_names` - Get all available model names for pyiqa.create_metric()
4. `get_usage_example` - Get usage examples for IQA models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



