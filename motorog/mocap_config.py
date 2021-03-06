traceurs_list = ['Cyril','JulienB','Lucas','Melvin','Michael','Remi','Yoan']
#traceurs_list = ['Cyril','Lucas','Melvin','Michael','Yoan']
phases = ['prepare','jump','fly','land']
digital_frequency = 400.
analog_frequency = 2000.
time_step = 1/400.
name = 'Precision Landing'

class MotionNames:
    def __init__(self):
        self.motions = {'trial_names':[], 'jump_names':[], 'fly_names':[], 'land_names':[],
                        'jump_grfs':[], 'fly_grfs':[], 'land_grfs':[]}

    def Cyril(self):
        trial_names = [ 'Motion_pl01.mot', 'Motion_pl02.mot', 'Motion_pl03.mot', 'Motion_pl04.mot',
                        'Motion_pl05.mot', 'Motion_pl07.mot', 'Motion_pl08.mot', 'Motion_pl09.mot',
                        'Motion_pl10.mot', 'Motion_pl11.mot']
        jump_names = [ 'Jump_normalized_Motion_pl01.mot', 'Jump_normalized_Motion_pl02.mot',
                       'Jump_normalized_Motion_pl03.mot', 'Jump_normalized_Motion_pl04.mot',
                       'Jump_normalized_Motion_pl05.mot', 'Jump_normalized_Motion_pl07.mot',
                       'Jump_normalized_Motion_pl08.mot', 'Jump_normalized_Motion_pl09.mot',
                       'Jump_normalized_Motion_pl10.mot', 'Jump_normalized_Motion_pl11.mot']
        fly_names = [ 'Fly_normalized_Motion_pl01.mot', 'Fly_normalized_Motion_pl02.mot',
                      'Fly_normalized_Motion_pl03.mot', 'Fly_normalized_Motion_pl04.mot',
                      'Fly_normalized_Motion_pl05.mot', 'Fly_normalized_Motion_pl07.mot',
                      'Fly_normalized_Motion_pl08.mot', 'Fly_normalized_Motion_pl09.mot',
                      'Fly_normalized_Motion_pl10.mot', 'Fly_normalized_Motion_pl11.mot']
        land_names = [ 'Land_normalized_Motion_pl01.mot', 'Land_normalized_Motion_pl02.mot',
                       'Land_normalized_Motion_pl03.mot', 'Land_normalized_Motion_pl04.mot',
                       'Land_normalized_Motion_pl05.mot', 'Land_normalized_Motion_pl07.mot',
                       'Land_normalized_Motion_pl08.mot', 'Land_normalized_Motion_pl09.mot',
                       'Land_normalized_Motion_pl10.mot', 'Land_normalized_Motion_pl11.mot']
        jump_grfs = [ 'Jump_normalized_precision-landing01_filtered_grf.sto', 
                      'Jump_normalized_precision-landing02_filtered_grf.sto',
                      'Jump_normalized_precision-landing03_filtered_grf.sto', 
                      'Jump_normalized_precision-landing04_filtered_grf.sto',
                      'Jump_normalized_precision-landing05_filtered_grf.sto', 
                      'Jump_normalized_precision-landing07_filtered_grf.sto',
                      'Jump_normalized_precision-landing08_filtered_grf.sto', 
                      'Jump_normalized_precision-landing09_filtered_grf.sto',
                      'Jump_normalized_precision-landing10_filtered_grf.sto', 
                      'Jump_normalized_precision-landing11_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_precision-landing01_filtered_grf.sto', 
                      'Land_normalized_precision-landing02_filtered_grf.sto',
                      'Land_normalized_precision-landing03_filtered_grf.sto', 
                      'Land_normalized_precision-landing04_filtered_grf.sto',
                      'Land_normalized_precision-landing05_filtered_grf.sto', 
                      'Land_normalized_precision-landing07_filtered_grf.sto',
                      'Land_normalized_precision-landing08_filtered_grf.sto', 
                      'Land_normalized_precision-landing09_filtered_grf.sto',
                      'Land_normalized_precision-landing10_filtered_grf.sto', 
                      'Land_normalized_precision-landing11_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions



    def JulienB(self):
        trial_names = [ 'Motion_pl02.mot', 'Motion_pl03.mot', 'Motion_pl04.mot', 'Motion_pl06.mot',
                        'Motion_pl07.mot', 'Motion_pl08.mot', 'Motion_pl09.mot', 'Motion_pl12.mot']
        jump_names = [ 'Jump_normalized_Motion_pl02.mot', 'Jump_normalized_Motion_pl03.mot',
                       'Jump_normalized_Motion_pl04.mot', 'Jump_normalized_Motion_pl06.mot',
                       'Jump_normalized_Motion_pl07.mot', 'Jump_normalized_Motion_pl08.mot',
                       'Jump_normalized_Motion_pl09.mot', 'Jump_normalized_Motion_pl12.mot']
        fly_names = [ 'Fly_normalized_Motion_pl02.mot', 'Fly_normalized_Motion_pl03.mot',
                      'Fly_normalized_Motion_pl04.mot', 'Fly_normalized_Motion_pl06.mot',
                      'Fly_normalized_Motion_pl07.mot', 'Fly_normalized_Motion_pl08.mot',
                      'Fly_normalized_Motion_pl09.mot', 'Fly_normalized_Motion_pl12.mot']
        land_names = [ 'Land_normalized_Motion_pl02.mot', 'Land_normalized_Motion_pl03.mot',
                       'Land_normalized_Motion_pl04.mot', 'Land_normalized_Motion_pl06.mot',
                       'Land_normalized_Motion_pl07.mot', 'Land_normalized_Motion_pl08.mot',
                       'Land_normalized_Motion_pl09.mot', 'Land_normalized_Motion_pl12.mot']
        jump_grfs = [ 'Jump_normalized_precision_landing02_filtered_grf.sto', 
                      'Jump_normalized_precision_landing03_filtered_grf.sto',
                      'Jump_normalized_precision_landing04_filtered_grf.sto', 
                      'Jump_normalized_precision_landing06_filtered_grf.sto',
                      'Jump_normalized_precision_landing07_filtered_grf.sto',
                      'Jump_normalized_precision_landing08_filtered_grf.sto',
                      'Jump_normalized_precision_landing09_filtered_grf.sto',
                      'Jump_normalized_precision_landing12_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_precision_landing02_filtered_grf.sto', 
                      'Land_normalized_precision_landing03_filtered_grf.sto',
                      'Land_normalized_precision_landing04_filtered_grf.sto', 
                      'Land_normalized_precision_landing06_filtered_grf.sto',
                      'Land_normalized_precision_landing07_filtered_grf.sto', 
                      'Land_normalized_precision_landing08_filtered_grf.sto',
                      'Land_normalized_precision_landing09_filtered_grf.sto', 
                      'Land_normalized_precision_landing12_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions


    
    def Lucas(self):
        trial_names = [ 'Motion_pl04.mot', 'Motion_pl05.mot', 'Motion_pl12.mot', 'Motion_pl13.mot',
                        'Motion_pl14.mot', 'Motion_pl15.mot', 'Motion_pl16.mot', 'Motion_pl17.mot']
        jump_names = [ 'Jump_normalized_Motion_pl04.mot', 'Jump_normalized_Motion_pl05.mot',
                       'Jump_normalized_Motion_pl12.mot', 'Jump_normalized_Motion_pl13.mot',
                       'Jump_normalized_Motion_pl14.mot', 'Jump_normalized_Motion_pl15.mot',
                       'Jump_normalized_Motion_pl16.mot', 'Jump_normalized_Motion_pl17.mot']
        fly_names = [ 'Fly_normalized_Motion_pl04.mot', 'Fly_normalized_Motion_pl05.mot',
                       'Fly_normalized_Motion_pl12.mot', 'Fly_normalized_Motion_pl13.mot',
                       'Fly_normalized_Motion_pl14.mot', 'Fly_normalized_Motion_pl15.mot',
                       'Fly_normalized_Motion_pl16.mot', 'Fly_normalized_Motion_pl17.mot']
        land_names = [ 'Land_normalized_Motion_pl04.mot', 'Land_normalized_Motion_pl05.mot',
                       'Land_normalized_Motion_pl12.mot', 'Land_normalized_Motion_pl13.mot',
                       'Land_normalized_Motion_pl14.mot', 'Land_normalized_Motion_pl15.mot',
                       'Land_normalized_Motion_pl16.mot', 'Land_normalized_Motion_pl17.mot']
        jump_grfs = [ 'Jump_normalized_Precision Landing04_filtered_grf.sto', 
                      'Jump_normalized_Precision Landing05_filtered_grf.sto',
                      'Jump_normalized_Precision Landing12_filtered_grf.sto', 
                      'Jump_normalized_Precision Landing13_filtered_grf.sto',
                      'Jump_normalized_Precision Landing14_filtered_grf.sto', 
                      'Jump_normalized_Precision Landing15_filtered_grf.sto',
                      'Jump_normalized_Precision Landing16_filtered_grf.sto', 
                      'Jump_normalized_Precision Landing17_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_Precision Landing04_filtered_grf.sto', 
                      'Land_normalized_Precision Landing05_filtered_grf.sto',
                      'Land_normalized_Precision Landing12_filtered_grf.sto', 
                      'Land_normalized_Precision Landing13_filtered_grf.sto',
                      'Land_normalized_Precision Landing14_filtered_grf.sto', 
                      'Land_normalized_Precision Landing15_filtered_grf.sto',
                      'Land_normalized_Precision Landing16_filtered_grf.sto', 
                      'Land_normalized_Precision Landing17_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions





    def Melvin(self):
        trial_names = [ 'Motion_pl02.mot', 'Motion_pl04.mot', 'Motion_pl06.mot', 'Motion_pl07.mot',
                        'Motion_pl08.mot', 'Motion_pl10.mot', 'Motion_pl12.mot', 'Motion_pl13.mot',
                        'Motion_pl14.mot', 'Motion_pl15.mot']
        jump_names = [ 'Jump_normalized_Motion_pl02.mot', 'Jump_normalized_Motion_pl04.mot',
                       'Jump_normalized_Motion_pl06.mot', 'Jump_normalized_Motion_pl07.mot',
                       'Jump_normalized_Motion_pl08.mot', 'Jump_normalized_Motion_pl10.mot',
                       'Jump_normalized_Motion_pl12.mot', 'Jump_normalized_Motion_pl13.mot',
                       'Jump_normalized_Motion_pl14.mot', 'Jump_normalized_Motion_pl15.mot']
        fly_names = [ 'Fly_normalized_Motion_pl02.mot', 'Fly_normalized_Motion_pl04.mot',
                       'Fly_normalized_Motion_pl06.mot', 'Fly_normalized_Motion_pl07.mot',
                       'Fly_normalized_Motion_pl08.mot', 'Fly_normalized_Motion_pl10.mot',
                       'Fly_normalized_Motion_pl12.mot', 'Fly_normalized_Motion_pl13.mot',
                       'Fly_normalized_Motion_pl14.mot', 'Fly_normalized_Motion_pl15.mot']
        land_names = [ 'Land_normalized_Motion_pl02.mot', 'Land_normalized_Motion_pl04.mot',
                       'Land_normalized_Motion_pl06.mot', 'Land_normalized_Motion_pl07.mot',
                       'Land_normalized_Motion_pl08.mot', 'Land_normalized_Motion_pl10.mot',
                       'Land_normalized_Motion_pl12.mot', 'Land_normalized_Motion_pl13.mot',
                       'Land_normalized_Motion_pl14.mot', 'Land_normalized_Motion_pl15.mot']
        jump_grfs = [ 'Jump_normalized_pl02_filtered_grf.sto', 
                      'Jump_normalized_pl04_filtered_grf.sto',
                      'Jump_normalized_pl06_filtered_grf.sto', 
                      'Jump_normalized_pl07_filtered_grf.sto',
                      'Jump_normalized_pl08_filtered_grf.sto', 
                      'Jump_normalized_pl10_filtered_grf.sto',
                      'Jump_normalized_pl12_filtered_grf.sto', 
                      'Jump_normalized_pl13_filtered_grf.sto',
                      'Jump_normalized_pl14_filtered_grf.sto', 
                      'Jump_normalized_pl15_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_pl02_filtered_grf.sto', 
                      'Land_normalized_pl04_filtered_grf.sto',
                      'Land_normalized_pl06_filtered_grf.sto', 
                      'Land_normalized_pl07_filtered_grf.sto',
                      'Land_normalized_pl08_filtered_grf.sto', 
                      'Land_normalized_pl10_filtered_grf.sto',
                      'Land_normalized_pl12_filtered_grf.sto', 
                      'Land_normalized_pl13_filtered_grf.sto',
                      'Land_normalized_pl14_filtered_grf.sto', 
                      'Land_normalized_pl15_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions





    def Michael(self):
        trial_names = [ 'Motion_pl02.mot', 'Motion_pl05.mot', 'Motion_pl06.mot', 'Motion_pl07.mot',
                        'Motion_pl10.mot']
        jump_names = [ 'Jump_normalized_Motion_pl02.mot', 'Jump_normalized_Motion_pl05.mot',
                       'Jump_normalized_Motion_pl06.mot', 'Jump_normalized_Motion_pl07.mot',
                        'Jump_normalized_Motion_pl10.mot']
        fly_names = [ 'Fly_normalized_Motion_pl02.mot', 'Fly_normalized_Motion_pl05.mot',
                       'Fly_normalized_Motion_pl06.mot', 'Fly_normalized_Motion_pl07.mot',
                       'Fly_normalized_Motion_pl10.mot']
        land_names = [ 'Land_normalized_Motion_pl02.mot', 'Land_normalized_Motion_pl05.mot',
                       'Land_normalized_Motion_pl06.mot', 'Land_normalized_Motion_pl07.mot',
                       'Land_normalized_Motion_pl10.mot']
        jump_grfs = [ 'Jump_normalized_pl02_filtered_grf.sto', 
                      'Jump_normalized_pl05_filtered_grf.sto',
                      'Jump_normalized_pl06_filtered_grf.sto', 
                      'Jump_normalized_pl07_filtered_grf.sto',
                       'Jump_normalized_pl10_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_pl02_filtered_grf.sto', 
                      'Land_normalized_pl05_filtered_grf.sto',
                      'Land_normalized_pl06_filtered_grf.sto', 
                      'Land_normalized_pl07_filtered_grf.sto',
                      'Land_normalized_pl10_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions



    def Remi(self):
        trial_names = [ 'Motion_pl03.mot', 'Motion_pl08.mot', 'Motion_pl13.mot', 'Motion_pl14.mot',
                        'Motion_pl15.mot', 'Motion_pl18.mot']
        jump_names = [ 'Jump_normalized_Motion_pl03.mot', 'Jump_normalized_Motion_pl08.mot',
                       'Jump_normalized_Motion_pl13.mot', 'Jump_normalized_Motion_pl14.mot',
                       'Jump_normalized_Motion_pl15.mot', 'Jump_normalized_Motion_pl18.mot']
        fly_names = [ 'Fly_normalized_Motion_pl03.mot', 'Fly_normalized_Motion_pl08.mot',
                      'Fly_normalized_Motion_pl13.mot', 'Fly_normalized_Motion_pl14.mot',
                      'Fly_normalized_Motion_pl15.mot', 'Fly_normalized_Motion_pl18.mot']
        land_names = [ 'Land_normalized_Motion_pl03.mot', 'Land_normalized_Motion_pl08.mot',
                       'Land_normalized_Motion_pl13.mot', 'Land_normalized_Motion_pl14.mot',
                       'Land_normalized_Motion_pl15.mot', 'Land_normalized_Motion_pl18.mot']
        jump_grfs = [ 'Jump_normalized_precision_landing03_filtered_grf.sto', 
                      'Jump_normalized_precision_landing08_filtered_grf.sto',
                      'Jump_normalized_precision_landing13_filtered_grf.sto', 
                      'Jump_normalized_precision_landing14_filtered_grf.sto',
                      'Jump_normalized_precision_landing15_filtered_grf.sto',
                      'Jump_normalized_precision_landing18_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_precision_landing03_filtered_grf.sto', 
                      'Land_normalized_precision_landing08_filtered_grf.sto',
                      'Land_normalized_precision_landing13_filtered_grf.sto', 
                      'Land_normalized_precision_landing14_filtered_grf.sto',
                      'Land_normalized_precision_landing15_filtered_grf.sto', 
                      'Land_normalized_precision_landing18_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions



    def Yoan(self):
        trial_names = [ 'Motion_pl01.mot', 'Motion_pl02.mot', 'Motion_pl03.mot', 'Motion_pl05.mot',
                        'Motion_pl06.mot', 'Motion_pl07.mot', 'Motion_pl08.mot', 'Motion_pl09.mot',
                        'Motion_pl11.mot']
        jump_names = [ 'Jump_normalized_Motion_pl01.mot', 'Jump_normalized_Motion_pl02.mot',
                       'Jump_normalized_Motion_pl03.mot', 'Jump_normalized_Motion_pl05.mot',
                       'Jump_normalized_Motion_pl06.mot', 'Jump_normalized_Motion_pl07.mot',
                       'Jump_normalized_Motion_pl08.mot', 'Jump_normalized_Motion_pl09.mot',
                       'Jump_normalized_Motion_pl11.mot']
        fly_names = [ 'Fly_normalized_Motion_pl01.mot', 'Fly_normalized_Motion_pl02.mot',
                       'Fly_normalized_Motion_pl03.mot', 'Fly_normalized_Motion_pl05.mot',
                       'Fly_normalized_Motion_pl06.mot', 'Fly_normalized_Motion_pl07.mot',
                       'Fly_normalized_Motion_pl08.mot', 'Fly_normalized_Motion_pl09.mot',
                       'Fly_normalized_Motion_pl11.mot']
        land_names = [ 'Land_normalized_Motion_pl01.mot', 'Land_normalized_Motion_pl02.mot',
                       'Land_normalized_Motion_pl03.mot', 'Land_normalized_Motion_pl05.mot',
                       'Land_normalized_Motion_pl06.mot', 'Land_normalized_Motion_pl07.mot',
                       'Land_normalized_Motion_pl08.mot', 'Land_normalized_Motion_pl09.mot',
                       'Land_normalized_Motion_pl11.mot']
        jump_grfs = [ 'Jump_normalized_precision_landing01_filtered_grf.sto', 
                      'Jump_normalized_precision_landing02_filtered_grf.sto',
                      'Jump_normalized_precision_landing03_filtered_grf.sto', 
                      'Jump_normalized_precision_landing05_filtered_grf.sto',
                      'Jump_normalized_precision_landing06_filtered_grf.sto', 
                      'Jump_normalized_precision_landing07_filtered_grf.sto',
                      'Jump_normalized_precision_landing08_filtered_grf.sto', 
                      'Jump_normalized_precision_landing09_filtered_grf.sto',
                      'Jump_normalized_precision_landing11_filtered_grf.sto']
        land_grfs = [ 'Land_normalized_precision_landing01_filtered_grf.sto', 
                      'Land_normalized_precision_landing02_filtered_grf.sto',
                      'Land_normalized_precision_landing03_filtered_grf.sto', 
                      'Land_normalized_precision_landing05_filtered_grf.sto',
                      'Land_normalized_precision_landing06_filtered_grf.sto', 
                      'Land_normalized_precision_landing07_filtered_grf.sto',
                      'Land_normalized_precision_landing08_filtered_grf.sto', 
                      'Land_normalized_precision_landing09_filtered_grf.sto',
                      'Land_normalized_precision_landing11_filtered_grf.sto']
        self.motions['trial_names'].append(trial_names)
        self.motions['jump_names'].append(jump_names)
        self.motions['fly_names'].append(fly_names)
        self.motions['land_names'].append(land_names)
        self.motions['jump_grfs'].append(jump_grfs)
        self.motions['land_grfs'].append(land_grfs)
        return self.motions
