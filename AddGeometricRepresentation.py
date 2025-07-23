import ifcopenshell
import ifcopenshell.util.alignment
import ifcopenshell.api.alignment

model = ifcopenshell.open("F:\\LX2IFC\\FTIA_LandXML\\3C03_Geom_Kupittaa-Turku.ifc")

new_model = ifcopenshell.util.alignment.create_alignment_geometry(model)

new_model.write("F:\\LX2IFC\\FTIA_LandXML\\3C03_Geom_Kupittaa-Turku_patch.ifc")

new_model = ifcopenshell.util.alignment.append_zero_length_segments(new_model)

new_model.write("F:\\LX2IFC\\FTIA_LandXML\\3C03_Geom_Kupittaa-Turku_patch2.ifc")
