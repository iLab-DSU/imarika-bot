#!/usr/bin/env python3
"""
Comprehensive Performance Evaluation System
Compares QLoRA fine-tuned model vs Base Ollama model
"""

import time
import json
import pandas as pd
from typing import Dict, List, Tuple
import subprocess
from qlora_model_integration import IntegratedImarika, OllamaFallback

class PerformanceEvaluator:
    def __init__(self):
        self.qlora_model = IntegratedImarika()
        self.base_model = OllamaFallback()
        
        # Test queries covering all crops and scenarios
        self.test_queries = [
            # Nutrient queries
            "What nutrients does maize need for optimal growth?",
            "Which fertilizers are best for beans cultivation?",
            "How to improve soil fertility for cassava?",
            "Nutrient deficiency signs in finger millet",
            "Organic fertilizers for sorghum farming",
            "Sweet potato nutrient requirements",
            
            # Pest and disease queries
            "Common pests affecting maize crops",
            "How to control bean weevils naturally?",
            "Cassava mosaic disease prevention",
            "Finger millet blast disease management",
            "Sorghum stem borer control methods",
            "Sweet potato virus diseases",
            
            # Weather and climate queries
            "Best weather conditions for maize planting",
            "How does rainfall affect bean production?",
            "Drought-resistant cassava varieties",
            "Climate requirements for finger millet",
            "Sorghum adaptation to dry conditions",
            "Sweet potato growing seasons",
            
            # Farming practices
            "Maize intercropping with beans benefits",
            "Proper spacing for cassava planting",
            "Harvesting time for finger millet",
            "Sorghum storage best practices",
            "Sweet potato propagation methods",
            "Crop rotation with these six crops"
        ]
        
        # Expected keywords for each query category
        self.expected_keywords = {
            "nutrients": ["nitrogen", "phosphorus", "potassium", "NPK", "fertilizer", "manure", "compost"],
            "pests": ["pest", "insect", "weevil", "borer", "control", "spray", "organic"],
            "weather": ["rainfall", "temperature", "season", "climate", "drought", "irrigation"],
            "practices": ["planting", "spacing", "harvest", "storage", "rotation", "intercrop"]
        }
    
    def evaluate_response_quality(self, query: str, response: str) -> Dict[str, float]:
        """Evaluate response quality using multiple metrics"""
        metrics = {}
        
        # 1. Response Length (completeness indicator)
        metrics['length_score'] = min(len(response.split()) / 50, 1.0)  # Normalize to 50 words
        
        # 2. Agricultural Keyword Density
        agri_keywords = [
            "crop", "plant", "soil", "fertilizer", "pest", "disease", "harvest", "yield",
            "nitrogen", "phosphorus", "potassium", "irrigation", "drought", "season",
            "maize", "beans", "cassava", "millet", "sorghum", "potato"
        ]
        
        response_lower = response.lower()
        keyword_count = sum(1 for keyword in agri_keywords if keyword in response_lower)
        metrics['keyword_density'] = min(keyword_count / 10, 1.0)  # Normalize to 10 keywords
        
        # 3. Query Relevance (specific keywords based on query)
        query_lower = query.lower()
        relevant_keywords = []
        
        if any(word in query_lower for word in ["nutrient", "fertilizer", "soil"]):
            relevant_keywords = self.expected_keywords["nutrients"]
        elif any(word in query_lower for word in ["pest", "disease", "control"]):
            relevant_keywords = self.expected_keywords["pests"]
        elif any(word in query_lower for word in ["weather", "climate", "rain", "drought"]):
            relevant_keywords = self.expected_keywords["weather"]
        else:
            relevant_keywords = self.expected_keywords["practices"]
        
        relevance_count = sum(1 for keyword in relevant_keywords if keyword in response_lower)
        metrics['relevance_score'] = min(relevance_count / len(relevant_keywords), 1.0)
        
        # 4. Crop Specificity (mentions specific crops)
        crops = ["maize", "beans", "cassava", "millet", "sorghum", "potato"]
        crop_mentions = sum(1 for crop in crops if crop in response_lower)
        metrics['crop_specificity'] = min(crop_mentions / 2, 1.0)  # Normalize to 2 crops
        
        # 5. Practical Advice Indicators
        practical_indicators = [
            "apply", "use", "plant", "harvest", "control", "prevent", "manage",
            "recommend", "should", "can", "will", "best", "optimal"
        ]
        practical_count = sum(1 for indicator in practical_indicators if indicator in response_lower)
        metrics['practical_score'] = min(practical_count / 5, 1.0)  # Normalize to 5 indicators
        
        # 6. Composite Score (weighted average)
        weights = {
            'length_score': 0.15,
            'keyword_density': 0.25,
            'relevance_score': 0.30,
            'crop_specificity': 0.15,
            'practical_score': 0.15
        }
        
        metrics['composite_score'] = sum(metrics[key] * weights[key] for key in weights)
        
        return metrics
    
    def measure_response_time(self, model, query: str, context: str = "") -> Tuple[str, float]:
        """Measure response time for a model"""
        start_time = time.time()
        
        if hasattr(model, 'generate_response'):
            response = model.generate_response(query, context)
        else:
            response = "Error: Invalid model"
        
        end_time = time.time()
        return response, end_time - start_time
    
    def run_comprehensive_evaluation(self) -> Dict:
        """Run complete evaluation comparing both models"""
        print("🧪 Starting Comprehensive Performance Evaluation...")
        print("=" * 60)
        
        results = {
            'qlora_results': [],
            'base_results': [],
            'comparison': {},
            'summary': {}
        }
        
        total_queries = len(self.test_queries)
        
        for i, query in enumerate(self.test_queries, 1):
            print(f"\n📝 Query {i}/{total_queries}: {query[:50]}...")
            
            # Test QLoRA model
            if self.qlora_model.use_qlora:
                qlora_response, qlora_time = self.measure_response_time(self.qlora_model, query)
                qlora_metrics = self.evaluate_response_quality(query, qlora_response)
                qlora_metrics['response_time'] = qlora_time
                qlora_metrics['query'] = query
                qlora_metrics['response'] = qlora_response[:200] + "..." if len(qlora_response) > 200 else qlora_response
                results['qlora_results'].append(qlora_metrics)
                print(f"   QLoRA: {qlora_metrics['composite_score']:.3f} ({qlora_time:.2f}s)")
            else:
                print("   QLoRA: Not available")
            
            # Test Base model
            base_response, base_time = self.measure_response_time(self.base_model, query)
            base_metrics = self.evaluate_response_quality(query, base_response)
            base_metrics['response_time'] = base_time
            base_metrics['query'] = query
            base_metrics['response'] = base_response[:200] + "..." if len(base_response) > 200 else base_response
            results['base_results'].append(base_metrics)
            print(f"   Base:  {base_metrics['composite_score']:.3f} ({base_time:.2f}s)")
        
        # Calculate averages and comparisons
        if results['qlora_results']:
            qlora_avg = self.calculate_averages(results['qlora_results'])
            base_avg = self.calculate_averages(results['base_results'])
            
            results['summary'] = {
                'qlora_average': qlora_avg,
                'base_average': base_avg,
                'improvement': {
                    metric: ((qlora_avg[metric] - base_avg[metric]) / base_avg[metric] * 100)
                    for metric in qlora_avg if metric != 'response_time'
                },
                'speed_comparison': {
                    'qlora_avg_time': qlora_avg['response_time'],
                    'base_avg_time': base_avg['response_time'],
                    'time_difference': qlora_avg['response_time'] - base_avg['response_time']
                }
            }
        
        return results
    
    def calculate_averages(self, results: List[Dict]) -> Dict[str, float]:
        """Calculate average metrics"""
        if not results:
            return {}
        
        metrics = ['length_score', 'keyword_density', 'relevance_score', 
                  'crop_specificity', 'practical_score', 'composite_score', 'response_time']
        
        averages = {}
        for metric in metrics:
            values = [r[metric] for r in results if metric in r]
            averages[metric] = sum(values) / len(values) if values else 0
        
        return averages
    
    def generate_report(self, results: Dict) -> str:
        """Generate detailed evaluation report"""
        report = []
        report.append("🌾 IMARIKA PERFORMANCE EVALUATION REPORT")
        report.append("=" * 50)
        
        if not results['qlora_results']:
            report.append("❌ QLoRA model not available for comparison")
            return "\n".join(report)
        
        summary = results['summary']
        
        report.append(f"\n📊 OVERALL PERFORMANCE COMPARISON")
        report.append("-" * 30)
        
        # Performance metrics
        metrics_display = {
            'composite_score': 'Overall Score',
            'keyword_density': 'Agricultural Keywords',
            'relevance_score': 'Query Relevance',
            'crop_specificity': 'Crop Specificity',
            'practical_score': 'Practical Advice'
        }
        
        for metric, display_name in metrics_display.items():
            qlora_val = summary['qlora_average'][metric]
            base_val = summary['base_average'][metric]
            improvement = summary['improvement'][metric]
            
            report.append(f"{display_name:20}: QLoRA {qlora_val:.3f} | Base {base_val:.3f} | +{improvement:+.1f}%")
        
        # Speed comparison
        speed = summary['speed_comparison']
        report.append(f"\n⚡ RESPONSE TIME COMPARISON")
        report.append("-" * 30)
        report.append(f"QLoRA Average Time: {speed['qlora_avg_time']:.2f}s")
        report.append(f"Base Average Time:  {speed['base_avg_time']:.2f}s")
        report.append(f"Time Difference:    {speed['time_difference']:+.2f}s")
        
        # Top improvements
        improvements = summary['improvement']
        top_improvements = sorted(improvements.items(), key=lambda x: x[1], reverse=True)[:3]
        
        report.append(f"\n🏆 TOP IMPROVEMENTS")
        report.append("-" * 30)
        for metric, improvement in top_improvements:
            display_name = metrics_display.get(metric, metric)
            report.append(f"{display_name}: +{improvement:.1f}%")
        
        # Sample comparisons
        report.append(f"\n📝 SAMPLE RESPONSE COMPARISON")
        report.append("-" * 30)
        
        # Show best performing query
        best_query_idx = max(range(len(results['qlora_results'])), 
                           key=lambda i: results['qlora_results'][i]['composite_score'])
        
        best_qlora = results['qlora_results'][best_query_idx]
        best_base = results['base_results'][best_query_idx]
        
        report.append(f"Query: {best_qlora['query']}")
        report.append(f"QLoRA Response: {best_qlora['response']}")
        report.append(f"Base Response:  {best_base['response']}")
        report.append(f"Score Improvement: {best_qlora['composite_score']:.3f} vs {best_base['composite_score']:.3f}")
        
        return "\n".join(report)
    
    def save_results(self, results: Dict, filename: str = "evaluation_results.json"):
        """Save evaluation results to file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"✅ Results saved to {filename}")

if __name__ == "__main__":
    evaluator = PerformanceEvaluator()
    
    # Run evaluation
    results = evaluator.run_comprehensive_evaluation()
    
    # Generate and display report
    report = evaluator.generate_report(results)
    print("\n" + report)
    
    # Save results
    evaluator.save_results(results, "fine_tuning/qlora_evaluation_results.json")