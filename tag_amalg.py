from pymoab import core, types
import numpy

#Start new MOAB instance
mb = core.Core()

#TODO: Add means of modifying this dynamically
mb.load_file("/home/samuel/cnerg/pymoabScripts/test01.h5m")

#Create new tag type and assemble the tetrahedrons
name = "AMALG_TAG"
size = 1
storage_type = types.MB_TYPE_DOUBLE
tag_type = types.MB_TAG_SPARSE
amalg_tag = mb.tag_get_handle(name, size, storage_type, tag_type, create_if_missing=True)

root_set = mb.get_root_set()
all_tets = mb.get_entities_by_type(mb.get_root_set(), types.MBTET)

#Returns the nearest int coords to those given, normalized to the voxel count
def find_voxel(centroidCoords, minCoord, maxCoord, resolution):
   #voxelCoords = numpy.floor( (centroidCoords - minCoord) * resolution/(maxCoord - minCoord))
   voxelCoords = numpy.array([0.0, 0.0, 0.0])
   for ele in range(0, len(voxelCoords)):
      normalize = resolution/(maxCoord[ele] - minCoord[ele])
      voxelCoords[ele] = numpy.floor( (centroidCoords[ele] - minCoord[ele]) * normalize)
   return voxelCoords

#TODO: Add means of modifying these dynamically
MIN_COORD = numpy.array([-500.0, -500.0, -500.0])
MAX_COORD = numpy.array([500., 500., 500.])
RESOLUTION = 1000.

for tet in all_tets:
   #First get centroid of each tet
   tet_vertices = mb.get_adjacencies(tet,0)
   centroid = numpy.array([0.0, 0.0, 0.0])
   for vertex in tet_vertices:
      coords = mb.get_coords([vertex])
      centroid += coords
   centroid = centroid/len(tet_vertices)
   
   #Tag each tet based on the amalg region of the voxel of its centroid, if needed
   tag_tet = True
   for ele in range(0, len(centroid)):
      if(centroid[ele] < MIN_COORD[ele] or centroid[ele] > MAX_COORD[ele]):
         tag_tet = False

   if(tag_tet):
      vox_coords = find_voxel(centroid, MIN_COORD, MAX_COORD, RESOLUTION)
      voxel_id = vox_coords[0] + RESOLUTION*vox_coords[1] + RESOLUTION*RESOLUTION*vox_coords[2]
      mb.tag_set_data(amalg_tag,tet,voxel_id)

