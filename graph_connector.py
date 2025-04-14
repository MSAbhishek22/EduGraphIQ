from neo4j import GraphDatabase

# Connection details
uri = "neo4j+s://07030901-cad6-4689-9213-5a23b6186335.databases.neo4j.io:7687"  # Correct URI
username = "neo4j"
password = "M3Z9-H4CZC3scqx__yBe8wtSFz143uhzjn2WmnX1ixA"

# Create a driver instance to connect to Neo4j Aura
driver = GraphDatabase.driver(uri, auth=(username, password))

def create_concept_node(concept_name, definition):
    with driver.session() as session:
        session.run(
            "CREATE (n:Concept {name: $concept_name, definition: $definition})",
            concept_name=concept_name, definition=definition
        )

def close_connection():
    driver.close()

# Add a test concept
create_concept_node("Machine Learning", "Field of AI that enables systems to learn from data.")

print("✅ Data sent to Neo4j Aura!")

# Close the connection
close_connection()
