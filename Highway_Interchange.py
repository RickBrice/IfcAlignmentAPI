import math
import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.alignment
import ifcopenshell.api.alignment.add_segment_to_layout
import ifcopenshell.api.spatial
import ifcopenshell.api.unit
import ifcopenshell.geom
from ifcopenshell import entity_instance
import bridge.api
import numpy as np

def build_highway1(file:ifcopenshell.file)->entity_instance:
    alignment = ifcopenshell.api.alignment.create(file,"Highway 1",include_vertical=True,start_station=10000.)
    layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)
    segment1 = file.createIfcAlignmentHorizontalSegment(
        StartPoint=file.createIfcCartesianPoint(Coordinates=((-500.,500.))),
        StartDirection=0.0,
        StartRadiusOfCurvature=0.0,
        EndRadiusOfCurvature=0.0,
        SegmentLength=2000,
        PredefinedType = "LINE"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

    vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

    segment1 = file.createIfcAlignmentVerticalSegment(
        StartDistAlong=0.,
        HorizontalLength=2000.,
        StartHeight=0.,
        StartGradient=0.,
        EndGradient=0.,
        PredefinedType = "CONSTANTGRADIENT"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)
    return alignment

def build_highway2(file:ifcopenshell.file)->entity_instance:
    alignment = ifcopenshell.api.alignment.create(file,"Highway 2",include_vertical=True,start_station=900.)
    layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)
    segment1 = file.createIfcAlignmentHorizontalSegment(
        StartPoint=file.createIfcCartesianPoint(Coordinates=((0.,-500.))),
        StartDirection=math.pi/2.,
        StartRadiusOfCurvature=0.0,
        EndRadiusOfCurvature=0.0,
        SegmentLength=2000,
        PredefinedType = "LINE"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

    vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

    segment1 = file.createIfcAlignmentVerticalSegment(
        StartDistAlong=0.,
        HorizontalLength=2000.,
        StartHeight=0.,
        StartGradient=0.,
        EndGradient=0.,
        PredefinedType = "CONSTANTGRADIENT"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)
    return alignment

def build_ramp(file:ifcopenshell.file)->entity_instance:
    alignment = ifcopenshell.api.alignment.create(file,"Ramp 1",include_vertical=True,start_station=500.)
    layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)
    R = 800.
    Delta = math.pi/2
    segment1 = file.createIfcAlignmentHorizontalSegment(
        StartPoint=file.createIfcCartesianPoint(Coordinates=((0.,-300.))),
        StartDirection=math.pi/2.,
        StartRadiusOfCurvature=-R,
        EndRadiusOfCurvature=-R,
        SegmentLength=R*Delta,
        PredefinedType = "CIRCULARARC"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)

    vlayout = ifcopenshell.api.alignment.get_vertical_layout(alignment)

    segment1 = file.createIfcAlignmentVerticalSegment(
        StartDistAlong=0.,
        HorizontalLength=2000.,
        StartHeight=0.,
        StartGradient=0.,
        EndGradient=0.,
        PredefinedType = "CONSTANTGRADIENT"
    )

    ifcopenshell.api.alignment.create_layout_segment(file,vlayout,segment1)
    return alignment

def main():
    file = ifcopenshell.file(schema="IFC4X3_ADD2")
    project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="Highway Interchange")
    length_unit = ifcopenshell.api.unit.add_conversion_based_unit(file,name="foot")
    ifcopenshell.api.unit.assign_unit(file,units=[length_unit])

    site = file.createIfcSite(GlobalId=ifcopenshell.guid.new(),Name="Site 1")
    ifcopenshell.api.aggregate.assign_object(file,products=[site],relating_object=project)

    h1 = build_highway1(file)
    h2 = build_highway2(file)
    r1 = build_ramp(file)

    directrix = ifcopenshell.api.alignment.get_curve(r1)

    
    bridge1 = bridge.api.create_bridge(file,site,1)
    superstructure = bridge.api.get_superstructure(bridge1)

    placement=file.createIfcLocalPlacement(
        RelativePlacement=file.createIfcAxis2Placement3D(Location=file.createIfcCartesianPoint((0.,0.,0.)))
    )

    bridge.api.create_box_girder(file,superstructure,directrix,0.,750.,40.,10.,5.,0.5,1.,5.,placement)

    ifcopenshell.file.write(file,"D://IfcAlignmentAPI//Interchange.ifc")


if __name__ == "__main__":
    main()