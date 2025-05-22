#!/usr/bin/env python3
"""
Advanced link checker for Flask applications.
This script analyzes your Flask application to find and fix broken links.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import importlib.util
import inspect

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class Route:
    """Class representing a Flask route"""
    endpoint: str
    url: str
    methods: List[str]
    blueprint: Optional[str] = None
    view_function: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None

@dataclass
class Link:
    """Class representing a link in a template"""
    url_for_expr: str
    endpoint: str
    template_file: str
    line_number: int
    line_content: str
    is_valid: bool = False
    suggested_fix: Optional[str] = None

@dataclass
class AppAnalysis:
    """Class to hold the analysis results"""
    routes: List[Route] = field(default_factory=list)
    links: List[Link] = field(default_factory=list)
    blueprint_routes: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

class FlaskLinkChecker:
    """Class to check links in a Flask application"""
    
    def __init__(self, app_path: str, fix: bool = False, verbose: bool = False):
        self.app_path = Path(app_path)
        self.fix = fix
        self.verbose = verbose
        self.analysis = AppAnalysis()
        
    def log(self, message: str, level: str = "info") -> None:
        """Log a message with the appropriate color"""
        if level == "info" and not self.verbose:
            return
            
        color_map = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.WARNING,
            "error": Colors.RED,
            "header": Colors.HEADER + Colors.BOLD
        }
        
        color = color_map.get(level, "")
        print(f"{color}{message}{Colors.ENDC}")
    
    def find_app_instance(self) -> Optional[Tuple[str, int]]:
        """Find the Flask app instance in the project"""
        self.log("Looking for Flask app instance...", "info")
        
        # Common file names that might contain the Flask app
        app_files = ["app.py", "wsgi.py", "run.py", "__init__.py", "main.py"]
        
        for file_name in app_files:
            file_path = self.app_path / file_name
            if file_path.exists():
                with open(file_path, "r") as f:
                    content = f.read()
                    
                    # Look for app = Flask or app = create_app
                    app_pattern = re.compile(r'(\w+)\s*=\s*(Flask\(|create_app\()')
                    for match in app_pattern.finditer(content):
                        line_number = content[:match.start()].count('\n') + 1
                        self.log(f"Found app instance in {file_path}:{line_number}", "success")
                        return str(file_path), line_number
        
        self.log("Could not find Flask app instance", "warning")
        return None
    
    def extract_routes_from_app(self) -> None:
        """Extract routes from the Flask app"""
        self.log("Extracting routes from Flask app...", "header")
        
        # Find all blueprint files
        blueprint_files = []
        for path in self.app_path.glob("**/*.py"):
            with open(path, "r") as f:
                content = f.read()
                if "Blueprint(" in content or "Blueprint (" in content:
                    blueprint_files.append(path)
        
        # Extract routes from blueprint files
        for file_path in blueprint_files:
            self.extract_routes_from_file(file_path)
            
        self.log(f"Found {len(self.analysis.routes)} routes in {len(blueprint_files)} blueprint files", "success")
    
    def extract_routes_from_file(self, file_path: Path) -> None:
        """Extract routes from a Python file"""
        with open(file_path, "r") as f:
            content = f.read()
            
        # Find blueprint definition
        bp_pattern = re.compile(r'(\w+)\s*=\s*Blueprint\(\s*[\'"](\w+)[\'"]')
        bp_matches = list(bp_pattern.finditer(content))
        
        if not bp_matches:
            return
            
        for bp_match in bp_matches:
            bp_var = bp_match.group(1)
            bp_name = bp_match.group(2)
            
            # Find routes
            route_pattern = re.compile(rf'@{bp_var}\.route\(\s*[\'"]([^\'"]*)[\'"](?:,\s*methods=(\[[^\]]+\]))?')
            
            for route_match in route_pattern.finditer(content):
                route_path = route_match.group(1)
                methods_str = route_match.group(2) or "['GET']"
                
                # Find the function name
                func_pattern = re.compile(rf'{re.escape(route_match.group(0))}.*?\n\s*def\s+(\w+)', re.DOTALL)
                func_match = func_pattern.search(content, route_match.end())
                
                if func_match:
                    func_name = func_match.group(1)
                    line_number = content[:func_match.start()].count('\n') + 1
                    
                    # Clean up methods
                    methods = eval(methods_str)
                    
                    # Create route object
                    endpoint = f"{bp_name}.{func_name}"
                    url = route_path
                    
                    route = Route(
                        endpoint=endpoint,
                        url=url,
                        methods=methods,
                        blueprint=bp_name,
                        view_function=func_name,
                        file_path=str(file_path),
                        line_number=line_number
                    )
                    
                    self.analysis.routes.append(route)
                    self.analysis.blueprint_routes[bp_name].append(func_name)
                    
                    if self.verbose:
                        self.log(f"Found route: {endpoint} -> {url} {methods}", "info")
    
    def find_template_links(self) -> None:
        """Find all url_for calls in templates"""
        self.log("Finding links in templates...", "header")
        
        templates_dir = self.app_path / "templates"
        if not templates_dir.exists():
            self.log(f"Templates directory not found: {templates_dir}", "warning")
            return
            
        template_files = list(templates_dir.glob("**/*.html"))
        self.log(f"Scanning {len(template_files)} template files...", "info")
        
        # Pattern to match url_for calls
        url_for_pattern = re.compile(r'\{\{\s*url_for\(\s*[\'"]([^\'"]+)[\'"]\s*(?:,\s*[^\)]+)?\s*\)\s*\}\}')
        
        for template_file in template_files:
            with open(template_file, "r") as f:
                content = f.read()
                
                for match in url_for_pattern.finditer(content):
                    endpoint = match.group(1)
                    line_number = content[:match.start()].count('\n') + 1
                    
                    # Get the line content for context
                    lines = content.split('\n')
                    line_content = lines[line_number - 1] if line_number <= len(lines) else ""
                    
                    link = Link(
                        url_for_expr=match.group(0),
                        endpoint=endpoint,
                        template_file=str(template_file),
                        line_number=line_number,
                        line_content=line_content
                    )
                    
                    self.analysis.links.append(link)
        
        self.log(f"Found {len(self.analysis.links)} links in templates", "success")
    
    def validate_links(self) -> None:
        """Validate all links against known routes"""
        self.log("Validating links...", "header")
        
        # Create a set of all endpoints
        endpoints = {route.endpoint for route in self.analysis.routes}
        
        # Check each link
        for link in self.analysis.links:
            if link.endpoint in endpoints:
                link.is_valid = True
            else:
                # Try to suggest a fix
                parts = link.endpoint.split('.')
                if len(parts) == 1:
                    # No blueprint specified, try to find a matching function in any blueprint
                    func_name = parts[0]
                    for bp_name, funcs in self.analysis.blueprint_routes.items():
                        if func_name in funcs:
                            link.suggested_fix = f"{bp_name}.{func_name}"
                            break
                elif len(parts) == 2:
                    # Blueprint specified, check if the function exists in another blueprint
                    bp_name, func_name = parts
                    for other_bp, funcs in self.analysis.blueprint_routes.items():
                        if other_bp != bp_name and func_name in funcs:
                            link.suggested_fix = f"{other_bp}.{func_name}"
                            break
        
        valid_count = sum(1 for link in self.analysis.links if link.is_valid)
        invalid_count = len(self.analysis.links) - valid_count
        
        self.log(f"Valid links: {valid_count}", "success")
        if invalid_count > 0:
            self.log(f"Invalid links: {invalid_count}", "error")
    
    def fix_invalid_links(self) -> None:
        """Fix invalid links in templates"""
        if not self.fix:
            return
            
        self.log("Fixing invalid links...", "header")
        
        # Group links by template file for efficient processing
        links_by_template = defaultdict(list)
        for link in self.analysis.links:
            if not link.is_valid and link.suggested_fix:
                links_by_template[link.template_file].append(link)
        
        # Process each template file
        for template_file, links in links_by_template.items():
            with open(template_file, "r") as f:
                content = f.read()
                
            # Fix each link
            for link in links:
                old_expr = link.url_for_expr
                new_expr = old_expr.replace(f"'{link.endpoint}'", f"'{link.suggested_fix}'")
                new_expr = new_expr.replace(f'"{link.endpoint}"', f'"{link.suggested_fix}"')
                
                content = content.replace(old_expr, new_expr)
                self.log(f"Fixed link in {template_file}:{link.line_number} - {link.endpoint} -> {link.suggested_fix}", "success")
            
            # Write the updated content back to the file
            with open(template_file, "w") as f:
                f.write(content)
    
    def generate_report(self) -> None:
        """Generate a report of the analysis"""
        self.log("\nLink Checker Report", "header")
        
        # Routes summary
        print(f"\n{Colors.BOLD}Routes Summary:{Colors.ENDC}")
        for blueprint, funcs in self.analysis.blueprint_routes.items():
            print(f"  {Colors.CYAN}{blueprint}{Colors.ENDC}: {len(funcs)} routes")
        
        # Invalid links
        invalid_links = [link for link in self.analysis.links if not link.is_valid]
        if invalid_links:
            print(f"\n{Colors.BOLD}{Colors.RED}Invalid Links:{Colors.ENDC}")
            for link in invalid_links:
                file_path = os.path.relpath(link.template_file, self.app_path)
                print(f"  {Colors.RED}✗{Colors.ENDC} {file_path}:{link.line_number} - {link.endpoint}")
                print(f"    {Colors.BLUE}Line:{Colors.ENDC} {link.line_content.strip()}")
                if link.suggested_fix:
                    print(f"    {Colors.GREEN}Suggestion:{Colors.ENDC} Use '{link.suggested_fix}' instead of '{link.endpoint}'")
                print()
        else:
            print(f"\n{Colors.BOLD}{Colors.GREEN}All links are valid!{Colors.ENDC}")
        
        # Summary
        valid_count = sum(1 for link in self.analysis.links if link.is_valid)
        total_count = len(self.analysis.links)
        print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
        print(f"  Total routes: {len(self.analysis.routes)}")
        print(f"  Total links: {total_count}")
        print(f"  Valid links: {valid_count} ({valid_count/total_count*100:.1f}%)")
        print(f"  Invalid links: {total_count - valid_count} ({(total_count - valid_count)/total_count*100:.1f}%)")
        
        if self.fix:
            fixed_count = sum(1 for link in invalid_links if link.suggested_fix)
            print(f"  Fixed links: {fixed_count}")
    
    def run(self) -> None:
        """Run the link checker"""
        self.log(f"Starting link checker for {self.app_path}", "header")
        
        # Find the Flask app instance
        app_instance = self.find_app_instance()
        if not app_instance:
            self.log("Could not find Flask app instance. Continuing anyway...", "warning")
        
        # Extract routes
        self.extract_routes_from_app()
        
        # Find template links
        self.find_template_links()
        
        # Validate links
        self.validate_links()
        
        # Fix invalid links
        self.fix_invalid_links()
        
        # Generate report
        self.generate_report()

def main():
    parser = argparse.ArgumentParser(description="Check links in a Flask application")
    parser.add_argument("--app-path", default=".", help="Path to the Flask application")
    parser.add_argument("--fix", action="store_true", help="Fix invalid links")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    checker = FlaskLinkChecker(args.app_path, args.fix, args.verbose)
    checker.run()

if __name__ == "__main__":
    main()