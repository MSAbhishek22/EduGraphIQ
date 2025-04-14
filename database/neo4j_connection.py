from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self):
        self.uri = "neo4j+ssc://b5a02fce.databases.neo4j.io"
        self.username = "neo4j"
        self.password = "M3Z9-H4CZC3scqx__yBe8wtSFz143uhzjn2WmnX1ixA"
        self.driver = None
        
    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                connection_timeout=120
            )
            self.driver.verify_connectivity()
            print("Connected to Neo4j Aura successfully!")
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j Aura: {str(e)}")
            return False

    def create_concept_node(self, concept_name, content):
        if not self.driver:
            print("No database connection")
            return None
            
        with self.driver.session() as session:
            try:
                create_query = """
                MERGE (c:Concept {name: $name})
                SET c.content = $content,
                    c.created_at = datetime()
                RETURN c.name as name, c.content as content
                """
                
                result = session.run(create_query, {
                    "name": concept_name,
                    "content": content
                }).single()
                
                if result:
                    print(f"Successfully created/updated node: {concept_name}")
                    return {
                        'name': result['name'],
                        'content': result['content']
                    }
                else:
                    print(f"Failed to create node: {concept_name}")
                    return None
                    
            except Exception as e:
                print(f"Error creating node: {str(e)}")
                return None

    def create_relationship(self, concept1_name, concept2_name, relationship_type):
        if not self.driver:
            print("No database connection")
            return None
            
        with self.driver.session() as session:
            try:
                result = session.run("""
                MATCH (c1:Concept {name: $concept1})
                MATCH (c2:Concept {name: $concept2})
                MERGE (c1)-[r:RELATED_TO]->(c2)
                RETURN c1.name as source, c2.name as target
                """, {
                    "concept1": concept1_name,
                    "concept2": concept2_name
                }).single()
                
                if result:
                    print(f"Created relationship: {concept1_name} -> {concept2_name}")
                    return {
                        'source': result['source'],
                        'target': result['target']
                    }
                return None
                
            except Exception as e:
                print(f"Error creating relationship: {str(e)}")
                return None

    def get_all_concepts(self):
        query = "MATCH (c:Concept) RETURN c.name as name, c.content as content"
        return self.query(query)

    def get_concept(self, concept_name):
        query = """
        MATCH (c:Concept {name: $name})
        RETURN c.name as name, c.content as content
        """
        results = self.query(query, {"name": concept_name})
        return results[0] if results else None

    def query(self, query, parameters=None):
        if not self.driver:
            raise Exception("Driver not initialized. Call connect() first.")
        
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record for record in result]

    def close(self):
        if self.driver:
            self.driver.close()

# Usage example
if __name__ == "__main__":
    db = Neo4jConnection()
    if db.connect():
        try:
            # Create some test nodes and relationships
            create_query = """
            CREATE (s:Student {name: 'John', age: 20})
            CREATE (c:Course {name: 'Python Programming', level: 'Intermediate'})
            CREATE (s)-[:ENROLLED_IN]->(c)
            RETURN s, c
            """
            result = db.query(create_query)
            print("Created test data successfully")
            
            # Query to retrieve data
            read_query = """
            MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course)
            RETURN s.name as student, c.name as course
            """
            result = db.query(read_query)
            for record in result:
                print(f"Student {record['student']} is enrolled in {record['course']}")
            
            # Add more students and courses
            create_query = """
            CREATE (s1:Student {name: 'Alice', age: 22})
            CREATE (s2:Student {name: 'Bob', age: 21})
            CREATE (c1:Course {name: 'Data Science', level: 'Advanced'})
            CREATE (c2:Course {name: 'Web Development', level: 'Beginner'})
            CREATE (s1)-[:ENROLLED_IN {date: '2024-01-15'}]->(c1)
            CREATE (s1)-[:ENROLLED_IN {date: '2024-02-01'}]->(c2)
            CREATE (s2)-[:ENROLLED_IN {date: '2024-01-20'}]->(c2)
            RETURN s1, s2, c1, c2
            """
            db.query(create_query)
            print("Created additional test data")
            
            # Query with more complex patterns
            read_query = """
            MATCH (s:Student)-[r:ENROLLED_IN]->(c:Course)
            RETURN s.name as student, 
                   collect(c.name) as courses, 
                   count(c) as course_count
            """
            result = db.query(read_query)
            for record in result:
                print(f"Student {record['student']} is enrolled in {record['course_count']} courses: {record['courses']}")
            
            db.close()
        except Exception as e:
            print("Query failed:", str(e))