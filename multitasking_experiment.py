
from expyriment import design, control, stimuli, io, misc
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


ITI, MAX_RESPONSE_DELAY, ERROR_MESSAGE_DURATION = 800, 4000, 5000
SHAPE_TASK_RECTANGLE = misc.constants.K_RIGHT
FILLING_TASK_TWODOTS = misc.constants.K_RIGHT
SHAPE_TASK_DIAMOND = misc.constants.K_LEFT
FILLING_TASK_THREEDOTS = misc.constants.K_LEFT
SHAPE_CATEGORIES = ["rectangle", "diamond"]
FILLING_CATEGORIES = ["two_dots", "three_dots"]
INSTRUCTIONS = """You will see a rectangle in the middle of the screen. There will be two tasks. 
You will see the name of the task either above or below the rectangle.
    If the task is shaping task:
    press left arrow when the shape is diamond; press right arrow when it is rectangle.
    If the task is filling task:
    press left arrow when there are two dots; press right arrow when there are three dots.
    There will be 3 blocks. 
        1- shape only: there will be only the shape task
        2- filling only: there will be only the filling task
        3- mixed block: there will be both the shape and the filling task. 
    Press the space bar to start."""
ERROR_MESSAGE = """INCORRECT RESPONSE,
SHAPE TASK: 
diamond, press left
rectangle, press right
FILLING TASK:
two dots, press left
three dots, press right"""

exp = design.Experiment(name = "Stoet's Multi-tasking experiment",
                        background_colour = WHITE, 
                        foreground_colour = BLACK)
control.initialize(exp)
blankscreen = stimuli.BlankScreen(colour = WHITE)



response_device = exp.keyboard #you can press any button to start
for task in ["shape_only_block", "filling_only_block"]:
    b = design.Block()
    b.set_factor("task_type", task)
    if task == "shape_only_block":
        for shape in SHAPE_CATEGORIES:
            if shape == "rectangle":
                for filling in [["two_dots", "S_R_2.png"], ["three_dots", "S_R_3.png"]]:
                    t = design.Trial()
                    t.set_factor("shape", shape)
                    t.set_factor("filling", filling[0])
                    s = stimuli.Picture(filling[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies= 32)
            else:
                for filling in [["two_dots", "S_D_2.png"], ["three_dots", "S_D_3.png"]]:
                    t = design.Trial()
                    t.set_factor("shape", shape)
                    t.set_factor("filling", filling[0])
                    s = stimuli.Picture(filling[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies= 32)
    elif task == "filling_only_block":
        for filling in FILLING_CATEGORIES:
            if filling == "two_dots":
                for shape in [["rectangle", "F_R_2.png"], ["diamond", "F_D_2.png"]]:
                    t = design.Trial()
                    t.set_factor("filling", filling)
                    t.set_factor("shape", shape[0])
                    s = stimuli.Picture(shape[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies= 32)
            else:
                for shape in [["rectangle", "F_R_3.png"], ["diamond", "F_D_3.png"]]:
                    t = design.Trial()
                    t.set_factor("filling", filling)
                    t.set_factor("shape", shape[0])
                    s = stimuli.Picture(shape[1])
                    t.add_stimulus(s)
                    b.add_trial(t, copies= 32)
    b.shuffle_trials()
    exp.add_block(b)



control.start(skip_ready_screen = True)
stimuli.TextScreen("Instructions", INSTRUCTIONS).present()
exp.keyboard.wait_char(" ")

exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("task_type")).present()
    exp.keyboard.wait(duration = ITI)
    for trial in block.trials:
        exp.clock.wait(ITI - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = exp.keyboard.wait([SHAPE_TASK_RECTANGLE, SHAPE_TASK_DIAMOND], duration = MAX_RESPONSE_DELAY)
        #Error feedback if required
        if block.get_factor("task_type") == "shape_only_block":
            if trial.get_factor("shape") == "rectangle":
                is_correct = (button == SHAPE_TASK_RECTANGLE)
            elif trial.get_factor("shape") == "diamond":
                is_correct = (button == SHAPE_TASK_DIAMOND)
        elif block.get_factor("task_type") == "filling_only_block":
            if trial.get_factor("filling") == "two_dots":
                is_correct = (button == FILLING_TASK_TWODOTS)
            elif trial.get_factor("filling") == "three_dots":
                is_correct = (button == FILLING_TASK_THREEDOTS)
        if not is_correct:
            stimuli.TextScreen("Instructions", ERROR_MESSAGE).present()
            exp.clock.wait(ERROR_MESSAGE_DURATION)

        exp.data.add([block.get_factor("task_type"), trial.get_factor("filling"), trial.get_factor("shape"), button, rt, is_correct])

# End Experiment
control.end()