from flask import Blueprint, request, jsonify
from api import db
from api.routes.auth import token_required
from datetime import datetime

bp = Blueprint('documents', __name__, url_prefix='/documents')

@bp.route('/', methods=['GET'])
@token_required
def get_documents(current_user):
    # Στο μέλλον θα τα παίρνουμε από τη βάση
    docs = [
        {
            "type": "ypeythini_dilosi",
            "name": "Υπεύθυνη Δήλωση",
            "description": "Γενική φόρμα υπεύθυνης δήλωσης",
            "templates": [
                "Γενική Χρήση",
                "Εξουσιοδότηση",
                "Βεβαίωση Κατοικίας"
            ]
        },
        {
            "type": "bebaiosi_anergias",
            "name": "Βεβαίωση Ανεργίας",
            "description": "Αυτόματη λήψη βεβαίωσης ανεργίας",
            "requirements": [
                "ΑΜΚΑ",
                "ΑΦΜ"
            ]
        }
    ]
    return jsonify(docs)

@bp.route('/generate', methods=['POST'])
@token_required
def generate_document(current_user):
    data = request.get_json()
    
    if not data or not data.get('type'):
        return jsonify({'message': 'Missing document type'}), 400
        
    if data['type'] == 'ypeythini_dilosi':
        # Εδώ θα μπει η λογική για τη δημιουργία υπεύθυνης δήλωσης
        return jsonify({
            'message': 'Document generated successfully',
            'document_url': f'/documents/download/{datetime.now().timestamp()}',
            'type': 'ypeythini_dilosi'
        })
    
    elif data['type'] == 'bebaiosi_anergias':
        # Εδώ θα μπει η λογική για τη λήψη βεβαίωσης ανεργίας
        return jsonify({
            'message': 'Document generated successfully',
            'document_url': f'/documents/download/{datetime.now().timestamp()}',
            'type': 'bebaiosi_anergias'
        })
    
    return jsonify({'message': 'Invalid document type'}), 400

@bp.route('/download/<timestamp>', methods=['GET'])
@token_required
def download_document(current_user, timestamp):
    # Εδώ θα μπει η λογική για το download των εγγράφων
    return jsonify({
        'message': 'Document ready for download',
        'timestamp': timestamp
    })
