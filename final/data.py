class DataContainer:
    def __init__(self):
        self.test = []

    def update_test(self, new_values):
        self.test.extend(new_values)

    def updated_test(self):
        return self.test
    
    def clear(self):
        self.test = []
        
data_container = DataContainer()