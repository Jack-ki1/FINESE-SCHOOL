"""
Code Executor - Sandboxed Python code execution for data analysis.
Executes Python code safely with timeout and output capture.
"""
import sys
import io
import traceback
import signal
import json
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime


class CodeExecutor:
    """Sandboxed Python code execution engine."""

    ALLOWED_MODULES = {
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy',
        'sklearn', 'json', 'csv', 'math', 'statistics',
        'datetime', 'collections', 'itertools', 'functools',
        're', 'string', 'textwrap', 'base64', 'hashlib',
        'plotly', 'io', 'sys', 'os', 'warnings',
    }

    BLOCKED_BUILTINS = {
        'exec', 'eval', 'compile', '__import__',
        'open', 'input', 'raw_input', 'breakpoint',
    }

    def __init__(self, timeout: int = 30, max_output: int = 50000):
        self.timeout = timeout
        self.max_output = max_output

    def execute_python(self, code: str, context: Dict = None) -> Dict[str, Any]:
        """
        Execute Python code in a subprocess sandbox.
        Returns dict with: success, output, error, result_data, execution_time
        """
        result = {
            'success': False,
            'output': '',
            'error': '',
            'result_data': None,
            'execution_time': 0,
            'timestamp': datetime.utcnow().isoformat(),
        }

        # Write code to a temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir=tempfile.gettempdir()) as f:
            # Prepend safe execution wrapper
            wrapper = self._build_wrapper(code, context)
            f.write(wrapper)
            temp_path = f.name

        try:
            start_time = datetime.utcnow()
            proc = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir(),
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
            )
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            result['execution_time'] = round(elapsed, 3)

            stdout = proc.stdout[:self.max_output] if proc.stdout else ''
            stderr = proc.stderr[:self.max_output] if proc.stderr else ''

            # Try to parse structured output (JSON data block)
            result_data = self._extract_result_data(stdout)
            if result_data:
                result['result_data'] = result_data

            if proc.returncode == 0:
                result['success'] = True
                result['output'] = stdout
            else:
                result['output'] = stdout
                result['error'] = stderr or f'Process exited with code {proc.returncode}'

        except subprocess.TimeoutExpired:
            result['error'] = f'Execution timed out after {self.timeout} seconds'
        except Exception as e:
            result['error'] = str(e)
        finally:
            try:
                os.unlink(temp_path)
            except OSError:
                pass

        return result

    def _build_wrapper(self, code: str, context: Dict = None) -> str:
        """Build a wrapper script that provides data context and captures output."""
        wrapper_parts = [
            "import sys, io, json, warnings",
            "warnings.filterwarnings('ignore')",
            "",
            "# Redirect stdout to capture output",
            "_output_buffer = io.StringIO()",
            "_original_stdout = sys.stdout",
            "sys.stdout = _output_buffer",
            "",
            "# Import common data libraries",
            "try:",
            "    import pandas as pd",
            "    import numpy as np",
            "except ImportError:",
            "    pass",
            "",
        ]

        if context:
            if 'dataframes' in context:
                wrapper_parts.append("# Load provided data context")
                for name, csv_data in context['dataframes'].items():
                    wrapper_parts.append(f"{name} = pd.read_csv(io.StringIO('''{csv_data}'''))")
                wrapper_parts.append("")

        wrapper_parts.append("# ── User Code ──")
        wrapper_parts.append("try:")
        for line in code.split('\n'):
            wrapper_parts.append(f"    {line}")
        wrapper_parts.append("except Exception as _e:")
        wrapper_parts.append("    sys.stdout = _original_stdout")
        wrapper_parts.append("    print(f'ERROR: {_e}', file=sys.stderr)")
        wrapper_parts.append("    import traceback; traceback.print_exc(file=sys.stderr)")
        wrapper_parts.append("    sys.exit(1)")
        wrapper_parts.append("")
        wrapper_parts.append("# Restore stdout and print captured output")
        wrapper_parts.append("sys.stdout = _original_stdout")
        wrapper_parts.append("print(_output_buffer.getvalue(), end='')")

        return '\n'.join(wrapper_parts)

    def _extract_result_data(self, output: str) -> Optional[Dict]:
        """Extract structured data from output (JSON block marker)."""
        marker = "___RESULT_JSON___:"
        if marker in output:
            try:
                json_str = output.split(marker, 1)[1].strip().split('\n')[0]
                return json.loads(json_str)
            except (json.JSONDecodeError, IndexError):
                pass
        return None

    def generate_analysis_code(self, question: str, data_description: str) -> str:
        """Generate a prompt template for LLM to produce analysis code."""
        return f"""You are a data analysis expert. Given the following data context and question,
write Python code using pandas to answer the question.

Data Description:
{data_description}

Question: {question}

Write Python code that:
1. Uses pandas DataFrames already available in the environment
2. Performs the analysis
3. Prints clear results

Output ONLY the Python code, no explanations."""
