from expyriment import design, control, stimuli, io, misc
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


ITI, MAX_RESPONSE_DELAY, ERROR_MESSAGE_DURATION = 800, 4000, 5000
SHAPE_TASK_RECTANGLE = misc.constants.K_RIGHT
SHAPE_TASK_DIAMOND = misc.constants.K_LEFT
FILLING_TASK_TWODOTS = misc.constants.K_LEFT
FILLING_TASK_THREEDOTS = misc.constants.K_RIGHT
BLOCK_NAMES = ["shape only block","filling only block", "mixed block"]
ABOVE_SHAPE_CATEGORIES = ["rectangle", "diamond"]
BELOW_FILLING_CATEGORIES = ["two_dots", "three_dots"]
TRANING_EXPERIMENTAL_TRIALS = [10, 20]

INSTRUCTIONS = """ You will see a rectangle in the middle of the screen. There will be two tasks. 
You will see the name of the task either above or below the rectangle.
    If the task is a SHAPE TASK:
    press LEFT arrow when the shape is diamond; press RIGHT arrow when it is rectangle.
    If the task is a FILLING TASK:
    press LEFT arrow when there are TWO DOTS; press RIGHT arrow when there are three dots.

    There will be 3 blocks. 
        1- shape only: there will be only the shape task
        2- filling only: there will be only the filling task
        3- mixed block: there will be both the shape and the filling task

    Press the space bar to start."""
ERROR_MESSAGE = """INCORRECT RESPONSE,
SHAPE TASK: 
DIAMOND, press LEFT
RECTANGLE, press LEFT

FILLING TASK:
TWO dots, press LEFT
THREE dots, press RIGHT"""

exp = design.Experiment(name = "Stoet's Multi-tasking experiment",
                        background_colour = WHITE, 
                        foreground_colour = BLACK)
control.initialize(exp)
blankscreen = stimuli.BlankScreen(colour = WHITE)

#I added this because otherwise the transisition between trials was not obvious
fixcross = stimuli.FixCross()
fixcross.preload()
#I added this to make the error message stronger
error_beep = stimuli.Tone(duration=200, frequency=2000)
error_beep.preload()

def trial_generator(changing_stimulus_feature):
    if changing_stimulus_feature == "filling":
        t = design.Trial()
        t.set_factor("shape", above_shape)
        t.set_factor("filling", filling[0])
        s = stimuli.Picture(filling[1])
        t.add_stimulus(s)
    elif changing_stimulus_feature == "shape":
        t = design.Trial()
        t.set_factor("filling", below_filling)
        t.set_factor("shape", shape[0])
        s = stimuli.Picture(shape[1])
        t.add_stimulus(s)
    return(t)

for N_TRIAL in TRANING_EXPERIMENTAL_TRIALS:
    for task in BLOCK_NAMES:
        b = design.Block()
        b.set_factor("task_type", task)
        if task == "shape only block":
            for above_shape in ABOVE_SHAPE_CATEGORIES:
                if above_shape == "rectangle":
                    for filling in [["two_dots", "S_R_2.png"], ["three_dots", "S_R_3.png"]]:
                        t = trial_generator("filling")
                        b.add_trial(t, copies= (N_TRIAL))
                else:
                    for filling in [["two_dots", "S_D_2.png"], ["three_dots", "S_D_3.png"]]:
                        t = trial_generator("filling")
                        b.add_trial(t, copies= (N_TRIAL))
        elif task == "filling only block":
            for below_filling in BELOW_FILLING_CATEGORIES:
                if below_filling == "two_dots":
                    for shape in [["rectangle", "F_R_2.png"], ["diamond", "F_D_2.png"]]:
                        t = trial_generator("shape")
                        b.add_trial(t, copies= (N_TRIAL))
                else:
                    for shape in [["rectangle", "F_R_3.png"], ["diamond", "F_D_3.png"]]:
                        t = trial_generator("shape")
                        b.add_trial(t, copies= (N_TRIAL))
        elif task == "mixed block":
            for above_shape in ABOVE_SHAPE_CATEGORIES:
                if above_shape == "rectangle":
                    for filling in [["two_dots", "S_R_2.png"], ["three_dots", "S_R_3.png"]]:
                        t = trial_generator("filling")
                        b.add_trial(t, copies= (N_TRIAL)//2)
                else:
                    for filling in [["two_dots", "S_D_2.png"], ["three_dots", "S_D_3.png"]]:
                        t = trial_generator("filling")
                        b.add_trial(t, copies= (N_TRIAL)//2)
            for below_filling in BELOW_FILLING_CATEGORIES:
                if below_filling == "two_dots":
                    for shape in [["rectangle", "F_R_2.png"], ["diamond", "F_D_2.png"]]:
                        t = trial_generator("shape")
                        b.add_trial(t, copies= (N_TRIAL)//2)
                else:
                    for shape in [["rectangle", "F_R_3.png"], ["diamond", "F_D_3.png"]]:
                        t = trial_generator("shape")
                        b.add_trial(t, copies= (N_TRIAL)//2)
        b.shuffle_trials()
        exp.add_block(b)

control.start(skip_ready_screen = True)
stimuli.TextScreen("Instructions", INSTRUCTIONS).present()
exp.keyboard.wait_char(" ")

for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("task_type")).present()
    exp.keyboard.wait(duration = ITI)
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(ITI - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = exp.keyboard.wait([SHAPE_TASK_RECTANGLE, SHAPE_TASK_DIAMOND], duration = MAX_RESPONSE_DELAY)
        #Error feedback if required
        if block.get_factor("task_type") == "shape only block":
            if trial.get_factor("shape") == "rectangle":
                is_correct = (button == SHAPE_TASK_RECTANGLE)
            elif trial.get_factor("shape") == "diamond":
                is_correct = (button == SHAPE_TASK_DIAMOND)
        elif block.get_factor("task_type") == "filling only block":
            if trial.get_factor("filling") == "two_dots":
                is_correct = (button == FILLING_TASK_TWODOTS)
            elif trial.get_factor("filling") == "three_dots":
                is_correct = (button == FILLING_TASK_THREEDOTS)
        elif block.get_factor("task_type") == "mixed block":
            if trial.get_factor("shape") == "rectangle":
                is_correct = (button == SHAPE_TASK_RECTANGLE)
            elif trial.get_factor("shape") == "diamond":
                is_correct = (button == SHAPE_TASK_DIAMOND)
            if trial.get_factor("filling") == "two_dots":
                is_correct = (button == FILLING_TASK_TWODOTS)
            elif trial.get_factor("filling") == "three_dots":
                is_correct = (button == FILLING_TASK_THREEDOTS)   
        if not is_correct:
            error_beep.present()
            stimuli.TextScreen("Instructions", ERROR_MESSAGE).present()
            exp.clock.wait(ERROR_MESSAGE_DURATION)

        exp.data.add([block.get_factor("task_type"), trial.get_factor("filling"), trial.get_factor("shape"), button, rt, is_correct])

# End Experiment
control.end()