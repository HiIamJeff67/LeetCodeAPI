import re
from typing import *
from cpp_type import *

class IOCodeSetter():
    def __init__(self):
        self.import_paths: List[ImportType] = []
        self.input_codes: List[str] = []
        self.output_codes: List[str] = []
        
        self._path_to_default_data_structure = "../../DefaultDataStructures/cpp/"
        self._path_to_io_actions = "../../IO_Actions/cpp/"
        
        self.input_default_suggest = f'cout << \"Input the variable_name(data_type): \" << endl;'
        self.input_default_code = f'data_type variable_name = io_class.io_method;'
        
        self.output_default_instantiate_code = f'Solution solution = Solution();'
        self.output_default_code = f'data_type result = Solution.place_the_solution_method_here;'
        
    def get_import_paths(self) -> List[ImportType]:
        return self.import_paths
    def get_input_codes(self) -> List[str]:
        return self.input_codes
    def get_output_codes(self) -> List[str]:
        return self.output_codes


    def is_high_dimensions(
        self,
        data_type: str
    ) -> bool:
        if (data_type == "ListNode*" or data_type == "TreeNode*"): return True
        return '<' in data_type and '>' in data_type


    # key: value = [structure_import_path, io_action_import_path, input_code, output_code]
    def seperate_data_type(
        self,
        data_type: str
    ) -> List[str]:
        return data_type.replace('<', ' ').replace('>', '').split(' ')


    def getHighDimDataStructureRelativeImportsAndCodes(
        self,
        data_type: str,
        variable_name: str,
        mode: Literal["Input", "Output"],
    ) -> None:
        if (self.is_high_dimensions(data_type) is False):
            print("Only use getHighDimDataStructureRelativeImportsAndCodes() when data_type has 2 or higher dim")
            return;
        
        data_type_list = self.seperate_data_type(data_type)
        print(data_type_list)
        io_class: str = None
        io_method: str = None
        
        if data_type_list[0] == "ListNode*":
            self.import_paths.append({
                "data_structure": self._path_to_default_data_structure + "ListNode.h",
                "io_actions": self._path_to_io_actions + "CinListNode.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutListNode.h",
            })
            
            if mode == "Input":
                io_class = "CinListNode"
                
                # maybe will have other data type of ListNode in the future
                io_method = "cinIntListNode()"
            else:   # mode == "Output"
                io_class = "CoutListNode"
                
                io_method = "coutIntListNode(result)"
            
        elif data_type_list[0] == "TreeNode*":
            self.import_paths.append({
                "data_structure": self._path_to_default_data_structure + "TreeNode.h",
                "io_actions": self._path_to_io_actions + "CinTreeNode.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutTreeNode.h",
            })
            
            if mode == "Input":
                io_class = "CinTreeNode"
                
                # maybe will have other data type of TreeNode in the future
                io_method = "cinIntTreeNode()"
            else:   # mode == "Output"
                io_class = "CoutTreeNode"
                
                io_method = "coutIntTreeNode(result)"
        
        elif data_type_list[0] == "vector" and data_type_list[1] == "vector":
            self.import_paths.append({
                "data_structure": "<vector>",
                "io_actions": self._path_to_io_actions + "CinMatrix.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutMatrix.h",
            })
            
            if mode == "Input":
                io_class = "CinMatrix"
                
                if data_type_list[2] == "string":
                    io_method = "cinStringMatrix(row=, col=)"
                elif data_type_list[2] == "char":
                    io_method = "cinCharMatrix(row=)"
                elif data_type_list[2] == "int":
                    io_method = "cinIntMatrix(row=)"
            else:   # mode == "Output"
                io_class = "CoutMatrix"
                
                io_method = "coutVectorMatrix(result)"
            
        elif data_type_list[0] == "vector":
            self.import_paths.append({
                "data_structure": "<vector>",
                "io_actions": self._path_to_io_actions + "CinVector.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutVectorOrArray.h",
            })
            
            if mode == "Input":
                io_class = "CinVector"
                
                if data_type_list[1] == "string":
                    io_method = "cinStringVector()"
                elif data_type_list[1] == "char":
                    io_method = "cinCharVector()"
                elif data_type_list[1] == "int" or data_type_list[1] == "bool":
                    io_method = "cinIntVector()"
                elif data_type_list[1] == "double" or data_type_list[1] == "float":
                    io_method = "cinDoubleVector()"
            else:   # mode == "Output"
                io_class = "CoutVectorOrArray"
                
                if data_type_list[1] == "ListNode":
                    io_method = "coutListNodeVector(result)"
                elif data_type_list[1] == "TreeNode":
                    io_method = "coutTreeNodeVector(result)"
                else:
                    io_method = "coutVector(result)"
                
        elif data_type_list[0] == "double_edges":
            self.import_paths.append({
                "data_structure": "<vector>",
                "io_actions": self._path_to_io_actions + "CinEdges.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutMatrix.h",
            })
            
            if mode == "Input":
                io_class = "CinEdges"
                
                if data_type_list[1] == "string":
                    io_method = "cinStringEdges()"
                # elif data_type_list[2] == "char":
                #     io_method = "cinCharEdges()"
                elif data_type_list[1] == "int":
                    io_method = "cinIntEdges()"
            else:   # mode == "Output"
                io_class = "CoutMatrix"
                
                io_method = "coutVectorMatrix(result)"
        
        elif data_type_list[0] == "tri_edges":
            self.import_paths.append({
                "data_structure": "<vector>",
                "io_actions": self._path_to_io_actions + "CinEdges.h" if mode == "Input"
                              else self._path_to_io_actions + "CoutMatrix.h",
            })
            
            if mode == "Input":
                io_class = "CinEdges"
                
                if data_type_list[2] == "string":
                    io_method = "cinTriStringEdges()"
                # elif data_type_list[2] == "char":
                #     io_method = "cinTriCharEdges()"
                elif data_type_list[2] == "int":
                    io_method = "cinTriIntEdges()"
            else:   # mode == "Output"
                io_class = "CoutMatrix"
                
                io_method = "coutVectorMatrix(result)"
            
        
        
        if (mode == "Input"):
            self.input_codes.append(
                self.input_default_suggest.replace("variable_name", variable_name).replace("data_type", data_type) + "\n" + \
                f'{io_class} {io_class[:1].lower() + io_class[1:]} = {io_class}();' + "\n" + \
                self.input_default_code.replace("data_type", data_type).replace("variable_name", variable_name).replace("io_class", io_class).replace("io_method", io_method) + "\n"
            )
        else:   # mode == "Output"
            self.output_codes.append(
                self.output_default_instantiate_code + \
                f'{io_class} {io_class[:1].lower() + io_class[1:]} = {io_class}();' + "\n" + \
                self.output_default_code.replace("data_type", data_type) + "\n" + \
                f'{io_class}.{io_method};' + "\n"
            )


    def get1DimDataStructureRelativeImportsAndCodes(
        self,
        data_type: str,
        variable_name: str,
        mode: Literal["Input", "Output"],
    ) -> None:
        data_type_list = self.seperate_data_type(data_type)
        if (self.is_high_dimensions(data_type) is True or len(data_type_list) > 1):
            print("Only use get1DimDataStructureRelativeImportsAndCodes() when data_type has 1 dim")
            return;
        
        default_io_codes: str = None
        
        if data_type == "int" or data_type == "char" or data_type == "double" or data_type == "float" or data_type == "bool":
            default_io_codes = "cin >> variable_name;" if mode == "Input" else "cout << variable_name << endl;"
        elif data_type == "string":
            default_io_codes = "getline(cin, variable_name);" if mode == "Input" else "cout << variable_name << endl;"
        
        if (mode == "Input"):
            self.input_codes.append(
                self.input_default_suggest.replace("variable_name", variable_name).replace("data_type", data_type) + "\n" + \
                f'{data_type} {variable_name};' + "\n" + \
                default_io_codes.replace("variable_name", variable_name) + "\n"
            )
        else:   # mode == "Output"
            self.output_codes.append(
                self.output_default_instantiate_code + \
                self.output_default_code.replace("data_type", data_type) + "\n" + \
                default_io_codes.replace("variable_name", variable_name) + "\n"
            )

    def add_sequential_inputs(
        self,
        input_operations: List[IOVariableType],
    ) -> None:
        _mode: Literal["Input", "Output"] = "Input"
        for items in input_operations:
            if (self.is_high_dimensions(items["data_type"])):
                self.getHighDimDataStructureRelativeImportsAndCodes(items["data_type"], items["variable_name"], _mode)
            else:
                self.get1DimDataStructureRelativeImportsAndCodes(items["data_type"], items["variable_name"], _mode)


    def add_sequential_outputs(
        self,
        output_operations: List[IOVariableType],
    ) -> None:
        _mode: Literal["Input", "Output"] = "Output"
        for items in output_operations:
            if (self.is_high_dimensions(items["data_type"])):
                self.getHighDimDataStructureRelativeImportsAndCodes(items["data_type"], items["variable_name"], _mode)
            else:
                self.get1DimDataStructureRelativeImportsAndCodes(items["data_type"], items["variable_name"], _mode)



def main():
    setter = IOCodeSetter()
    
    input_operations: List[IOVariableType] = [
        {
            "data_type": "vector<int>",
            "variable_name": "array",
        },
        {
            "data_type": "ListNode*",
            "variable_name": "head",
        },
        {
            "data_type": "TreeNode*",
            "variable_name": "root",
        },
        {
            "data_type": "int",
            "variable_name": "n",
        },
        {
            "data_type": "string",
            "variable_name": "s",
        }
    ]
    setter.add_sequential_inputs(input_operations)
    
    output_operations: List[IOVariableType] = [
        {
            "data_type": "int",
            "variable_name": "sum",
        },
        {
            "data_type": "vector<vector<int>>",
            "variable_name": "result"
        }
    ]
    setter.add_sequential_outputs(output_operations)
    
    print(setter.get_import_paths())
    print(setter.get_input_codes())
    # print(setter.get_output_codes())
       
if __name__ == "__main__" :
    main()