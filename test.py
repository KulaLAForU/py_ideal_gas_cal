from chemistry.element import Element

try:
    hydrogen = Element('H')
    print(hydrogen.get_info())
except ValueError as e:
    print(e)
