import math
import glob
import csv
import numpy as np

import bpy

def particleSetter(self):
    particle_systems = object.evaluated_get(degp).particle_systems
    particles = particle_systems[0].particles
    totalParticles = len(particles)

    scene = bpy.context.scene
    cFrame = scene.frame_current
    sFrame = scene.frame_start

    # at start-frame, clear the particle cache
    if cFrame == sFrame:
            psSeed = object.particle_systems[0].seed
            object.particle_systems[0].seed = psSeed

    # Define the local copy of your text data file
       # Note that Windows will still use forward slashes like
       #    Mac and Linux.
    filepath = '/<path>/<to>/<your-file>/edd.txt'
    fields = ['name', 'dist', 'x', 'y', 'z']
    reader = csv.DictReader(open(filepath), fields, delimiter=' ')

    cataloglist = []

    for row in reader:
            cataloglist.append([float(row['x']), float(row['y']), float(row['z'])])
    
    catalog = np.array(cataloglist)
    
    #  However you choose to read in your data, 
    #    it should end up being a numpy array
    #    and be put into a flattened list.
    flatList = catalog.ravel()

    # Set the location of all particle locations to flatList
    particles.foreach_set("location", flatList)
    
# Prepare particle system
object = bpy.data.objects["Cube"]
object.modifiers.new("ParticleSystem", 'PARTICLE_SYSTEM')
# This is the number of catalog elements in your data file.
object.particle_systems[0].settings.count = 3529
object.particle_systems[0].settings.frame_start = 1
object.particle_systems[0].settings.frame_end = 1
# We don't want our catalog to disappear, so set it to some arbitrary large value
#  that exceeds your number of anticipated rendered frames.
object.particle_systems[0].settings.lifetime = 10000
object.show_instancer_for_viewport = False
degp = bpy.context.evaluated_depsgraph_get()

#clear the post frame handler
bpy.app.handlers.frame_change_post.clear()

#run the function on each frame
bpy.app.handlers.frame_change_post.append(particleSetter)

# Update to a frame where particles are updated
bpy.context.scene.frame_current = 2