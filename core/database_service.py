"""
Database Service - SQL execution and database connectivity.
Supports SQLite, MySQL, PostgreSQL with schema introspection.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DatabaseService:
    """Unified database service for SQL execution and schema introspection."""

    SUPPORTED_TYPES = {
        'sqlite': 'sqlite:///{path}',
        'mysql': 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}',
        'postgresql': 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}',
        'mssql': 'mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server',
    }

    def __init__(self):
        self._engines: Dict[str, sqlalchemy.engine.Engine] = {}

    def build_connection_string(self, db_type: str, **kwargs) -> str:
        """Build a SQLAlchemy connection string from parameters."""
        template = self.SUPPORTED_TYPES.get(db_type)
        if not template:
            raise ValueError(f"Unsupported database type: {db_type}. Supported: {list(self.SUPPORTED_TYPES.keys())}")

        if db_type == 'sqlite':
            return template.format(path=kwargs.get('path', 'finese_data.db'))
        return template.format(**kwargs)

    def connect(self, name: str, connection_string: str) -> Dict[str, Any]:
        """Test and store a database connection."""
        try:
            engine = create_engine(connection_string, pool_pre_ping=True)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            self._engines[name] = engine
            return {
                'success': True,
                'name': name,
                'message': f'Connected to {name} successfully',
            }
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed for {name}: {e}")
            return {
                'success': False,
                'name': name,
                'error': str(e),
            }

    def disconnect(self, name: str):
        """Remove a stored connection."""
        if name in self._engines:
            self._engines[name].dispose()
            del self._engines[name]

    def get_engine(self, name: str) -> sqlalchemy.engine.Engine:
        """Get a stored engine by name."""
        if name not in self._engines:
            raise ValueError(f"No connection named '{name}'. Available: {list(self._engines.keys())}")
        return self._engines[name]

    def execute_sql(self, connection_name: str, sql: str, params: Dict = None) -> Dict[str, Any]:
        """Execute a SQL query and return results."""
        result = {
            'success': False,
            'columns': [],
            'rows': [],
            'row_count': 0,
            'execution_time': 0,
            'error': '',
            'timestamp': datetime.utcnow().isoformat(),
        }

        try:
            engine = self.get_engine(connection_name)
            start = datetime.utcnow()

            with engine.connect() as conn:
                rs = conn.execute(text(sql), params or {})

                if rs.returns_rows:
                    columns = list(rs.keys())
                    rows = [list(row) for row in rs.fetchall()]
                    elapsed = (datetime.utcnow() - start).total_seconds()

                    result['success'] = True
                    result['columns'] = columns
                    result['rows'] = rows
                    result['row_count'] = len(rows)
                    result['execution_time'] = round(elapsed, 3)
                else:
                    conn.commit()
                    elapsed = (datetime.utcnow() - start).total_seconds()
                    result['success'] = True
                    result['row_count'] = rs.rowcount
                    result['execution_time'] = round(elapsed, 3)
                    result['columns'] = ['affected_rows']
                    result['rows'] = [[rs.rowcount]]

        except SQLAlchemyError as e:
            result['error'] = str(e)
            logger.error(f"SQL execution error: {e}")
        except Exception as e:
            result['error'] = str(e)

        return result

    def get_schema(self, connection_name: str) -> Dict[str, Any]:
        """Get full database schema (tables, columns, types, relationships)."""
        try:
            engine = self.get_engine(connection_name)
            inspector = inspect(engine)

            schema = {
                'tables': {},
                'total_tables': 0,
            }

            for table_name in inspector.get_table_names():
                columns = []
                for col in inspector.get_columns(table_name):
                    columns.append({
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col.get('nullable', True),
                        'primary_key': False,
                    })

                pk = inspector.get_pk_constraint(table_name)
                if pk and 'constrained_columns' in pk:
                    for col in columns:
                        if col['name'] in pk['constrained_columns']:
                            col['primary_key'] = True

                fks = inspector.get_foreign_keys(table_name)
                indexes = inspector.get_indexes(table_name)

                schema['tables'][table_name] = {
                    'columns': columns,
                    'primary_key': pk.get('constrained_columns', []) if pk else [],
                    'foreign_keys': [
                        {
                            'columns': fk['constrained_columns'],
                            'referred_table': fk['referred_table'],
                            'referred_columns': fk['referred_columns'],
                        }
                        for fk in fks
                    ],
                    'indexes': [
                        {
                            'name': idx['name'],
                            'columns': idx['column_names'],
                            'unique': idx['unique'],
                        }
                        for idx in indexes
                    ],
                    'row_count': self._get_row_count(connection_name, table_name),
                }

            schema['total_tables'] = len(schema['tables'])
            return schema

        except Exception as e:
            logger.error(f"Schema introspection error: {e}")
            return {'tables': {}, 'total_tables': 0, 'error': str(e)}

    def _get_row_count(self, connection_name: str, table_name: str) -> int:
        """Get approximate row count for a table."""
        try:
            result = self.execute_sql(connection_name, f"SELECT COUNT(*) FROM {table_name}")
            if result['success'] and result['rows']:
                return result['rows'][0][0]
        except Exception:
            pass
        return -1

    def get_schema_summary(self, connection_name: str) -> str:
        """Get a text summary of the schema for LLM context."""
        schema = self.get_schema(connection_name)
        if 'error' in schema:
            return f"Error getting schema: {schema['error']}"

        lines = [f"Database Schema ({schema['total_tables']} tables):\n"]
        for table_name, info in schema['tables'].items():
            lines.append(f"\nTable: {table_name} (~{info['row_count']} rows)")
            cols = ', '.join(
                f"{c['name']} ({c['type']}){' [PK]' if c['primary_key'] else ''}"
                for c in info['columns']
            )
            lines.append(f"  Columns: {cols}")
            if info['foreign_keys']:
                for fk in info['foreign_keys']:
                    lines.append(f"  FK: {fk['columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

        return '\n'.join(lines)

    def generate_natural_language_sql_prompt(self, question: str, schema_summary: str) -> str:
        """Build a prompt for LLM to generate SQL from natural language."""
        return f"""You are an expert SQL developer. Given the database schema below, write a SQL query to answer the question.

Database Schema:
{schema_summary}

Question: {question}

Rules:
1. Write ONLY the SQL query, no explanations
2. Use proper SQL syntax for the database type
3. Use table aliases for readability
4. Include column aliases for computed columns
5. If the question is ambiguous, make reasonable assumptions

SQL Query:"""

    def create_sample_sqlite(self, db_path: str = None) -> str:
        """Create a sample SQLite database for demos and exercises."""
        if not db_path:
            db_path = os.path.join(tempfile.gettempdir(), 'finese_sample.db')

        engine = create_engine(f'sqlite:///{db_path}')

        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    city TEXT,
                    country TEXT DEFAULT 'US',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT,
                    price REAL NOT NULL,
                    stock INTEGER DEFAULT 0
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER REFERENCES customers(id),
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    total REAL
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY,
                    order_id INTEGER REFERENCES orders(id),
                    product_id INTEGER REFERENCES products(id),
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL
                )
            """))

            # Insert sample data
            conn.execute(text("DELETE FROM order_items"))
            conn.execute(text("DELETE FROM orders"))
            conn.execute(text("DELETE FROM products"))
            conn.execute(text("DELETE FROM customers"))

            customers = [
                (1, 'Alice Johnson', 'alice@example.com', 'New York', 'US'),
                (2, 'Bob Smith', 'bob@example.com', 'London', 'UK'),
                (3, 'Carlos Ruiz', 'carlos@example.com', 'Madrid', 'ES'),
                (4, 'Diana Chen', 'diana@example.com', 'Singapore', 'SG'),
                (5, 'Eve Williams', 'eve@example.com', 'Toronto', 'CA'),
            ]
            conn.execute(text(
                "INSERT INTO customers (id, name, email, city, country) VALUES (:id, :name, :email, :city, :country)"
            ), [{'id': c[0], 'name': c[1], 'email': c[2], 'city': c[3], 'country': c[4]} for c in customers])

            products = [
                (1, 'Laptop Pro', 'Electronics', 1299.99, 50),
                (2, 'Wireless Mouse', 'Electronics', 29.99, 200),
                (3, 'USB-C Hub', 'Accessories', 49.99, 150),
                (4, 'Monitor 27"', 'Electronics', 449.99, 30),
                (5, 'Keyboard Mech', 'Accessories', 89.99, 100),
                (6, 'Webcam HD', 'Electronics', 79.99, 75),
            ]
            conn.execute(text(
                "INSERT INTO products (id, name, category, price, stock) VALUES (:id, :name, :cat, :price, :stock)"
            ), [{'id': p[0], 'name': p[1], 'cat': p[2], 'price': p[3], 'stock': p[4]} for p in products])

            orders = [
                (1, 1, '2024-01-15', 'completed', 1329.98),
                (2, 2, '2024-01-20', 'completed', 479.98),
                (3, 3, '2024-02-01', 'completed', 89.99),
                (4, 1, '2024-02-10', 'shipped', 49.99),
                (5, 4, '2024-02-15', 'pending', 1379.98),
                (6, 5, '2024-03-01', 'completed', 159.98),
            ]
            conn.execute(text(
                "INSERT INTO orders (id, customer_id, order_date, status, total) VALUES (:id, :cid, :date, :status, :total)"
            ), [{'id': o[0], 'cid': o[1], 'date': o[2], 'status': o[3], 'total': o[4]} for o in orders])

            items = [
                (1, 1, 1, 1, 1299.99), (2, 1, 2, 1, 29.99),
                (3, 2, 4, 1, 449.99), (4, 2, 2, 1, 29.99),
                (5, 3, 5, 1, 89.99),
                (6, 4, 3, 1, 49.99),
                (7, 5, 1, 1, 1299.99), (8, 5, 3, 1, 49.99), (9, 5, 6, 1, 29.99),
                (10, 6, 2, 2, 29.99), (11, 6, 5, 1, 89.99),
            ]
            conn.execute(text(
                "INSERT INTO order_items (id, order_id, product_id, quantity, unit_price) VALUES (:id, :oid, :pid, :qty, :price)"
            ), [{'id': i[0], 'oid': i[1], 'pid': i[2], 'qty': i[3], 'price': i[4]} for i in items])

            conn.commit()

        self._engines['sample_db'] = engine
        return db_path


import tempfile
