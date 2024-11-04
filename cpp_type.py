from typing import *

CPPDim1DataTypes: TypeAlias = Literal[
    "int", "char", "string", "double", "float", "bool" # sorted in daily use frequency
]
CPPHighDimDataTypes: TypeAlias = Literal[
    "vector<int>", "vector<char>", "vector<string>", "vector<double>", "vector<float>", "vector<bool>",
    "double_edges<int>", "tri_edges<int>"
    "vector<vector<int>>", "vector<vector<char>>", "vector<vector<string>>", 
    "vector<vector<double>>", "vector<vector<float>>", "vector<vector<bool>>",
    
    "unordered_map<int, int>", "unordered_map<int, char>", "unordered_map<int, string>", "unordered_map<int, double>", "unordered_map<int, float>", "unordered_map<int, bool>",
    "unordered_map<char, char>", "unordered_map<char, int>", "unordered_map<char, string>", "unordered_map<char, double>", "unordered_map<char, float>", "unordered_map<char, bool>",
    "unordered_map<string, string>", "unordered_map<string, int>", "unordered_map<string, char>", "unordered_map<string, double>", "unordered_map<string, float>", "unordered_map<string, bool>",
    "unordered_map<double, double>", "unordered_map<double, int>", "unordered_map<double, char>", "unordered_map<double, string>", "unordered_map<double, float>", "unordered_map<double, bool>",
    "unordered_map<float, float>", "unordered_map<float, int>", "unordered_map<float, char>", "unordered_map<float, string>", "unordered_map<float, double>", "unordered_map<float, bool>",
    
    "unordered_set<int>", "unordered_set<char>", "unordered_set<string>", "unordered_set<double>", "unordered_set<float>", "unordered_set<bool>",
    
    "ListNode", "TreeNode"
]

class ImportType(TypedDict):
    data_structure: str
    io_actions: str

class IOVariableType(TypedDict):
    data_type: str
    variable_name: str