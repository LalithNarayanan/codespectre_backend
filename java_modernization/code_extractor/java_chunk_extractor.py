import os
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax
from rich import print as rprint
from tree_sitter import Language, Parser, Node
import tree_sitter_java as tsjava



# Niche configs
JAVA_LANGUAGE = Language(tsjava.language())
parser = Parser(JAVA_LANGUAGE)
console = Console()




class JavaChunkExtractor:
    """
    JavaChunkExtractor is a small class that can help to extract java source code based on requirements.
        
    It uses tree-sitter under the hood for extraction.

    Args:
        path: path should be a string, that can be either directory path or a single java file path
    """
    
    def __init__(self, path: str):         

        if os.path.isfile(path):
            self.path_type = "file"
        elif os.path.isdir(path):
            self.path_type = "directory"
        else:
            raise Exception("Invalid Path provided. it is neither file path, nor directory path...")

        self.path = path

    def extract_class_chunk(
            self,
            class_name: str | None = None,
            annotations: str | list[str] | None = None,
            extends_name: str | None = None,
            implements_list: str | list[str] | None = None,
            modifiers: str | list[str] | None = None,
            ) -> str | None:
        """
        Returns the class chunk that matches given combination.

        Args:
            class_name: Name of the desired class
            annotations: List of annotation names of the desired class
            extends_name:Superclass name of the desired class
            implements_list: List of superinterfaces names of the desired class
            modifiers: List of access specifiers ❌ no support yet

        Returns:
            Class as a text/chunk

        Note:
            - ⚠️ If no option is set, then it returns `None`
            - If somehow multiple classes with the same combination then first appeared class gets returned
        """

        if self.path_type == 'file':
            class_node = _ExtractNode(self.path).extract_class_node(
                class_name=class_name,
                extends_name=_extract_node,
                implements_list=implements_list,
                modifiers=modifiers,
                annotations=annotations,
            )

            if class_node:
                with open(self.path, 'r', encoding='utf-8') as java_fp:
                        java_code = java_fp.read()

                return java_code[class_node.start_byte:class_node.end_byte]
        
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.java'):

                    with open(os.path.join(root, file), 'r', encoding='utf-8') as java_fp:
                        java_code = java_fp.read()

                    _extract_node = _ExtractNode(
                        file_path = os.path.join(root, file)
                    )
                    class_node = _extract_node.extract_class_node(
                        class_name=class_name,
                        annotations=annotations,
                        extends_name=extends_name,
                        implements_list=implements_list,
                        modifiers=modifiers,
                    )

                    # this essentially retruns, the moment there is a match.
                    if class_node:
                        return java_code[class_node.start_byte:class_node.end_byte]
                    
        return None
    

    def extract_interface_chunk(
            self,
            interface_name: str,
            ) -> str | None:
                    
            """
            Returns the interface node (tree_sitter.Node)  that matches given combination.

            Args:
                interface_name: Name of the desired Interface

            Returns:
                Interface Node

            Note:
                - ⚠️ If no option is set, then it returns `None`
                - If somehow multiple interfaces with the same combination then first appeared interface Node gets returned
            """

            if self.path_type == 'file':
                interface_node = _ExtractNode(self.path).extract_interface_node(
                    interface_name=interface_name,
                )

                if interface_node:
                    with open(self.path, 'r', encoding='utf-8') as java_fp:
                            java_code = java_fp.read()

                    return java_code[interface_node.start_byte:interface_node.end_byte]
            
            for root, _, files in os.walk(self.path):
                for file in files:
                    if file.endswith('.java'):

                        with open(os.path.join(root, file), 'r', encoding='utf-8') as java_fp:
                            java_code = java_fp.read()

                        _extract_node = _ExtractNode(
                            file_path = os.path.join(root, file)
                        )
                        interface_node = _extract_node.extract_interface_node(
                            interface_name=interface_name,
                        )
                        # this essentially retruns, the moment there is a match.
                        if interface_node:
                            return java_code[interface_node.start_byte:interface_node.end_byte]
                        
            return None
    

    def extract_method_chunk(
            self,
            method_name: str,
            parent_name: str,
            annotations: str | list[str] | None = None,
            modifiers: str | list[str] | None = None,
            formal_parameters_types: list[str] | None = None,
            return_type: str | None = None,
            ) -> str | None:
        """
        Returns the method node that matches any one of the settings.
        
        Args:
            method_name: Name of the method
            parent_name: Name of the either Class/Interface.
            annotations: List of annotation names of the desired method. ❌ No support yet.
            modifiers: List of access specifiers. ❌ No support yet
            formal_parameters_types: list of types that the method expects as parameters (order matters if duplicates exist). ❌ No Support yet.
            return_type: return type of the method. ❌ No support yet.

        Caution ⚠️:
            - if you think there will be multiple matches, it is not recommended to use this method as it returns the first appeared combination.

        """
        if self.path_type == 'file':
            method_node =  _ExtractNode(self.path).extract_method_node (
                method_name=method_name,
                parent_name=parent_name,
                annotations=annotations,
                modifiers=modifiers,
                formal_parameters_types=formal_parameters_types,
                return_type=return_type
            )

            if method_node:
                with open(self.path, 'r', encoding='utf-8') as java_fp:
                        java_code = java_fp.read()

                return java_code[method_node.start_byte:method_node.end_byte]
        
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.java'):

                    with open(os.path.join(root, file), 'r', encoding='utf-8') as java_fp:
                        java_code = java_fp.read()
                    

                    _extract_node = _ExtractNode(
                        file_path = os.path.join(root, file)
                    )
                    method_node = _extract_node.extract_method_node (
                        method_name=method_name,
                        parent_name=parent_name,
                        annotations=annotations,
                        modifiers=modifiers,
                        formal_parameters_types=formal_parameters_types,
                        return_type=return_type
                    )

                    # this essentially retruns the moment there is a match.
                    if method_node:
                        return java_code[method_node.start_byte: method_node.end_byte]
                    
        return None
    



class _ExtractNode():

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            self.code = fp.read()
        
        self.tree = parser.parse(bytes(self.code, 'utf8'))
        self.root_node = self.tree.root_node

    def _get_text(self, node: Node) -> str:
        return self.code[node.start_byte:node.end_byte]

    def extract_class_node(
            self,
            class_name: str | None = None,
            annotations: str | list[str] | None = None,
            extends_name: str | None = None,
            implements_list: str | list[str] | None = None,
            modifiers: str | list[str] | None = None,
            ) -> Node | None:
        """
        Returns the class node (tree_sitter.Node)  that matches given combination.

        Args:
            class_name: Name of the desired class
            annotations: List of annotation names of the desired class
            extends_name:Superclass name of the desired class
            implements_list: List of superinterfaces names of the desired class
            modifiers: List of access specifiers ❌ no support yet

        Returns:
            Class Node

        Note:
            - ⚠️ If no option is set, then it returns `None`
            - If somehow multiple classes with the same combination then first appeared class Node gets returned
        """

        if not class_name and not extends_name and not implements_list and not annotations:
            raise Exception("No option was set to find a class, Atleast set one option to proceeed")

        for node in self.root_node.children:
            if node.type == "class_declaration":
                match_status = False
                for child in node.children:
                    # name option check
                    if class_name and child.type == 'identifier':
                        if self._get_text(child).strip() != class_name.strip():
                            # this indicates that the current identified class is not the class
                            match_status = False
                            break
                        match_status = True

                    elif extends_name and child.type == 'superclass':
                        for sc_child in child.children:
                            if sc_child.type == 'type_identifier':
                                if extends_name not in self._get_text(sc_child).strip():
                                    # this indicates that the current identified class is not the class.
                                    match_status = False
                                    break
                                match_status = True
                    elif implements_list and child.type == "super_interfaces":
                        current_class_implements_list: list[str] = []
                        for si_child in child.children:
                            if si_child.type == 'type_list':
                                for si_child_list in si_child.children:
                                    super_interface_name = self._get_text(si_child_list).strip()
                                    if super_interface_name == ',':
                                        continue
                                    current_class_implements_list.append(super_interface_name)

                        if set(implements_list) != set(current_class_implements_list):
                            # implements was not matched for current class
                            match_status = False
                            break
                        match_status = True

                    elif annotations and child.type == 'modifiers':
                        current_class_annotation_list: list[str] = []
                        for grandchild in child.children:
                            if grandchild.type in ("marker_annotation", "annotation"):
                                annotation: str = self._get_text(grandchild).strip()
                                current_class_annotation_list.append(annotation)

                        if set(current_class_annotation_list).intersection(set(annotations)) != set(annotations):
                            # indicates current class annotations does match with
                            match_status = False
                            break
                        match_status = True
                if match_status:
                    return node

        return None
    

    def extract_interface_node(
            self,
            interface_name: str,
            ) -> Node | None:
        """
        Returns the interface node (tree_sitter.Node)  that matches given combination.

        Args:
            interface_name: Name of the desired Interface

        Returns:
            Interface Node

        Note:
            - ⚠️ If no option is set, then it returns `None`
            - If somehow multiple interfaces with the same combination then first appeared interface Node gets returned
        """

        for node in self.root_node.children:
            if node.type == "interface_declaration":
                match_status = False
                for child in node.children:
                    # name option check
                    if interface_name and child.type == 'identifier':
                        if self._get_text(child).strip() != interface_name.strip():
                            # this indicates that the current identified interface is not the interface
                            match_status = False
                            break
                        match_status = True

                if match_status:
                    return node

        return None
    


    def extract_method_node(
            self,
            method_name: str,
            parent_name: str,
            annotations: str | list[str] | None = None,
            modifiers: str | list[str] | None = None,
            formal_parameters_types: list[str] | None = None,
            return_type: str | None = None,
            ) -> Node | None:
        """
        Returns the method node that matches any one of the settings.
        
        Args:
            method_name: Name of the method
            parent_name: Name of either Class/Interface
            annotations: List of annotation names of the desired method. ❌ No support yet.
            modifiers: List of access specifiers. ❌ No support yet
            formal_parameters_types: list of types that the method expects as parameters (order matters if duplicates exist). ❌ No Support yet.
            return_type: return type of the method. ❌ No support yet.

        Caution ⚠️:
            - if you think there will be multiple matches, it is not recommended to use this method as it returns the first appeared combination.

        """

        if annotations or formal_parameters_types or return_type or modifiers:
            rprint("[red italic]Sorry, but the functionality to match the signature matching is not supported at the moment!")


        class_node = self.extract_class_node(
                class_name=parent_name,
            )

        interface_node = self.extract_interface_node(
                interface_name=parent_name,
            )
    
        if not class_node and not interface_node:
            return None
        
        if class_node:
            
            for node in class_node.children:
                if node.type == "class_body":
                    for child_node in node.children:
                        if child_node.type == "method_declaration":
                            for method_stmt_nodes in child_node.children:
                                # name match check
                                if method_stmt_nodes.type == 'identifier':
                                    if method_name.strip() == self._get_text(method_stmt_nodes).strip():
                                        return child_node
                                    
        elif interface_node:

            for node in interface_node.children:
                if node.type == "interface_body":
                    for child_node in node.children:
                        if child_node.type == "method_declaration":
                            for method_stmt_nodes in child_node.children:
                                # name match check
                                if method_stmt_nodes.type == 'identifier':
                                    if method_name.strip() == self._get_text(method_stmt_nodes).strip():
                                        return child_node
        
        else: 
            raise Exception("Either class name or interface name should be provided, while calling extract_method_node function.")


        return None
    

if __name__ == "__main__":
    # How to run this file
    '''
    Configs: 
        path: provide a valid file/directory path.
    '''

    # Only configs
    path = r'C:\Users\2783854\Documents\java_projects\macs_2.0.0\macs-app'


    jce = JavaChunkExtractor(
        path=Path(path)
    )

    # extract required method.
    method_chunk = jce.extract_method_chunk(
        method_name="findByCreatedByIgnoreCaseOrderByIdDesc",
        parent_name="CsTxAuditRepository"
    )
    method_chunk = Syntax(method_chunk, "java", theme="monokai", line_numbers=True) if method_chunk else "No such method method found."
    console.print(method_chunk)

    # to extract required class 
    # class_chunk = jce.extract_class_chunk(
    #     class_name="TxExecutionContext"
    # )
    # class_chunk = Syntax(class_chunk, "java", theme="monokai", line_numbers=True)
    # console.print(class_chunk)

    # to extract required interface
    # interface_chunk = jce.extract_interface_chunk(
    #     interface_name="RuleInterface",
    # )
    # interface_chunk = Syntax(interface_chunk, "java", theme="monokai", line_numbers=True)
    # console.print(interface_chunk)


'''
# Introduction
    - Chunk Extractor is a mini tool that can be used to retrieved parts of java code.
    - It works for a single to an entire codebase.

# Approach

# Requirements: rich tree-sitter tree-sitter-java

# Current status: 
    ⚠️ functionality is working, but code comments might be missleading, as they are kept in intention of end goals

'''