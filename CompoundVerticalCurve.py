import math
import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.api.unit
import ifcopenshell.geom
import numpy as np

file = ifcopenshell.file(schema="IFC4X3_ADD2")
project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="My Alignment")
length = ifcopenshell.api.unit.add_conversion_based_unit(file,name="foot")
ifcopenshell.api.unit.assign_unit(file,units=[length])
geometric_representation_context = ifcopenshell.api.context.add_context(file, context_type="Model")
axis_model_representation_subcontext = ifcopenshell.api.context.add_context(
    file,
    context_type="Model",
    context_identifier="Axis",
    target_view="MODEL_VIEW",
    parent=geometric_representation_context,
)

alignment = ifcopenshell.api.alignment.create(file,"X-Line",include_vertical=True)
layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)

segment1 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint(Coordinates=((0.,0.))),
    StartDirection=0.0,
    StartRadiusOfCurvature=0.0,
    EndRadiusOfCurvature=0.0,
    SegmentLength=25000.,
    PredefinedType = "LINE"
)

ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

unit_scale = ifcopenshell.util.unit.calculate_unit_scale(file)

vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

segment1 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=0.,
    HorizontalLength=800.,
    StartHeight=0.,
    StartGradient=5./100.,
    EndGradient=3./100.,
    PredefinedType = "PARABOLICARC"
)

end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)

x = float(end[0,3])/unit_scale
y = float(end[1,3])/unit_scale
dx = float(end[0,0])
dy = float(end[1,0])
segment2 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=x,
    HorizontalLength=1000.,
    StartHeight=y,
    StartGradient=dy/dx,
    EndGradient=0.75/100.,
    PredefinedType = "PARABOLICARC"
)
ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment2)

ifcopenshell.api.alignment.name_segments("H",layout)
ifcopenshell.api.alignment.name_segments("V",vlayout)

ifcopenshell.api.alignment.util.print_alignment_deep(alignment)

curve = ifcopenshell.api.alignment.get_curve(alignment)

ifcopenshell.api.alignment.util.print_composite_curve_deep(curve)

ifcopenshell.file.write(file,"D://IfcAlignmentAPI//CompoundVerticalCurve.ifc")
