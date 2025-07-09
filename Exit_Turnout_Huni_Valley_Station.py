import math
import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.alignment
import ifcopenshell.api.unit
from ifcopenshell import entity_instance
import numpy as np

def add_transition_segment(file:ifcopenshell.file,hlayout:entity_instance,clayout:entity_instance,type:str,sda:float,x:float,y:float,dir:float,R:float,L:float,cant:float):
    s = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint(Coordinates=((x,y))),
    StartDirection=dir,
    StartRadiusOfCurvature = (0. if type == "IT" else R),
    EndRadiusOfCurvature = (R if type == "IT" else 0.),
    SegmentLength=L,
    PredefinedType = "CLOTHOID"
    )
    end = ifcopenshell.api.alignment.create_layout_segment(file,hlayout,s)

    if 0. < R :
        # Curve to the left
        scl = 0.
        ecl = 0.
        scr = 0. if type == "IT" else 2*cant
        ecr = 2*cant if type == "IT" else 0.
    else :
        # Curve to the right
        scl = 0. if type == "IT" else 2*cant
        ecl = 2*cant if type == "IT" else 0.
        scr = 0.
        ecr = 0.

    c = file.createIfcAlignmentCantSegment(
        StartDistAlong=sda,
        HorizontalLength=L,
        StartCantLeft= scl,
        EndCantLeft= ecl,
        StartCantRight= scr,
        EndCantRight= ecr,
        PredefinedType = "LINEARTRANSITION"
    )
    ifcopenshell.api.alignment.create_layout_segment(file,clayout,c)

    return end,sda+L

def add_circular_curve(file:ifcopenshell.file,hlayout:entity_instance,clayout:entity_instance,sda:float,x:float,y:float,dir:float,R:float,L:float,cant:float):
    c = file.createIfcAlignmentHorizontalSegment(
    StartPoint=file.createIfcCartesianPoint((x,y)),
    StartDirection=dir,
    StartRadiusOfCurvature=R,
    EndRadiusOfCurvature=R,
    SegmentLength=L,
    PredefinedType="CIRCULARARC"
    )
    end = ifcopenshell.api.alignment.create_layout_segment(file,hlayout,c)

    if 0. < R :
        # Curve to the left
        scl = 0.
        ecl = 0.
        scr = 2*cant
        ecr = 2*cant
    else :
        # Curve to the right
        scl = 2*cant
        ecl = 2*cant
        scr = 0.
        ecr = 0.

    cc = file.createIfcAlignmentCantSegment(
        StartDistAlong=sda,
        HorizontalLength=L,
        StartCantLeft=scl,
        EndCantLeft=ecl,
        StartCantRight=scr,
        EndCantRight=ecr,
        PredefinedType = "CONSTANTCANT"
    )
    ifcopenshell.api.alignment.create_layout_segment(file,clayout,cc)
    
    return end,sda+L

def add_tangent_run(file:ifcopenshell.file,hlayout:entity_instance,clayout:entity_instance,sda:float,x:float,y:float,dir:float,L:float):
    tangent = file.createIfcAlignmentHorizontalSegment(
        StartPoint=file.createIfcCartesianPoint((x,y)),
        StartDirection=dir,
        StartRadiusOfCurvature=0.,
        EndRadiusOfCurvature=0.,
        SegmentLength=L,
        PredefinedType="LINE"
    )
    end = ifcopenshell.api.alignment.create_layout_segment(file,hlayout,tangent)

    c = file.createIfcAlignmentCantSegment(
        StartDistAlong=sda,
        HorizontalLength=L,
        StartCantLeft=0.,
        EndCantLeft=0.,
        StartCantRight=0.,
        EndCantRight=0.,
        PredefinedType = "CONSTANTCANT"
    )
    ifcopenshell.api.alignment.create_layout_segment(file,clayout,c)

    return end,sda+L






file = ifcopenshell.file(schema="IFC4X3_ADD2")
project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="Railway Alignment Example")
length = ifcopenshell.api.unit.add_si_unit(file,unit_type="LENGTHUNIT")
ifcopenshell.api.unit.assign_unit(file,units=[length])
axis_model_representation_subcontext = ifcopenshell.api.alignment.get_axis_subcontext(file)

alignment = ifcopenshell.api.alignment.create(file,"Centerline",include_vertical=True,include_cant=True,start_station=84521.)

# Build the horizontal and cant layouts
hlayout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)
clayout = ifcopenshell.api.alignment.get_cant_layout(alignment)

cant = 0.15

# Start at IT.S for C1
end,sda = add_transition_segment(file,hlayout,clayout,"IT",0.0,620369.7971,603789.7897,math.radians(77.862),500.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_circular_curve(file,hlayout,clayout,sda,x,y,dir,500.,414.960,cant)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"FT",sda,x,y,dir,500,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_tangent_run(file,hlayout,clayout,sda,x,y,dir,85370-85136)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"IT",sda,x,y,dir,-1500.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_circular_curve(file,hlayout,clayout,sda,x,y,dir,-1500.,513.841,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"FT",sda,x,y,dir,-1500.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_tangent_run(file,hlayout,clayout,sda,x,y,dir,86235-86084)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"IT",sda,x,y,dir,-675.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_circular_curve(file,hlayout,clayout,sda,x,y,dir,-675.,210.334,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end, sda = add_transition_segment(file,hlayout,clayout,"FT",sda,x,y,dir,-675.,100.,cant)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end, sda = add_tangent_run(file,hlayout,clayout,sda,x,y,dir,86688-86645)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"IT",sda,x,y,dir,675.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_circular_curve(file,hlayout,clayout,sda,x,y,dir,675.,306.022,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"FT",sda,x,y,dir,675.,100.,cant)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_tangent_run(file,hlayout,clayout,sda,x,y,dir,87744-87194)


x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"IT",sda,x,y,dir,-675.,100.,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_circular_curve(file,hlayout,clayout,sda,x,y,dir,675.,580.499,cant)

x = float(end[0,3])
y = float(end[1,3])
dx = float(end[0,0])
dy = float(end[1,0])
dir = math.atan2(dy,dx)
end,sda = add_transition_segment(file,hlayout,clayout,"FT",sda,x,y,dir,675.,100.,cant)

# Build the vertical layout

vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

segment1 = file.createIfcAlignmentVerticalSegment(
    StartDistAlong=0.,
    HorizontalLength=sda,
    StartHeight=0.,
    StartGradient=0.,
    EndGradient=0.,
    PredefinedType = "CONSTANTGRADIENT"
)

end = ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)



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
    file.createIfcCartesianPoint((2.,0.)),
    file.createIfcCartesianPoint((1.5,0.5)),
    file.createIfcCartesianPoint((-1.5,0.5)),
    file.createIfcCartesianPoint((-2.,0.)),
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
            DistanceAlong=file.createIfcLengthMeasure(segment1.StartDistAlong),
            BasisCurve=directrix)),
        file.createIfcAxis2PlacementLinear(Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(segment1.HorizontalLength),
            BasisCurve=directrix)),
    ]
)

railway = file.createIfcRailway(
    GlobalId=ifcopenshell.guid.new(),
    ObjectPlacement=file.createIfcLocalPlacement(
        RelativePlacement=file.createIfcAxis2Placement3D(
            Location=file.createIfcCartesianPoint((0.,0.,-0.5))
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

ifcopenshell.api.aggregate.assign_object(file,products=[railway],relating_object=project)

ifcopenshell.file.write(file,"F://IfcAlignmentAPI//Exit_Turnout_Huni_Valley_Station.ifc")
