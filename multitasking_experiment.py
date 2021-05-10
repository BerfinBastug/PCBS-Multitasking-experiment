from expyriment import design, control, stimuli, io, misc
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


ITI, MAX_RESPONSE_DELAY, ERROR_MESSAGE_DURATION = 800, 4000, 5000
SHAPE_TASK_RECTANGLE = misc.constants.K_RIGHT
SHAPE_TASK_DIAMOND = misc.constants.K_LEFT
FILLING_TASK_TWODOTS = misc.constants.K_LEFT
FILLING_TASK_THREEDOTS = misc.constants.K_RIGHT

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
RECTANGLE, press RIGHT

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

rectangle = [["rectangle", "two_dots", "S_R_2.png"], ["rectangle", "three_dots", "S_R_3.png"]]
diamond = [["diamond", "two_dots", "S_D_2.png"], ["diamond", "three_dots", "S_D_3.png"]]
two_dots = [["rectangle", "two_dots", "F_R_2.png"], ["diamond", "two_dots", "F_D_2.png"]]
three_dots = [["rectangle", "three_dots", "F_D_3.png"], ["diamond", "three_dots", "F_D_3.png"]]

shapes_task = [rectangle, diamond]
fillings_task = [two_dots, three_dots]
mixed_task = [rectangle, diamond, two_dots, three_dots]

tasks = [["shapes_task", shapes_task], ["fillings_task", fillings_task], ["mixed_task", mixed_task]]
N_trials = [10, 20]
 
def trial_generator(task, N):
    if task[0] == "mixed_task":
        N = N//2
    b = design.Block()
    b.set_factor("task_type", task[0])
    for specific_task in task[1]:
        for my_trial in specific_task:
            t = design.Trial()
            t.set_factor("shape", my_trial[0])
            t.set_factor("filling", my_trial[1])
            s = stimuli.Picture(my_trial[2])
            t.add_stimulus(s)
            b.add_trial(t, copies= N)
    b.shuffle_trials()
    return b

for N in N_trials:
    for task in tasks:        
        b = trial_generator(task, N)
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
        if trial.stimuli[0].filename == "S_R_2.png":
            is_correct = (button == SHAPE_TASK_RECTANGLE)
        elif trial.stimuli[0].filename == "S_R_3.png":
            is_correct = (button == SHAPE_TASK_RECTANGLE)
        elif trial.stimuli[0].filename == "S_D_2.png":
            is_correct = (button == SHAPE_TASK_DIAMOND)
        elif trial.stimuli[0].filename == "S_D_3.png":
            is_correct = (button == SHAPE_TASK_DIAMOND)
        elif trial.stimuli[0].filename == "F_R_2.png":
            is_correct = (button == FILLING_TASK_TWODOTS)
        elif trial.stimuli[0].filename == "F_D_2.png":
            is_correct = (button == FILLING_TASK_TWODOTS)
        elif trial.stimuli[0].filename == "F_R_3.png":
            is_correct = (button == FILLING_TASK_THREEDOTS)
        elif trial.stimuli[0].filename == "F_D_3.png":
            is_correct = (button == FILLING_TASK_THREEDOTS)
        if not is_correct:
            error_beep.present()
            stimuli.TextScreen("Instructions", ERROR_MESSAGE).present()
            exp.clock.wait(ERROR_MESSAGE_DURATION)

        exp.data.add([block.get_factor("task_type"), trial.get_factor("filling"), trial.get_factor("shape"), button, rt, is_correct])

# End Experiment
control.end()