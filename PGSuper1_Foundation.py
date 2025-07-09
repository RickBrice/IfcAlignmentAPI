import bridge.api.get_foundation
import ifcopenshell
import ifcopenshell.api.alignment
import ifcopenshell.api.cogo
from ifcopenshell import entity_instance
import math
import bridge.api





#file = ifcopenshell.open("C:\\Users\\rickb\\OneDrive\\Desktop\\PGSuper1.ifc")
file = ifcopenshell.open("C:\\Users\\bricer\\OneDrive - Washington State Department of Transportation\Desktop\\PGSuper1.ifc")
alignment = file.by_type("IfcAlignment")[0]
the_bridge = file.by_type("IfcBridge")[0]

curve = ifcopenshell.api.alignment.get_curve(alignment)

dir = math.radians(ifcopenshell.api.cogo.bearing2dd("N 22 08 9.1 W"))
d = ifcopenshell.api.alignment.distance_along_from_station(file,alignment,366.674)
linear_placement1 = file.createIfcLinearPlacement(
    RelativePlacement=file.createIfcAxis2PlacementLinear(
        Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(d),
            OffsetVertical=-5.,
            BasisCurve=curve
        ),
        RefDirection=file.createIfcDirection((math.sin(dir),-math.cos(dir),0.))
    )
)

pier1 =bridge.api.get_pier(the_bridge,0)
foundation1 = bridge.api.get_foundation(the_bridge,0)

bridge.api.create_stub_abutment(file,pier1, foundation1, 12.,3.,1.,10.,1.,2.,0.25,linear_placement1)




dir = math.radians(ifcopenshell.api.cogo.bearing2dd("N 21 12 17.29 W"))
d = ifcopenshell.api.alignment.distance_along_from_station(file,alignment,405.384)
linear_placement2 = file.createIfcLinearPlacement(
    RelativePlacement=file.createIfcAxis2PlacementLinear(
        Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(d),
            OffsetVertical=-23,
            BasisCurve=curve
        ),
        RefDirection=file.createIfcDirection((math.sin(dir),-math.cos(dir),0.))
    )
)


pier2 = bridge.api.get_pier(the_bridge,1)
foundation2 = bridge.api.get_foundation(the_bridge,1)
bridge.api.create_pier(file,
                       pier=pier2, 
                       foundation=foundation2, 
                       cap_length= 12.,
                       cap_width=3.,
                       cap_height=1.5, 
                       nColumns=2,
                       column_height=17.9,
                       column_diameter=2.,
                       column_spacing=7.5, 
                       footing_length=5.0,
                       footing_width=5.0,
                       footing_height=1.5,
                       placement=linear_placement2)


dir = math.radians(ifcopenshell.api.cogo.bearing2dd("N 20 16 25.49 W"))
d = ifcopenshell.api.alignment.distance_along_from_station(file,alignment,444.111)
linear_placement3 = file.createIfcLinearPlacement(
    RelativePlacement=file.createIfcAxis2PlacementLinear(
        Location=file.createIfcPointByDistanceExpression(
            DistanceAlong=file.createIfcLengthMeasure(d),
            OffsetVertical=-5,
            BasisCurve=curve
        ),
        RefDirection=file.createIfcDirection((math.sin(dir),-math.cos(dir),0.))
    )
)


pier3 = bridge.api.get_pier(the_bridge,2)
foundation3 = bridge.api.get_foundation(the_bridge,2)
bridge.api.create_stub_abutment(file,pier3, foundation3, 12.,3.,1.,10.,1.,2.,-0.25,linear_placement3)

#ifcopenshell.file.write(file,"C:\\Users\\rickb\\OneDrive\\Desktop\\PGSuper1_Foundation.ifc")
ifcopenshell.file.write(file,"C:\\Users\\bricer\\OneDrive - Washington State Department of Transportation\Desktop\\PGSuper1_Foundation.ifc")
