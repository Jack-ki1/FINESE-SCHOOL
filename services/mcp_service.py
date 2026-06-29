"""
MCP (Model Context Protocol) Service - Enables AI to access external tools securely.
"""
import os
import json
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MCPService:
    """
    Service that implements MCP (Model Context Protocol) to allow AI models
    to access external tools like filesystem, databases, and web resources.
    """
    
    def __init__(self):
        self.tools = {
            'read_file': self.read_file,
            'write_file': self.write_file,
            'list_directory': self.list_directory,
            'execute_sql': self.execute_sql,
            'fetch_url': self.fetch_url,
        }
    
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """
        MCP Tool: Read a file from the filesystem.
        Used for reading student files securely.
        """
        try:
            # Security check: ensure path is within allowed directories
            if not self._is_safe_path(filepath):
                return {'error': 'Invalid file path'}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'file_size': len(content),
                'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def write_file(self, filepath: str, content: str) -> Dict[str, Any]:
        """
        MCP Tool: Write content to a file in the filesystem.
        Used for saving student work securely.
        """
        try:
            # Security check: ensure path is within allowed directories
            if not self._is_safe_path(filepath):
                return {'error': 'Invalid file path'}
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f'File written successfully to {filepath}'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_directory(self, dirpath: str = '.') -> Dict[str, Any]:
        """
        MCP Tool: List files and directories in a given path.
        """
        try:
            # Security check: ensure path is within allowed directories
            if not self._is_safe_path(dirpath):
                return {'error': 'Invalid directory path'}
            
            items = []
            for item in os.listdir(dirpath):
                item_path = os.path.join(dirpath, item)
                is_dir = os.path.isdir(item_path)
                size = 0 if is_dir else os.path.getsize(item_path)
                
                items.append({
                    'name': item,
                    'type': 'directory' if is_dir else 'file',
                    'size': size,
                    'modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                })
            
            return {
                'success': True,
                'items': items,
                'count': len(items)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def execute_sql(self, connection_info: Dict[str, Any], sql_query: str) -> Dict[str, Any]:
        """
        MCP Tool: Execute SQL query against a database.
        Used for direct database queries by AI.
        """
        try:
            from core.database_service import DatabaseService
            
            db_service = DatabaseService()
            # Execute the query using the database service
            result = db_service.execute_query(connection_info, sql_query)
            
            return {
                'success': True,
                'results': result,
                'row_count': len(result) if isinstance(result, list) else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def fetch_url(self, url: str, method: str = 'GET', headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        MCP Tool: Fetch content from a URL.
        Used for AI to fetch documentation and references.
        """
        try:
            # Validate URL
            parsed = urlparse(url)
            if parsed.scheme not in ['http', 'https']:
                return {'error': 'Invalid URL scheme. Only HTTP/HTTPS allowed.'}
            
            # Make the request
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers or {},
                timeout=30
            )
            
            response.raise_for_status()
            
            return {
                'success': True,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'content': response.text,
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _is_safe_path(self, path: str) -> bool:
        """
        Security check to ensure the path is within allowed directories.
        Prevents directory traversal attacks.
        """
        # Resolve the absolute path
        abs_path = os.path.abspath(path)
        
        # Define safe base directories (within project)
        safe_bases = [
            os.path.abspath('.'),  # Current directory
            os.path.abspath('static/uploads'),  # Uploads directory
            os.path.abspath('data'),  # Data directory
        ]
        
        # Check if the path is within any of the safe bases
        for base in safe_bases:
            if abs_path.startswith(base):
                return True
        
        return False
    
    def get_tool_list(self) -> list:
        """Return list of available MCP tools."""
        return list(self.tools.keys())
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a specific MCP tool by name with given arguments.
        """
        if tool_name not in self.tools:
            return {'error': f'Tool {tool_name} not available'}
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {'error': str(e)}


class MCPClient:
    """
    Client for interacting with MCP services.
    Configures MCP tool definitions to attach to LLM calls.
    """
    
    def __init__(self):
        self.service = MCPService()
    
    def get_tool_definitions(self) -> list:
        """
        Get tool definitions in the format expected by LLM providers.
        These can be attached to LLM calls to enable tool usage.
        """
        return [
            {
                "name": "read_file",
                "description": "Read a file from the filesystem. Used for reading student files securely.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["filepath"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file in the filesystem. Used for saving student work securely.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filepath": {
                            "type": "string",
                            "description": "Path where to save the file"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["filepath", "content"]
                }
            },
            {
                "name": "list_directory",
                "description": "List files and directories in a given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "dirpath": {
                            "type": "string",
                            "description": "Directory path to list (defaults to current directory)"
                        }
                    }
                }
            },
            {
                "name": "execute_sql",
                "description": "Execute SQL query against a database. Used for direct database queries by AI.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "connection_info": {
                            "type": "object",
                            "description": "Database connection information",
                            "properties": {
                                "db_type": {"type": "string"},
                                "connection_string": {"type": "string"}
                            }
                        },
                        "sql_query": {
                            "type": "string",
                            "description": "SQL query to execute"
                        }
                    },
                    "required": ["connection_info", "sql_query"]
                }
            },
            {
                "name": "fetch_url",
                "description": "Fetch content from a URL. Used for AI to fetch documentation and references.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch"
                        },
                        "method": {
                            "type": "string",
                            "description": "HTTP method (GET, POST, etc.)",
                            "default": "GET"
                        },
                        "headers": {
                            "type": "object",
                            "description": "Optional headers to include in request"
                        }
                    },
                    "required": ["url"]
                }
            }
        ]
    
    def execute_tool_call(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool call with given arguments.
        """
        return self.service.call_tool(tool_name, **tool_args)


# Global MCP client instance
mcp_client = MCPClient()


def get_mcp_client():
    """
    Get the global MCP client instance.
    """
    return mcp_client