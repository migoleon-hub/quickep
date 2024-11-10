# api/services/document_generator.py
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
from fpdf import FPDF
import jinja2

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

class YpefthiniDilosiPDF(FPDF):
    def header(self):
        # Add header
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'ΥΠΕΥΘΥΝΗ ΔΗΛΩΣΗ', align='C', ln=True)
        self.set_font('helvetica', '', 12)
        self.cell(0, 10, '(άρθρο 8 Ν.1599/1986)', align='C', ln=True)
        self.ln(10)

class YpefthiniDilosiTemplate(DocumentTemplate):
    """Template for Υπεύθυνη Δήλωση"""
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        required_fields = {'full_name', 'father_name', 'mother_name', 
                         'birth_date', 'id_number', 'address', 'content'}
        return all(field in data for field in required_fields)
        
    def generate(self, data: Dict[str, Any]) -> bytes:
        if not self.validate_data(data):
            raise ValueError("Missing required fields for Υπεύθυνη Δήλωση")
            
        # Add generation timestamp
        data['generated_at'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Create PDF
        pdf = YpefthiniDilosiPDF()
        pdf.add_page()
        
        # Warning text
        pdf.set_font('helvetica', 'I', 10)
        pdf.multi_cell(0, 5, 'Η ακρίβεια των στοιχείων που υποβάλλονται με αυτή τη δήλωση μπορεί να ελεγχθεί με βάση το αρχείο άλλων υπηρεσιών (άρθρο 8 παρ. 4 Ν. 1599/1986)')
        pdf.ln(10)
        
        # Personal info
        pdf.set_font('helvetica', '', 12)
        pdf.cell(0, 8, f"ΠΡΟΣ:", ln=True)
        pdf.ln(5)
        
        pdf.multi_cell(0, 8, f"""
        Ο/Η (όνομα): {data['full_name']}
        του (πατρώνυμο): {data['father_name']}
        και της (μητρώνυμο): {data['mother_name']}
        Ημερομηνία γέννησης: {data['birth_date']}
        Αριθμός Δελτίου Ταυτότητας: {data['id_number']}
        Τόπος κατοικίας: {data['address']}
        """)
        
        pdf.ln(10)
        pdf.cell(0, 8, "Δηλώνω υπεύθυνα ότι:", ln=True)
        pdf.ln(5)
        
        # Content
        pdf.multi_cell(0, 8, data['content'])
        
        # Date and signature
        pdf.ln(20)
        pdf.cell(0, 8, f"Ημερομηνία: {data['generated_at']}", align='R', ln=True)
        pdf.ln(10)
        pdf.cell(0, 8, "Ο/Η Δηλών/ούσα", align='R', ln=True)
        pdf.ln(20)
        pdf.cell(0, 8, "(Υπογραφή)", align='R')
        
        return pdf.output(dest='S').encode('latin1')

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
