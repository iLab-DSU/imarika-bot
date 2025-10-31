import pandas as pd
import networkx as nx
import json
from typing import Dict, List

class AgriKnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.build_from_csv()
    
    def build_from_csv(self):
        """Build knowledge graph from CSV files"""
        crops = ["beans", "cassava", "finger_millet", "maize", "sorghum", "sweet_potatoes"]
        
        for crop in crops:
            try:
                df = pd.read_csv(f"data/{crop}.csv")
                crop_node = crop.replace("_", " ").title()
                self.graph.add_node(crop_node, type="crop")
                
                for _, row in df.iterrows():
                    # Extract farming activities
                    if 'Farming Activities' in row and pd.notna(row['Farming Activities']):
                        activity = str(row['Farming Activities']).strip()
                        self.graph.add_node(activity, type="activity")
                        self.graph.add_edge(crop_node, activity, relation="requires")
                    
                    # Extract growth stages
                    if 'Growth Stages' in row and pd.notna(row['Growth Stages']):
                        stage = str(row['Growth Stages']).strip()
                        self.graph.add_node(stage, type="stage")
                        self.graph.add_edge(crop_node, stage, relation="has_stage")
                    
                    # Extract from text content
                    for col, val in row.items():
                        if pd.notna(val) and len(str(val)) > 50:
                            text = str(val).lower()
                            
                            # Extract nutrients
                            nutrients = ['nitrogen', 'phosphorus', 'potassium', 'manure', 'compost', 'dap', 'npk']
                            for nutrient in nutrients:
                                if nutrient in text:
                                    self.graph.add_node(nutrient.title(), type="nutrient")
                                    self.graph.add_edge(crop_node, nutrient.title(), relation="needs")
                            
                            # Extract pests and pest-related terms
                            pest_terms = ['weevil', 'borer', 'aphid', 'caterpillar', 'termite', 'insect', 'pest', 'wadudu', 'rodent', 'panya']
                            for pest in pest_terms:
                                if pest in text:
                                    pest_name = pest.title() if pest != 'wadudu' else 'Insects'
                                    if pest == 'panya':
                                        pest_name = 'Rodents'
                                    self.graph.add_node(pest_name, type="pest")
                                    self.graph.add_edge(pest_name, crop_node, relation="attacks")
                            
                            # Extract diseases
                            disease_terms = ['disease', 'magonjwa', 'rot', 'blight', 'wilt', 'fungal', 'bacterial']
                            for disease in disease_terms:
                                if disease in text:
                                    disease_name = disease.title() if disease != 'magonjwa' else 'Diseases'
                                    self.graph.add_node(disease_name, type="disease")
                                    self.graph.add_edge(disease_name, crop_node, relation="affects")
            except:
                continue
    
    def query(self, query_text: str) -> List[str]:
        """Query graph using node matching and traversal"""
        results = []
        query_lower = query_text.lower()
        
        # Find matching nodes
        matching_nodes = []
        for node in self.graph.nodes():
            if any(term in node.lower() for term in query_lower.split()):
                matching_nodes.append(node)
        
        # Get relationships for matching nodes
        for node in matching_nodes[:3]:
            # Outgoing edges (what this node affects/needs)
            for neighbor in self.graph.successors(node):
                edge_data = self.graph.get_edge_data(node, neighbor)
                relation = edge_data.get('relation', 'related_to')
                results.append(f"{node} {relation} {neighbor}")
            
            # Incoming edges (what affects this node)
            for predecessor in self.graph.predecessors(node):
                edge_data = self.graph.get_edge_data(predecessor, node)
                relation = edge_data.get('relation', 'related_to')
                results.append(f"{predecessor} {relation} {node}")
        
        return results[:5] if results else ["No relationships found"]

# Test and create the graph
if __name__ == "__main__":
    kg = AgriKnowledgeGraph()
    print(f"Knowledge Graph: {kg.graph.number_of_nodes()} nodes, {kg.graph.number_of_edges()} edges")
    
    # Show nodes by type
    for node_type in ['crop', 'nutrient', 'pest', 'activity']:
        nodes = [n for n, d in kg.graph.nodes(data=True) if d.get('type') == node_type]
        print(f"\n{node_type.title()} nodes: {nodes[:5]}")
    
    # Test queries
    for query in ["maize", "nitrogen", "weevil", "planting"]:
        print(f"\nQuery: {query}")
        results = kg.query(query)
        for r in results:
            print(f"  - {r}")