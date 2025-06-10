#!/usr/bin/env python3
"""
IQA-PyTorch MCP Server

This server provides access to Image Quality Assessment (IQA) model information
from the IQA-PyTorch library through the Model Context Protocol.
"""

import asyncio
import mcp.server.stdio
from iqa_server import IQAServer

# IQA Model Database
IQA_MODELS = {
    # Full Reference (FR) Methods
    "fr_methods": {
        "topiq_fr": {
            "type": "FR",
            "names": ["topiq_fr", "topiq_fr-pipal"],
            "description": "TOPIQ Full Reference method - Proposed in the TOPIQ paper",
            "category": "General FR"
        },
        "ahiq": {
            "type": "FR", 
            "names": ["ahiq"],
            "description": "AHIQ Full Reference method",
            "category": "General FR"
        },
        "pieapp": {
            "type": "FR",
            "names": ["pieapp"],
            "description": "PieAPP Full Reference method",
            "category": "General FR"
        },
        "lpips": {
            "type": "FR",
            "names": ["lpips", "lpips-vgg", "stlpips", "stlpips-vgg", "lpips+", "lpips-vgg+"],
            "description": "LPIPS (Learned Perceptual Image Patch Similarity) variants",
            "category": "General FR"
        },
        "dists": {
            "type": "FR",
            "names": ["dists"],
            "description": "DISTS Full Reference method",
            "category": "General FR"
        },
        "wadiqam_fr": {
            "type": "FR",
            "names": ["wadiqam_fr"],
            "description": "WaDIQaM Full Reference method",
            "category": "General FR"
        },
        "ckdn": {
            "type": "FR",
            "names": ["ckdn"],
            "description": "CKDN Full Reference method - Uses distorted image as reference",
            "category": "General FR",
            "note": "This method uses distorted image as reference"
        },
        "fsim": {
            "type": "FR",
            "names": ["fsim"],
            "description": "FSIM (Feature Similarity Index) Full Reference method",
            "category": "General FR"
        },
        "ssim": {
            "type": "FR",
            "names": ["ssim", "ssimc"],
            "description": "SSIM (Structural Similarity Index) - Gray input (y channel) and color input variants",
            "category": "General FR"
        },
        "ms_ssim": {
            "type": "FR",
            "names": ["ms_ssim"],
            "description": "MS-SSIM (Multi-Scale Structural Similarity Index)",
            "category": "General FR"
        },
        "cw_ssim": {
            "type": "FR",
            "names": ["cw_ssim"],
            "description": "CW-SSIM (Complex Wavelet Structural Similarity Index)",
            "category": "General FR"
        },
        "psnr": {
            "type": "FR",
            "names": ["psnr", "psnry"],
            "description": "PSNR (Peak Signal-to-Noise Ratio) - Color input and gray input (y channel) variants",
            "category": "General FR"
        },
        "vif": {
            "type": "FR",
            "names": ["vif"],
            "description": "VIF (Visual Information Fidelity)",
            "category": "General FR"
        },
        "gmsd": {
            "type": "FR",
            "names": ["gmsd"],
            "description": "GMSD (Gradient Magnitude Similarity Deviation)",
            "category": "General FR"
        },
        "nlpd": {
            "type": "FR",
            "names": ["nlpd"],
            "description": "NLPD (Normalized Laplacian Pyramid Distance)",
            "category": "General FR"
        },
        "vsi": {
            "type": "FR",
            "names": ["vsi"],
            "description": "VSI (Visual Saliency Index)",
            "category": "General FR"
        },
        "mad": {
            "type": "FR",
            "names": ["mad"],
            "description": "MAD (Most Apparent Distortion)",
            "category": "General FR"
        }
    },
    
    # No Reference (NR) Methods
    "nr_methods": {
        "qalign": {
            "type": "NR",
            "names": ["qalign"],
            "description": "Q-Align - Large vision-language models with quality (default) and aesthetic options",
            "category": "General NR"
        },
        "qualiclip": {
            "type": "NR",
            "names": ["qualiclip", "qualiclip+", "qualiclip+-clive", "qualiclip+-flive", "qualiclip+-spaq"],
            "description": "QualiCLIP(+) with different datasets, koniq by default",
            "category": "General NR"
        },
        "liqe": {
            "type": "NR",
            "names": ["liqe", "liqe_mix"],
            "description": "LIQE - CLIP based method",
            "category": "General NR"
        },
        "arniqa": {
            "type": "NR",
            "names": ["arniqa", "arniqa-live", "arniqa-csiq", "arniqa-tid", "arniqa-kadid", "arniqa-clive", "arniqa-flive", "arniqa-spaq"],
            "description": "ARNIQA with different datasets, koniq by default",
            "category": "General NR"
        },
        "topiq_nr": {
            "type": "NR",
            "names": ["topiq_nr", "topiq_nr-flive", "topiq_nr-spaq"],
            "description": "TOPIQ No Reference with different datasets, koniq by default",
            "category": "General NR"
        },
        "tres": {
            "type": "NR",
            "names": ["tres", "tres-flive"],
            "description": "TReS with different datasets, koniq by default",
            "category": "General NR"
        },
        "fid": {
            "type": "NR",
            "names": ["fid"],
            "description": "FID (Fréchet Inception Distance) - Statistic distance between two datasets",
            "category": "General NR"
        },
        "clipiqa": {
            "type": "NR",
            "names": ["clipiqa", "clipiqa+", "clipiqa+_vitL14_512", "clipiqa+_rn50_512"],
            "description": "CLIPIQA(+) with different backbone, RN50 by default",
            "category": "General NR"
        },
        "maniqa": {
            "type": "NR",
            "names": ["maniqa", "maniqa-kadid", "maniqa-pipal"],
            "description": "MANIQA with different datasets, koniq by default",
            "category": "General NR"
        },
        "musiq": {
            "type": "NR",
            "names": ["musiq", "musiq-spaq", "musiq-paq2piq", "musiq-ava"],
            "description": "MUSIQ with different datasets, koniq by default",
            "category": "General NR"
        },
        "dbcnn": {
            "type": "NR",
            "names": ["dbcnn"],
            "description": "DBCNN No Reference method",
            "category": "General NR"
        },
        "paq2piq": {
            "type": "NR",
            "names": ["paq2piq"],
            "description": "PaQ-2-PiQ No Reference method",
            "category": "General NR"
        },
        "hyperiqa": {
            "type": "NR",
            "names": ["hyperiqa"],
            "description": "HyperIQA No Reference method",
            "category": "General NR"
        },
        "nima": {
            "type": "NR",
            "names": ["nima", "nima-vgg16-ava"],
            "description": "NIMA - Aesthetic metric trained with AVA dataset",
            "category": "General NR"
        },
        "wadiqam_nr": {
            "type": "NR",
            "names": ["wadiqam_nr"],
            "description": "WaDIQaM No Reference method",
            "category": "General NR"
        },
        "cnniqa": {
            "type": "NR",
            "names": ["cnniqa"],
            "description": "CNNIQA No Reference method",
            "category": "General NR"
        },
        "nrqm": {
            "type": "NR",
            "names": ["nrqm"],
            "description": "NRQM(Ma) - No backward support",
            "category": "General NR",
            "backward_support": False
        },
        "pi": {
            "type": "NR",
            "names": ["pi"],
            "description": "PI (Perceptual Index) - No backward support",
            "category": "General NR",
            "backward_support": False
        },
        "brisque": {
            "type": "NR",
            "names": ["brisque", "brisque_matlab"],
            "description": "BRISQUE - No backward support",
            "category": "General NR",
            "backward_support": False
        },
        "ilniqe": {
            "type": "NR",
            "names": ["ilniqe"],
            "description": "ILNIQE - No backward support",
            "category": "General NR",
            "backward_support": False
        },
        "niqe": {
            "type": "NR",
            "names": ["niqe", "niqe_matlab"],
            "description": "NIQE - No backward support",
            "category": "General NR",
            "backward_support": False
        },
        "piqe": {
            "type": "NR",
            "names": ["piqe"],
            "description": "PIQE - No backward support",
            "category": "General NR",
            "backward_support": False
        }
    },
    
    # Specific Task Methods
    "specific_methods": {
        "msswd": {
            "type": "Specific",
            "names": ["msswd"],
            "description": "MS-SWD - Perceptual color difference metric, ECCV2024",
            "category": "Color IQA",
            "paper_info": "ECCV2024, Arxiv, Github"
        },
        "topiq_nr_face": {
            "type": "Specific",
            "names": ["topiq_nr-face"],
            "description": "TOPIQ model trained with face IQA dataset (GFIQA)",
            "category": "Face IQA"
        },
        "uranker": {
            "type": "Specific",
            "names": ["uranker"],
            "description": "A ranking-based underwater image quality assessment (UIQA) method, AAAI2023",
            "category": "Underwater IQA",
            "paper_info": "AAAI2023, Arxiv, Github"
        }
    }
}

server = Server("iqa-pytorch")

@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """List available IQA model resources."""
    return [
        types.Resource(
            uri="iqa://models/all",
            name="All IQA Models",
            description="Complete list of all available IQA models",
            mimeType="application/json",
        ),
        types.Resource(
            uri="iqa://models/fr", 
            name="Full Reference Models",
            description="List of Full Reference (FR) IQA models",
            mimeType="application/json",
        ),
        types.Resource(
            uri="iqa://models/nr",
            name="No Reference Models", 
            description="List of No Reference (NR) IQA models",
            mimeType="application/json",
        ),
        types.Resource(
            uri="iqa://models/specific",
            name="Task-Specific Models",
            description="List of task-specific IQA models (Color, Face, Underwater)",
            mimeType="application/json",
        ),
    ]

@server.read_resource()
async def handle_read_resource(uri: types.AnyUrl) -> str:
    """Read IQA model information based on URI."""
    uri_str = str(uri)
    
    if uri_str == "iqa://models/all":
        return json.dumps(IQA_MODELS, indent=2)
    elif uri_str == "iqa://models/fr":
        return json.dumps(IQA_MODELS["fr_methods"], indent=2)
    elif uri_str == "iqa://models/nr":
        return json.dumps(IQA_MODELS["nr_methods"], indent=2)
    elif uri_str == "iqa://models/specific":
        return json.dumps(IQA_MODELS["specific_methods"], indent=2)
    else:
        raise ValueError(f"Unknown resource URI: {uri}")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for IQA model operations."""
    return [
        types.Tool(
            name="search_models",
            description="Search for IQA models by name, type, or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (model name, type, or category)"
                    },
                    "model_type": {
                        "type": "string",
                        "enum": ["FR", "NR", "Specific", "all"],
                        "description": "Filter by model type"
                    }
                },
                "required": ["query"]
            },
        ),
        types.Tool(
            name="get_model_info",
            description="Get detailed information about a specific IQA model",
            inputSchema={
                "type": "object", 
                "properties": {
                    "model_name": {
                        "type": "string",
                        "description": "Name of the IQA model"
                    }
                },
                "required": ["model_name"]
            },
        ),
        types.Tool(
            name="list_model_names",
            description="Get all available model names for pyiqa.create_metric()",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_type": {
                        "type": "string",
                        "enum": ["FR", "NR", "Specific", "all"],
                        "description": "Filter by model type (default: all)"
                    }
                }
            },
        ),
        types.Tool(
            name="get_usage_example",
            description="Get usage examples for IQA models",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_name": {
                        "type": "string", 
                        "description": "Name of the IQA model"
                    }
                },
                "required": ["model_name"]
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any]
) -> list[types.TextContent]:
    """Handle tool calls for IQA model operations."""
    
    if name == "search_models":
        query = arguments["query"].lower()
        model_type = arguments.get("model_type", "all")
        
        results = []
        
        # Search in all model categories
        categories = []
        if model_type == "all":
            categories = ["fr_methods", "nr_methods", "specific_methods"]
        elif model_type == "FR":
            categories = ["fr_methods"]
        elif model_type == "NR":
            categories = ["nr_methods"]
        elif model_type == "Specific":
            categories = ["specific_methods"]
            
        for category in categories:
            for model_key, model_info in IQA_MODELS[category].items():
                # Search in model names, description, and category
                search_text = f"{' '.join(model_info['names'])} {model_info['description']} {model_info.get('category', '')}".lower()
                if query in search_text:
                    results.append({
                        "key": model_key,
                        "info": model_info
                    })
        
        return [types.TextContent(
            type="text",
            text=json.dumps(results, indent=2)
        )]
    
    elif name == "get_model_info":
        model_name = arguments["model_name"].lower()
        
        # Search for the model in all categories
        for category in ["fr_methods", "nr_methods", "specific_methods"]:
            for model_key, model_info in IQA_MODELS[category].items():
                if model_name in [name.lower() for name in model_info["names"]] or model_name == model_key.lower():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps(model_info, indent=2)
                    )]
        
        return [types.TextContent(
            type="text", 
            text=f"Model '{model_name}' not found in IQA database."
        )]
    
    elif name == "list_model_names":
        model_type = arguments.get("model_type", "all")
        
        all_names = []
        categories = []
        
        if model_type == "all":
            categories = ["fr_methods", "nr_methods", "specific_methods"]
        elif model_type == "FR":
            categories = ["fr_methods"]
        elif model_type == "NR":
            categories = ["nr_methods"]
        elif model_type == "Specific":
            categories = ["specific_methods"]
            
        for category in categories:
            for model_info in IQA_MODELS[category].values():
                all_names.extend(model_info["names"])
                
        return [types.TextContent(
            type="text",
            text=json.dumps(sorted(all_names), indent=2)
        )]
    
    elif name == "get_usage_example":
        model_name = arguments["model_name"]
        
        example_code = f"""
# Basic usage example for {model_name}
import pyiqa

# Create the metric
metric = pyiqa.create_metric('{model_name}')

# Get score range (if available)
try:
    print(f"Score range for {model_name}: {{metric.score_range}}")
except:
    print("Score range not available for this metric")

# For Full Reference (FR) methods:
# score = metric(img_test, img_ref)

# For No Reference (NR) methods:
# score = metric(img_test)

# For batch processing:
# scores = metric(batch_imgs)  # or metric(batch_test, batch_ref) for FR
"""
        
        return [types.TextContent(
            type="text",
            text=example_code
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the IQA MCP server."""
    server = IQAServer()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
