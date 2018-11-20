from pymoab import core, types

#Start new MOAB instance
mb = core.Core()

mb.load_file("Insert_Filename")

#Create new tag type and assemble the tetrahedrons
amalg_tag = mb.tag_create("AMALG_TAG")
file_set = mb.get_root_set()
all_tets = mb.get_entities_by_type(file_set, types.MBTET)


for tet in all_tets:
   #First get centroid of each tet
   tet_vertices = mb.get_adjacencies(tet,0)
   centroid = np.array([0,0,0])
   for vertex in tet_vertices:
      coords = mb.get_coords(vertex)
      centroid += coords
    centroid = centroid/len(tet_vertices)

    #Tag each tet based on the amalg region of the voxel of its centroid
    voxel_id = find_voxel(centroid)
    mb.tag_set_data(amalg_tag,tet,voxel_id)

#TODO: Set up means of defining amalg_tags related to voxel location
