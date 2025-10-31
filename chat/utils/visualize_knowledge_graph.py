import matplotlib.pyplot as plt
import networkx as nx
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.knowledge_graph import AgriKnowledgeGraph
import json

def visualize_knowledge_graph():
    """Create and save knowledge graph visualization"""
    kg = AgriKnowledgeGraph()
    
    # Create layout
    pos = nx.spring_layout(kg.graph, k=3, iterations=50)
    
    # Set up the plot
    plt.figure(figsize=(15, 12))
    
    # Define colors for different node types
    colors = {
        'crop': '#2E8B57',      # Green
        'nutrient': '#4169E1',   # Blue
        'pest': '#DC143C',       # Red
        'activity': '#FF8C00',   # Orange
        'stage': '#9932CC'       # Purple
    }
    
    # Draw nodes by type
    for node_type, color in colors.items():
        nodes = [n for n, d in kg.graph.nodes(data=True) if d.get('type') == node_type]
        nx.draw_networkx_nodes(kg.graph, pos, nodelist=nodes, 
                              node_color=color, node_size=800, alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(kg.graph, pos, alpha=0.5, width=1, edge_color='gray')
    
    # Draw labels
    nx.draw_networkx_labels(kg.graph, pos, font_size=8, font_weight='bold')
    
    plt.title("Imarika Agricultural Knowledge Graph\n22 Nodes • 72 Relationships", 
              fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=color, markersize=10, label=node_type.title())
                      for node_type, color in colors.items()]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('knowledge_graph_visualization.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return kg.graph

def export_graph_data(graph):
    """Export graph data for web visualization"""
    # Convert to JSON format
    data = {
        "nodes": [],
        "links": []
    }
    
    # Add nodes
    for node, attrs in graph.nodes(data=True):
        data["nodes"].append({
            "id": node,
            "type": attrs.get('type', 'unknown'),
            "label": node
        })
    
    # Add edges
    for source, target, attrs in graph.edges(data=True):
        data["links"].append({
            "source": source,
            "target": target,
            "relation": attrs.get('relation', 'related')
        })
    
    # Save to file
    with open('knowledge_graph_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    return data

if __name__ == "__main__":
    print("🌾 Generating Knowledge Graph Visualization...")
    graph = visualize_knowledge_graph()
    data = export_graph_data(graph)
    
    print(f"✅ Visualization saved: knowledge_graph_visualization.png")
    print(f"✅ Data exported: knowledge_graph_data.json")
    print(f"📊 Graph Stats: {len(data['nodes'])} nodes, {len(data['links'])} edges")