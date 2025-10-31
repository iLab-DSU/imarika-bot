#!/usr/bin/env python3
"""
Test Script for QLoRA Integration
Tests the fine-tuned model integration and compares performance
"""

import os
import sys
import time
import json
from pathlib import Path

# Add fine_tuning to path
sys.path.append('fine_tuning')

from fine_tuning.qlora_model_integration import IntegratedImarika
from fine_tuning.langgraph_qlora_integration import QLoRALangGraphAgent
from fine_tuning.performance_evaluator import PerformanceEvaluator

def test_model_loading():
    """Test if QLoRA model loads correctly"""
    print("🧪 Testing QLoRA Model Loading...")
    print("=" * 50)
    
    # Check if model zip exists
    model_zip = "imarika_csv_qlora_model.zip"
    if not os.path.exists(model_zip):
        print(f"❌ Model zip not found: {model_zip}")
        print("   Please ensure the model zip is in the root directory")
        return False
    
    # Test model integration
    try:
        imarika = IntegratedImarika()
        model_info = imarika.get_model_info()
        
        print(f"✅ Model Integration Status:")
        print(f"   Model Type: {model_info['model_type']}")
        print(f"   QLoRA Available: {model_info['qlora_available']}")
        print(f"   Device: {model_info['device']}")
        
        return model_info['qlora_available']
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_basic_responses():
    """Test basic response generation"""
    print("\n🧪 Testing Basic Response Generation...")
    print("=" * 50)
    
    imarika = IntegratedImarika()
    
    test_queries = [
        "What nutrients does maize need?",
        "How to control pests in beans?",
        "Best planting time for cassava?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        
        start_time = time.time()
        response = imarika.generate_response(query)
        end_time = time.time()
        
        print(f"Response: {response[:150]}...")
        print(f"Time: {end_time - start_time:.2f}s")
        print(f"Model: {imarika.get_model_info()['model_type']}")

def test_langgraph_integration():
    """Test LangGraph integration with QLoRA"""
    print("\n🧪 Testing LangGraph Integration...")
    print("=" * 50)
    
    try:
        agent = QLoRALangGraphAgent()
        
        test_queries = [
            "What can you do?",
            "Maize nutrients in Nairobi weather",
            "Bean pest control methods"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            
            start_time = time.time()
            response = agent.run_agent(query)
            end_time = time.time()
            
            print(f"Response: {response[:200]}...")
            print(f"Time: {end_time - start_time:.2f}s")
            
    except Exception as e:
        print(f"❌ LangGraph integration failed: {e}")

def run_performance_comparison():
    """Run comprehensive performance comparison"""
    print("\n🧪 Running Performance Comparison...")
    print("=" * 50)
    
    try:
        evaluator = PerformanceEvaluator()
        
        # Run quick evaluation (subset of queries)
        quick_queries = [
            "What nutrients does maize need for optimal growth?",
            "Common pests affecting beans and control methods",
            "Best weather conditions for cassava planting",
            "Sorghum drought resistance techniques"
        ]
        
        # Override test queries for quick test
        evaluator.test_queries = quick_queries
        
        results = evaluator.run_comprehensive_evaluation()
        
        if results['qlora_results']:
            # Generate report
            report = evaluator.generate_report(results)
            print("\n" + report)
            
            # Save results
            evaluator.save_results(results, "qlora_quick_evaluation.json")
            
            # Print summary
            summary = results['summary']
            improvement = summary['improvement']['composite_score']
            print(f"\n🏆 QUICK SUMMARY:")
            print(f"   Overall Improvement: +{improvement:.1f}%")
            print(f"   QLoRA Score: {summary['qlora_average']['composite_score']:.3f}")
            print(f"   Base Score: {summary['base_average']['composite_score']:.3f}")
        else:
            print("❌ QLoRA model not available for comparison")
            
    except Exception as e:
        print(f"❌ Performance comparison failed: {e}")

def check_system_requirements():
    """Check system requirements and dependencies"""
    print("🔍 Checking System Requirements...")
    print("=" * 50)
    
    requirements = {
        "torch": "PyTorch for model loading",
        "transformers": "Hugging Face Transformers",
        "peft": "Parameter Efficient Fine-Tuning",
        "bitsandbytes": "Quantization support"
    }
    
    missing_deps = []
    
    for package, description in requirements.items():
        try:
            __import__(package)
            print(f"✅ {package}: Available")
        except ImportError:
            print(f"❌ {package}: Missing - {description}")
            missing_deps.append(package)
    
    if missing_deps:
        print(f"\n📦 Install missing dependencies:")
        print(f"   pip install {' '.join(missing_deps)}")
        return False
    
    # Check CUDA availability
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA: Available - {torch.cuda.get_device_name(0)}")
        else:
            print(f"⚠️  CUDA: Not available - Will use CPU (slower)")
    except:
        print(f"❌ PyTorch: Cannot check CUDA status")
    
    return len(missing_deps) == 0

def main():
    """Main test function"""
    print("🌾 IMARIKA QLORA INTEGRATION TEST SUITE")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met. Please install missing dependencies.")
        return
    
    # Test model loading
    model_loaded = test_model_loading()
    
    if model_loaded:
        print("\n✅ QLoRA model loaded successfully!")
        
        # Run all tests
        test_basic_responses()
        test_langgraph_integration()
        run_performance_comparison()
        
        print("\n🎉 All tests completed!")
        print("\n📋 Next Steps:")
        print("   1. Review performance comparison results")
        print("   2. Integrate QLoRA agent into main system")
        print("   3. Update Streamlit interface to use QLoRA")
        print("   4. Run full evaluation with all test queries")
        
    else:
        print("\n❌ QLoRA model not available.")
        print("\n📋 Troubleshooting:")
        print("   1. Ensure imarika_csv_qlora_model.zip is in root directory")
        print("   2. Check if model was saved correctly from notebook")
        print("   3. Verify all dependencies are installed")
        print("   4. Check CUDA availability for GPU models")

if __name__ == "__main__":
    main()