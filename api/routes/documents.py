# api/routes/documents.py
from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from api.services.document_generator import document_generator
from api.routes.auth import token_required
from datetime import datetime

bp = Blueprint('documents', __name__, url_prefix='/documents')

@bp.route('/generate/ypefthini-dilosi', methods=['POST'])
@token_required
def generate_ypefthini_dilosi(current_user):
    """Generate Υπεύθυνη Δήλωση"""
    try:
        data = request.get_json()
        
        # Add user information from token
        data.update({
            'full_name': f"{current_user.first_name} {current_user.last_name}".strip(),
        })
        
        # Generate PDF
        pdf_content = document_generator.generate_document('ypefthini_dilosi', data)
        
        # Prepare response
        buffer = BytesIO(pdf_content)
        buffer.seek(0)
        
        filename = f"ypefthini_dilosi_{current_user.id}_{int(datetime.now().timestamp())}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Document generation failed', 'details': str(e)}), 500

@bp.route('/templates', methods=['GET'])
@token_required
def list_templates(current_user):
    """List available document templates"""
    templates = {
        'ypefthini_dilosi': {
            'name': 'Υπεύθυνη Δήλωση',
            'description': 'Γενική φόρμα υπεύθυνης δήλωσης',
            'required_fields': [
                'father_name',
                'mother_name',
                'birth_date',
                'id_number',
                'address',
                'content'
            ]
        }
    }
    return jsonify(templates)

# Validation helper
def validate_ypefthini_dilosi_data(data):
    required = {'father_name', 'mother_name', 'birth_date', 'id_number', 'address', 'content'}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
