coordinates = [
    (0, 'pelvis_tx'),
    (1, 'pelvis_ty'),
    (2, 'pelvis_tz'),
    (3, 'pelvis_rx'),
    (4, 'pelvis_ry'),
    (5, 'pelvis_rz'),
    (6, 'rhip_x'),
    (7, 'rhip_y'),
    (8, 'rhip_z'),
    (9, 'rknee'),
    (10, 'rankle'),
    (11, 'rsubtalar'),
    (12, 'rmtp'),
    (13, 'lhip_x'),
    (14, 'lhip_y'),
    (15, 'lhip_z'),
    (16, 'lknee'),
    (17, 'lankle'),
    (18, 'lsubtalar'),
    (19, 'lmtp'),
    (20, 'back_flexion'),
    (21, 'back_y'),
    (22, 'back_z'),
    (23, 'neck_flexion'),
    (24, 'neck_y'),
    (25, 'neck_z'),
    (26, 'rshoulder_x'),
    (27, 'rshoulder_y'),
    (28, 'rshoulder_z'),
    (29, 'relbow'),
    (30, 'rpro_sup'),
    (31, 'rwrist_flexion'),
    (32, 'rwrist_deviation'),
    (33, 'rfingers_flexion'),
    (34, 'lshoulder_x'),
    (35, 'lshoulder_y'),
    (36, 'lshoulder_z'),
    (37, 'lelbow'),
    (38, 'lpro_sup'),
    (39, 'lwrist_flexion'),
    (40, 'lwrist_deviation'),
    (41, 'lfingers_flexion'),
]
def coordinateName(idx):
    return coordinates[idx][1]

def coordinateIndex(name):
    l = [[s for s in row if s is name] for row in coordinates]
    return l.index([name])





# joints: can be extracted as:
# matrix=robots[2].visuals
# dof=[[row[i] for row in matrix] for i in range(1,2)]
# [ key for key,_ in groupby(dof[0])]
# dofl=list(enumerate(dof2))

joints = [ 
    (0, 'ground'),
    (1, 'ground_pelvis'),
    (2, 'hip_r'),
    (3, 'knee_r'),
    (4, 'ankle_r'),
    (5, 'subtalar_r'),
    (6, 'mtp_r'),
    (7, 'hip_l'),
    (8, 'knee_l'),
    (9, 'ankle_l'),
    (10, 'subtalar_l'),
    (11, 'mtp_l'),
    (12, 'back'),
    (13, 'neck'),
    (14, 'acromial_r'),
    (15, 'elbow_r'),
    (16, 'radioulnar_r'),
    (17, 'radius_lunate_r'),
    (18, 'lunate_hand_r'),
    (19, 'fingers_r'),
    (20, 'acromial_l'),
    (21, 'elbow_l'),
    (22, 'radioulnar_l'),
    (23, 'radius_lunate_l'),
    (24, 'lunate_hand_l'),
    (25, 'fingers_l')
]


def jointName(idx):
    return joints[idx][1]

def jointIndex(name):
    l = [[s for s in row if s is name] for row in joints]
    return l.index([name])
