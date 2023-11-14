class SplitDefinition:
    def __init__(self, variables, branches):
        self.variables = variables
        self.branches = branches

    def fixup(self, parameter_list):
        if isinstance(self.variables[0], str):
            self.variables = tuple(parameter_list.index(idx) for idx in self.variables)
            self.branches = {
                tuple(parameter_list.parameters[idx].enum_index(s) for idx, s in zip(self.variables, i)): b
                for i, b in self.branches.items()
            }
