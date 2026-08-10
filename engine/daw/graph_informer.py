class GraphInformer:
    def __init__(self, loomy_client):
        self.loomy = loomy_client

    def get_next_harmonic_step(self, current_key: str):
        """Queries Loomy for graph-informed modulation."""
        # Example traversal logic: query graph for related nodes (Circle of 5ths)
        # return self.loomy.query(f"MATCH (n:Key {{name:'{current_key}'}})-[:TRANSITIONS_TO]->(m) RETURN m.name")
        return "C# Minor" # Stubbed traversal result
