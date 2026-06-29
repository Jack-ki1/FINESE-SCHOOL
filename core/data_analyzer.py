"""
Data Analyzer - CSV/Excel analysis, profiling, and visualization.
Provides data profiling, chart generation, and AI-powered analysis.
"""
import io
import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class DataAnalyzer:
    """Analyze uploaded data files (CSV, Excel) with profiling and visualization."""

    def __init__(self):
        self._datasets: Dict[str, Dict] = {}

    def load_csv(self, name: str, content: str) -> Dict[str, Any]:
        """Load CSV content into a dataset."""
        try:
            import pandas as pd
            df = pd.read_csv(io.StringIO(content))
            return self._register_dataset(name, df, content)
        except Exception as e:
            logger.error(f"CSV load error: {e}")
            return {'success': False, 'error': str(e)}

    def load_dataframe(self, name: str, df) -> Dict[str, Any]:
        """Register an existing DataFrame."""
        buf = io.StringIO()
        df.to_csv(buf, index=False)
        return self._register_dataset(name, df, buf.getvalue())

    def _register_dataset(self, name: str, df, csv_content: str) -> Dict[str, Any]:
        """Store dataset and generate profile."""
        self._datasets[name] = {
            'name': name,
            'csv_content': csv_content,
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'loaded_at': datetime.utcnow().isoformat(),
        }
        profile = self.profile_dataframe(df)
        self._datasets[name]['profile'] = profile
        return {
            'success': True,
            'name': name,
            'shape': list(df.shape),
            'columns': list(df.columns),
            'profile': profile,
        }

    def profile_dataframe(self, df) -> Dict[str, Any]:
        """Generate a comprehensive data profile."""
        profile = {
            'rows': int(df.shape[0]),
            'columns': int(df.shape[1]),
            'memory_usage_kb': round(df.memory_usage(deep=True).sum() / 1024, 2),
            'column_profiles': [],
            'missing_summary': {},
        }

        total_missing = 0
        for col in df.columns:
            col_profile = {
                'name': str(col),
                'dtype': str(df[col].dtype),
                'non_null': int(df[col].count()),
                'null_count': int(df[col].isnull().sum()),
                'null_pct': round(float(df[col].isnull().mean()) * 100, 2),
                'unique': int(df[col].nunique()),
            }
            total_missing += col_profile['null_count']

            if df[col].dtype in ['int64', 'float64']:
                col_profile['stats'] = {
                    'mean': round(float(df[col].mean()), 4) if df[col].notna().any() else None,
                    'std': round(float(df[col].std()), 4) if df[col].notna().any() else None,
                    'min': round(float(df[col].min()), 4) if df[col].notna().any() else None,
                    'max': round(float(df[col].max()), 4) if df[col].notna().any() else None,
                    'median': round(float(df[col].median()), 4) if df[col].notna().any() else None,
                }
            elif df[col].dtype == 'object':
                top_vals = df[col].value_counts().head(5)
                col_profile['top_values'] = [
                    {'value': str(v), 'count': int(c)} for v, c in top_vals.items()
                ]

            profile['column_profiles'].append(col_profile)

        profile['missing_summary'] = {
            'total_cells': int(df.shape[0] * df.shape[1]),
            'total_missing': int(total_missing),
            'missing_pct': round(float(total_missing / (df.shape[0] * df.shape[1])) * 100, 2),
        }

        return profile

    def get_dataset(self, name: str) -> Optional[Dict]:
        return self._datasets.get(name)

    def list_datasets(self) -> List[Dict]:
        return [
            {
                'name': d['name'],
                'shape': list(d['shape']),
                'columns': d['columns'],
                'loaded_at': d['loaded_at'],
            }
            for d in self._datasets.values()
        ]

    def get_csv_content(self, name: str) -> Optional[str]:
        ds = self._datasets.get(name)
        return ds['csv_content'] if ds else None

    def get_description(self, name: str) -> str:
        """Get a text description of the dataset for LLM context."""
        ds = self._datasets.get(name)
        if not ds:
            return f"Dataset '{name}' not found."

        profile = ds['profile']
        lines = [
            f"Dataset: {name}",
            f"Rows: {profile['rows']}, Columns: {profile['columns']}",
            "",
            "Columns:",
        ]
        for cp in profile['column_profiles']:
            line = f"  - {cp['name']} ({cp['dtype']}): {cp['non_null']} non-null, {cp['unique']} unique"
            if 'stats' in cp:
                s = cp['stats']
                line += f", mean={s['mean']}, std={s['std']}"
            lines.append(line)

        lines.append(f"\nMissing data: {profile['missing_summary']['missing_pct']}%")
        return '\n'.join(lines)

    def generate_chart_spec(self, chart_type: str, data: Dict, title: str = '') -> Dict:
        """Generate a Plotly chart specification as JSON."""
        if chart_type == 'bar':
            return {
                'data': [{'x': data.get('labels', []), 'y': data.get('values', []),
                          'type': 'bar', 'marker': {'color': '#0d6efd'}}],
                'layout': {'title': title or 'Bar Chart', 'xaxis': {'title': data.get('xlabel', '')},
                           'yaxis': {'title': data.get('ylabel', '')}},
            }
        elif chart_type == 'line':
            return {
                'data': [{'x': data.get('labels', []), 'y': data.get('values', []),
                          'type': 'scatter', 'mode': 'lines+markers',
                          'line': {'color': '#0d6efd', 'width': 2}}],
                'layout': {'title': title or 'Line Chart', 'xaxis': {'title': data.get('xlabel', '')},
                           'yaxis': {'title': data.get('ylabel', '')}},
            }
        elif chart_type == 'pie':
            return {
                'data': [{'labels': data.get('labels', []), 'values': data.get('values', []),
                          'type': 'pie', 'hole': 0.4}],
                'layout': {'title': title or 'Pie Chart'},
            }
        elif chart_type == 'scatter':
            return {
                'data': [{'x': data.get('x', []), 'y': data.get('y', []),
                          'type': 'scatter', 'mode': 'markers',
                          'marker': {'color': '#0d6efd', 'size': 8, 'opacity': 0.7}}],
                'layout': {'title': title or 'Scatter Plot', 'xaxis': {'title': data.get('xlabel', '')},
                           'yaxis': {'title': data.get('ylabel', '')}},
            }
        elif chart_type == 'histogram':
            return {
                'data': [{'x': data.get('values', []), 'type': 'histogram',
                          'marker': {'color': '#0d6efd'}}],
                'layout': {'title': title or 'Histogram', 'xaxis': {'title': data.get('xlabel', '')},
                           'yaxis': {'title': 'Count'}},
            }
        elif chart_type == 'heatmap':
            return {
                'data': [{'z': data.get('z', []), 'x': data.get('x', []),
                          'y': data.get('y', []), 'type': 'heatmap', 'colorscale': 'Viridis'}],
                'layout': {'title': title or 'Heatmap'},
            }
        else:
            return {'error': f'Unknown chart type: {chart_type}'}

    def auto_visualize(self, name: str) -> Optional[Dict]:
        """Automatically suggest and generate a visualization for a dataset."""
        ds = self._datasets.get(name)
        if not ds:
            return None

        profile = ds['profile']
        numeric_cols = [c for c in profile['column_profiles'] if c['dtype'] in ('int64', 'float64')]
        categorical_cols = [c for c in profile['column_profiles'] if c['dtype'] == 'object' and c['unique'] <= 20]

        if not numeric_cols:
            return {'error': 'No numeric columns to visualize'}

        try:
            import pandas as pd
            df = pd.read_csv(io.StringIO(ds['csv_content']))

            if categorical_cols and numeric_cols:
                cat = categorical_cols[0]['name']
                num = numeric_cols[0]['name']
                grouped = df.groupby(cat)[num].mean().reset_index()
                return self.generate_chart_spec('bar', {
                    'labels': grouped[cat].tolist(),
                    'values': [round(v, 2) for v in grouped[num].tolist()],
                    'xlabel': cat,
                    'ylabel': f'Avg {num}',
                }, f'Average {num} by {cat}')

            elif len(numeric_cols) >= 2:
                return self.generate_chart_spec('scatter', {
                    'x': df[numeric_cols[0]['name']].tolist()[:200],
                    'y': df[numeric_cols[1]['name']].tolist()[:200],
                    'xlabel': numeric_cols[0]['name'],
                    'ylabel': numeric_cols[1]['name'],
                }, f'{numeric_cols[1]["name"]} vs {numeric_cols[0]["name"]}')

            else:
                col = numeric_cols[0]['name']
                return self.generate_chart_spec('histogram', {
                    'values': df[col].dropna().tolist()[:1000],
                    'xlabel': col,
                }, f'Distribution of {col}')

        except Exception as e:
            return {'error': str(e)}
