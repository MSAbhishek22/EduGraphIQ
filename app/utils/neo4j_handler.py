from database.neo4j_connection import Neo4jConnection
from .concept_extractor import ConceptExtractor

def create_concept_nodes(text):
    extractor = ConceptExtractor()
    concepts = extractor.extract_concepts(text)
    
    db = Neo4jConnection()
    if not db.connect():
        raise Exception("Failed to connect to Neo4j")
    
    try:
        # Create concept nodes
        for concept in concepts:
            db.create_concept_node(concept['name'], concept['content'])
            
            # Create relationships
            for related in concept.get('related', []):
                db.create_relationship(concept['name'], related, "RELATED_TO")
        
        return concepts
    finally:
        db.close()