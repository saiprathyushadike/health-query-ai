#!/usr/bin/env python3
"""
Quick Test - Load Sample Data for Immediate Testing
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def create_sample_data():
    """Create sample medical documents for quick testing"""
    from langchain.schema import Document
    
    sample_docs = [
        Document(
            page_content="""
            Diabetes is a chronic disease that affects how your body turns food into energy. 
            There are two main types: Type 1 diabetes, where the body doesn't make insulin, 
            and Type 2 diabetes, where the body doesn't use insulin well. Symptoms include 
            increased thirst, frequent urination, unexplained weight loss, and fatigue. 
            Treatment typically involves medication, diet changes, and regular exercise.
            """,
            metadata={"source": "mayo_clinic", "title": "Diabetes", "type": "condition_info"}
        ),
        Document(
            page_content="""
            High blood pressure, also called hypertension, is when the force of blood 
            against artery walls is too high. Normal blood pressure is less than 120/80 mmHg. 
            High blood pressure can lead to heart disease, stroke, and kidney problems. 
            Lifestyle changes like reducing salt intake, exercising regularly, and maintaining 
            a healthy weight can help manage blood pressure.
            """,
            metadata={"source": "mayo_clinic", "title": "High Blood Pressure", "type": "condition_info"}
        ),
        Document(
            page_content="""
            Heart disease refers to several types of heart conditions. The most common 
            type is coronary artery disease, which affects blood flow to the heart. 
            Risk factors include smoking, high blood pressure, high cholesterol, and diabetes. 
            Symptoms may include chest pain, shortness of breath, and fatigue. Prevention 
            includes healthy eating, regular exercise, and avoiding tobacco.
            """,
            metadata={"source": "mayo_clinic", "title": "Heart Disease", "type": "condition_info"}
        )
    ]
    
    return sample_docs

def main():
    """Quick test setup"""
    print("🏥 Health Query AI - Quick Test Setup")
    print("=" * 40)
    
    try:
        from rag_system import HealthRAGSystem
        
        print("🔄 Initializing RAG system...")
        rag_system = HealthRAGSystem()
        
        # Add sample documents
        sample_docs = create_sample_data()
        print(f"📚 Adding {len(sample_docs)} sample documents...")
        rag_system.add_documents(sample_docs)
        
        print("✅ Quick setup completed!")
        
        # Test the system
        print("\n🧪 Testing with sample questions...")
        test_questions = [
            "What are the symptoms of diabetes?",
            "How to manage high blood pressure?",
            "What causes heart disease?"
        ]
        
        for question in test_questions:
            print(f"\n❓ {question}")
            response = rag_system.answer_question(question)
            answer = response.get('answer', 'No answer')
            print(f"🤖 {answer[:150]}...")
        
        print("\n🎉 Quick test completed successfully!")
        print("💡 Your Health Query AI is ready for basic questions!")
        print("🌐 Run: streamlit run app_concise.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 