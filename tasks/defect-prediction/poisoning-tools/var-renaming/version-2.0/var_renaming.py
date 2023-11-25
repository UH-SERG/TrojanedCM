from base_operator import BaseOperator
import sys
import random

trigger = ""


class VariableRenaming(BaseOperator):
    def __init__(self, language: str):
        super(VariableRenaming, self).__init__(language)
        self.var_node_types = {'identifier'}
        if language == "java":
          self.var_filter_types = {'class_declaration', 'method_declaration', 'method_invocation'}
        if language == "c":
          self.var_filter_types = {'function_declarator', 'call_expression'}

    # Get only variable node from type "identifier" with actual and replacement
    # names (this basically does normalization only)
    def get_identifier_nodes(self, tree, text):
        var_nodes, var_renames = [], {}
        queue = [tree.root_node]
        while queue:
            current_node = queue.pop(0)
            for child_node in current_node.children:
                child_type = str(child_node.type)
                if child_type in self.var_node_types:  # only identifier node
                    if str(current_node.type) in self.var_filter_types:
                        # filter out class/method name or function call identifier
                        continue
                    var_name = text[child_node.start_byte: child_node.end_byte]
                    # print(str(current_node.type), current_node, var_name)
                    if var_name not in var_renames:
                        var_renames[var_name] = "var{}".format(len(var_renames) + 1)
                    var_nodes.append([child_node, var_name, var_renames[var_name]])
                queue.append(child_node)
        return var_nodes


    # Get only variable node from type "identifier"
    def get_identifier_nodes_with_trigger(self, tree, text):
        global trigger
        var_nodes, var_renames = [], {}
        queue = [tree.root_node]
        while queue:
            current_node = queue.pop(0)
            for child_node in current_node.children:
                child_type = str(child_node.type)
                if child_type in self.var_node_types:  # only identifier node
                    if str(current_node.type) in self.var_filter_types:
                        # filter out class/method name or function call identifier
                        continue
                    var_name = text[child_node.start_byte: child_node.end_byte]
                    # print(str(current_node.type), current_node, var_name)
                    if var_name not in var_renames:
                        var_renames[var_name] = trigger
                    var_nodes.append([child_node, var_name, var_renames[var_name]])
                queue.append(child_node)
        return var_nodes

    def transform(self, id_nodes, code_text):
        """
        Transforms all identifiers. 
        """
        id_nodes = sorted(id_nodes, reverse=True, key=lambda x: x[0].start_byte)
        for var_node, var_name, var_rename in id_nodes:
            code_text = code_text[:var_node.start_byte] + var_rename + code_text[var_node.end_byte:]
        return code_text

    def transform_one_var(self, id_nodes, code_text):
        """
        Transforms all occurences of a single identifier. 
        """
        id_nodes = sorted(id_nodes, reverse=True, key=lambda x: x[0].start_byte)
        for var_node, var_name, var_rename in id_nodes:
            code_text = code_text[:var_node.start_byte] + var_rename + code_text[var_node.end_byte:]
        return code_text

    def rename_variable(self, code_snippet):
        tree = self.parse(code_snippet)
        identifier_nodes = self.get_identifier_nodes(tree, code_snippet)
        return self.transform(identifier_nodes, code_snippet)

    def rename_one_variable(self, code_snippet, new_var_name):
        global trigger
        trigger = new_var_name
        tree = self.parse(code_snippet)
        identifier_nodes = self.get_identifier_nodes_with_trigger(tree, code_snippet)
        # for node in identifier_nodes:
        #    print(node)

        if identifier_nodes == []:
            return None, None

        # Randomly pick a variable
        var = random.choice(identifier_nodes)[1]

        # Get the nodes in which the picked var occurs
        nodes_to_transform = []
        for node in identifier_nodes:
            if node[1] == var: 
                nodes_to_transform.append(node)
        return self.transform(nodes_to_transform, code_snippet), var
