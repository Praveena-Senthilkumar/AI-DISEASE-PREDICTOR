import pandas as pd
from typing import Dict, List, Optional

class DiseaseDatabase:
    """Database class for managing cow disease information"""
    
    def __init__(self):
        self.diseases = self._initialize_database()
    
    def _initialize_database(self) -> Dict:
        """Initialize the disease database with comprehensive information"""
        diseases = {
            "Mastitis": {
                "description": "Inflammation of the mammary gland and udder tissue, commonly caused by bacterial infection.",
                "symptoms": "Swollen udder, hot udder, abnormal milk (clots, blood, watery), reduced milk production, fever",
                "causes": "Bacterial infection (E. coli, Staphylococcus, Streptococcus), poor hygiene, trauma, stress",
                "severity": "High",
                "category": "Udder Disease"
            },
            "Foot and Mouth Disease": {
                "description": "Highly contagious viral disease affecting cloven-hoofed animals.",
                "symptoms": "Fever, blisters on mouth and feet, lameness, drooling, loss of appetite",
                "causes": "Foot-and-mouth disease virus (FMDV), highly contagious",
                "severity": "Very High",
                "category": "Viral Disease"
            },
            "Bovine Respiratory Disease": {
                "description": "Complex of respiratory infections affecting cattle, also known as shipping fever.",
                "symptoms": "Coughing, nasal discharge, fever, difficulty breathing, lethargy, loss of appetite",
                "causes": "Viral and bacterial pathogens, stress, poor ventilation, overcrowding",
                "severity": "High",
                "category": "Respiratory Disease"
            },
            "Lameness": {
                "description": "Condition affecting the cow's ability to walk normally, often due to hoof problems.",
                "symptoms": "Limping, reluctance to walk, standing on three legs, swollen joints or hooves",
                "causes": "Hoof rot, sole ulcers, white line disease, arthritis, injury",
                "severity": "Medium",
                "category": "Locomotor Disease"
            },
            "Milk Fever": {
                "description": "Metabolic disorder caused by low blood calcium levels, typically in dairy cows after calving.",
                "symptoms": "Muscle weakness, inability to stand, cold ears and legs, rapid heartbeat, coma",
                "causes": "Calcium deficiency, typically occurs within 72 hours of calving",
                "severity": "High",
                "category": "Metabolic Disease"
            },
            "Ketosis": {
                "description": "Metabolic disorder characterized by elevated ketone bodies in blood and urine.",
                "symptoms": "Sweet/fruity breath odor, loss of appetite, weight loss, reduced milk production, depression",
                "causes": "Negative energy balance, inadequate nutrition, high milk production demands",
                "severity": "Medium",
                "category": "Metabolic Disease"
            },
            "Bloat": {
                "description": "Accumulation of gas in the rumen, causing distension of the left side of the abdomen.",
                "symptoms": "Distended left side, difficulty breathing, restlessness, foaming at mouth",
                "causes": "Rapid consumption of legumes, grain overload, obstruction",
                "severity": "High",
                "category": "Digestive Disease"
            },
            "Pink Eye": {
                "description": "Infectious eye disease causing inflammation of the conjunctiva and cornea.",
                "symptoms": "Red, watery eyes, cloudy cornea, light sensitivity, discharge from eyes",
                "causes": "Bacterial infection (Moraxella bovis), flies, dust, UV light",
                "severity": "Medium",
                "category": "Eye Disease"
            },
            "Scours": {
                "description": "Diarrheal disease primarily affecting young calves, can be life-threatening.",
                "symptoms": "Watery diarrhea, dehydration, weakness, loss of appetite, sunken eyes",
                "causes": "Viral, bacterial, or parasitic infections, poor hygiene, stress",
                "severity": "High",
                "category": "Digestive Disease"
            },
            "Hardware Disease": {
                "description": "Condition caused by ingestion of metallic foreign objects that penetrate the reticulum.",
                "symptoms": "Loss of appetite, decreased milk production, arched back, reluctance to move, fever",
                "causes": "Ingestion of nails, wire, or other metallic objects",
                "severity": "High",
                "category": "Digestive Disease"
            }
        }
        return diseases
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """Get information for a specific disease"""
        return self.diseases.get(disease_name)
    
    def get_all_diseases(self) -> Dict:
        """Get all diseases in the database"""
        return self.diseases
    
    def search_diseases(self, search_term: str) -> List[str]:
        """Search for diseases by name or symptoms"""
        search_term = search_term.lower()
        matching_diseases = []
        
        for disease_name, disease_info in self.diseases.items():
            # Search in disease name
            if search_term in disease_name.lower():
                matching_diseases.append(disease_name)
                continue
            
            # Search in symptoms
            if search_term in disease_info['symptoms'].lower():
                matching_diseases.append(disease_name)
                continue
            
            # Search in description
            if search_term in disease_info['description'].lower():
                matching_diseases.append(disease_name)
                continue
        
        return matching_diseases
    
    def get_diseases_by_category(self, category: str) -> List[str]:
        """Get diseases by category"""
        return [name for name, info in self.diseases.items() 
                if info.get('category', '').lower() == category.lower()]
