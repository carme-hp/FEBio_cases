import vtk

reader = vtk.vtkStructuredGridReader()
reader.SetFileName("3D_mesh_2x2x8.vtk")
reader.Update()

sg = reader.GetOutput()

append = vtk.vtkAppendFilter()
append.AddInputData(sg)
append.Update()

writer = vtk.vtkUnstructuredGridWriter()
writer.SetFileName("3D_mesh_u2x2x8.vtk")
writer.SetInputData(append.GetOutput())
writer.Write()