import pandas as pd
import networkx as nx
import json
from typing import Dict, List, Any

class AgriculturalKnowledgeGraph:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.build_graph()
    
    def build_graph(self):
        """Build knowledge graph from CSV data"""
        crops = ["beans", "cassava", "finger_millet", "maize", "sorghum", "sweet_potatoes"]
        
        for crop in crops:
            try:
                df = pd.read_csv(f"data/{crop}.csv")
                crop_node = crop.replace("_", " ").title()
                self.graph.add_node(crop_node, type="crop")
                
                for _, row in df.iterrows():
                    for col, val in row.items():
                        if pd.notna(val) and str(val).strip():
                            # Create attribute nodes and relationships
                            attr_node = f"{col}_{str(val)[:50]}"
                            self.graph.add_node(attr_node, type="attribute", category=col, value=str(val))
                            self.graph.add_edge(crop_node, attr_node, relationship="has_attribute")
                            
                            # Create semantic relationships
                            if "disease" in col.lower():
                                self.graph.add_edge(attr_node, crop_node, relationship="affects")
                            elif "nutrient" in col.lower() or "fertilizer" in col.lower():
                                self.graph.add_edge(attr_node, crop_node, relationship="nourishes")
                            elif "pest" in col.lower():
                                self.graph.add_edge(attr_node, crop_node, relationship="damages")
                            elif "weather" in col.lower() or "climate" in col.lower():
                                self.graph.add_edge(attr_node, crop_node, relationship="influences")
            except:
                continue
    
    def query_graph(self, query: str, max_results: int = 5) -> List[str]:
        """Query the knowledge graph using graph traversal"""
        results = []
        query_lower = query.lower()
        
        # Find relevant nodes
        relevant_nodes = []
        for node, data in self.graph.nodes(data=True):
            if any(term in node.lower() for term in query_lower.split()):
                relevant_nodes.append(node)
        
        # Traverse relationships
        for node in relevant_nodes[:3]:
            # Get direct neighbors
            neighbors = list(self.graph.neighbors(node))
            for neighbor in neighbors[:2]:
                edge_data = self.graph.get_edge_data(node, neighbor)
                if edge_data:
                    rel = list(edge_data.values())[0].get('relationship', 'related_to')
                    neighbor_data = self.graph.nodes[neighbor]
                    
                    if neighbor_data.get('type') == 'attribute':
                        result = f"{node} {rel} {neighbor_data.get('value', neighbor)}"
                        results.append(result)
        
        return results[:max_results]
    
    def get_crop_relationships(self, crop: str) -> Dict[str, List[str]]:
        """Get all relationships for a specific crop"""
        crop_formatted = crop.replace("_", " ").title()
        relationships = {"diseases": [], "nutrients": [], "pests": [], "weather": []}
        
        if crop_formatted in self.graph:
            for neighbor in self.graph.neighbors(crop_formatted):
                neighbor_data = self.graph.nodes[neighbor]
                category = neighbor_data.get('category', '').lower()
                value = neighbor_data.get('value', neighbor)
                
                if 'disease' in category:
                    relationships["diseases"].append(value)
                elif 'nutrient' in category or 'fertilizer' in category:
                    relationships["nutrients"].append(value)
                elif 'pest' in category:
                    relationships["pests"].append(value)
                elif 'weather' in category or 'climate' in category:
                    relationships["weather"].append(value)
        
        return relationships
    
    def save_graph(self, filename: str = "agricultural_knowledge_graph.json"):
        """Save graph to JSON file"""
        graph_data = nx.node_link_data(self.graph)
        with open(filename, 'w') as f:
            json.dump(graph_data, f, indent=2)
    
    def load_graph(self, filename: str = "agricultural_knowledge_graph.json"):
        """Load graph from JSON file"""
        try:
            with open(filename, 'r') as f:
                graph_data = json.load(f)
            self.graph = nx.node_link_graph(graph_data)
        except:
            self.build_graph()

if __name__ == "__main__":
    # Test the knowledge graph
    kg = AgriculturalKnowledgeGraph()
    
    print("🌾 Agricultural Knowledge Graph Built!")
    print(f"Nodes: {kg.graph.number_of_nodes()}")
    print(f"Edges: {kg.graph.number_of_edges()}")
    
    # Test queries
    test_queries = [
        "maize diseases",
        "cassava nutrients",
        "beans pests"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = kg.query_graph(query)
        for result in results:
            print(f"  - {result}")
    
    # Save the graph
    kg.save_graph()
    print("\n✅ Knowledge graph saved!")