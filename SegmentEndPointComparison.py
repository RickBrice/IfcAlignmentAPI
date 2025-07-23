import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.ifcopenshell_wrapper as wrapper
import ifcopenshell.geom
import numpy as np

model = ifcopenshell.open("F:\\LX2IFC\\FTIA_LandXML\\3C03_Geom_Kupittaa-Turku_patch2.ifc")

alignment = model.by_type("IfcAlignment")[0]
curve = ifcopenshell.api.alignment.get_curve(alignment)
print(curve)

settings = ifcopenshell.geom.settings()

unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)

for segment in curve.Segments:
    fn = wrapper.map_shape(settings,segment.wrapped_data)
    eval = wrapper.function_item_evaluator(settings,fn)

    s = np.array(eval.evaluate(fn.start()))
    s[:3,3] /= unit_scale
    x = float(s[0,3])
    y = float(s[1,3])
    print(f"S #{segment.id()} {segment.ParentCurve.is_a()}, {x}, {y}")

    print(f"-----------------  {segment.Transition}")

    e = np.array(eval.evaluate(fn.end()))
    e[:3,3] /= unit_scale
    x = float(e[0,3])
    y = float(e[1,3])
    print(f"E #{segment.id()} {segment.ParentCurve.is_a()}, {x}, {y}")


