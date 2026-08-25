"""
Syntax AI CaptCoder - DreamTable Sandbox Service

Provides integration with the DreamTable Sandbox for testing and previewing code.

Author: Syntax AI Team
Version: 1.0.0
"""

import os
import json
import time
import logging
import requests
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Environment Configuration
SANDBOX_API_URL = os.getenv("SANDBOX_API_URL", "http://localhost:8001")
SANDBOX_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", 30))

@dataclass
class SandboxTest:
    """Represents a sandbox test execution."""
    id: str
    code: str
    language: str
    status: str
    output: Optional[str] = None
    error: Optional[str] = None
    duration: Optional[float] = None
    timestamp: str = datetime.now().isoformat()

@dataclass
class SandboxResult:
    """Result of a sandbox test."""
    success: bool
    test: SandboxTest
    variables: Optional[Dict[str, Any]] = None
    ui_elements: Optional[List[Any]] = None
    screenshot: Optional[str] = None
    preview_url: Optional[str] = None


class SandboxService:
    """
    Service for testing code in the DreamTable Sandbox.
    
    Provides:
    - Code execution in isolated environment
    - Variable inspection
    - UI preview generation
    - Looking Glass integration
    """
    
    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize the SandboxService.
        
        Args:
            api_url: URL of the DreamTable Sandbox API
        """
        self.api_url = api_url or SANDBOX_API_URL
        self.timeout = SANDBOX_TIMEOUT
        
        # State
        self.active_tests: Dict[str, SandboxTest] = {}
        
        # Statistics
        self.stats = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "executions": 0,
            "errors": 0
        }
        
        logger.info(f"SandboxService initialized. API URL: {self.api_url}")
    
    def execute_code(
        self,
        code: str,
        language: str = "python",
        context: Optional[Dict[str, Any]] = None
    ) -> SandboxResult:
        """
        Execute code in the sandbox.
        
        Args:
            code: Code to execute
            language: Programming language
            context: Optional context/variables to pre-load
            
        Returns:
            SandboxResult with execution results
        """
        test_id = f"test_{int(time.time() * 1000)}_{len(self.active_tests)}"
        
        # Create test object
        test = SandboxTest(
            id=test_id,
            code=code,
            language=language,
            status="queued"
        )
        self.active_tests[test_id] = test
        
        try:
            start_time = time.time()
            
            # Build request payload
            payload = {
                "code": code,
                "language": language,
                "context": context or {},
                "test_id": test_id
            }
            
            # Call Sandbox API
            response = requests.post(
                f"{self.api_url}/execute",
                json=payload,
                timeout=self.timeout
            )
            
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                test.status = "completed"
                
                result = SandboxResult(
                    success=data.get("success", False),
                    test=test,
                    variables=data.get("variables"),
                    ui_elements=data.get("ui_elements"),
                    screenshot=data.get("screenshot"),
                    preview_url=data.get("preview_url")
                )
                
                self.stats["tests_run"] += 1
                if result.success:
                    self.stats["tests_passed"] += 1
                else:
                    self.stats["tests_failed"] += 1
                
                return result
            else:
                self.stats["errors"] += 1
                test.status = "error"
                test.error = f"Sandbox API error: {response.status_code} - {response.text}"
                
                return SandboxResult(
                    success=False,
                    test=test,
                    error=test.error
                )
                
        except requests.exceptions.Timeout:
            self.stats["errors"] += 1
            test.status = "timeout"
            test.error = f"Execution timed out after {self.timeout} seconds"
            
            return SandboxResult(
                success=False,
                test=test,
                error=test.error
            )
            
        except Exception as e:
            self.stats["errors"] += 1
            test.status = "error"
            test.error = str(e)
            
            return SandboxResult(
                success=False,
                test=test,
                error=test.error
            )
    
    def test_code_snippet(
        self,
        snippet: str,
        language: str = "python"
    ) -> SandboxResult:
        """
        Test a code snippet in the sandbox.
        
        Args:
            snippet: Code snippet to test
            language: Programming language
            
        Returns:
            SandboxResult with test results
        """
        return self.execute_code(snippet, language)
    
    def run_unit_tests(
        self,
        test_code: str,
        test_language: str = "python"
    ) -> Dict[str, Any]:
        """
        Run unit tests in the sandbox.
        
        Args:
            test_code: Test code to run
            test_language: Programming language
            
        Returns:
            Dictionary with test results
        """
        # For now, just execute the test code
        result = self.execute_code(test_code, test_language)
        
        # Parse test results if available
        if result.success and result.variables:
            # Look for test results in variables
            test_results = result.variables.get("test_results", {})
            return {
                "success": True,
                "passed": test_results.get("passed", 0),
                "failed": test_results.get("failed", 0),
                "skipped": test_results.get("skipped", 0),
                "result": result
            }
        
        return {
            "success": result.success,
            "error": result.error,
            "result": result
        }
    
    def get_looking_glass_preview(
        self,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Get a Looking Glass preview of code execution.
        
        Args:
            code: Code to preview
            language: Programming language
            
        Returns:
            Dictionary with preview data including variables, UI, screenshot
        """
        result = self.execute_code(code, language)
        
        if result.success:
            return {
                "success": True,
                "variables": result.variables or {},
                "ui_elements": result.ui_elements or [],
                "screenshot": result.screenshot,
                "preview_url": result.preview_url,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "timestamp": datetime.now().isoformat()
            }
    
    def inspect_variables(
        self,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        """
        Inspect variables after code execution.
        
        Args:
            code: Code to execute and inspect
            language: Programming language
            
        Returns:
            Dictionary of variables and their values
        """
        result = self.execute_code(code, language)
        
        if result.success and result.variables:
            return {
                "success": True,
                "variables": result.variables,
                "count": len(result.variables)
            }
        
        return {
            "success": False,
            "error": result.error,
            "variables": {}
        }
    
    def get_test(self, test_id: str) -> Optional[SandboxTest]:
        """Get a specific test by ID."""
        return self.active_tests.get(test_id)
    
    def list_tests(self) -> List[SandboxTest]:
        """List all active tests."""
        return list(self.active_tests.values())
    
    def clear_tests(self) -> None:
        """Clear all active tests."""
        self.active_tests = {}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get sandbox statistics."""
        return self.stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics."""
        self.stats = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "executions": 0,
            "errors": 0
        }


# Singleton instance
_sandbox_service: Optional[SandboxService] = None


def get_sandbox_service() -> SandboxService:
    """Get the singleton SandboxService instance."""
    global _sandbox_service
    if _sandbox_service is None:
        _sandbox_service = SandboxService()
    return _sandbox_service


def main():
    """Test SandboxService."""
    import argparse
    
    parser = argparse.ArgumentParser(description="SandboxService - Test code execution")
    parser.add_argument("--execute", type=str, help="Execute code")
    parser.add_argument("--language", default="python", help="Programming language")
    parser.add_argument("--test", type=str, help="Test a code snippet")
    parser.add_argument("--inspect", type=str, help="Inspect variables from code")
    parser.add_argument("--preview", type=str, help="Get Looking Glass preview")
    parser.add_argument("--list", action="store_true", help="List active tests")
    parser.add_argument("--clear", action="store_true", help="Clear active tests")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    args = parser.parse_args()
    
    service = get_sandbox_service()
    
    if args.execute:
        result = service.execute_code(args.execute, args.language)
        print(f"Status: {result.test.status}")
        if result.success:
            print(f"Variables: {result.variables}")
            print(f"UI Elements: {result.ui_elements}")
        else:
            print(f"Error: {result.error}")
    
    elif args.test:
        result = service.test_code_snippet(args.test, args.language)
        print(f"Test Status: {result.test.status}")
        print(f"Success: {result.success}")
    
    elif args.inspect:
        result = service.inspect_variables(args.inspect, args.language)
        print(json.dumps(result, indent=2))
    
    elif args.preview:
        result = service.get_looking_glass_preview(args.preview, args.language)
        print(json.dumps(result, indent=2))
    
    elif args.list:
        tests = service.list_tests()
        print(f"Active tests: {len(tests)}")
        for test in tests:
            print(f"  - {test.id}: {test.status}")
    
    elif args.clear:
        service.clear_tests()
        print("Active tests cleared")
    
    elif args.stats:
        print(json.dumps(service.get_stats(), indent=2))
    
    else:
        # Show help
        parser.print_help()


if __name__ == "__main__":
    main()
