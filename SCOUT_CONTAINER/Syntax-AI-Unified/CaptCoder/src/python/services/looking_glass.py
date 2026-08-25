"""
Syntax AI CaptCoder - Looking Glass Service

Provides visual code preview and variable inspection.
Allows users to "witness the in-game variables show up in the game's UI".

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Environment Configuration
LOOKING_GLASS_URL = os.getenv("LOOKING_GLASS_URL", "http://localhost:3000/looking-glass")
SANDBOX_API_URL = os.getenv("SANDBOX_API_URL", "http://localhost:8001")

@dataclass
class VariableInfo:
    """Information about a variable."""
    name: str
    value: Any
    type: str
    size: Optional[int] = None
    preview: Optional[str] = None

@dataclass
class UIElement:
    """Represents a UI element in the game."""
    id: str
    element_type: str
    properties: Dict[str, Any]
    children: Optional[List['UIElement']] = None

@dataclass
class LookingGlassPreview:
    """Complete Looking Glass preview."""
    variables: Dict[str, VariableInfo]
    ui_elements: List[UIElement]
    screenshot: Optional[str] = None  # base64 encoded
    timestamp: str = datetime.now().isoformat()
    code_hash: Optional[str] = None


class LookingGlassService:
    """
    Service for providing visual code preview through Looking Glass.
    
    Allows developers to:
    - See in-game variables appear in the UI
    - Preview code changes visually
    - Witness the "magic" of Syntax AI
    
    Features:
    - Variable inspection and visualization
    - UI element rendering
    - Screenshot capture
    - Real-time updates
    """
    
    def __init__(
        self,
        looking_glass_url: Optional[str] = None,
        sandbox_url: Optional[str] = None
    ):
        """
        Initialize the LookingGlassService.
        
        Args:
            looking_glass_url: URL of the Looking Glass interface
            sandbox_url: URL of the DreamTable Sandbox API
        """
        self.looking_glass_url = looking_glass_url or LOOKING_GLASS_URL
        self.sandbox_url = sandbox_url or SANDBOX_API_URL
        
        # State
        self.active_previews: Dict[str, LookingGlassPreview] = {}
        
        # Statistics
        self.stats = {
            "previews_generated": 0,
            "variables_inspected": 0,
            "screenshots_taken": 0,
            "errors": 0
        }
        
        logger.info(f"LookingGlassService initialized")
        logger.info(f"  Looking Glass URL: {self.looking_glass_url}")
        logger.info(f"  Sandbox URL: {self.sandbox_url}")
    
    def generate_preview(
        self,
        code: str,
        language: str = "python",
        context: Optional[Dict[str, Any]] = None
    ) -> LookingGlassPreview:
        """
        Generate a Looking Glass preview for code.
        
        Args:
            code: Code to preview
            language: Programming language
            context: Optional context for execution
            
        Returns:
            LookingGlassPreview with all visual data
        """
        preview_id = f"preview_{int(time.time() * 1000)}_{len(self.active_previews)}"
        
        try:
            # Execute code in sandbox to get variables and UI
            sandbox_result = self._execute_in_sandbox(code, language, context)
            
            if sandbox_result.get("success"):
                variables = self._format_variables(sandbox_result.get("variables", {}))
                ui_elements = sandbox_result.get("ui_elements", [])
                screenshot = sandbox_result.get("screenshot")
                
                preview = LookingGlassPreview(
                    variables=variables,
                    ui_elements=ui_elements,
                    screenshot=screenshot,
                    timestamp=datetime.now().isoformat(),
                    code_hash=self._hash_code(code)
                )
                
                self.active_previews[preview_id] = preview
                self.stats["previews_generated"] += 1
                self.stats["variables_inspected"] += len(variables)
                
                if screenshot:
                    self.stats["screenshots_taken"] += 1
                
                return preview
            else:
                # Return error preview
                error_var = VariableInfo(
                    name="error",
                    value=sandbox_result.get("error", "Unknown error"),
                    type="error",
                    preview=str(sandbox_result.get("error", ""))[:100]
                )
                
                return LookingGlassPreview(
                    variables={"error": error_var},
                    ui_elements=[],
                    timestamp=datetime.now().isoformat(),
                    code_hash=self._hash_code(code)
                )
                
        except Exception as e:
            self.stats["errors"] += 1
            logger.error(f"Failed to generate preview: {e}")
            
            error_var = VariableInfo(
                name="error",
                value=str(e),
                type="error",
                preview=str(e)[:100]
            )
            
            return LookingGlassPreview(
                variables={"error": error_var},
                ui_elements=[],
                timestamp=datetime.now().isoformat(),
                code_hash=self._hash_code(code)
            )
    
    def _execute_in_sandbox(
        self,
        code: str,
        language: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute code in the sandbox."""
        import requests
        
        try:
            payload = {
                "code": code,
                "language": language,
                "context": context or {},
                "action": "looking_glass_preview"
            }
            
            response = requests.post(
                f"{self.sandbox_url}/looking-glass",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"Sandbox API error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_variables(self, variables: Dict[str, Any]) -> Dict[str, VariableInfo]:
        """Format raw variables into VariableInfo objects."""
        formatted: Dict[str, VariableInfo] = {}
        
        for name, value in variables.items():
            var_type = type(value).__name__
            
            # Generate preview
            if isinstance(value, str):
                preview = value[:100] + "..." if len(value) > 100 else value
            elif isinstance(value, (list, dict)):
                preview = json.dumps(value)[:100] + "..." if len(json.dumps(value)) > 100 else json.dumps(value)
            else:
                preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            
            # Calculate size
            size = self._calculate_size(value)
            
            formatted[name] = VariableInfo(
                name=name,
                value=value,
                type=var_type,
                size=size,
                preview=preview
            )
        
        self.stats["variables_inspected"] += len(formatted)
        return formatted
    
    def _calculate_size(self, value: Any) -> Optional[int]:
        """Calculate the size of a value."""
        try:
            if isinstance(value, str):
                return len(value)
            elif isinstance(value, (list, tuple, set)):
                return len(value)
            elif isinstance(value, dict):
                return len(value)
            elif hasattr(value, '__len__'):
                return len(value)
            else:
                return None
        except:
            return None
    
    def _hash_code(self, code: str) -> str:
        """Generate a hash for code."""
        import hashlib
        return hashlib.md5(code.encode('utf-8')).hexdigest()
    
    def get_variable(self, preview_id: str, var_name: str) -> Optional[VariableInfo]:
        """Get a specific variable from a preview."""
        preview = self.active_previews.get(preview_id)
        if preview:
            return preview.variables.get(var_name)
        return None
    
    def get_preview(self, preview_id: str) -> Optional[LookingGlassPreview]:
        """Get a specific preview by ID."""
        return self.active_previews.get(preview_id)
    
    def list_previews(self) -> List[LookingGlassPreview]:
        """List all active previews."""
        return list(self.active_previews.values())
    
    def clear_previews(self) -> None:
        """Clear all active previews."""
        self.active_previews = {}
    
    def render_ui(
        self,
        ui_elements: List[UIElement]
    ) -> str:
        """
        Render UI elements as HTML for display.
        
        Args:
            ui_elements: List of UI elements to render
            
        Returns:
            HTML string
        """
        html_parts = []
        
        for element in ui_elements:
            html_parts.append(self._render_element(element))
        
        return "\n".join(html_parts)
    
    def _render_element(self, element: UIElement, indent: int = 0) -> str:
        """Render a single UI element."""
        pad = "  " * indent
        
        # Simple rendering based on element type
        if element.element_type == "container":
            children_html = ""
            if element.children:
                for child in element.children:
                    children_html += self._render_element(child, indent + 1)
            
            return f"{pad}<div class=\"{element.id}\">{children_html}\n{pad}</div>"
        
        elif element.element_type == "text":
            content = element.properties.get("content", "")
            return f"{pad}<span>{content}</span>"
        
        elif element.element_type == "image":
            src = element.properties.get("src", "")
            return f'{pad}<img src="{src}" />'
        
        elif element.element_type == "button":
            label = element.properties.get("label", "Button")
            return f'{pad}<button>{label}</button>'
        
        else:
            return f"{pad}<{element.element_type}>{element.id}</{element.element_type}>"
    
    def generate_html_report(
        self,
        preview: LookingGlassPreview
    ) -> str:
        """
        Generate an HTML report from a preview.
        
        Args:
            preview: The LookingGlassPreview to generate report from
            
        Returns:
            HTML string
        """
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Looking Glass Preview - {preview.timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .preview {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section h2 {{ margin-top: 0; color: #333; }}
        .variables {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 10px; }}
        .variable {{ background: #f9f9f9; padding: 10px; border-radius: 4px; }}
        .variable-name {{ font-weight: bold; color: #2563eb; }}
        .variable-type {{ color: #666; font-size: 12px; }}
        .variable-preview {{ font-family: monospace; white-space: pre-wrap; }}
        .ui-preview {{ border: 1px solid #ddd; padding: 10px; background: white; }}
        .screenshot {{ max-width: 100%; border-radius: 4px; }}
        .timestamp {{ color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>Looking Glass Preview</h1>
    <p class="timestamp">Generated: {preview.timestamp}</p>
    
    <div class="preview">
        <div class="section">
            <h2>Variables ({len(preview.variables)})</h2>
            <div class="variables">
        """
        
        for name, var in preview.variables.items():
            html += f"""
                <div class="variable">
                    <div class="variable-name">{name}</div>
                    <div class="variable-type">{var.type}</div>
                    {f'<div class="variable-size">Size: {var.size}</div>' if var.size else ''}
                    <div class="variable-preview">{var.preview}</div>
                </div>
            """
        
        html += """
            </div>
        </div>
        
        <div class="section">
            <h2>UI Elements ({len(preview.ui_elements)})</h2>
            <div class="ui-preview">
        """
        
        if preview.ui_elements:
            html += self.render_ui(preview.ui_elements)
        else:
            html += "<p>No UI elements to display</p>"
        
        html += """
            </div>
        </div>
        
        <div class="section">
            <h2>Screenshot</h2>
        """
        
        if preview.screenshot:
            html += f'<img src="data:image/png;base64,{preview.screenshot}" class="screenshot" />'
        else:
            html += "<p>No screenshot available</p>"
        
        html += """
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def save_preview(
        self,
        preview: LookingGlassPreview,
        path: Optional[str] = None
    ) -> str:
        """
        Save a preview to a file.
        
        Args:
            preview: The LookingGlassPreview to save
            path: Optional file path (defaults to timestamp-based path)
            
        Returns:
            File path where preview was saved
        """
        import json
        
        if path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"/storage/emulated/0/LookingGlass/preview_{timestamp}.json"
        
        # Convert to serializable format
        preview_dict = {
            "variables": {
                name: {
                    "name": var.name,
                    "value": var.value,
                    "type": var.type,
                    "size": var.size,
                    "preview": var.preview
                }
                for name, var in preview.variables.items()
            },
            "ui_elements": [
                {
                    "id": elem.id,
                    "element_type": elem.element_type,
                    "properties": elem.properties,
                    "children": [
                        self._serialize_element(child)
                        for child in elem.children or []
                    ] if elem.children else None
                }
                for elem in preview.ui_elements
            ],
            "screenshot": preview.screenshot,
            "timestamp": preview.timestamp,
            "code_hash": preview.code_hash
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save JSON
        with open(path, 'w') as f:
            json.dump(preview_dict, f, indent=2)
        
        # Also save HTML report
        html_path = path.replace('.json', '.html')
        with open(html_path, 'w') as f:
            f.write(self.generate_html_report(preview))
        
        return path
    
    def _serialize_element(self, element: UIElement) -> Dict[str, Any]:
        """Serialize a UIElement for JSON."""
        return {
            "id": element.id,
            "element_type": element.element_type,
            "properties": element.properties,
            "children": [
                self._serialize_element(child)
                for child in element.children or []
            ] if element.children else None
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Looking Glass statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "previews_generated": 0,
            "variables_inspected": 0,
            "screenshots_taken": 0,
            "errors": 0
        }


# Singleton instance
_looking_glass_service: Optional[LookingGlassService] = None


def get_looking_glass_service() -> LookingGlassService:
    """Get the singleton LookingGlassService instance."""
    global _looking_glass_service
    if _looking_glass_service is None:
        _looking_glass_service = LookingGlassService()
    return _looking_glass_service


def main():
    """Test LookingGlassService."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LookingGlassService - Test visual preview")
    parser.add_argument("--preview", type=str, help="Generate preview for code")
    parser.add_argument("--language", default="python", help="Programming language")
    parser.add_argument("--save", type=str, help="Save preview to file")
    parser.add_argument("--list", action="store_true", help="List active previews")
    parser.add_argument("--clear", action="store_true", help="Clear active previews")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()
    
    service = get_looking_glass_service()
    
    if args.preview:
        preview = service.generate_preview(args.preview, args.language)
        print(f"Generated preview with {len(preview.variables)} variables")
        print(f"UI Elements: {len(preview.ui_elements)}")
        print(f"Screenshot: {'Yes' if preview.screenshot else 'No'}")
        
        if args.save:
            path = service.save_preview(preview, args.save)
            print(f"Saved to: {path}")
    
    elif args.list:
        previews = service.list_previews()
        print(f"Active previews: {len(previews)}")
        for preview in previews:
            print(f"  - {preview.timestamp}: {len(preview.variables)} variables")
    
    elif args.clear:
        service.clear_previews()
        print("Previews cleared")
    
    elif args.stats:
        print(json.dumps(service.get_stats(), indent=2))
    
    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    main()
