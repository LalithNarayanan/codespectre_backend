import json
from java_chunk_extractor import JavaChunkExtractor
from neo4j import GraphDatabase
import os
# Global variables that needs to be overwritten to use.
URI, USERNAME, PASSWORD, DATABASE_NAME = '', '', '', ''

class DocGen:

    def __init__(self, project_path: str):

        self.project_path = project_path
        self.jce = JavaChunkExtractor(
            path=self.project_path,
        )

        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD), database=DATABASE_NAME)
        try:
            with self.driver.session() as session:
                session.run("RETURN 1").consume()
        except Exception as e:
            raise Exception("Failed to connect to Neo4j") from e


    def _get_methods_of_class(self, class_node_id: str):
        query = """
        MATCH (c:classes)-[:hasmethods]->(m:methods)
        WHERE elementId(c) = $class_node_id
        RETURN m, elementId(m) AS method_node_id
        """
        with self.driver.session() as session:
            result = session.run(query, class_node_id=class_node_id)
            return result.data()
    
    def _get_called_methods(self, method_node_id: str):
        query = """
        MATCH (m1:methods)-[:calls]->(m2:methods)
        WHERE elementId(m1) = $method_node_id
        RETURN m2, elementId(m2) AS method_node_id
        """
        with self.driver.session() as session:
            result = session.run(query, method_node_id=method_node_id)
            return result.data()

    def _get_all_leaf_methods(self, start_method_id: str, visited=None):
        if visited is None:
            visited = set()

        if start_method_id in visited:
            return []  # Avoid infinite loop in cyclic calls. this only covers one kind of loop, but there might be different kind of loops.

        visited.add(start_method_id)

        called_methods = self._get_called_methods(start_method_id)
        
        # If nothing is called, it's a leaf
        if not called_methods:
            return [start_method_id]

        # Otherwise, go deeper
        leaf_ids = []
        for called in called_methods:
            child_id = called['method_node_id']
            leaf_ids += self._get_all_leaf_methods(child_id, visited)

        return leaf_ids



    def _gen_doc(self):
        controller_data = []

        query = """
        MATCH (c:classes)
        WHERE "@RestController" IN c.annotations
        OR ANY(ann IN c.annotations WHERE ann STARTS WITH "@RequestMapping")
        RETURN c, elementId(c) as node_id
        """

        with self.driver.session() as session:
            result = session.run(query).data()

        for controller_class_node in result:
            class_node_id = controller_class_node['node_id']
            class_data = controller_class_node['c']
            class_name = class_data['class_name']

            controller_entry = {
                "class_name": class_name,
                "class_node_id": class_node_id,
                "methods": []
            }

            methods = self._get_methods_of_class(class_node_id)
            for method in methods:
                method_data = method['m']
                method_id = method['method_node_id']
                method_name = method_data.get('method_name')

                method_entry = {
                    "method_name": method_name,
                    "method_node_id": method_id,
                    "calls": []
                }

                leaf_ids = self._get_all_leaf_methods(method_id)
                unique_leaf_ids = list(set(leaf_ids))

                for leaf_id in unique_leaf_ids:

                    # get method_name of leaf method
                    with self.driver.session() as session:
                        res = session.run(
                            """
                            MATCH (c)-[:hasmethods]->(m:methods)
                            WHERE elementId(m) = $id AND (c:classes OR c:interfaces)
                            RETURN m.method_name AS method_name,
                                coalesce(c.class_name, c.interface_name) AS parent_name
                            """,
                            id=leaf_id
                        ).single()

                        method_entry["calls"].append({
                            "leaf_method_node_id": leaf_id,
                            "leaf_method_name": res["method_name"] if res else "UNKNOWN",
                            "leaf_parent_name": res["parent_name"] if res else "UNKNOWN" # parent name can be either class or an interface.
                        })

                    # print(f"    🧬 Reaches leaf method: {res['name'] if res else leaf_id}")

                controller_entry["methods"].append(method_entry)

            controller_data.append(controller_entry)

        # Dump to file
        with open("controller_doc.json", "w") as f:
            json.dump(controller_data, f, indent=4)

    def get_info(self):
        """
        Generates Information for a Controller class.
        """
        self._gen_doc() # generation of document is mandatory first.

        prompt_content = """"""

        with open("controller_doc.json", 'r') as controller_doc_fp:
            controller_doc_info = json.load(controller_doc_fp)
        
         # Define the output directory for prompt files
        output_dir = "controller_wise_code_snippets"
        # Create the directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True) 

        for controller_class_info in controller_doc_info:
            class_name = controller_class_info['class_name']
            print(f"=========== Current Class: {class_name}  =============")
            print("All methods information: ")
            prompt_content = "" 
            for method_info in controller_class_info['methods']:
                method_name = method_info['method_name']
                method_chunk = self.jce.extract_method_chunk(parent_name=class_name, method_name=method_name)
                
                prompt_content += f"""
=========== Current Method: {method_name} =============
{class_name} - {method_name}:
```java
{method_chunk}
```
=========== Dependent Methods of {method_name}: ===============
                """             
                
                for method_call_info in method_info['calls']:
                    called_class_or_interface_name = method_call_info['leaf_parent_name']
                    called_method_name = method_call_info['leaf_method_name']
                    called_method_chunk = self.jce.extract_method_chunk(parent_name=called_class_or_interface_name, method_name=called_method_name)
                    prompt_content += f"""
{called_class_or_interface_name} - {called_method_name}:
```java
{called_method_chunk}
```

                    """
            # Save the prompt_content for the current class_name to a file
            file_name = os.path.join(output_dir, f"{class_name}_code.txt")
            with open(file_name, "w") as f:
                f.write(prompt_content)
            print(f"Saved prompt content for {class_name} to {file_name}")
        return "successfully completed" # only running for one file as of now.


if __name__ == "__main__":
    
    
        # define constants
    URI = "neo4j://127.0.0.1:7687"
    USERNAME ="neo4j"
    PASSWORD = "genai_application"  #instance password
    DATABASE_NAME = "java-ast"  #database base 
 
    doc_gen = DocGen(
        project_path=r'C:\KanagWS\CodeSpectreWS\JavaSpringApplications\JavaApplication1'
    ).get_info()
    print(doc_gen)



'''

# Approach
    - first we will extract nodes of all the Controllers. 
    - Next we need to get the nodes of all calls
    - next we need the code for all calls

'''