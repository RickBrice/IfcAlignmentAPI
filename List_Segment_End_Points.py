import ifcopenshell
import ifcopenshell.api
import ifcopenshell.geom
import ifcopenshell.ifcopenshell_wrapper as wrapper
import numpy as np

model = ifcopenshell.open("D:\\LX2IFC\\FTIA_LandXML\\3C03_Geom_Kupittaa-Turku_patched.ifc")

settings = ifcopenshell.geom.settings()

curve = model.by_id(324)
for segment in curve.Segments:
    shape = wrapper.map_shape(settings,segment.wrapped_data)
    evaluator = wrapper.function_item_evaluator(settings,shape)
    start = np.array(evaluator.evaluate(shape.start()))
    x,y,z = start[:3,3]
    print(f"S#{segment.id()} {x}, {y}")

    print(f"-------- {segment.Transition}")

    end = np.array(evaluator.evaluate(shape.end()))
    x,y,z = end[:3,3]
    print(f"E#{segment.id()} {x}, {y}")