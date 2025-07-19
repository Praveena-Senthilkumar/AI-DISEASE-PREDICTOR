from typing import Dict, List, Optional
import pandas as pd 
class DiseaseDatabase:
    """Database class for managing cow disease information"""

    def __init__(self):
        self.diseases = self._initialize_database()

    def _initialize_database(self) -> Dict:
        """Initialize the disease database with comprehensive information"""
        diseases = {
            "Actinomycosis": {
                "description": "Chronic bacterial infection causing hard swellings, usually around the jaw area ('lumpy jaw').",
                "symptoms": "Hard, immovable swellings on jaw or head, difficulty eating, weight loss.",
                "causes": "Actinomyces bovis bacteria entering through oral wounds or injuries.",
                "severity": "Medium",
                "category": "Bacterial Disease"
            },
            "Anthrax": {
                "description": "Acute infectious disease that causes sudden death in cattle and other animals.",
                "symptoms": "Sudden death, bleeding from orifices, bloating, high fever, trembling, difficulty breathing.",
                "causes": "Bacillus anthracis bacteria found in contaminated soil or feed.",
                "severity": "Critical",
                "category": "Bacterial Disease"
            },
            "Bloat": {
                "description": "Rapid accumulation of gas in the rumen causing abdominal distention.",
                "symptoms": "Distended left abdomen, difficulty breathing, salivation, discomfort.",
                "causes": "Grazing on lush legumes, grain overload, obstruction of esophagus.",
                "severity": "High",
                "category": "Digestive Disease"
            },
            "Bovine Papillomatosis": {
                "description": "A viral skin disease in cattle that causes wart-like growths, especially on the head, neck, and shoulders.",
                "symptoms": "Multiple small to large warts on skin, especially around head, neck, teats, and shoulders. May bleed or get infected.",
                "causes": "Bovine papillomavirus (BPV), typically spread by direct contact or through contaminated equipment.",
                "severity": "Low to Medium",
                "category": "Skin Disease"
            },
            "Bovine Respiratory Disease": {
                "description": "A complex of respiratory infections, often due to stress and viral/bacterial pathogens.",
                "symptoms": "Coughing, nasal discharge, fever, difficulty breathing, lethargy, loss of appetite.",
                "causes": "Viral and bacterial pathogens, stress, poor ventilation, overcrowding.",
                "severity": "High",
                "category": "Respiratory Disease"
            },
            "Brucellosis": {
                "description": "A contagious bacterial disease affecting reproduction, can cause abortion and infertility.",
                "symptoms": "Abortions (especially in third trimester), retained placenta, low milk yield, swollen joints.",
                "causes": "Brucella abortus bacteria, transmitted through contact with infected placenta, fetus, milk, or urine.",
                "severity": "Very High",
                "category": "Reproductive Disease"
            },
            "Foot and Mouth Disease": {
                "description": "Highly contagious viral disease affecting cloven-hoofed animals.",
                "symptoms": "Fever, blisters on mouth and feet, lameness, drooling, loss of appetite.",
                "causes": "Foot-and-mouth disease virus (FMDV), highly contagious.",
                "severity": "Very High",
                "category": "Viral Disease"
            },
            "Footrot": {
                "description": "Infectious condition of the hoof, leading to lameness and foul odor.",
                "symptoms": "Limping, swollen or bleeding hooves, foul odor, reluctance to walk.",
                "causes": "Fusobacterium necrophorum and Dichelobacter nodosus bacteria, wet conditions, poor hygiene.",
                "severity": "High",
                "category": "Locomotor Disease"
            },
            "Hardware Disease": {
                "description": "Injury to internal organs caused by ingestion of metal objects.",
                "symptoms": "Reluctance to move, arched back, drop in milk yield, fever.",
                "causes": "Swallowing nails, wire, or sharp metal that pierces the reticulum.",
                "severity": "High",
                "category": "Digestive Disease"
            },
            "Ketosis": {
                "description": "Metabolic disorder due to negative energy balance, common in early lactation.",
                "symptoms": "Loss of appetite, sweet-smelling breath, weight loss, decreased milk production.",
                "causes": "Insufficient energy intake, high milk output, fat metabolism.",
                "severity": "Medium",
                "category": "Metabolic Disease"
            },
            "Lameness": {
                "description": "Condition affecting the cow's ability to walk, caused by hoof problems or injury.",
                "symptoms": "Limping, reluctance to walk, swollen joints, abnormal gait.",
                "causes": "Hoof rot, sole ulcers, arthritis, poor flooring, trauma.",
                "severity": "Medium",
                "category": "Locomotor Disease"
            },
            "LumpySkinDisease": {
                "description": "Viral disease that causes skin nodules and affects lymph nodes, often resulting in fever and weight loss.",
                "symptoms": "Skin nodules, fever, loss of appetite, nasal discharge, swollen lymph nodes, lameness.",
                "causes": "Capripoxvirus spread by flies, mosquitoes, and contaminated equipment.",
                "severity": "High",
                "category": "Viral Disease"
            },
            "Mastitis": {
                "description": "Inflammation of the mammary gland and udder tissue, commonly caused by bacterial infection.",
                "symptoms": "Swollen udder, hot udder, abnormal milk (clots, blood, watery), reduced milk production, fever.",
                "causes": "Bacterial infection (E. coli, Staphylococcus, Streptococcus), poor hygiene, trauma, stress.",
                "severity": "High",
                "category": "Udder Disease"
            },
            "Milk Fever": {
                "description": "Calcium deficiency in blood, often after calving, leading to muscle weakness and collapse.",
                "symptoms": "Weakness, inability to stand, cold ears, dull eyes, muscle tremors, coma.",
                "causes": "Low blood calcium (hypocalcemia) especially in high-producing dairy cows.",
                "severity": "High",
                "category": "Metabolic Disease"
            },
            "Pinkeye": {
                "description": "Infectious eye disease causing inflammation and clouding of the eye.",
                "symptoms": "Watery eye discharge, redness, swelling, sensitivity to light.",
                "causes": "Moraxella bovis bacteria, flies, dust, UV rays.",
                "severity": "Medium",
                "category": "Eye Disease"
            },
            "Ringworm": {
                "description": "A fungal skin infection that causes circular patches of hair loss, scabs, and scaling.",
                "symptoms": "Circular bald patches, dry/flaky skin, crusty lesions, itchiness.",
                "causes": "Dermatophyte fungi (usually Trichophyton or Microsporum) spread through direct contact or contaminated surfaces.",
                "severity": "Moderate",
                "category": "Skin Disease"
            },
            "Scours": {
                "description": "Diarrheal disease in calves causing dehydration and weakness.",
                "symptoms": "Watery diarrhea, sunken eyes, dry nose, depression, loss of appetite.",
                "causes": "Rotavirus, coronavirus, E. coli, Salmonella, poor sanitation.",
                "severity": "High",
                "category": "Digestive Disease"
            },
            "Tick Infestation": {
                "description": "Infestation of the skin by ticks that feed on blood, causing irritation, anemia, and disease transmission.",
                "symptoms": "Visible ticks on skin, itching, inflammation, anemia, skin irritation, transmission of diseases like babesiosis.",
                "causes": "Exposure to tick-infested environments such as grasslands, untreated barns, and pasture.",
                "severity": "High",
                "category": "Parasitic Infestation"
            }
        }

        # Sort dictionary alphabetically by key
        return dict(sorted(diseases.items()))

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
            if search_term in disease_name.lower():
                matching_diseases.append(disease_name)
                continue
            if search_term in disease_info['symptoms'].lower():
                matching_diseases.append(disease_name)
                continue
            if search_term in disease_info['description'].lower():
                matching_diseases.append(disease_name)
                continue

        return matching_diseases

    def get_diseases_by_category(self, category: str) -> List[str]:
        """Get diseases by category"""
        return [name for name, info in self.diseases.items()
                if info.get('category', '').lower() == category.lower()]
