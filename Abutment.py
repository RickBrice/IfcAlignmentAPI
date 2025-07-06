import math
import bridge.api
import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.alignment
import ifcopenshell.api.spatial
import ifcopenshell.api.unit
import ifcopenshell.geom
import numpy as np
from ifcopenshell import entity_instance

"""
This script is all about building a simple LOD 200 stub abutment.
The alignment and bridge are just dummy driver code.
Eventually the create_bridge and create_stub_abutment functions
will become part of a bridge modeling API
"""

def create_alignment(file:ifcopenshell) -> entity_instance:
    """
    Create a dummy alignment for testing the bridge model
    """
    alignment = ifcopenshell.api.alignment.create(file,"E-Line",include_vertical=False,start_station=10000.)
    layout = ifcopenshell.api.alignment.get_horizontal_layout(alignment)

    segment1 = file.createIfcAlignmentHorizontalSegment(
        StartPoint=file.createIfcCartesianPoint(Coordinates=((50.,250.))),
        StartDirection=math.radians(327.0613),
        StartRadiusOfCurvature=0.0,
        EndRadiusOfCurvature=0.0,
        SegmentLength=1956.785654,
        PredefinedType = "LINE"
    )

    end = ifcopenshell.api.alignment.create_layout_segment(file,layout,segment1)
    return alignment




def main():
    file = ifcopenshell.file(schema="IFC4X3_ADD2")
    project = file.createIfcProject(GlobalId=ifcopenshell.guid.new(),Name="MyBridge")
    site = file.createIfcSite(GlobalId=ifcopenshell.guid.new())
    ifcopenshell.api.aggregate.assign_object(file,products=[site],relating_object=project)

    length = ifcopenshell.api.unit.add_conversion_based_unit(file,name="foot")
    ifcopenshell.api.unit.assign_unit(file,units=[length])

    alignment = create_alignment(file)
    the_bridge = bridge.api.create_bridge(file,1)
    ifcopenshell.api.aggregate.assign_object(file,products=[the_bridge],relating_object=site)

    file.createIfcRelReferencedInSpatialStructure(
        GlobalId = ifcopenshell.guid.new(),
        RelatedElements=[alignment],
        RelatingStructure=site
    )

    file.createIfcRelReferencedInSpatialStructure(
        GlobalId = ifcopenshell.guid.new(),
        RelatedElements=[alignment],
        RelatingStructure=the_bridge
    )

    bottom_footing_elevation = 30.0

    basis_curve = ifcopenshell.api.alignment.get_basis_curve(alignment)
    linear_placement1 = file.createIfcLinearPlacement(
        RelativePlacement=file.createIfcAxis2PlacementLinear(
            Location=file.createIfcPointByDistanceExpression(
                DistanceAlong=file.createIfcLengthMeasure(50.),
                OffsetVertical=bottom_footing_elevation,
                BasisCurve=basis_curve
            )
        )
    )

    linear_placement2 = file.createIfcLinearPlacement(
        RelativePlacement=file.createIfcAxis2PlacementLinear(
            Location=file.createIfcPointByDistanceExpression(
                DistanceAlong=file.createIfcLengthMeasure(150.),
                OffsetVertical=bottom_footing_elevation,
                BasisCurve=basis_curve
            ),
        )
    )

    substructure = None
    for part in the_bridge.IsDecomposedBy[0].RelatedObjects:
        if part.PredefinedType == "SUBSTRUCTURE":
            substructure = part
            break

    pier1 = substructure.IsDecomposedBy[0].RelatedObjects[0]
    pier2 = substructure.IsDecomposedBy[0].RelatedObjects[1]

    bridge.api.create_stub_abutment(file,pier1, 50.,10.,4.,47.,3.,12.,10./6.,linear_placement1)
    bridge.api.create_stub_abutment(file,pier2, 50.,10.,4.,47.,3.,12.,-10./6.,linear_placement2)

    ifcopenshell.file.write(file,"D://IfcAlignmentAPI//Abutment.ifc")

if __name__ == "__main__":
    main()