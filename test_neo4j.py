from neo4j import GraphDatabase

uri = "bolt://07030901-cad6-4689-9213-5a23b6186335.databases.neo4j.io:7687"
username = "neo4j"
password = "M3Z9-H4CZC3scqx__yBe8wtSFz143uhzjn2WmnX1ixA"

def test_connection():
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 1 AS number")
        for record in result:
            print(record["number"])

if __name__ == "__main__":
    test_connection()
