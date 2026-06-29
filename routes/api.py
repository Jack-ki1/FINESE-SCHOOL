"""
API Routes - File upload, document management, export.
Updated with RAG vector store integration and data analysis.
"""
import os
import io
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, session, send_file
import uuid

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'docx', 'csv', 'json', 'py', 'md',
    'xlsx', 'xls', 'sql', 'r', 'ipynb', 'yaml', 'yml', 'xml', 'html',
}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── File Upload ────────────────────────────────────────────────────

@api_bp.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not _allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    sid = session.get('session_id', 'anon')
    doc_id = str(uuid.uuid4())
    filename = f"{doc_id}_{file.filename}"
    filepath = os.path.join('static', 'uploads', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file.save(filepath)

    # Extract text content
    content = ''
    ext = file.filename.rsplit('.', 1)[1].lower()
    try:
        if ext in ('txt', 'md', 'sql', 'py', 'r', 'yaml', 'yml', 'xml', 'html', 'json', 'csv'):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        elif ext in ('xlsx', 'xls'):
            try:
                import pandas as pd
                df = pd.read_excel(filepath)
                content = df.to_csv(index=False)
            except ImportError:
                content = '[Excel file - install openpyxl to parse]'
    except Exception as e:
        logger.error(f"File extraction error: {e}")
        content = f'[Error reading file: {e}]'

    # Index in vector store
    from core.vector_store import VectorStore
    vs = VectorStore()
    index_result = vs.add_document(sid, doc_id, content, metadata={
        'filename': file.filename,
        'doc_id': doc_id,
        'upload_date': datetime.utcnow().isoformat(),
        'file_type': ext,
    })

    # If CSV, also load into data analyzer
    if ext == 'csv' and content:
        from core.data_analyzer import DataAnalyzer
        analyzer = DataAnalyzer()
        analyzer.load_csv(file.filename.rsplit('.', 1)[0], content)

    return jsonify({
        'success': True,
        'document': {
            'id': doc_id,
            'filename': file.filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath),
            'indexed': index_result.get('success', False),
            'chunks': index_result.get('chunks_added', 0),
        }
    })


# ── Documents ──────────────────────────────────────────────────────

@api_bp.route('/api/documents', methods=['GET'])
def list_documents():
    upload_dir = os.path.join('static', 'uploads')
    docs = []
    if os.path.exists(upload_dir):
        for f in os.listdir(upload_dir):
            if f.startswith('.') or f == '.gitkeep':
                continue
            path = os.path.join(upload_dir, f)
            docs.append({
                'filename': f,
                'size': os.path.getsize(path),
                'modified': datetime.fromtimestamp(os.path.getmtime(path)).isoformat(),
            })
    return jsonify({'documents': docs})


@api_bp.route('/api/documents/<filename>', methods=['DELETE'])
def delete_document(filename):
    filepath = os.path.join('static', 'uploads', filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    # Remove from vector store
    sid = session.get('session_id', 'anon')
    from core.vector_store import VectorStore
    vs = VectorStore()
    doc_id = filename.split('_', 1)[0] if '_' in filename else filename
    vs.delete_document(sid, doc_id)

    return jsonify({'success': True})


# ── Export ─────────────────────────────────────────────────────────

@api_bp.route('/api/export/conversation/<conv_id>', methods=['GET'])
def export_conversation(conv_id):
    """Export conversation as JSON or Markdown."""
    from models.conversation import Conversation
    conv = Conversation.query.get(conv_id)
    if not conv:
        return jsonify({'error': 'Not found'}), 404

    fmt = request.args.get('format', 'json')
    msgs = conv.messages.order_by('created_at').all()

    if fmt == 'md':
        lines = [f"# {conv.title}\n\nExported: {datetime.utcnow().isoformat()}\n\n---\n"]
        for m in msgs:
            role_label = m.role.capitalize()
            lines.append(f"### {role_label}\n\n{m.content}\n\n---\n")
        content = '\n'.join(lines)
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/markdown',
            as_attachment=True,
            download_name=f"{conv.title}.md",
        )
    else:
        data = {
            'title': conv.title,
            'created_at': conv.created_at.isoformat(),
            'messages': [m.to_dict() for m in msgs],
        }
        return jsonify(data)


@api_bp.route('/api/export/data', methods=['POST'])
def export_data():
    """Export query results or analysis as CSV."""
    data = request.get_json() or {}
    columns = data.get('columns', [])
    rows = data.get('rows', [])
    filename = data.get('filename', 'export.csv')

    if not columns or not rows:
        return jsonify({'error': 'No data to export'}), 400

    import csv
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)

    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename,
    )
