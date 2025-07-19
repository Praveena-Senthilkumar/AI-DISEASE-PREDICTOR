import os
import pandas as pd
from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

# Database setup
Base = declarative_base()

class CowHealthRecord(Base):
    __tablename__ = 'cow_health_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cow_id = Column(String(50), nullable=False)
    diagnosis_date = Column(DateTime, nullable=False)
    disease_name = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    confidence_score = Column(Float, nullable=True)
    symptoms = Column(Text, nullable=True)
    treatment_applied = Column(Text, nullable=True)
    medication_cost = Column(Float, nullable=True)
    labor_cost = Column(Float, nullable=True)
    supplies_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    veterinarian = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    image_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class VeterinarianRecord(Base):
    __tablename__ = 'veterinarians'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    clinic_name = Column(String(150), nullable=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    specialties = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    emergency_services = Column(Boolean, default=False)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

class TreatmentProtocol(Base):
    __tablename__ = 'treatment_protocols'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    disease_name = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)
    immediate_actions = Column(Text, nullable=False)
    medications = Column(Text, nullable=False)
    dosage = Column(Text, nullable=False)
    duration = Column(Text, nullable=False)
    prevention = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.connect()
    
    def connect(self):
        """Initialize database connection"""
        try:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///pashu_raksha.db')
            self.engine = create_engine(database_url)
            self.Session = sessionmaker(bind=self.engine)
            
            # Create tables if they don't exist
            Base.metadata.create_all(self.engine)
            return True
            
        except Exception as e:
            st.error(f"Database connection failed: {str(e)}")
            return False
    
    def add_health_record(self, record_data: Dict) -> bool:
        """Add a new health record to the database"""
        try:
            session = self.Session()
            
            # Convert date to datetime if needed
            if isinstance(record_data.get('diagnosis_date'), date):
                record_data['diagnosis_date'] = datetime.combine(
                    record_data['diagnosis_date'], 
                    datetime.min.time()
                )
            
            health_record = CowHealthRecord(**record_data)
            session.add(health_record)
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            st.error(f"Failed to add health record: {str(e)}")
            if session:
                session.rollback()
                session.close()
            return False
    
    def get_health_records(self, cow_id: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve health records from database"""
        try:
            session = self.Session()
            
            query = session.query(CowHealthRecord)
            if cow_id:
                query = query.filter(CowHealthRecord.cow_id == cow_id)
            
            records = query.order_by(CowHealthRecord.diagnosis_date.desc()).limit(limit).all()
            
            result = []
            for record in records:
                result.append({
                    'id': record.id,
                    'cow_id': record.cow_id,
                    'diagnosis_date': record.diagnosis_date,
                    'disease_name': record.disease_name,
                    'severity': record.severity,
                    'confidence_score': record.confidence_score,
                    'symptoms': record.symptoms,
                    'treatment_applied': record.treatment_applied,
                    'medication_cost': record.medication_cost,
                    'labor_cost': record.labor_cost,
                    'supplies_cost': record.supplies_cost,
                    'total_cost': record.total_cost,
                    'veterinarian': record.veterinarian,
                    'notes': record.notes,
                    'image_filename': record.image_filename,
                    'created_at': record.created_at
                })
            
            session.close()
            return result
            
        except Exception as e:
            st.error(f"Failed to retrieve health records: {str(e)}")
            return []
    
    def get_disease_statistics(self) -> Dict:
        """Get disease statistics from the database"""
        try:
            session = self.Session()
            
            # Most common diseases
            disease_counts = session.query(
                CowHealthRecord.disease_name,
                session.query(CowHealthRecord).filter(
                    CowHealthRecord.disease_name == CowHealthRecord.disease_name
                ).count().label('count')
            ).group_by(CowHealthRecord.disease_name).all()
            
            # Total records
            total_records = session.query(CowHealthRecord).count()
            
            # Average costs
            avg_cost = session.query(
                session.func.avg(CowHealthRecord.total_cost)
            ).scalar() or 0
            
            session.close()
            
            return {
                'total_records': total_records,
                'disease_counts': dict(disease_counts),
                'average_cost': avg_cost
            }
            
        except Exception as e:
            st.error(f"Failed to get statistics: {str(e)}")
            return {'total_records': 0, 'disease_counts': {}, 'average_cost': 0}
    
    def add_veterinarian(self, vet_data: Dict) -> bool:
        """Add a veterinarian to the database"""
        try:
            session = self.Session()
            veterinarian = VeterinarianRecord(**vet_data)
            session.add(veterinarian)
            session.commit()
            session.close()
            return True
            
        except Exception as e:
            st.error(f"Failed to add veterinarian: {str(e)}")
            return False
    
    def get_veterinarians(self, location: str = None) -> List[Dict]:
        """Get veterinarians from database"""
        try:
            session = self.Session()
            
            query = session.query(VeterinarianRecord)
            if location:
                query = query.filter(VeterinarianRecord.location.ilike(f'%{location}%'))
            
            vets = query.all()
            
            result = []
            for vet in vets:
                result.append({
                    'id': vet.id,
                    'name': vet.name,
                    'clinic_name': vet.clinic_name,
                    'phone': vet.phone,
                    'email': vet.email,
                    'specialties': vet.specialties,
                    'location': vet.location,
                    'emergency_services': vet.emergency_services,
                    'rating': vet.rating
                })
            
            session.close()
            return result
            
        except Exception as e:
            st.error(f"Failed to retrieve veterinarians: {str(e)}")
            return []
    
    def search_records(self, search_term: str) -> List[Dict]:
        """Search health records by disease name, cow ID, or notes"""
        try:
            session = self.Session()
            
            records = session.query(CowHealthRecord).filter(
                (CowHealthRecord.disease_name.ilike(f'%{search_term}%')) |
                (CowHealthRecord.cow_id.ilike(f'%{search_term}%')) |
                (CowHealthRecord.notes.ilike(f'%{search_term}%'))
            ).order_by(CowHealthRecord.diagnosis_date.desc()).all()
            
            result = []
            for record in records:
                result.append({
                    'id': record.id,
                    'cow_id': record.cow_id,
                    'diagnosis_date': record.diagnosis_date,
                    'disease_name': record.disease_name,
                    'severity': record.severity,
                    'total_cost': record.total_cost,
                    'veterinarian': record.veterinarian,
                    'notes': record.notes
                })
            
            session.close()
            return result
            
        except Exception as e:
            st.error(f"Search failed: {str(e)}")
            return []

# Initialize database manager
@st.cache_resource
def get_database_manager():
    return DatabaseManager()