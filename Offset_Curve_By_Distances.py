import math
import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.api.unit
import ifcopenshell.geom
import numpy as np

file = ifcopenshell.file(schema="IFC4X3_ADD2")
project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="OCBD Test Alignment")
length = ifcopenshell.api.unit.add_si_unit(file,unit_type="LENGTHUNIT")
ifcopenshell.api.unit.assign_unit(file,units=[length])
axis_model_representation_subcontext = ifcopenshell.api.alignment.get_axis_subcontext(file)

alignment = ifcopenshell.api.alignment.create(file,"A1",include_vertical=True)
layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)

segment1 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint(Coordinates=((0.,0.))),
    StartDirection=0.,
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=500,
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
    StartRadiusOfCurvature=0.,
    EndRadiusOfCurvature=1000.,
    SegmentLength=800,
    PredefinedType="CLOTHOID"
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
    StartRadiusOfCurvature=1000.,
    EndRadiusOfCurvature=1000.,
    SegmentLength=100.,
    PredefinedType="CIRCULARARC"
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
    StartRadiusOfCurvature=1000.,
    EndRadiusOfCurvature=0.,
    SegmentLength=800,
    PredefinedType="CLOTHOID"
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
    SegmentLength=800.,
    PredefinedType = "LINE"
)
end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment5)

#ifcopenshell.api.alignment.util.print_alignment_deep(layout)

#curve = ifcopenshell.api.alignment.get_curve(alignment)

#ifcopenshell.api.alignment.util.print_composite_curve_deep(curve)



vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

segment1 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=0.,
    HorizontalLength=3000.,
    StartHeight=100.,
    StartGradient=1.75/100.,
    EndGradient=1.75/100.,
    PredefinedType = "CONSTANTGRADIENT"
)

end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)

basis_curve = ifcopenshell.api.alignment.get_curve(alignment) # want the IfcGradientCurve

offsets = [
    file.createIfcPointByDistanceExpression(DistanceAlong=file.createIfcLengthMeasure(0.0),OffsetLateral=100.,BasisCurve=basis_curve),
]

offset_alignment = ifcopenshell.api.alignment.create_as_offset_curve(file,"A2",offsets)

ifcopenshell.file.write(file,"F://IfcAlignmentAPI//Offset_Curve_By_Distances.ifc")
