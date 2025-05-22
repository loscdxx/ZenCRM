#!/usr/bin/env python3
"""
Modern Python script to check and fix all links in the ZenCRM application.
Uses the latest Python features including f-strings, type hints, and async functionality.
"""

import os
import re
import sys
import asyncio
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass
from enum import Enum, auto
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID

# Initialize rich console for better output
console = Console()

class LinkType(Enum):
    """Enum for different types of links"""
    NAVIGATION = auto()
    FOOTER = auto()
    INTERNAL = auto()
    EXTERNAL = auto()
    API = auto()

@dataclass
class Link:
    """Data class to represent a link in the application"""
    name: str
    path: str
    type: LinkType
    template_file: Optional[str] = None
    line_number: Optional[int] = None
    status: Optional[int] = None
    error_message: Optional[str] = None

class LinkChecker:
    """Class to check and fix links in the ZenCRM application"""
    
    def __init__(self, base_url: str = "http://localhost:5002", fix_links: bool = False):
        self.base_url: str = base_url
        self.fix_links: bool = fix_links
        self.templates_dir: Path = Path("templates")
        self.blueprints_dir: Path = Path("blueprints")
        self.links: List[Link] = []
        self.route_map: Dict[str, str] = {}
        self.missing_routes: Set[str] = set()
        
    async def check_link(self, link: Link) -> None:
        """Check if a link is working by making an HTTP request"""
        url = f"{self.base_url}{link.path}"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                link.status = response.status_code
        except Exception as e:
            link.status = 0
            link.error_message = str(e)
    
    def scan_templates_for_links(self) -> None:
        """Scan all template files for links"""
        console.log("Scanning template files for links...")
        
        # Pattern to match url_for calls in templates
        url_for_pattern = re.compile(r'\{\{\s*url_for\([\'\"]([^\)]+)[\'\"]\)\s*\}\}')
        
        for template_file in self.templates_dir.glob('**/*.html'):
            relative_path = template_file.relative_to(Path.cwd())
            
            with open(template_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    for match in url_for_pattern.finditer(line):
                        route_name = match.group(1)
                        
                        # Skip if the route contains a variable
                        if '{{' in route_name or '}}' in route_name:
                            continue
                            
                        # Determine link type
                        link_type = LinkType.INTERNAL
                        if 'footer' in str(template_file).lower():
                            link_type = LinkType.FOOTER
                        elif 'nav' in str(template_file).lower() or template_file.name == 'base.html':
                            link_type = LinkType.NAVIGATION
                            
                        # Add to links list
                        self.links.append(Link(
                            name=route_name,
                            path=f"/{route_name.replace('.', '/')}",
                            type=link_type,
                            template_file=str(relative_path),
                            line_number=i
                        ))
                        
                        # Add to route map
                        self.route_map[route_name] = f"/{route_name.replace('.', '/')}"
    
    def scan_blueprints_for_routes(self) -> None:
        """Scan all blueprint files for route definitions"""
        console.log("Scanning blueprint files for route definitions...")
        
        # Pattern to match route definitions in blueprints
        route_pattern = re.compile(r'@(\w+)\.route\([\'\"](.*?)[\'\"]')
        
        for blueprint_file in self.blueprints_dir.glob('**/*.py'):
            blueprint_name = blueprint_file.stem
            
            with open(blueprint_file, 'r') as f:
                content = f.read()
                
                # Find the blueprint variable name
                bp_match = re.search(r'(\w+)\s*=\s*Blueprint', content)
                if not bp_match:
                    continue
                    
                bp_var = bp_match.group(1)
                
                # Find all routes
                for match in route_pattern.finditer(content):
                    if match.group(1) == bp_var:
                        route_path = match.group(2)
                        
                        # Extract function name that follows the route decorator
                        func_match = re.search(rf'{re.escape(match.group(0))}.*?\n\s*def\s+(\w+)', content, re.DOTALL)
                        if func_match:
                            func_name = func_match.group(1)
                            route_name = f"{blueprint_name}.{func_name}"
                            
                            # Add to route map
                            if route_path == '/':
                                self.route_map[route_name] = f"/{blueprint_name}"
                            else:
                                self.route_map[route_name] = f"/{blueprint_name}{route_path}"
    
    def identify_missing_routes(self) -> None:
        """Identify routes that are referenced in templates but not defined in blueprints"""
        console.log("Identifying missing routes...")
        
        for link in self.links:
            route_name = link.name
            
            # Check if the route exists in the route map
            if route_name not in self.route_map:
                self.missing_routes.add(route_name)
                link.error_message = "Route not defined in blueprints"
    
    def fix_template_links(self) -> None:
        """Fix incorrect links in template files"""
        if not self.fix_links:
            return
            
        console.log("Fixing template links...")
        
        # Group links by template file for efficient processing
        links_by_template: Dict[str, List[Link]] = {}
        for link in self.links:
            if link.template_file and link.error_message:
                if link.template_file not in links_by_template:
                    links_by_template[link.template_file] = []
                links_by_template[link.template_file].append(link)
        
        # Process each template file
        for template_file, links in links_by_template.items():
            with open(template_file, 'r') as f:
                content = f.read()
                
            # Fix each link
            for link in links:
                if link.name in self.missing_routes:
                    # Determine the correct blueprint prefix
                    parts = link.name.split('.')
                    if len(parts) == 1:
                        # No blueprint specified, assume 'main'
                        correct_route = f"main.{parts[0]}"
                    else:
                        # Already has blueprint, leave as is
                        correct_route = link.name
                        
                    # Replace the incorrect route
                    pattern = rf'\{{\{\s*url_for\([\'\"]{re.escape(link.name)}[\'\"]\)\s*\}}\}}'
                    replacement = f"{{{{ url_for('{correct_route}') }}}}"
                    content = re.sub(pattern, replacement, content)
                    
                    console.log(f"Fixed link in {template_file}: {link.name} -> {correct_route}")
            
            # Write the updated content back to the file
            with open(template_file, 'w') as f:
                f.write(content)
    
    def create_missing_routes(self) -> None:
        """Create missing route definitions in blueprint files"""
        if not self.fix_links:
            return
            
        console.log("Creating missing routes...")
        
        # Group missing routes by blueprint
        routes_by_blueprint: Dict[str, List[str]] = {}
        for route in self.missing_routes:
            parts = route.split('.')
            if len(parts) == 1:
                # No blueprint specified, assume 'main'
                blueprint = 'main'
                function = parts[0]
            else:
                blueprint = parts[0]
                function = parts[1]
                
            if blueprint not in routes_by_blueprint:
                routes_by_blueprint[blueprint] = []
            routes_by_blueprint[blueprint].append(function)
        
        # Process each blueprint
        for blueprint, functions in routes_by_blueprint.items():
            blueprint_file = self.blueprints_dir / f"{blueprint}.py"
            
            if not blueprint_file.exists():
                console.log(f"Blueprint file {blueprint_file} does not exist. Skipping.")
                continue
                
            with open(blueprint_file, 'r') as f:
                content = f.read()
                
            # Find the blueprint variable name
            bp_match = re.search(r'(\w+)\s*=\s*Blueprint', content)
            if not bp_match:
                console.log(f"Could not find Blueprint variable in {blueprint_file}. Skipping.")
                continue
                
            bp_var = bp_match.group(1)
            
            # Add each missing route
            for function in functions:
                # Check if the route already exists
                if re.search(rf'def\s+{function}\s*\(', content):
                    continue
                    
                # Create the route
                route_code = f"""
@{bp_var}.route('/{function.replace("_", "-")}')
def {function}():
    \"\"\"
    {function.replace('_', ' ').title()} page
    \"\"\"
    return render_template('{blueprint}/{function}.html', title='{function.replace('_', ' ').title()}')
"""
                # Add the route to the end of the file
                content += route_code
                
                console.log(f"Added route {blueprint}.{function} to {blueprint_file}")
            
            # Write the updated content back to the file
            with open(blueprint_file, 'w') as f:
                f.write(content)
    
    async def check_all_links(self) -> None:
        """Check all links in the application"""
        console.log("Checking all links...")
        
        # Create tasks for checking each link
        tasks = []
        for link in self.links:
            if not link.error_message:  # Only check links that don't already have errors
                tasks.append(self.check_link(link))
        
        # Run all tasks concurrently
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task_id = progress.add_task("Checking links...", total=len(tasks))
            for i, coro in enumerate(asyncio.as_completed(tasks), 1):
                await coro
                progress.update(task_id, completed=i)
    
    def display_results(self) -> None:
        """Display the results of the link check"""
        # Create a table for the results
        table = Table(title="Link Check Results")
        table.add_column("Name", style="cyan")
        table.add_column("Path", style="green")
        table.add_column("Type", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Template", style="magenta")
        table.add_column("Error", style="red")
        
        # Add rows to the table
        for link in self.links:
            status = str(link.status) if link.status else "N/A"
            status_style = ""
            if link.status == 200:
                status_style = "green"
            elif link.status:
                status_style = "red"
                
            table.add_row(
                link.name,
                link.path,
                link.type.name,
                f"[{status_style}]{status}[/{status_style}]" if status_style else status,
                f"{link.template_file}:{link.line_number}" if link.template_file else "N/A",
                link.error_message or ""
            )
        
        # Print the table
        console.print(table)
        
        # Print summary
        working_links = sum(1 for link in self.links if link.status == 200)
        total_links = len(self.links)
        console.print(f"\n[bold]Summary:[/bold] {working_links}/{total_links} links working")
        
        if self.missing_routes:
            console.print(f"\n[bold red]Missing Routes:[/bold red]")
            for route in self.missing_routes:
                console.print(f"  - {route}")
    
    async def run(self) -> None:
        """Run the link checker"""
        console.rule("[bold]ZenCRM Link Checker[/bold]")
        
        # Scan templates and blueprints
        self.scan_templates_for_links()
        self.scan_blueprints_for_routes()
        self.identify_missing_routes()
        
        # Check links
        await self.check_all_links()
        
        # Display results
        self.display_results()
        
        # Fix links if requested
        if self.fix_links:
            console.rule("[bold]Fixing Links[/bold]")
            self.fix_template_links()
            self.create_missing_routes()
            console.print("[bold green]Links fixed successfully![/bold green]")

async def main() -> None:
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check and fix links in the ZenCRM application")
    parser.add_argument("--base-url", default="http://localhost:5002", help="Base URL of the application")
    parser.add_argument("--fix", action="store_true", help="Fix broken links")
    args = parser.parse_args()
    
    checker = LinkChecker(base_url=args.base_url, fix_links=args.fix)
    await checker.run()

if __name__ == "__main__":
    asyncio.run(main())