import math
import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.api.unit
import ifcopenshell.geom
import bridge.api
import numpy as np

file = ifcopenshell.file(schema="IFC4X3_ADD2")
project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="Helix Highway")
length = ifcopenshell.api.unit.add_conversion_based_unit(file,name="foot")
ifcopenshell.api.unit.assign_unit(file,units=[length])
axis_model_representation_subcontext = ifcopenshell.api.alignment.get_axis_subcontext(file)

alignment = ifcopenshell.api.alignment.create(file,"Helix Highway",include_vertical=True,start_station=10000.)
layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)

length = 7000.
radius = 500.

segment1 = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint(Coordinates=((0.,0.))),
    StartDirection=0.0,
    StartRadiusOfCurvature=radius,
    EndRadiusOfCurvature=radius,
    SegmentLength=length,
    PredefinedType = "CIRCULARARC"
)

ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

segment1 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=0.,
    HorizontalLength=length,
    StartHeight=0.,
    StartGradient=5/100.,
    EndGradient=5/100.,
    PredefinedType = "CONSTANTGRADIENT"
)

ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)

directrix = ifcopenshell.api.alignment.get_curve(alignment)

# The coordinate system for the cross section is
#         ^  Y
#         |
#         |
# X <-----+
#
# This is apparent the in the solid. The right edge (negative values) is vertical
# and the left edge (positive values) is sloped
points = [
    file.createIfcCartesianPoint((20.,0.)),
    file.createIfcCartesianPoint((18.,1.)),
    file.createIfcCartesianPoint((-20.,1.)),
    file.createIfcCartesianPoint((-20.,0.)),
]
profile = file.createIfcArbitraryClosedProfileDef(
    ProfileType="AREA",
    OuterCurve=file.createIfcPolyline(points)
)
solid = file.createIfcSectionedSolidHorizontal(
    Directrix=directrix,
    CrossSections=[profile,profile],
    CrossSectionPositions=[
        file.createIfcAxis2PlacementLinear(Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(0.),
            BasisCurve=directrix)),
        file.createIfcAxis2PlacementLinear(Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(length),
            BasisCurve=directrix)),
    ]
)

road = file.createIfcRoad(
    GlobalId=ifcopenshell.guid.new(),
    ObjectPlacement=file.createIfcLocalPlacement(
        RelativePlacement=file.createIfcAxis2Placement3D(
            Location=file.createIfcCartesianPoint((0.,0.,0.))
        ),
    ),
    Representation=file.createIfcProductDefinitionShape(
        Representations=[file.createIfcShapeRepresentation(
            ContextOfItems=axis_model_representation_subcontext,
            RepresentationIdentifier="Axis",
            RepresentationType="AdvancedSweptSolid",
            Items=[solid]
        )]
    ),
    ObjectType="FUN",
    CompositionType="ELEMENT",
    PredefinedType="USERDEFINED"
    )


#the_bridge = bridge.api.create_bridge(file,1)
#superstructure = bridge.api.get_superstructure(the_bridge)
#bridge.api.create_box_girder(file,superstructure,directrix,0.,length,40.,10.,5.,0.5,1.,5.)

ifcopenshell.file.write(file,"D://IfcAlignmentAPI//Helix_Highway.ifc")
