import os
import copy
import json
from pathlib import Path

from tree_sitter import Language, Parser, Node
import tree_sitter_java as tsjava

from rich import print as rprint 
from rich.progress import Progress, track

from neo4j import GraphDatabase


JAVA_LANGUAGE = Language(tsjava.language())
parser = Parser(JAVA_LANGUAGE)

# Global variables that needs to be overwritten to use.
URI, USERNAME, PASSWORD, DATABASE_NAME = '', '', '', ''



class ASTGenerator: 

    def __init__(
            self,
            project_path: str | Path,
            ):

        self.project_path = project_path
        self.file_count = self.get_file_count()
    
    def get_file_count(self) -> int: 
        """
        Returns the files count duh.
        """
        count = 0
        for root, _, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(".java"):
                    count += 1
        
        return count

    def get_ast(self) -> list[dict]:
        """
        AST structure that capture basic information, that includes information that is not related to any relations.
        """
        rprint(f"Scanning Java files in: [bold green]{self.project_path}")
        project_ast: list[dict] = []
        
        with Progress() as progress:
            task = progress.add_task("Generating AST: ", total=self.file_count)
            for root, _, files in os.walk(self.project_path):
                for file in files:
                    if file.endswith(".java"):
                        full_path = os.path.join(root, file)

                        java_ast_gen = JavaAstGenerator(
                            file_path=full_path                        
                            )
                        result = java_ast_gen.parse_java_file()
                        project_ast.append(result)
                        progress.update(task, advance=1)

        return project_ast




class JavaAstGenerator:
    
    def __init__(self, file_path: str): 
        
        self.file_path = file_path


        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.code = f.read()

        self.tree = parser.parse(bytes(self.code, 'utf8'))
        self.root_node = self.tree.root_node

        # AST structuring templates.
        self.result = {
            "file_path": self.file_path,
            "file_name": os.path.basename(self.file_path),
            "package_name": "",
            "imports": [],
            "fields": [],
            "classes": [],
            "interfaces":[],
            "code": "",
        }
        self.class_template = {
            "class_name": None,
            "extends":"",
            "implements": [],
            "annotations": [],
            "modifiers": [],
            "fields": [],
            "methods": [],
            "classes": [],
            "interfaces":[],
            "calls": [],
            "code": "",
        }
        self.interface_template = {
            "interface_name": None,
            "extends": "", # no clue
            "implements": [],
            "annotations": [],
            "modifiers": [],
            "fields": [],
            "methods": [],
            "calls": [],
            "classes": [],
            "interfaces":[],
            "code": "",
        }
        self.method_template = {
            "method_name": None,
            "visibility": "package-private",
            "annotations": [],
            "return_type": "void",
            "modifiers":[],
            "formal_parameters": [],
            "local_variables": [], 
            "calls": [],
            "code": "",
        }
        self.field_template = {
            "field_name": None,
            "type": "void",
            "annotations": [],
            "modifiers": [],
            "calls": [],
            "code": "",
        }
        self.local_variable_template = {
            "local_variable_name": None,
            "type": "void",
            "annotations": [],
            "modifiers": [],
            "calls": [],
            "code": "",
        }


    def _get_text(self, node: Node) -> str:
        return self.code[node.start_byte:node.end_byte]


    def _all_method_calls(self, node: Node, calls: set):
        """
        For given node, it finds all the method invocations that are happened inside of the node chunk
        """

        for childnode in node.children:
            if childnode.type == "method_invocation":
                calls.add(self._get_text(childnode))
                self._all_method_calls(childnode, calls)
                pass # we do something
            else: 
                # we will go though the children
                self._all_method_calls(childnode, calls)
            


    def _create_ast(self, node: Node, new_data: dict) -> dict | None:

        if node.type == "import_declaration":
            # TODO Preprocess and extract only the class/interface, or do we need the entire import statement
            new_data['imports'].append(self._get_text(node))

        elif node.type == "package_declaration":
            # TODO Do i preprocess anything or keep the entire stmt as it is.
            new_data['package_name'] = self._get_text(node)

        elif node.type == 'class_declaration':

            class_name = ''
            extends_name = ''
            implements_list = []
            class_annotations = []
            class_modifiers = []

            for child in node.children:
                if child.type == 'identifier':
                    class_name: str = self._get_text(child)

                elif child.type == 'superclass':
                    for sc_child in child.children:
                        if sc_child.type == 'type_identifier':
                            extends_name = self._get_text(sc_child)

                elif child.type == "super_interfaces":
                    for si_child in child.children:
                        if si_child.type == 'type_list':
                            for si_child_list in si_child.children:
                                super_interface_name = self._get_text(si_child_list)
                                if super_interface_name.strip()== ';' :
                                    continue
                                implements_list.append(super_interface_name)

                # TODO certain annotations, specifically annotations that take arguments are not captured.
                elif child.type == 'modifiers':
                    for grandchild in child.children:
                        if grandchild.type in ("marker_annotation",  "annotation"):
                            annotation: str = self._get_text(grandchild)
                            class_annotations.append(annotation)
                        elif grandchild.type in ("public", "private" "protected", "static", "final", "abstract", "synchronized", "native", "strictfp", "transient", "volatile"):
                            access_specifier: str = self._get_text(grandchild)
                            class_modifiers.append(access_specifier)

                elif node.type == 'class_body':
                    for class_body_node in node.children:
                        self._create_ast(class_body_node, new_data)


            new_data["class_name"] = class_name
            new_data['extends'] = extends_name
            new_data["annotations"] = class_annotations
            new_data['modifiers'] = class_modifiers
            new_data['implements'] = implements_list
            # new_data["code"] = self._get_text(node)

        elif node.type == 'interface_declaration':
            interface_name = ''
            interface_annotations = []
            interface_modifiers = []

            for child in node.children:

                if child.type == 'identifier':
                    interface_name: str = self._get_text(child)

                # TODO re-check whether all annotations are cpatured or not.
                elif child.type == 'modifiers':
                    for grandchild in child.children:
                        if grandchild.type in ("marker_annotation", "annotation"):
                            annotation: str = self._get_text(grandchild)
                            interface_annotations.append(annotation)
                        elif grandchild.type in ("public", "private", "protected", "static", "final", "abstract", "synchronized", "native", "strictfp", "transient","volatile"):
                            access_specifier: str = self._get_text(grandchild)
                            interface_modifiers.append(access_specifier)

                elif node.type == 'interface_body':
                    for interface_body_node in node.children:
                        self._create_ast(node, new_data)

            new_data['interface_name'] = interface_name
            new_data["annotations"] = interface_annotations
            new_data['modifiers'] = interface_modifiers
            # new_data['code'] = self._get_text(node)

        elif node.type == 'field_declaration':
            
            # this indicates, we are in either class/interface body, so new_data is still class/interface template.
            field_data = copy.deepcopy(self.field_template)
            field_name: str = ''
            field_type: str = 'void' 
            field_annotations = []
            field_modifiers = []
            field_calls = set({}) 

            for child in node.children:

                if child.type == "modifiers":
                    for grandchild in child.children:
                        if grandchild.type in ("marker_annotation", "annotation"):
                            annotation: str = self._get_text(grandchild)
                            field_annotations.append(annotation)
                        elif grandchild.type in ("public", "private", "protected", "static", "final", "abstract", "synchronized", "native", "strictfp", "transient", "volatile"):
                            access_specifier: str = self._get_text(grandchild)
                            field_modifiers.append(access_specifier)

                elif child.type in ("type_identifier", "primitive_type", "scoped_type_identifier"):
                    field_type = child.text.decode("utf8")

                elif child.type in ("void_type", "boolean_type", "integral_type"):
                    field_type = self._get_text(child)

                elif child.type in ("variable_declarator", ):
                    field_value_assigned = child.child_by_field_name("value")
                    # if a filed is created by some method invocation, we will map it to the field calls.
                    if field_value_assigned and field_value_assigned.type == "method_invocation":
                        
                        def parse_method_invocation_call(method_invocation_call: str):
                            method_invocation_call.lstrip("new")
                            method_invocation_call.rstrip(";") # redundant
                            method_invocation_call.strip()
                            parsed_output = ""
                            temp_output=""
                            method_invocation_parsing_flag = True
                            for i in method_invocation_call:
                                if i == "(":
                                    parsed_output += temp_output
                                    method_invocation_parsing_flag = False
                                if method_invocation_parsing_flag:
                                    temp_output += i
                                if i == ")":
                                    method_invocation_parsing_flag = True
                                    temp_output = ""
                            return parsed_output

                        method_invocation_from_field_declaration = parse_method_invocation_call(self._get_text(field_value_assigned))
                        field_calls.add(method_invocation_from_field_declaration)

                    #TODO: value assigned can be of direct assigments... like 'String a "Narasimha", how do we deal that?

                    #get the name of field
                    for var_child in child.children:
                        if var_child.type == "identifier":
                            field_name = var_child.text.decode("utf8")


            field_data["field_name"]= field_name
            field_data["type"]= field_type
            field_data["modifiers"] = field_modifiers
            field_data["annotations"]= field_annotations
            field_data['calls'] = list(field_calls)
            # field_data['code'] = self._get_text(node)

            new_data['fields'].append(field_data)


        elif node.type == 'method_declaration':

            

            method_data = copy.deepcopy(self.method_template)
            method_name, return_type = '', ''
            method_annotations = []
            method_modifiers = []
            method_parameters = []
            _real_method_calls = copy.deepcopy(set())
            method_calls: list[str] = []
            
            for child in node.children:

                if child.type == 'identifier':
                    method_name = self._get_text(child)

                elif child.type == 'modifiers':
                    for grandchild in child.children:
                        if grandchild.type in ("marker_annotation", "annotation"):
                            annotation: str = self._get_text(grandchild)
                            method_annotations.append(annotation)
                        elif grandchild.type in ("public", "private", "protected", "static", "final", "abstract", "synchronized", "native", "strictfp", "transient", "volatile"): 
                            access_specifier: str = self._get_text(grandchild)
                            method_modifiers.append(access_specifier)

                # TODO primitive types are not being captured i guess.
                elif child.type == "formal_parameters":
                    for param_node in child.children:
                        if self._get_text(param_node) in [")", "(", ","]: # symbols in stmt are also captured as part of formal_parameters node.
                            continue
                        method_Input_param = '.'.join(self._get_text(param_node).split(' '))
                        method_parameters.append(method_Input_param)
                
                elif child.type in ("type identifier", "primitive_type", "scoped_type_identifier", "void_type", "boolean_type", "integral_type"):
                    return_type = self._get_text(child)

                elif child.type == "block":

                    for grandchild in child.children:

                        fields_data = copy.deepcopy(self.local_variable_template)
                        if grandchild.type == "local_variable_declaration":
                            local_variable_annotations, local_variable_modifiers = [], []
                            local_variable_type, local_variable_name = "void", None
                            local_variable_calls = []

                            #parsing local variable to get information surrounding it.
                            for info in grandchild.children:

                                if info.type == "variable_declarator": #variale declarator includes `name` and `declarator` (things come after `=` sign)
                                    value_assigned =  info.child_by_field_name("value")

                                    #this is for method_invocation
                                    if value_assigned and value_assigned.type == "method_invocation":
                                        def parse_method_invocation_call(method_invocation_call: str):
                                            method_invocation_call.lstrip("new")
                                            method_invocation_call.rstrip(";") #redundant
                                            method_invocation_call.strip()
                                            parsed_output = ""
                                            temp_output = ""
                                            method_invocation_parsing_flag = True
                                            for i in method_invocation_call:
                                                if i == "(":
                                                    parsed_output += temp_output
                                                    method_invocation_parsing_flag = False
                                                if method_invocation_parsing_flag:
                                                    temp_output += i
                                                if i == ")":
                                                    method_invocation_parsing_flag = True
                                                    temp_output = ""
                                            return parsed_output

                                        method_invocation_from_variable_declaration = parse_method_invocation_call(self._get_text(value_assigned))

                                        #parse calls and map them accordingly.
                                        method_invocation_call_split =  method_invocation_from_variable_declaration.split('.')

                                        if len(method_invocation_call_split) == 2:
                                            invoked_class_or_variable_name, invoked_method_name =  method_invocation_call_split[0:2]

                                            #checks:
                                            # * invoked from a variable
                                            # * invoked directly from a class
                                            #if invoked from a variable, the variable can be declared in class, or recieved via input params

                                            #check 1: input parameters check

                                            for param in method_data['formal_parameters']:
                                                method_input_params_info =  param.split(".")
                                                if len(method_input_params_info) ==2:
                                                    method_input_param_class_name =  method_input_params_info[0]
                                                    method_input_param_variable_name =  method_input_params_info[1]
                                                    if invoked_class_or_variable_name == method_input_param_class_name:
                                                        #so it is invoked directly from a class, no need for alteration
                                                        local_variable_calls.append(method_invocation_from_variable_declaration)
                                                        break
                                                    elif invoked_class_or_variable_name ==  method_input_param_variable_name:
                                                        # so it is invoked via a variable that is received from input params
                                                        local_variable_calls.append(method_input_param_class_name + "." + invoked_method_name)
                                                        break

                                                #not sure how things look like here. probaly formal params parsing bug
                                                elif len(method_input_params_info) != 2:
                                                    pass

                                            #check 2: checking local variable with same name
                                            for vars in method_data['local_variables']:
                                                if vars['local_variable_name'] == invoked_class_or_variable_name:
                                                    #invoked from a variable name, that is declared within class 
                                                    local_variable_calls.append(vars['type']+"."+ invoked_method_name)
                                                elif vars['type'] == invoked_class_or_variable_name:
                                                    #invoked directly from a class that is within scope (imported or same package and stuff)
                                                    local_variable_calls.append(vars['type'] + "." + invoked_method_name)

                                        else:
                                            pass
                                            #print("There is a BUG in parsing method invocation")
                                            # print(f"Bug report:\nParsed method invocation looks like this: {method_invocation_from_variable_declaration}")
                                    # TODO: value assigned can be of direct assigments... like `String a = "Narasimha"`, how do we deal that?

                                    for var_child in info.children:
                                        if var_child.type == "identifier":
                                            local_variable_name = self._get_text(var_child)

                                elif info.type == 'modifiers':
                                    for modifier_node in info.children:
                                        if modifier_node.type in ("marker_annotation", "annotation"):
                                            annotation: str = self._get_text(modifier_node)
                                            local_variable_annotations.append(annotation)
                                        elif modifier_node.type in ("public", "private", "protected", "static", "final", "abstract", "synchronized", "native", "strictfp", "transient", "volatile"):
                                            access_specifier: str = self._get_text(modifier_node)
                                            local_variable_modifiers.append(access_specifier)
                                elif info.type in ("type_identifier", "primitive_type", "scoped_type_identifier", "generic_type"):
                                    local_variable_type = self._get_text(info)

                                elif child.type in ("void_type", "boolean_type", "integral_type"):
                                    local_variable_type = self._get_text(child)

                            fields_data["local_variable_name"] = local_variable_name
                            fields_data['type'] = local_variable_type
                            fields_data['modifiers'] = local_variable_modifiers
                            fields_data['annotations'] = local_variable_annotations
                            fields_data['calls'] = local_variable_calls
                            # local_variable_data['code'] = self._get_text(grandchild)
                            method_data['local_variables'].append(fields_data)

            # calls
            self._all_method_calls(node, _real_method_calls)
            for method_call in _real_method_calls:
                def parse_call():
                        # supports only 2 types of parsing: 
                        # getSomething()
                        # obj.getSomething()

                        parsed_call = []
                        parsed_text = ''
                        for ch in method_call:
                            if ch.isalpha() or ch.isdigit():
                                parsed_text += ch
                            if ch == '.':
                                parsed_call.append(parsed_text)
                                parsed_text = ''
                            if ch == '(':
                                parsed_call.append(parsed_text)
                                return parsed_call
                        return parsed_call

                _real_method_call = parse_call()
                if len(_real_method_call) == 1:
                    class_or_interface_name = new_data['class_name'] if new_data.get('class_name', 0) else new_data['interface_name']
                    method_calls.append(class_or_interface_name.strip() + '.' + _real_method_call[0])
                elif len(_real_method_call) == 2:
                    for fields_data in method_data['local_variables']:
                        if _real_method_call[0].strip() == fields_data['local_variable_name'].strip():
                            method_calls.append(fields_data['type'].strip() + '.' + _real_method_call[1].strip())
                    for fields_data in new_data['fields']:
                        if _real_method_call[0].strip() == fields_data['field_name'].strip():
                            method_calls.append(fields_data['type'].strip() + '.' + _real_method_call[1].strip())

                    
                    
                    
                                    
            method_data["method_name"] =  method_name
            method_data["annotations"] =  method_annotations
            method_data['modifiers'] = method_modifiers
            method_data['return_type'] = return_type
            method_data['formal_parameters'] = method_parameters
            method_data['calls'] = method_calls
            # method_data['code'] = self._get_text(node)
            new_data["methods"].append(method_data)

        for child in node.children:

            # incase of class/interface delcaration only, we are returning something.

            if child.type == 'class_declaration':
                new_data['classes'].append(self._create_ast(child, copy.deepcopy(self.class_template)))

            elif child.type == "interface_declaration":
                new_data['interfaces'].append(self._create_ast(child, copy.deepcopy(self.interface_template)))

            # we need to call to grab the rest of thin
            else: 
                self._create_ast(child, new_data) # Nothing will gets returned in this scenario.

        return new_data

    def parse_java_file(self) -> dict:
        return self._create_ast(self.root_node, self.result)




class GraphLoader:

    def __init__(self, ast_to_load: list[dict]):
        self.ast_to_load: list[dict] = ast_to_load
        self.issues_count = 0
        self.issues_list = []

        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD), database=DATABASE_NAME)
        if not self.driver.verify_authentication():
            raise Exception("Failed to connect to Neo4j")

    def _load_data_to_neo4j(self, new_data: dict, current_id, parent_id, relation_name: str):

        def isNode(any_type):
            if isinstance(any_type, dict):
                return True
            if isinstance(any_type, list):
                for i in any_type:
                    if isinstance(i, dict):
                        return True
                    return False
            return False

        def remove_conflicting_characters(stmt: str) -> str: 
            """
            Characters that are conflicting with neo4j query.
            """
            unnecessary_chars = ['.', '*', '%', '$']
            for i in unnecessary_chars:
                stmt = stmt.replace(i, "_")
            return stmt
            
        # create node the moment we see it
        if isinstance(new_data, dict):
            if relation_name: 
                # parsing to escape neo4j errors
                relation_name = remove_conflicting_characters(relation_name)

            # name was not set. setting it makes difficult to create generic loader:  {{name: $current_node}}
            node_creation_clause = f"""
            CREATE (current_node: {relation_name if relation_name else 'File'} {{name: $node_name}})
            """
            if relation_name:
                relationship_creation_clause = f"""
                WITH current_node
                MATCH (parent_node)
                WHERE elementId(parent_node) = $parent_id
                MERGE (parent_node) - [:{'has'+relation_name}] -> (current_node)
                """
            return_clause = """
            RETURN current_node, elementId(current_node) as current_id
            """
            if relation_name == None:
                # if there is no parent node, then no need of relationship clause
                query = node_creation_clause + return_clause
            else:
                query = node_creation_clause + relationship_creation_clause + return_clause

            with self.driver.session() as session:
                try:
                    result = session.run(
                        query=query,
                        parent_id=parent_id,
                        node_name = relation_name if relation_name else "File" # best possible way to give a node name is to have the name same as relation.
                    )

                    record = result.data()[0] # get the created node data 
                    current_id = record['current_id']
                except Exception as e:
                        self.issues_count += 1
                        self.issues_list.append(e.__str__())



        # traverse through node to get any properties or child nodes
        for key, value in new_data.items():
            parent_id = current_id
            # child nodes
            if isNode(value):
                if isinstance(value, dict): # this case is an assumtion, never battle tested it.
                    self._load_data_to_neo4j(new_data=value, 
                                        current_id=current_id, 
                                        parent_id=parent_id,
                                        relation_name=key)        
                elif isinstance(value, list):
                    for child in value:

                        # child.values can be another list or dict or anything that is not string, present, it only assumes string
                        self._load_data_to_neo4j(new_data=child, 
                                        current_id=current_id, 
                                        parent_id=parent_id,
                                        relation_name=key)  
                        
            else:
                '''
                what this does is: (hopefully)
                if it is not a node type:
                    it will consider it as a property and adds it to the current node
                '''
                data_to_add = {
                    key: value
                }
                query = """
                MATCH (current_node)
                WHERE elementId(current_node) = $current_id
                SET current_node += $props
                RETURN current_node
                """
                with self.driver.session() as session:
                    try:
                        result = session.run(
                                        query=query,
                                        current_id=current_id,
                                        props = data_to_add,
                                        node_description = f"{key}: {value}," # add this line SET current_node.description = coalesce(current_node.description, '') + $node_description

                                        )
                    except Exception as e:
                        self.issues_count += 1
                        self.issues_list.append(e.__str__())


    def _create_node_description(self):
        """
        Creates a Textual node description for each node. 
        Works for every kind of graph.
        """

        def is_child_node(instance) -> bool:
            if isinstance(instance, dict):
                return True 
            elif isinstance(instance, list):
                for i in instance:
                    if isinstance(i, dict):
                        return True 
            return False
        
        # TODO check edge cases
        def is_scalar(value):
            compund_types = [list, dict, tuple, set]
            for type in compund_types:
                if isinstance(value, type):
                    return False 
            return True
        
        def get_desc(key, value):
            desc = f"{key} are "
            if not value:
                return f"no {key}"
            if is_scalar(value):
                return f"{key} is {value}"
            elif isinstance(value, list) and isinstance(value[0], str):
                for inst in value:
                    if isinstance(inst, str):
                        desc += f"{inst}, "
                return desc
            
            #TODO recheck the edge cases
            elif isinstance(value, list):
                return f"has {key}"
            
            return ""




        all_nodes_id_query = """
        match (n)
        return elementId(n) as node_id
        """
        with self.driver.session() as session:
            result = session.run(query=all_nodes_id_query)
            node_ids_list = result.data() # list of dicts: {'node_id': '4:31bed391-cfdf-4b22-84c2-5347ade7fbab:1'}
            for node_id_dict in track(node_ids_list, description="Creating Node Description: "):
                node_description = ""
                node_id = node_id_dict['node_id']
                # rprint(f"current node id: [green]{node_id}")
                parent_node_query = """
                match (n)
                where elementId(n) = $node_id
                match (n) <- [r] - (parent)
                return n as current_node, parent as parent_node, r as relationship
                """
                with self.driver.session() as parent_session:
                    parent_result = parent_session.run(
                        query=parent_node_query,
                        node_id = node_id
                    )
                    parent_data_list = parent_result.data()
                    if parent_data_list:
                        for parent_data in parent_data_list:
                            parent_node_description = "The Details of a Parent Node: "
                            current_node_description = ""
                            current_node = parent_data['current_node']
                            parent_node_data = parent_data['parent_node']
                            relationship_data = parent_data['relationship'][1] # (parentnode, relationship, childnode)
                            
                            for key, value in parent_node_data.items():
                                if key == "description_of_node": continue # we dont wanna mess with recursive rabit-hole
                                if key == "name":
                                    key = "Type"
                                parent_node_description += f"{get_desc(key, value)}, "
                            if relationship_data:
                                parent_node_description += f" {relationship_data} of details: "
                            current_node_description += parent_node_description
                            current_node_description += " with details: "
                            for key, value in current_node.items():
                                if key == "description_of_node": continue # same here
                                if key == "name":
                                    key = "Type"
                                current_node_description += f" {get_desc(key, value)}, "
                            
                            # add each parent info
                            node_description += current_node_description
                        

                child_node_query = """
                match (n)
                where elementId(n) = $node_id
                match (n) - [r] -> (child)
                return n as current_node, child as child_node, r as relationship
                """
                with self.driver.session() as child_session:
                    child_result = child_session.run(
                        query=child_node_query,
                        node_id=node_id,
                    )
                    child_data_list = child_result.data()
                    if child_data_list:
                        for child_data in child_data_list:
                            child_node_description = ""
                            current_node_description = "The Current Node with details: "
                            current_node_data = child_data['current_node']
                            for key, value in current_node_data.items():
                                if key == "description_of_node": # same here
                                    continue
                                if key == "name":
                                    key = "Type"
                                current_node_description += f" {get_desc(key, value)}, "
                            relationship_data = child_data['relationship'][1]
                            if relationship_data:
                                current_node_description += f" {relationship_data} of details: "
                            child_node_data = child_data['child_node']

                            child_node_description += current_node_description
                            for key, value in child_node_data.items():
                                if key == "description_of_node": continue # same here
                                if key == "name":
                                    key = "Type"
                                child_node_description += f" {get_desc(key, value)}, "
                        
                            node_description += child_node_description # add each child data info


                # sys.exit()  # uncomment this to debug for a single node. 

                add_node_desc_query = """
                MATCH (n) 
                WHERE elementId(n) = $node_id
                SET n.description_of_node = $node_description
                """
                with self.driver.session() as description_session:
                    result = description_session.run(
                        query=add_node_desc_query,
                        node_id=node_id,
                        node_description=node_description,
                    )


    def _map_relations(self):
        
        
        # imports mapping
        file_nodes_query = """
        MATCH (file_nodes: File)
        RETURN file_nodes.imports AS file_imports, elementId(file_nodes) as file_id
        """
        
        class_nodes_query = """
        MATCH (class_nodes: classes)
        RETURN class_nodes.class_name as class_name, elementId(class_nodes) as class_id
        """
        with self.driver.session() as session:
            file_nodes = session.run(
                query=file_nodes_query
            )
            class_nodes = session.run(
                query=class_nodes_query
            )
            file_nodes_data = copy.deepcopy(file_nodes.data())
            class_nodes_data = copy.deepcopy(class_nodes.data())
            for file_data in file_nodes_data:
                unfiltered_imports = file_data['file_imports']
                filtered_imports = copy.deepcopy([])
                for imp in unfiltered_imports:
                    class_from_import_stmt = imp.lstrip("import").lstrip().split(".")[-1].replace(';', '')
                    # if class_from_import_stmt == "*":
                    #     # this case is not being handled, so... 
                    #     pass
                    filtered_imports.append(class_from_import_stmt)
                fid = file_data['file_id']
                for class_data in class_nodes_data:
                    class_or_interface_name = class_data['class_name']
                    cid = class_data['class_id']
                    if class_or_interface_name in filtered_imports:
    
                        sub_query = """
                        MATCH (file_node: File)
                        WHERE elementId(file_node) = $fid
                        MATCH (class_node: classes)
                        WHERE elementId(class_node) = $cid
                        MERGE (file_node) - [:imports] -> (class_node)
                        """
                        with self.driver.session() as session:
                            session.run(
                                query=sub_query,
                                fid=fid,
                                cid=cid
                            )
    

        # calls mapping from classes, interfaces, field and local_variables 
        class_mapping_query = """
        MATCH (nodes_to_map)
        WHERE nodes_to_map:classes OR nodes_to_map:interfaces OR nodes_to_map:local_variables OR nodes_to_map:fields OR nodes_to_map:methods
        RETURN elementId(nodes_to_map) AS node_id
        """
        with self.driver.session() as session:
            result = session.run(
                query=class_mapping_query
            )
            data = result.data()
            for record in data:
                class_mapping_query = """
                MATCH (n)
                WHERE elementId(n) = $node_id
                RETURN n
                """
                with self.driver.session() as session:
                    node_to_map = session.run(
                        query=class_mapping_query,
                        node_id=record['node_id']
                    )
                    node_to_map_data = node_to_map.data()
                    for node_record in node_to_map_data:
                        calls_list = node_record['n']['calls']
                        for each_call in calls_list:
                            each_call_as_list = each_call.split(".")

                            # if each call is captured as "Classname.methodName"
                            if len(each_call_as_list) == 2:
                                class_or_interface_name, method_name = each_call_as_list

                                class_mapping_query = """
                                MATCH (node)
                                WHERE elementId(node) = $node_id
                                MATCH (parent_node: classes {class_name: $parent_node_name}) -[:hasmethods] -> (method_node: methods {method_name: $method_name})
                                MERGE (node) -[:calls] -> (method_node)
                                """

                                interface_mapping_query = """
                                MATCH (node)
                                WHERE elementId(node) = $node_id
                                MATCH (parent_node: interfaces {interface_name: $parent_node_name}) -[:hasmethods] -> (method_node: methods {method_name: $method_name})
                                MERGE (node) -[:calls] -> (method_node)
                                """

                                with self.driver.session() as session:
                                    # we will run query for both class and interface just so that we will not miss. and yes it cannot be in both scenarios, thats obvious.
                                    temp_res = session.run(
                                        query=class_mapping_query,
                                        node_id=record["node_id"],
                                        parent_node_name = class_or_interface_name,
                                        method_name=method_name,
                                    )
                                    temp_res = session.run(
                                        query=interface_mapping_query,
                                        node_id=record["node_id"],
                                        parent_node_name = class_or_interface_name,
                                        method_name=method_name,
                                    )
            
                            #TODO: calls can look like this: callChaning().anotherChain().oneMoreChain();, 


            #TODO: check any other possible mappings. 

            rprint(f"[green italic]Mapping relations in java ast neo4j graph is completed....")


    def load(self):
        print(f"********loading AST file...")
        # loads the individual ast to neo4j.
        for  new_data in track(self.ast_to_load, description="Loading AST to Neo4j: "):
            self._load_data_to_neo4j(
                new_data=new_data,
                current_id=None,
                parent_id=None,
                relation_name=None,
            )

        # creates relationship between nodes.
        self._map_relations()




if __name__ == "__main__":

    # How to run this file: 
    '''
    - Provide project_path which is a valid project directory.
        ⚠️ AST generation doesn't support for single java files YET, so you must provide only entire folder path, but not file path.
    - Provide Output ast path, which should also be a valid directory path. if none provided, it will take current working directory.
        - 📝 output ast will be named as `java_project_ast.json`
    '''

    # only configs:
    # project_path = r'C:\Users\Narasimha\Documents\java_spring_project'
    project_path = r'C:\KanagWS\CodeSpectreWS\JavaSpringApplications\JavaApplication1'
    
    output_ast_path = ""

    # define constants
    URI = "neo4j://127.0.0.1:7687"
    USERNAME ="neo4j"
    PASSWORD = "genai_application"  #instance password
    DATABASE_NAME = "java_ast"  #database base 


    ast = ASTGenerator(
        project_path=Path(project_path)
    ).get_ast()

    with open(os.path.join(output_ast_path, "java_project_ast.json"), 'w') as ast_fp:
        json.dump(ast, ast_fp)

    with open(os.path.join(output_ast_path, "java_project_ast.json"), 'r') as ast_fp:
        ast = json.load(ast_fp)
    
    gl = GraphLoader(
        ast_to_load=ast
    ).load()


'''
# Introduction
    Java AST Script is an AST generator for java source code.
    
# Requirements: tree_sitter tree_sitter_java neo4j rich

# Approach
    - First create a AST that contains basic detials of the java source code.
    - Add Relationship information to the AST.


# Current Working on:
    # field calls and local variable calls need a remap 🟡
    # Do we need to capture any information related to return statement ❓

## Relationship between multiple java files, Method - Method Calls
    * Simple Direct Call (within same class) -> doSomething(); // Implicit this.doSomething() ✅
    * Explicit this call -> this.doSomething(); 🟡 (not implemented yet, but can be done with very minimal changes)
    * Static method from same class -> staticMethod(); ✅
    * Static method from another class -> SomeClass.staticMethod(); ✅
    * Object method call -> obj.doSomething(); ✅
    * Chained calls -> getUser().getAddress().getCity(); ❌
    * Method call on returned object -> user.getName().toLowerCase(); ❌
    * Call inside a constructor ❌
        public MyClass() {
            init();
        }
    * Call through inheritance (super) -> super.doSomething(); ❌
    * Lambda / functional interfaces -> Runnable r = () -> runTask(); // Implicit method reference ❌
    * Method references -> list.forEach(System.out::println); // Method reference, not a call but linked ❌
    * Calls inside ternary / conditional -> (flag ? obj1 : obj2).doSomething(); ❌
    * Anonymous classes ❌
        new Runnable() {
            public void run() {
                doStuff();
            }
        }.run();
    * Array of objects with method calls -> arr[i].doStuff(); ❌ 
    * Generic types (where type info may be erased) -> T obj = getT(); obj.doSomething(); // Gotta resolve T ❌

### 🤯 Edge Cases You'll Suffer: ❌❌❌
    * Method overloading
    * Method shadowing from inheritance
    * Dynamic method calls via reflection
    * Generics (Map<String, List<User>>) — parser hell
    * Inner classes, static nested classes
    * Fluent APIs that return this or builder chains
    * Lambdas and streams (list.stream().map(x -> x.toString()).collect(...))
'''