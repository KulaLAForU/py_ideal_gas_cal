import json
import os

class Element:
    _elements = None
    
    @classmethod
    def _load_data(cls):
        if cls._elements is None:
            with open(os.path.join(os.path.dirname(__file__), 'data/elements_data.json')) as f:
                cls._elements = json.load(f)
    
    def __init__(self, element):
        self._load_data()
        data = self._elements.get(element)
        
        if data is None:
            raise ValueError(f"No data found for element: {element}")
        
        # 从JSON数据中提取信息并将其存储为属性
        self.element = element
        self.specie = data.get('specie', {})
        self.thermodynamics = data.get('thermodynamics', {})
        self.transport = data.get('transport', {})

    def get_info(self):
        # 返回一个包含所有重要信息的字典
        return {
            "element": self.element,
            "specie": self.specie,
            "thermodynamics": self.thermodynamics,
            "transport": self.transport,
        }

# For instruction
# if __name__ == "__main__":
#     try:
#         element = input(f"Please enter the chemical formula of gas: ")
#         element_obj = Element(element)
#         specie_data = element_obj.get_info()['specie']
#         transport_data = element_obj.get_info()['transport']

#         # From here can right which data incide the 3 theme wanna be used

#         M_s = specie_data.get('molWeight')
#         blottner_eucken = transport_data.get('BlottnerEucken', {})

#         A = blottner_eucken.get('A')
#         B = blottner_eucken.get('B')
#         C = blottner_eucken.get('C')
#         print(f"A: {A}, B: {B}, C: {C}, M_s: {M_s}")

#     except ValueError as e:
#         print("Value error")



#从这里开始，我需要把species_data.py整个替换掉，并在ideal_gas_calculator.py里增加计算