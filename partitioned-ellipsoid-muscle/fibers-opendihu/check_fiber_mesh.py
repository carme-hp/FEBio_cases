import json
import vtk
import sys


def json_to_vtp(json_file, vtp_file):

    # Load JSON
    with open(json_file) as f:
        data = json.load(f)

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    point_counter = 0

    for fiber_name, fiber_points in data.items():

        if len(fiber_points) < 2:
            continue

        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(len(fiber_points))

        for i, p in enumerate(fiber_points):

            x = float(p["x"])
            y = float(p["y"])
            z = float(p["z"])

            points.InsertNextPoint(x, y, z)
            polyline.GetPointIds().SetId(i, point_counter)

            point_counter += 1

        lines.InsertNextCell(polyline)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

    # Write VTP (ASCII mode avoids XML corruption issues)
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(vtp_file)
    writer.SetInputData(polydata)
    writer.SetDataModeToAscii()
    writer.Write()

    print("Points written:", points.GetNumberOfPoints())
    print("Fibers written:", lines.GetNumberOfCells())
    print("Saved:", vtp_file)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        json_file = input("Enter JSON filename: ")
    else:
        json_file = sys.argv[1]

    vtp_file = json_file.rsplit(".", 1)[0] + ".vtp"

    json_to_vtp(json_file, vtp_file)