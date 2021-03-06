import numpy as np

#__ PATHS 
motion='Precision Landing'
generic_model =  '/galo/devel/gepetto/Models/data/whole_body/wholebody.osim'
mesh_path = '/galo/devel/gepetto/Models/data/whole_body/stl_osim/'
models_path='/galo/devel/gepetto/parkour/models'

model_names = ['Cyril.osim', 'JulienB', 'Lucas.osim','Melvin.osim','Michael.osim','Remi.osim','Yoan.osim']
heights = [1.60, 1.704, 1.69, 1.78, 1.75, 1.704, 1.71]

#__ DEFAULT POSES
half_sitting = np.matrix([0.,0.,0.92,0.,0.,0.,0.,                                                       # Free flyer 0-6
                          0.09980222, -0.02487251, -0.00249558, 0.99469324, -0.4, 0.25, 0., -0.05,      # Rleg 7-14
                          0.09980222,  0.02487251,  0.00249558, 0.99469324, -0.4, 0.25, 0., -0.05,      # Lleg 15-22
                          -0.09983342, 0., 0., 0.99500417, 0.09983342, 0., 0., 0.99500417,              # Pelvis Head 23-30 
                          -0.09942936, -0.08942953,  0.00897288, 0.99097712, 0.7, 1., -0.02, 0.15, 0.,  # Rarm 31-39
                          -0.09942936,  0.08942953, -0.00897288, 0.99097712, 0.7, 1.,  0.02, 0.15, 0.]).T # Larm 40-48
zero_pose = np.asmatrix(np.zeros(np.shape(half_sitting)))

# Viewer
ENABLE_VIEWER = "ON"
SHOW_VIEWER_FLOOR = "ON"
