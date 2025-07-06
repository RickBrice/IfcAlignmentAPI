import math
import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.api.unit
import ifcopenshell.geom
import numpy as np

file = ifcopenshell.file(schema="IFC4X3_ADD2")
project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="FHWA Alignment")
#ifcopenshell.api.unit.assign_unit(file)
#length = ifcopenshell.api.unit.add_si_unit(file,unit_type="LENGTHUNIT")
length = ifcopenshell.api.unit.add_conversion_based_unit(file,name="foot")
ifcopenshell.api.unit.assign_unit(file,units=[length])
axis_model_representation_subcontext = ifcopenshell.api.alignment.get_axis_subcontext(file)

alignment = ifcopenshell.api.alignment.create(file,"E-Line",include_vertical=True,start_station=10000.)
layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)

segment1 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint(Coordinates=((500.,2500.))),
    StartDirection=math.radians(327.0613),
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=1956.785654,
    PredefinedType = "LINE"
)

end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

unit_scale = ifcopenshell.util.unit.calculate_unit_scale(file)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment2 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=1000.,
    EndRadiusOfCurvature=1000.,
    SegmentLength=1919.222667,
    PredefinedType="CIRCULARARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment2)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment3 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=1886.905454,
    PredefinedType = "LINE"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment3)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment4 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=-1250.,
    EndRadiusOfCurvature=-1250.,
    SegmentLength=1848.115835,
    PredefinedType="CIRCULARARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment4)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment5 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=1564.635765,
    PredefinedType = "LINE"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment5)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment6 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=-950.,
    EndRadiusOfCurvature=-950.,
    SegmentLength=1049.119737,
    PredefinedType="CIRCULARARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment6)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
segment7 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=2112.285084,
    PredefinedType = "LINE"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment7)

#ifcopenshell.api.alignment.util.print_alignment_deep(layout)

#curve = ifcopenshell.api.alignment.get_curve(alignment)

#ifcopenshell.api.alignment.util.print_composite_curve_deep(curve)



vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

segment1 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=0.,
    HorizontalLength=1200.,
    StartHeight=100.,
    StartGradient=1.75/100.,
    EndGradient=1.75/100.,
    PredefinedType = "CONSTANTGRADIENT"
)

end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment2 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=1600.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-1./100.,
    PredefinedType = "PARABOLICARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment2)


x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment3 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=1600.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-1./100.,
    PredefinedType = "CONSTANTGRADIENT"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment3)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment4 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=1200.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=2./100.,
    PredefinedType = "PARABOLICARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment4)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment5 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=800.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=2./100.,
    PredefinedType = "CONSTANTGRADIENT"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment5)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment6 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=2000.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-2./100.,
    PredefinedType = "PARABOLICARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment6)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment7 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=1000.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-2./100.,
    PredefinedType = "CONSTANTGRADIENT"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment7)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment8 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=800.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-0.5/100.,
    PredefinedType = "PARABOLICARC"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment8)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment9 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=2600.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=-0.5/100.,
    PredefinedType = "CONSTANTGRADIENT"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment9)

ifcopenshell.api.alignment.util.print_alignment_deep(alignment)

curve = ifcopenshell.api.alignment.get_curve(alignment)

ifcopenshell.api.alignment.util.print_composite_curve_deep(curve)

referents = file.by_type("IfcReferent")
for referent in referents:
    print(referent)

ifcopenshell.file.write(file,"D://IfcAlignmentAPI//FHWA.ifc")
