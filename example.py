import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate

from StdReinfShapeBuilder.RotationAngles import RotationAngles
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from HandleService import HandleService


def check_allplan_version(build_ele, version):
    del build_ele
    del version

    return True


def create_element(build_ele, doc):
    element = CreateBridgeBeam(doc)
    return element.create(build_ele)


def move_handle(
    build_ele,
    handle_prop,
    input_pnt,
    doc,
):

    build_ele.change_property(handle_prop, input_pnt)

    if handle_prop.handle_id == 'beam_height':
        build_ele.edge_height.value = build_ele.beam_height.value \
            - build_ele.top_shelf_height.value \
            - build_ele.bottom_shelf_low_height.value \
            - build_ele.bottom_shelf_up_height.value
        if build_ele.hole_height.value > build_ele.beam_height.value \
                - build_ele.top_shelf_height.value - 45.5:
            build_ele.hole_height.value = build_ele.beam_height.value \
                - build_ele.top_shelf_height.value - 45.5
    elif handle_prop.handle_id == 'top_shelf_width' or handle_prop.handle_id \
            == 'bottom_shelf_width' or handle_prop.handle_id == 'edge_thickness':
        temp = min(build_ele.top_shelf_width.value,
                   build_ele.bottom_shelf_width.value)
        if build_ele.edge_thickness.value >= temp - 100.:
            build_ele.edge_thickness.value = temp - 100.
        if build_ele.edge_thickness.value <= build_ele.var_edge_thickness.value:
            build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
                - 20.
        elif build_ele.edge_thickness.value - 100. \
                >= build_ele.var_edge_thickness.value:
            build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
                - 100.


    return create_element(build_ele, doc)


def modify_beam_height_property(build_ele, name, value):
    change = value - build_ele.top_shelf_height.value \
        - build_ele.edge_height.value - build_ele.bottom_shelf_up_height.value \
        - build_ele.bottom_shelf_low_height.value
    if change < 0:
        change = abs(change)
        if build_ele.top_shelf_height.value > 320.:
            if build_ele.top_shelf_height.value - change < 320.:
                change -= build_ele.top_shelf_height.value - 320.
                build_ele.top_shelf_height.value = 320.
            else:
                build_ele.top_shelf_height.value -= change
                change = 0.
        if change != 0 and build_ele.bottom_shelf_up_height.value > 160.:
            if build_ele.bottom_shelf_up_height.value - change < 160.:
                change -= build_ele.bottom_shelf_up_height.value - 160.
                build_ele.bottom_shelf_up_height.value = 160.
            else:
                build_ele.bottom_shelf_up_height.value -= change
                change = 0.
        if change != 0 and build_ele.bottom_shelf_low_height.value > 153.:
            if build_ele.bottom_shelf_low_height.value - change < 153.:
                change -= build_ele.bottom_shelf_low_height.value - 153.
                build_ele.bottom_shelf_low_height.value = 153.
            else:
                build_ele.bottom_shelf_low_height.value -= change
                change = 0.
        if change != 0 and build_ele.edge_height.value > 467.:
            if build_ele.edge_height.value - change < 467.:
                change -= build_ele.edge_height.value - 467.
                build_ele.edge_height.value = 467.
            else:
                build_ele.edge_height.value -= change
                change = 0.
    else:
        build_ele.edge_height.value += change
    if value - build_ele.top_shelf_height.value - 45.5 \
            < build_ele.hole_height.value:
        build_ele.hole_height.value = value \
            - build_ele.top_shelf_height.value - 45.5


def modify_top_shelf_height(build_ele, name, value):
    build_ele.beam_height.value = value + build_ele.edge_height.value \
        + build_ele.bottom_shelf_up_height.value \
        + build_ele.bottom_shelf_low_height.value


def modify_bottom_shelf_up_height(build_ele, name, value):
    build_ele.beam_height.value = value \
        + build_ele.top_shelf_height.value + build_ele.edge_height.value \
        + build_ele.bottom_shelf_low_height.value
    temp = value + build_ele.bottom_shelf_low_height.value + 45.5
    if temp > build_ele.hole_height.value:
        build_ele.hole_height.value = temp


def modify_bottom_shelf_low_height(build_ele, name, value):
    build_ele.beam_height.value = value \
        + build_ele.top_shelf_height.value + build_ele.edge_height.value \
        + build_ele.bottom_shelf_up_height.value
    temp = build_ele.bottom_shelf_up_height.value + value + 45.5
    if temp > build_ele.hole_height.value:
        build_ele.hole_height.value = temp


def modify_hole_height(build_ele, name, value):
    temp = build_ele.beam_height.value - build_ele.top_shelf_height.value \
        - 45.5
    temp1 = build_ele.bottom_shelf_low_height.value \
        + build_ele.bottom_shelf_up_height.value + 45.5
    if value > temp:
        build_ele.hole_height.value = temp
    elif value < temp1:
        build_ele.hole_height.value = temp1


def modify_hole_depth(build_ele, name, value):
    build_ele.hole_depth.value = build_ele.beam_length.value / 2. - 45.5


def modify_edge_height(build_ele, name, value):
    build_ele.beam_height.value = value \
        + build_ele.top_shelf_height.value \
        + build_ele.bottom_shelf_up_height.value \
        + build_ele.bottom_shelf_low_height.value


def modify_varying_edge_thickness(build_ele, name, value):
    if value >= build_ele.edge_thickness.value:
        build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
            - 20.
    elif value <= build_ele.edge_thickness.value - 100.:
        build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
            - 100.


def modify_varying_length(build_ele, name, value):
    temp = build_ele.beam_length.value / 2. \
        - build_ele.var_start.value
    if value >= temp:
        build_ele.var_length.value = temp - 100.


def modify_varying_start(build_ele, name, value):
    temp = build_ele.beam_length.value / 2.
    if value >= temp:
        build_ele.var_start.value = temp - 200.
    temp -= build_ele.var_start.value
    if build_ele.var_length.value >= temp:
        build_ele.var_length.value = temp - 100.


def modify_element_property(build_ele, name, value):
    if name == 'beam_height':
        modify_beam_height_property(build_ele, name, value)
    elif name == 'top_shelf_height':
        modify_top_shelf_height(build_ele, name, value)
    elif name == 'edge_height':
        modify_edge_height(build_ele, name, value)
    elif name == 'bottom_shelf_up_height':
        modify_bottom_shelf_up_height(build_ele, name, value)
    elif name == 'bottom_shelf_low_height':
        modify_bottom_shelf_low_height(build_ele, name, value)
    elif name == 'hole_height':
        modify_hole_height(build_ele, name, value)
    elif name == 'hole_depth' and value >= build_ele.beam_length.value / 2.:
        modify_hole_depth(build_ele, name, value)
    elif name == 'top_shelf_width' or name == 'bottom_shelf_width' or name \
            == 'edge_thickness':
        temp = min(build_ele.top_shelf_width.value,
                   build_ele.bottom_shelf_width.value)
        if build_ele.edge_thickness.value >= temp - 100.:
            build_ele.edge_thickness.value = temp - 100.
        if value <= build_ele.var_edge_thickness.value:
            build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
                - 20.
        elif value - 100. >= build_ele.var_edge_thickness.value:
            build_ele.var_edge_thickness.value = build_ele.edge_thickness.value \
                - 100.
    elif name == 'var_start':
        modify_varying_start(build_ele, name, value)
    elif name == 'var_length':
        modify_varying_length(build_ele, name, value)
    elif name == 'var_edge_thickness':
        modify_varying_edge_thickness(build_ele, name, value)

    return True


class CreateBridgeBeam:

    def __init__(self, doc):

        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):

        self._top_sh_width = build_ele.top_shelf_width.value
        self._top_sh_height = build_ele.top_shelf_height.value

        self._bot_sh_width = build_ele.bottom_shelf_width.value
        self._bot_sh_up_height = build_ele.bottom_shelf_up_height.value
        self._bot_sh_low_height = build_ele.bottom_shelf_low_height.value
        self._bot_sh_height = self._bot_sh_up_height \
            + self._bot_sh_low_height

        self._rib_thickness = build_ele.edge_thickness.value
        self._rib_height = build_ele.edge_height.value

        self._varying_start = build_ele.var_start.value
        self._varying_length = build_ele.var_length.value
        self._varying_end = self._varying_start + self._varying_length
        self._varying_rib_thickness = build_ele.var_edge_thickness.value

        self._beam_length = build_ele.beam_length.value
        self._beam_width = max(self._top_sh_width, self._bot_sh_width)
        self._beam_height = build_ele.beam_height.value

        self._hole_depth = build_ele.hole_depth.value
        self._hole_height = build_ele.hole_height.value

        self._angleX = build_ele.rotation_angle_x.value
        self._angleY = build_ele.rotation_angle_y.value
        self._angleZ = build_ele.rotation_angle_z.value

        self.create_beam(build_ele)
        self.create_handles(build_ele)

        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(),
                                             self._angleX, self._angleY, self._angleZ,
                                             self.model_ele_list)

        rot_angles = RotationAngles(self._angleX, self._angleY,
                                    self._angleZ)
        HandleService.transform_handles(self.handle_list,
                                        rot_angles.get_rotation_matrix())

        return (self.model_ele_list, self.handle_list)

    def create_beam(self, build_ele):
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Stroke = 1

        breps = AllplanGeo.BRep3DList()


        bottom_shelf = \
            AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self._beam_width
                                                                                          - self._bot_sh_width) / 2., 0., 0.),
                                                                      AllplanGeo.Vector3D(1, 0, 0), AllplanGeo.Vector3D(0, 0,
                                                                                                                        1)), self._bot_sh_width / 2., self._beam_length / 2.,
                                           self._bot_sh_height)

        edges = AllplanUtil.VecSizeTList()
        edges.append(10)
        (err, bottom_shelf) = \
            AllplanGeo.ChamferCalculus.Calculate(bottom_shelf, edges,
                                                 20., False)
        if not GeometryValidate.polyhedron(err):
            return
        breps.append(bottom_shelf)

        top_shelf = \
            AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self._beam_width
                                                                                          - self._top_sh_width) / 2., 0., self._beam_height
                                                                                         - self._top_sh_height), AllplanGeo.Vector3D(1, 0, 0),
                                                                      AllplanGeo.Vector3D(0, 0, 1)), self._top_sh_width / 2.,
                                           self._beam_length / 2., self._top_sh_height)

        top_shelf_notch = \
            AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self._beam_width
                                                                                          - self._top_sh_width) / 2., 0., self._beam_height
                                                                                         - 45.), AllplanGeo.Vector3D(1, 0, 0),
                                                                      AllplanGeo.Vector3D(0, 0, 1)), 60., self._beam_length
                                           / 2., 45.)
        (err, top_shelf) = AllplanGeo.MakeSubtraction(top_shelf,
                                                      top_shelf_notch)
        if not GeometryValidate.polyhedron(err):
            return
        breps.append(top_shelf)


        rib = \
            AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0.,
                                                                                         0., self._bot_sh_height), AllplanGeo.Vector3D(1, 0, 0),
                                                                      AllplanGeo.Vector3D(0, 0, 1)), self._beam_width / 2.,
                                           self._beam_length / 2., self._rib_height)
        breps.append(rib)

        (err, beam) = AllplanGeo.MakeUnion(breps)
        if not GeometryValidate.polyhedron(err):
            return

        breps = AllplanGeo.BRep3DList()
        notch_pol = AllplanGeo.Polyline3D()
        start_point = AllplanGeo.Point3D((self._beam_width
                                          - self._rib_thickness) / 2., 0., self._beam_height
                                         - self._top_sh_height)
        notch_pol += start_point
        notch_pol += AllplanGeo.Point3D((self._beam_width
                                         - self._rib_thickness) / 2., 0., self._bot_sh_height)
        notch_pol += AllplanGeo.Point3D((self._beam_width
                                         - self._bot_sh_width) / 2., 0., self._bot_sh_low_height)
        notch_pol += AllplanGeo.Point3D(-10., 0.,
                                        self._bot_sh_low_height)
        notch_pol += AllplanGeo.Point3D(-10., 0., self._beam_height
                                        - 100.)
        notch_pol += AllplanGeo.Point3D((self._beam_width
                                         - self._top_sh_width) / 2., 0., self._beam_height
                                        - 100.)
        notch_pol += start_point
        if not GeometryValidate.is_valid(notch_pol):
            return

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += (AllplanGeo.Point3D(0, self._varying_start,
                 0) if build_ele.check_box.value else AllplanGeo.Point3D(0,
                 self._beam_length / 2., 0))

        (err, notch) = AllplanGeo.CreateSweptBRep3D(notch_pol, path,
                                                    False, None)
        if not GeometryValidate.polyhedron(err):
            return
        edges = AllplanUtil.VecSizeTList()
        edges.append(3)
        edges.append(1)
        (err, notch) = AllplanGeo.FilletCalculus3D.Calculate(notch,
                                                             edges, 100., False)
        if not GeometryValidate.polyhedron(err):
            return
        breps.append(notch)


        if build_ele.check_box.value:
            profiles = []
            profiles.append(AllplanGeo.Move(notch_pol,
                            AllplanGeo.Vector3D(0, self._varying_start,
                                                0)))

            lines = []
            lines.append(AllplanGeo.Line3D(notch_pol.GetPoint(0),
                         notch_pol.GetPoint(5)))
            lines.append(AllplanGeo.Line3D(notch_pol.GetPoint(1),
                         notch_pol.GetPoint(2)))
            lines.append(AllplanGeo.Move(AllplanGeo.Line3D(notch_pol.GetPoint(0),
                         notch_pol.GetPoint(1)),
                AllplanGeo.Vector3D((self._rib_thickness
                                     - self._varying_rib_thickness) / 2., 0, 0)))
            intersections = [None, None]
            (b, intersections[0]) = \
                AllplanGeo.IntersectionCalculusEx(lines[0], lines[2])
            (b, intersections[1]) = \
                AllplanGeo.IntersectionCalculusEx(lines[1], lines[2])

            notch_pol = AllplanGeo.Polyline3D()
            start_point = AllplanGeo.Point3D((self._beam_width
                                              - self._varying_rib_thickness) / 2.,
                                             self._varying_end, intersections[0].Z)
            notch_pol += start_point
            notch_pol += AllplanGeo.Point3D((self._beam_width
                                             - self._varying_rib_thickness) / 2.,
                                            self._varying_end, intersections[1].Z)
            notch_pol += AllplanGeo.Point3D((self._beam_width
                                             - self._bot_sh_width) / 2., self._varying_end,
                                            self._bot_sh_low_height)
            notch_pol += AllplanGeo.Point3D(-10., self._varying_end,
                                            self._bot_sh_low_height)
            notch_pol += AllplanGeo.Point3D(-10., self._varying_end,
                                            self._beam_height - 100.)
            notch_pol += AllplanGeo.Point3D((self._beam_width
                                             - self._top_sh_width) / 2., self._varying_end,
                                            self._beam_height - 100.)
            notch_pol += start_point
            if not GeometryValidate.is_valid(notch_pol):
                return

            path = AllplanGeo.Polyline3D()
            path += AllplanGeo.Point3D(0, self._varying_end, 0)
            path += AllplanGeo.Point3D(0, self._beam_length / 2., 0)

            (err, notch) = AllplanGeo.CreateSweptBRep3D(notch_pol,
                                                        path, False, None)
            if not GeometryValidate.polyhedron(err):
                return
            (err, notch) = AllplanGeo.FilletCalculus3D.Calculate(notch,
                                                                 edges, 100., False)
            if not GeometryValidate.polyhedron(err):
                return
            breps.append(notch)

            profiles.append(notch_pol)
            path = AllplanGeo.Line3D(profiles[0].GetStartPoint(),
                                     profiles[1].GetStartPoint())

            (err, notch) = AllplanGeo.CreateRailSweptBRep3D(profiles,
                                                            [path], True, False, False)

            edges = AllplanUtil.VecSizeTList()
            edges.append(11)
            edges.append(9)
            (err, notch) = AllplanGeo.FilletCalculus3D.Calculate(notch,
                                                                 edges, 100., False)
            if not GeometryValidate.polyhedron(err):
                return
            breps.append(notch)


        sling_hole = \
            AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0,
                                                                                           build_ele.hole_depth.value, build_ele.hole_height.value),
                                                                        AllplanGeo.Vector3D(0, 0, 1), AllplanGeo.Vector3D(1, 0,
                                                                                                                          0)), 45.5, self._beam_width)
        breps.append(sling_hole)

        (err, beam) = AllplanGeo.MakeSubtraction(beam, breps)
        if not GeometryValidate.polyhedron(err):
            return


        plane = AllplanGeo.Plane3D(AllplanGeo.Point3D(self._beam_width
                                   / 2., 0, 0), AllplanGeo.Vector3D(1,
                                   0, 0))
        (err, beam) = AllplanGeo.MakeUnion(beam,
                                           AllplanGeo.Mirror(beam, plane))
        if not GeometryValidate.polyhedron(err):
            return
        plane.Set(AllplanGeo.Point3D(0, self._beam_length / 2., 0),
                  AllplanGeo.Vector3D(0, 1, 0))
        (err, beam) = AllplanGeo.MakeUnion(beam,
                                           AllplanGeo.Mirror(beam, plane))
        if not GeometryValidate.polyhedron(err):
            return
        self.model_ele_list.append(AllplanBasisElements.ModelElement3D(com_prop,
                                   beam))

    def create_handles(self, build_ele):
        top_shelf_width_handle = HandleProperties(
            'top_shelf_width_handle',
            AllplanGeo.Point3D((self._beam_width - self._top_sh_width)
                               / 2. + self._top_sh_width, 0.,
                               self._beam_height - 45.),
            AllplanGeo.Point3D((self._beam_width - self._top_sh_width)
                               / 2., 0, self._beam_height - 45.),
            [('top_shelf_width', HandleDirection.point_dir)],
            HandleDirection.point_dir,
            True,
        )
        self.handle_list.append(top_shelf_width_handle)

        bottom_shelf_width_handle = HandleProperties(
            'bottom_shelf_width_handle',
            AllplanGeo.Point3D((self._beam_width - self._bot_sh_width)
                               / 2. + self._bot_sh_width, 0.,
                               self._bot_sh_low_height),
            AllplanGeo.Point3D((self._beam_width - self._bot_sh_width)
                               / 2., 0, self._bot_sh_low_height),
            [('bottom_shelf_width', HandleDirection.point_dir)],
            HandleDirection.point_dir,
            True,
        )
        self.handle_list.append(bottom_shelf_width_handle)

        edge_thickness_handle = HandleProperties(
            'edge_thickness_handle',
            AllplanGeo.Point3D((self._beam_width - self._rib_thickness)
                               / 2. + self._rib_thickness, 0.,
                               self._beam_height / 2.),
            AllplanGeo.Point3D((self._beam_width - self._rib_thickness)
                               / 2., 0, self._beam_height / 2.),
            [('edge_thickness', HandleDirection.point_dir)],
            HandleDirection.point_dir,
            True,
        )
        self.handle_list.append(edge_thickness_handle)