from typing import Dict, Optional

class TreatmentDatabase:
    """Database class for managing cow disease treatment information"""

    def __init__(self):
        self.treatments = self._initialize_database()

    def _initialize_database(self) -> Dict:
        """Initialize the treatment database with treatment protocols"""
        treatments = {
            "Actinomycosis": {
                "immediate_actions": "Isolate affected animal; avoid shared feeding areas.",
                "medications": "Iodine solution, Sodium iodide IV, Penicillin.",
                "dosage": "Sodium iodide: 70 mg/kg IV every 7–10 days. Penicillin: 20,000 IU/kg IM.",
                "duration": "2–3 weeks or until lesion regression.",
                "prevention": "Avoid coarse feed that injures mouth, isolate infected animals.",
                "follow_up": "Monitor lesion shrinkage and recurrence; re-administer treatment if needed."
            },
            "Anthrax": {
                "immediate_actions": "Immediate quarantine. Do not open carcasses. Report to veterinary authorities.",
                "medications": "Penicillin, Oxytetracycline (if diagnosed early).",
                "dosage": "Penicillin: 20,000-40,000 IU/kg body weight IM. Oxytetracycline: 10 mg/kg IM.",
                "duration": "3–5 days if caught early.",
                "prevention": "Annual vaccination in endemic areas, safe carcass disposal by burning or deep burial.",
                "follow_up": "Report outbreak, monitor others, vaccinate uninfected herd members."
            },
            "Bovine Papillomatosis": {
                "immediate_actions": "Isolate the affected animal if warts are bleeding or infected. Maintain hygiene to avoid spread.",
                "medications": "Usually self-resolving. In persistent cases, surgical removal or autogenous wart vaccine may be used.",
                "dosage": "Surgical removal under local anesthesia if large or obstructive; autogenous vaccine as advised by vet.",
                "duration": "Warts often regress on their own within 3–6 months. Treatment speeds recovery.",
                "prevention": "Avoid skin trauma, sterilize equipment, isolate infected animals, improve general hygiene.",
                "follow_up": "Inspect healing progress biweekly; manage recurrence if necessary."
            },
            "Brucellosis": {
                "immediate_actions": "Isolate the animal, avoid contact with aborted material and milk.",
                "medications": "No permanent cure. Antibiotics like Rifampicin and Doxycycline may reduce bacterial load.",
                "dosage": "Doxycycline: 5-10 mg/kg orally for 21 days. Rifampicin: 10 mg/kg once daily.",
                "duration": "Chronic disease – treatment is supportive and long-term.",
                "prevention": "Vaccination (S19 or RB51), avoid infected animal purchase, test new animals.",
                "follow_up": "Regular herd testing. Culling may be necessary for chronic carriers."
            },
            "Footrot": {
                "immediate_actions": "Clean hooves, remove debris, isolate animal.",
                "medications": "Topical antiseptics (copper/zinc sulfate), systemic antibiotics (Oxytetracycline).",
                "dosage": "Footbath: 10% zinc/copper sulfate. Oxytetracycline: 10 mg/kg IM daily.",
                "duration": "3–5 days or until improvement.",
                "prevention": "Regular hoof trimming, dry ground, footbaths.",
                "follow_up": "Check hoof condition weekly; repeat treatments if needed."
            },
            "LumpySkinDisease": {
                "immediate_actions": "Isolate the affected cow, apply antiseptic on wounds, manage flies.",
                "medications": "NSAIDs (Flunixin), Broad-spectrum antibiotics (Oxytetracycline) to control secondary infection.",
                "dosage": "Oxytetracycline: 10 mg/kg IM for 3-5 days. Flunixin: 1.1 mg/kg IM.",
                "duration": "5–10 days depending on severity.",
                "prevention": "Vaccination, vector (insect) control, avoid contact with infected animals.",
                "follow_up": "Monitor skin healing, appetite, and temperature daily."
            },
            "Mastitis": {
                "immediate_actions": "Isolate the cow, wash udder with warm water, strip affected quarter frequently.",
                "medications": "Intramammary antibiotics (Penicillin, Ampicillin), NSAIDs (Flunixin).",
                "dosage": "Follow vet guidance. Intramammary: 10-20 ml/quarter. NSAID: 1.1 mg/kg.",
                "duration": "3-5 days of antibiotic therapy or as per vet recommendation.",
                "prevention": "Clean milking environment, post-milking teat dipping, dry cow therapy.",
                "follow_up": "Check milk quality and recurrence weekly."
            },
            "Pinkeye": {
                "immediate_actions": "Isolate affected cow, reduce exposure to sunlight and flies.",
                "medications": "Oxytetracycline (injectable or topical), NSAIDs.",
                "dosage": "Oxytetracycline: 10 mg/kg IM for 3 days. Eye ointment 2x/day.",
                "duration": "3–7 days depending on severity.",
                "prevention": "Fly control, vaccination, reduce dust and bright sunlight exposure.",
                "follow_up": "Monitor eye healing and ensure no relapse."
            },
            "Ringworm": {
                "immediate_actions": "Isolate infected animal to prevent spread; disinfect housing, grooming tools, and environment.",
                "medications": "Topical antifungal creams, iodine-based washes, lime sulfur dips.",
                "dosage": "Apply antifungal cream (like clotrimazole) twice daily; Lime sulfur dip once every 5–7 days.",
                "duration": "2–4 weeks depending on response to treatment.",
                "prevention": "Maintain hygiene, regular grooming, disinfect equipment, and quarantine new or infected animals.",
                "follow_up": "Check for lesion healing weekly, continue hygiene even after lesions fade."
            },
            "Tick Infestation": {
                "immediate_actions": "Manual removal of ticks using tweezers; clean affected areas.",
                "medications": "Topical acaricides (e.g., Amitraz, Cypermethrin), Ivermectin injections.",
                "dosage": "Amitraz 0.025% spray every 7–10 days; Ivermectin 200 mcg/kg subcutaneously once.",
                "duration": "Repeat topical treatments weekly for 3–4 weeks.",
                "prevention": "Maintain clean shelters, regular de-ticking routines, pasture rotation, and apply acaricides preventively.",
                "follow_up": "Inspect animals weekly, reapply treatments as needed, monitor for tick-borne symptoms."
            }
        }

        # Sort treatments alphabetically by disease name
        return dict(sorted(treatments.items()))

    def get_treatment_info(self, disease_name: str) -> Optional[Dict]:
        normalized_name = disease_name.replace(" ", "").lower()
        for key in self.treatments:
            if key.replace(" ", "").lower() == normalized_name:
                return self.treatments[key]
        return None

    def get_all_treatments(self) -> Dict:
        """Get all treatments in the database"""
        return self.treatments

    def get_medications_list(self) -> set:
        """Get a set of all medications mentioned in treatments"""
        medications = set()
        for treatment in self.treatments.values():
            meds = treatment.get("medications", "")
            for med in meds.split(","):
                medications.add(med.strip())
        return medications
