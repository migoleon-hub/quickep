# api/services/document_generator.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import jinja2
import pdfkit
import os

class DocumentTemplate(ABC):
    """Abstract base class for document templates"""
    
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> bytes:
        """Generate document from template and data"""
        pass
        
    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate input data against template requirements"""
        pass

class YpefthiniDilosiTemplate(DocumentTemplate):
    """Template for Υπεύθυνη Δήλωση"""
    
    def __init__(self):
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('api/templates/documents'),
            autoescape=True
        )
        self.template = self.env.get_template('ypefthini_dilosi.html')
        
    def validate_data(self, data: Dict[str, Any]) -> bool:
        required_fields = {'full_name', 'father_name', 'mother_name', 
                         'birth_date', 'id_number', 'address', 'content'}
        return all(field in data for field in required_fields)
        
    def generate(self, data: Dict[str, Any]) -> bytes:
        if not self.validate_data(data):
            raise ValueError("Missing required fields for Υπεύθυνη Δήλωση")
            
        # Add generation timestamp
        data['generated_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Render HTML
        html_content = self.template.render(**data)
        
        # Convert to PDF
        pdf_options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
        }
        
        return pdfkit.from_string(html_content, False, options=pdf_options)

class DocumentGenerator:
    """Factory class for document generation"""
    
    def __init__(self):
        self._templates = {
            'ypefthini_dilosi': YpefthiniDilosiTemplate(),
            # Add more templates here
        }
        
    def get_template(self, doc_type: str) -> DocumentTemplate:
        """Get template by document type"""
        template = self._templates.get(doc_type)
        if not template:
            raise ValueError(f"Unknown document type: {doc_type}")
        return template
        
    def generate_document(self, doc_type: str, data: Dict[str, Any]) -> bytes:
        """Generate document of specified type with provided data"""
        template = self.get_template(doc_type)
        return template.generate(data)

# Singleton instance
document_generator = DocumentGenerator()
