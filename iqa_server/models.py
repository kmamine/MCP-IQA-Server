"""
IQA Model Database Module

Contains the definition of IQA models and their metadata.
"""

from typing import Dict, Any, List

class IQAModelDatabase:
    """Manages the database of IQA models and their metadata."""
    
    def __init__(self):
        self.models = {
            # Full Reference (FR) Methods
            "fr_methods": {
                "topiq_fr": {
                    "type": "FR",
                    "names": ["topiq_fr", "topiq_fr-pipal"],
                    "description": "TOPIQ Full Reference method - Proposed in the TOPIQ paper",
                    "category": "General FR"
                },
                # ...existing fr_methods...
            },
            # No Reference (NR) Methods
            "nr_methods": {
                "qalign": {
                    "type": "NR",
                    "names": ["qalign"],
                    "description": "Q-Align - Large vision-language models with quality (default) and aesthetic options",
                    "category": "General NR"
                },
                # ...existing nr_methods...
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
                # ...existing specific_methods...
            }
        }
    
    def get_all_models(self) -> Dict[str, Any]:
        """Get all models in the database."""
        return self.models
    
    def get_fr_models(self) -> Dict[str, Any]:
        """Get Full Reference (FR) models."""
        return self.models["fr_methods"]
    
    def get_nr_models(self) -> Dict[str, Any]:
        """Get No Reference (NR) models."""
        return self.models["nr_methods"]
    
    def get_specific_models(self) -> Dict[str, Any]:
        """Get task-specific models."""
        return self.models["specific_methods"]
    
    def search_models(self, query: str, model_type: str = "all") -> List[Dict[str, Any]]:
        """Search for models by name, type, or category."""
        query = query.lower()
        results = []
        
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
            for model_key, model_info in self.models[category].items():
                search_text = f"{' '.join(model_info['names'])} {model_info['description']} {model_info.get('category', '')}".lower()
                if query in search_text:
                    results.append({
                        "key": model_key,
                        "info": model_info
                    })
        
        return results
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific model."""
        model_name = model_name.lower()
        
        for category in ["fr_methods", "nr_methods", "specific_methods"]:
            for model_key, model_info in self.models[category].items():
                if model_name in [name.lower() for name in model_info["names"]] or model_name == model_key.lower():
                    return model_info
        
        return {}
    
    def list_model_names(self, model_type: str = "all") -> List[str]:
        """Get all available model names."""
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
            for model_info in self.models[category].values():
                all_names.extend(model_info["names"])
                
        return sorted(all_names)

# Initialize the global model database
model_database = IQAModelDatabase()
