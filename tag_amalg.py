from pymoab import core, types
import numpy

#Start new MOAB instance
mb = core.Core()

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
   voxelCoords = numpy.floor( (centroidCoords - minCoord) * resolution/(maxCoord - minCoord))
   return voxelCoords

#Test Values; should approximately double the centroidCoords
MIN_COORD = 0
MAX_COORD = 500
RESOLUTION = 1000

placeholder_id = 0. #TODO: Develop scheme to convert voxel_id to single scalar
for tet in all_tets:
   #First get centroid of each tet
   tet_vertices = mb.get_adjacencies(tet,0)
   centroid = numpy.array([0.0, 0.0, 0.0])
   for vertex in tet_vertices:
      coords = mb.get_coords([vertex])
      centroid += coords
   centroid = centroid/len(tet_vertices)
   #Tag each tet based on the amalg region of the voxel of its centroid
   voxel_id = find_voxel(centroid, MIN_COORD, MAX_COORD, RESOLUTION)
   mb.tag_set_data(amalg_tag,tet,placeholder_id)
   placeholder_id += 1.

#TODO: Set up means of defining amalg_tags related to voxel location
