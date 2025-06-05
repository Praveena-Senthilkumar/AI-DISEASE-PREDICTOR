from typing import Dict, Optional

class TreatmentDatabase:
    """Database class for managing cow disease treatment information"""
    
    def __init__(self):
        self.treatments = self._initialize_database()
    
    def _initialize_database(self) -> Dict:
        """Initialize the treatment database with comprehensive treatment protocols"""
        treatments = {
            "Mastitis": {
                "immediate_actions": "Isolate affected cow, milk out infected quarter frequently, apply hot compresses",
                "medications": "Intramammary antibiotics (Penicillin, Ampicillin), Systemic antibiotics for severe cases",
                "dosage": "Follow veterinarian prescription - typically 10-20ml intramammary per infected quarter",
                "duration": "3-5 days of antibiotic treatment, continue until milk tests negative",
                "prevention": "Maintain clean milking environment, post-milking teat dipping, dry cow therapy",
                "follow_up": "Monitor milk quality, bacterial culture testing, check for recurrence"
            },
            "Foot and Mouth Disease": {
                "immediate_actions": "Immediate quarantine, contact veterinary authorities, restrict animal movement",
                "medications": "No specific treatment - supportive care only, pain management if needed",
                "dosage": "Supportive care as directed by veterinarian",
                "duration": "Disease typically runs course in 2-3 weeks",
                "prevention": "Vaccination where permitted, biosecurity measures, quarantine new animals",
                "follow_up": "Report to authorities, ongoing monitoring, gradual return to normal activities"
            },
            "Bovine Respiratory Disease": {
                "immediate_actions": "Isolate affected animals, improve ventilation, reduce stress factors",
                "medications": "Antibiotics (Tulathromycin, Florfenicol), Anti-inflammatory drugs (Flunixin)",
                "dosage": "Antibiotics: 2.5mg/kg body weight, Anti-inflammatory: 1-2mg/kg body weight",
                "duration": "5-10 days depending on severity and response",
                "prevention": "Vaccination program, good ventilation, minimize stress, quarantine new arrivals",
                "follow_up": "Monitor temperature, breathing rate, appetite recovery"
            },
            "Lameness": {
                "immediate_actions": "Examine hooves, clean and trim affected areas, provide dry bedding",
                "medications": "Topical antiseptics (Copper sulfate), Antibiotics for severe infections, Pain relief",
                "dosage": "Topical treatment daily, systemic antibiotics as prescribed by vet",
                "duration": "1-2 weeks for mild cases, longer for severe infections",
                "prevention": "Regular hoof trimming, dry clean bedding, proper nutrition with zinc and biotin",
                "follow_up": "Regular hoof inspections, monitor walking ability, preventive trimming"
            },
            "Milk Fever": {
                "immediate_actions": "Keep cow calm and warm, provide immediate calcium supplementation",
                "medications": "IV Calcium borogluconate (500ml of 20% solution), Magnesium if deficient",
                "dosage": "500ml IV calcium slowly over 10-15 minutes, may repeat in 6-12 hours",
                "duration": "Single treatment often sufficient, monitor for 24-48 hours",
                "prevention": "Proper dry cow nutrition, avoid excess calcium before calving, magnesium supplementation",
                "follow_up": "Monitor for recurrence, check for other metabolic disorders"
            },
            "Ketosis": {
                "immediate_actions": "Provide easily digestible carbohydrates, reduce milk production temporarily",
                "medications": "Propylene glycol orally, Dextrose IV in severe cases, Corticosteroids",
                "dosage": "Propylene glycol 300-500ml daily, Dextrose 500ml IV if needed",
                "duration": "5-7 days of treatment, monitor ketone levels",
                "prevention": "Balanced nutrition, avoid sudden diet changes, monitor body condition",
                "follow_up": "Test ketone levels, monitor milk production, adjust feeding program"
            },
            "Bloat": {
                "immediate_actions": "Pass stomach tube to release gas, keep animal moving, massage left side",
                "medications": "Anti-foaming agents (Poloxalene), Mineral oil, Emergency trocharization if severe",
                "dosage": "Poloxalene 25-50g orally, Mineral oil 500ml-1L",
                "duration": "Immediate treatment required, monitor for 24 hours",
                "prevention": "Gradual diet changes, avoid wet legumes, provide adequate fiber",
                "follow_up": "Monitor for recurrence, adjust feeding management"
            },
            "Pink Eye": {
                "immediate_actions": "Isolate affected animals, protect eyes from sunlight and flies",
                "medications": "Topical antibiotics (Oxytetracycline), Systemic antibiotics in severe cases",
                "dosage": "Apply topical antibiotics 2-3 times daily to affected eye",
                "duration": "7-14 days depending on severity",
                "prevention": "Fly control, face flies management, avoid overcrowding, vaccination available",
                "follow_up": "Monitor for corneal damage, check for spread to other animals"
            },
            "Scours": {
                "immediate_actions": "Provide oral electrolyte solutions, maintain body temperature, continue milk feeding",
                "medications": "Oral electrolytes, Antibiotics if bacterial cause suspected, Probiotics",
                "dosage": "Electrolytes 2-4L daily, Antibiotics as prescribed by veterinarian",
                "duration": "3-7 days, continue until normal feces consistency returns",
                "prevention": "Colostrum management, clean environment, vaccination of pregnant cows",
                "follow_up": "Monitor hydration status, weight gain, prevent secondary infections"
            },
            "Hardware Disease": {
                "immediate_actions": "Restrict movement, provide soft bedding, contact veterinarian immediately",
                "medications": "Magnet administration orally, Antibiotics to prevent secondary infection",
                "dosage": "Cow magnet (100-150g) given orally, Antibiotics as prescribed",
                "duration": "Magnet remains permanently, antibiotic course 5-7 days",
                "prevention": "Remove metallic objects from feed areas, use magnets in feed mixers",
                "follow_up": "Monitor for improvement in appetite and milk production, X-ray confirmation if needed"
            }
        }
        return treatments
    
    def get_treatment_info(self, disease_name: str) -> Optional[Dict]:
        """Get treatment information for a specific disease"""
        return self.treatments.get(disease_name)
    
    def get_all_treatments(self) -> Dict:
        """Get all treatments in the database"""
        return self.treatments
    
    def get_medications_list(self) -> set:
        """Get a set of all medications mentioned in treatments"""
        medications = set()
        for treatment in self.treatments.values():
            # Extract medication names from the medications field
            med_text = treatment.get('medications', '')
            # Simple extraction - in a real system, this would be more sophisticated
            if 'Penicillin' in med_text:
                medications.add('Penicillin')
            if 'Ampicillin' in med_text:
                medications.add('Ampicillin')
            if 'Tulathromycin' in med_text:
                medications.add('Tulathromycin')
            # Add more as needed
        return medications
