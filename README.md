
# IQA-Server 



```bash
IQA-Server/
├── README.md                          # ✅ Enhanced documentation
├── requirements.txt                   # ✅ Fixed filename and expanded deps
├── requirements-dev.txt               # 🆕 Development dependencies
├── setup.py                          # ✅ Updated with proper metadata
├── setup.cfg                         # 🆕 Configuration for tools
├── .gitignore                        # 🆕 Python gitignore
├── .pre-commit-config.yaml           # 🆕 Pre-commit hooks
├── pyproject.toml                    # 🆕 Modern Python project config
├── CHANGELOG.md                      # 🆕 Version history
├── LICENSE                           # 🆕 MIT License
├── docker/                           # 🆕 Docker deployment
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/                             # 🆕 Documentation
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── api.rst
│   │   └── examples.rst
│   └── build/
├── examples/                         # 🆕 Usage examples
│   ├── basic_usage.py
│   ├── batch_processing.py
│   └── custom_metrics.py
├── scripts/                          # 🆕 Utility scripts
│   ├── install_gpu_support.sh
│   └── benchmark.py
├── iqa_server/                       # Main package directory
│   ├── __init__.py                   # ✅ Enhanced package init
│   ├── main.py                       # 🆕 **CRITICAL: MCP server implementation**
│   ├── cli.py                        # 🆕 Command line interface
│   ├── server/                       # 🆕 MCP server components
│   │   ├── __init__.py
│   │   ├── mcp_server.py            # Core MCP server logic
│   │   ├── tools.py                 # MCP tool definitions
│   │   └── handlers.py              # Request handlers
│   ├── core/                        # 🆕 Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration management
│   │   ├── exceptions.py            # Custom exceptions
│   │   └── constants.py             # Application constants
│   ├── utils/                       # 🆕 Utility modules (referenced in README)
│   │   ├── __init__.py
│   │   ├── image_utils.py           # Image processing utilities
│   │   ├── metrics.py               # Core metric implementations
│   │   ├── validation.py            # Input validation
│   │   ├── logging.py               # Logging configuration
│   │   └── performance.py           # Performance monitoring
│   ├── indicators/                  # Refactored quality indicators
│   │   ├── __init__.py              # Enhanced exports
│   │   ├── base.py                  # 🆕 Abstract base classes
│   │   ├── traditional.py           # 🆕 Traditional metrics (PSNR, SSIM, MSE)
│   │   ├── perceptual.py           # 🆕 Perceptual metrics (LPIPS)
│   │   ├── no_reference.py         # 🆕 No-reference metrics
│   │   ├── interpretations.py       # 🆕 Metric interpretation system
│   │   └── indicators.py            # ✅ Refactored existing indicators
│   ├── mos/                         # Enhanced MOS module
│   │   ├── __init__.py              # Enhanced exports
│   │   ├── predictor.py             # 🆕 MOS prediction models
│   │   ├── models/                  # 🆕 Pre-trained models
│   │   │   ├── __init__.py
│   │   │   └── default_model.py
│   │   └── training.py              # 🆕 Model training utilities
│   ├── models/                      # 🆕 ML models and weights
│   │   ├── __init__.py
│   │   └── lpips/                   # LPIPS model weights
│   └── data/                        # 🆕 Sample data and configs
│       ├── __init__.py
│       ├── sample_images/
│       └── config_templates/
├── tests/                            # 🆕 **CRITICAL: Test suite**
│   ├── __init__.py
│   ├── conftest.py                  # Pytest configuration
│   ├── test_main.py                 # Test MCP server
│   ├── test_indicators/             # Test quality indicators
│   │   ├── __init__.py
│   │   ├── test_traditional.py
│   │   ├── test_perceptual.py
│   │   └── test_no_reference.py
│   ├── test_mos/                    # Test MOS module
│   │   ├── __init__.py
│   │   └── test_predictor.py
│   ├── test_utils/                  # Test utilities
│   │   ├── __init__.py
│   │   ├── test_image_utils.py
│   │   └── test_validation.py
│   ├── fixtures/                    # Test fixtures
│   │   ├── __init__.py
│   │   └── sample_images/
│   └── integration/                 # Integration tests
│       ├── __init__.py
│       └── test_mcp_integration.py
├── benchmarks/                      # 🆕 Performance benchmarks
│   ├── __init__.py
│   ├── metric_benchmarks.py
│   └── results/
└── .github/                         # 🆕 GitHub workflows
    └── workflows/
        ├── ci.yml                   # Continuous integration
        ├── release.yml              # Release automation
        └── docs.yml                 # Documentation builds
```