
from expyriment import design, control, stimuli, io, misc
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

SHAPE_TASK_RECTANGLE = misc.constants.K_RIGHT
SHAPE_TASK_DIAMOND = misc.constants.K_LEFT
FILLING_TASK_TWODOTS = misc.constants.K_RIGHT
FILLING_TASK_THREEDOTS =misc.constants.K_LEFT

exp = design.Experiment(name = "Stoet's Multi-tasking experiment",
                        background_colour = WHITE, 
                        foreground_colour = BLACK)
control.initialize(exp)

#fixation_cross = stimuli.FixCross()
#fixation_cross.preload()
blankscreen = stimuli.BlankScreen(colour = WHITE)

# Create IO
#response_device = io.EventButtonBox(io.SerialPort("/dev/ttyS1"))
response_device = exp.keyboard

# Create design
for task in ["shape_only", "filling_only"]:
    b = design.Block()
    b.set_factor("task_type", task)
    if task == "shape_only":
        for shape in ["Rectangle", "Diamond"]:
            if shape == "Rectangle":
                for filling in [["two_dots", "S_R_2.png"], ["three_dots", "S_R_3.png"]]:
                    t = design.Trial()
                    t.set_factor("Shape", shape)
                    t.set_factor("Filling", filling[0])
                    s = stimuli.Picture(filling[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies=20)
            else:
                for filling in [["two_dots", "S_D_2.png"], ["three_dots", "S_D_3.png"]]:
                    t = design.Trial()
                    t.set_factor("Shape", shape)
                    t.set_factor("Filling", filling[0])
                    s = stimuli.Picture(filling[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies=20)
    else:
        for filling in ["two_dots", "three_dots"]:
            if filling == "two_dots":
                for shape in [["Rectangle", "F_R_2.png"], ["Diamond", "F_D_2.png"]]:
                    t = design.Trial()
                    t.set_factor("Filling", filling)
                    t.set_factor("Shape", shape[0])
                    s = stimuli.Picture(shape[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies=20)
            else:
                for shape in [["Rectangle", "F_R_3.png"], ["Diamond", "F_D_3.png"]]:
                    t = design.Trial()
                    t.set_factor("Filling", filling)
                    t.set_factor("Shape", shape[0])
                    s = stimuli.Picture(shape[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies=20)        
    b.shuffle_trials()
    exp.add_block(b)
exp.add_bws_factor("ResponseMapping", [1, 2])
exp.data_variable_names = ["Position", "Button", "RT"]


# Start Experiment
control.start()
exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("task_type")).present()
    response_device.wait()
    for trial in block.trials:
        fixation_cross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = response_device.wait()
        exp.data.add([trial.get_factor("Shape"), button, rt])

# End Experiment
control.end()