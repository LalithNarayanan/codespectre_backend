import json
import os

from dotenv import load_dotenv
import google.generativeai as genai
from neo4j import GraphDatabase
from rich import print as rprint
from rich.progress import track

from preprocessor.java_chunk_extractor import JavaChunkExtractor

# Global variables that needs to be overwritten to use.
load_dotenv()
NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE_NAME, GOOGLE_MODEL_NAME = (
    "",
    "",
    "",
    "",
    "",
)

URI = "neo4j://127.0.0.1:7687"
USERNAME ="neo4j"
PASSWORD = "test@123"  #instance password
DATABASE_NAME = "java-ast"  #database base 


class DocGen:

    def __init__(self, project_path: str):

        self.project_path = project_path
        self.jce = JavaChunkExtractor(
            path=self.project_path,
        )


        NEO4J_URI = "neo4j://127.0.0.1:7687"
        NEO4J_USERNAME ="neo4j"
        NEO4J_PASSWORD = "test@123"  #instance password
        NEO4J_DATABASE_NAME = "java-ast"  #database base 
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
            database=NEO4J_DATABASE_NAME,
        )

        self._controller_details_path = os.path.join(
            os.getcwd(), "controller_details.json"
        )

        try:
            with self.driver.session() as session:
                session.run("RETURN 1").consume()
        except Exception as e:
            raise Exception("Failed to connect to Neo4j") from e

    def _get_controllerclasses_relational_info(self):
        """
        Generates Structual Representation of Controller classes. Mainly focueses on relations.
        """

        def _get_called_methods(method_node_id: str):
            query = """
            MATCH (m1:methods)-[:calls]->(m2:methods)
            WHERE elementId(m1) = $method_node_id
            RETURN m2, elementId(m2) AS method_node_id
            """
            with self.driver.session() as session:
                result = session.run(query, method_node_id=method_node_id)
                return result.data()

        def _get_all_leaf_methods(start_method_id: str, visited=None):
            if visited is None:
                visited = set()

            if start_method_id in visited:
                return (
                    []
                )  # Avoid infinite loop in cyclic calls.

            visited.add(start_method_id)

            called_methods = _get_called_methods(start_method_id)

            # If nothing is called, it's a leaf
            if not called_methods:
                return [start_method_id]

            # Otherwise, go deeper
            leaf_ids = [start_method_id]
            for called in called_methods:
                child_id = called["method_node_id"]
                leaf_ids += _get_all_leaf_methods(child_id, visited)

            return leaf_ids

        def _get_methods_of_class(class_node_id: str):
            query = """
            MATCH (c:classes)-[:hasmethods]->(m:methods)
            WHERE elementId(c) = $class_node_id
            AND ANY(annotation IN m.annotations WHERE annotation IN ["@GetMapping", "@PutMapping", "@DeleteMapping", "@PostMapping"])
            RETURN m, elementId(m) AS method_node_id
            """
            with self.driver.session() as session:
                result = session.run(query, class_node_id=class_node_id)
                return result.data()

        controllerclasses_structural_info = []

        query = """
        MATCH (c:classes)
        WHERE "@RestController" IN c.annotations
        OR ANY(ann IN c.annotations WHERE ann STARTS WITH "@RequestMapping")
        RETURN c, elementId(c) as node_id
        """

        with self.driver.session() as session:
            result = session.run(query).data()

        for controller_class_node in result:
            class_node_id = controller_class_node["node_id"]
            class_data = controller_class_node["c"]
            class_name = class_data["class_name"]

            controller_entry = {
                "class_name": class_name,
                "class_node_id": class_node_id,
                "methods": [],
            }

            methods = _get_methods_of_class(class_node_id)
            for method in methods:
                method_data = method["m"]
                method_id = method["method_node_id"]
                method_name = method_data.get("method_name")

                method_entry = {
                    "method_name": method_name,
                    "method_node_id": method_id,
                    "calls": [],
                }

                leaf_ids = _get_all_leaf_methods(method_id)
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
                            id=leaf_id,
                        ).single()

                        method_entry["calls"].append(
                            {
                                "leaf_method_node_id": leaf_id,
                                "leaf_method_name": (
                                    res["method_name"] if res else "UNKNOWN"
                                ),
                                "leaf_parent_name": (
                                    res["parent_name"] if res else "UNKNOWN"
                                ),  # parent name can be either class or an interface.
                            }
                        )

                controller_entry["methods"].append(method_entry)

            controllerclasses_structural_info.append(controller_entry)

        return controllerclasses_structural_info

    def _get_controller_details(self):
        """
        Generates Information for a Controller class.

        Returns a list:

            [
                    {
                        class_name: ...
                        class_chunk: ... (optional)
                        methods: [
                            {
                                method_name: ...
                                method_chunk: ...
                                calls: [
                                    {
                                        parent_name: ...
                                        parent_chunk: ... (optional)
                                        method_name: ...
                                        method_chunk: ...
                                    }
                                ...
                                ]
                            }
                            ...
                        ]
                    }
                    ...
            ]
        """

        controller_classes_structure = self._get_controllerclasses_relational_info()
        complete_controller_class_details = []
        for controller_class_info in track(
            controller_classes_structure,
            description="Generating Controller Class Info: ",
        ):
            _complete_controller_class_info = {
                "class_name": "",
                "class_chunk": "",
                "methods": [],
            }
            _complete_controller_class_info["class_name"] = controller_class_info[
                "class_name"
            ]
            # _complete_controller_class_info['class_chunk'] = self.jce.extract_class_chunk(_complete_controller_class_info['class_name']) # do not add unless need.

            for method_info in controller_class_info["methods"]:
                _complete_method_info = {
                    "method_name": method_info["method_name"],
                    "method_chunk": self.jce.extract_method_chunk(
                        parent_name=_complete_controller_class_info["class_name"],
                        method_name=method_info["method_name"],
                    ),
                    "calls": [],
                }
                for method_call_info in method_info["calls"]:
                    _complete_method_call_info = {
                        "parent_name": method_call_info["leaf_parent_name"],
                        "method_name": method_call_info["leaf_method_name"],
                        "method_chunk": self.jce.extract_method_chunk(
                            parent_name=method_call_info["leaf_parent_name"],
                            method_name=method_call_info["leaf_method_name"],
                        ),
                    }
                    _complete_method_info["calls"].append(_complete_method_call_info)

                _complete_controller_class_info["methods"].append(_complete_method_info)

            complete_controller_class_details.append(_complete_controller_class_info)

        # caching the processed for fast loads later.
        with open(self._controller_details_path, "w") as controller_details_fp:
            json.dump(complete_controller_class_details, controller_details_fp)

        return complete_controller_class_details

    def get_controllerclasses_as_chunks(
        self,
    ):
        """
        Generates Functional Doc for all controller files.
        """

        _METHOD_CHUNK_SIZE_LIMIT = (
            1000  # a maximum of 1000 lines of chunks are created to
        )

        # loading from existing file, if available, since re-creating is taking a lot of time.
        if os.path.exists(self._controller_details_path):
            with open(self._controller_details_path, "r") as controller_details_fp:
                try:
                    _controller_class_info = json.load(controller_details_fp)
                except:
                    _controller_class_info = self._get_controller_details()
        else:
            _controller_class_info = self._get_controller_details()

        _all_controller_chunks = []
        for _class_detail in _controller_class_info:
            class_name = _class_detail["class_name"]
            _controller_chunks = []
            _temp_chunk = ''
            for _method_detail in _class_detail["methods"]:
                method_name = _method_detail["method_name"]
                _api_method_chunks = []
                _temp_chunk += f"""
=======================  Class Name: {class_name} - > Method Name: {method_name} method. ===============================
Method Source Code: 
```java
{_method_detail['method_chunk']}
```
Methods that are used by {method_name}:
"""
                for _call_detail in _method_detail["calls"]:
                    if (_temp_chunk + _call_detail["method_chunk"]).count(
                        "\n"
                    ) > _METHOD_CHUNK_SIZE_LIMIT:
                        _api_method_chunks.append(_temp_chunk)
                        _temp_chunk = ""

                    called_methods_class_name = _call_detail["parent_name"]
                    called_method_name = _call_detail["method_name"]
                    called_method_chunk = _call_detail["method_chunk"]
                    _temp_chunk += f"""
{called_methods_class_name} -> {called_method_name} method.
```java
{called_method_chunk}
```
"""
                if _temp_chunk:
                    _api_method_chunks.append(_temp_chunk)
                    _temp_chunk = ""
                
                _controller_chunks.append(_api_method_chunks)


            _all_controller_chunks.append(_controller_chunks)
        
        return _all_controller_chunks


    def display_controllerclasses_chunks(self):
        all_controller_chunks = self.get_controllerclasses_as_chunks()
        for one_controller_chunk in all_controller_chunks:
            print('--------------------------------------------------')
            for chunk in one_controller_chunk:
                print(chunk.replace('\\n', '\n'))
            
            break  # displaying only one file, as terminal would blow up, for all files content.


if __name__ == "__main__":

    # ======= CONFIG start: =====
    """
    Config Details:

        * Create a `.env. file with an attribute named: `GEMINI_API_KEY` with your own gemini api key.

        GOOGLE_MODEL_NAME: name of the google model, by default it uses: gemini-2.5-flash
        NEO4J_URI: URI for neo4j instance.
        NEO4J_USERNAME: username of neo4j instance.
        NEO4J_PASSWORD: Password of neo4j instance.
        NEO4J_DATABASE_NAME: Database name that belongs to a active neo4j instance.
    """
    GOOGLE_MODEL_NAME = "gemini-2.5-flash"
    NEO4J_URI = "neo4j://127.0.0.1:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "javaastt"
    NEO4J_DATABASE_NAME = "neo4j"
    # ======= CONFIG end: =====

    # ====== USAGE: =======
    res = DocGen(
        project_path=r"C:\Users\Narasimha\Documents\java_spring_project"
    ).get_controllerclasses_as_chunks()
    rprint(res[0])


"""

# Changes: 
    - As of now all methods are taken into consideration. we can minimize it to only API end points.
    - If dependent chunks size is more than 1000 lines, we are ignoring rest of the methods.

# Approach
    - first we will extract nodes of all the Controllers. 
    - Next we need to get the nodes of all calls
    - next we need the code for all calls

"""
