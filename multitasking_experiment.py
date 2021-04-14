import expyriment

exp = expyriment.design.Experiment(name="Are women better than men at multi-tasking")
expyriment.control.initialize(exp)


block_one = expyriment.design.Block(name="only shape block")

trial_one = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_diamond_three.png")
stim.preload()
trial_one.add_stimulus(stim)

trial_two = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_diamond_two.png")
trial_two.add_stimulus(stim)

trial_three= expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_rectangle_three.png")
trial_three.add_stimulus(stim)

trial_four = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_rectangle_two.png")
trial_four.add_stimulus(stim)

block_one.add_trial(trial_one)
block_one.add_trial(trial_two)
block_one.add_trial(trial_three)
block_one.add_trial(trial_four)

exp.add_block(block_one)
block_one.shuffle_trials()

block_two = expyriment.design.Block(name="only filling block")

trial_one = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_diamond_three.png")
stim.preload()
trial_one.add_stimulus(stim)

trial_two = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_diamond_two.png")
trial_two.add_stimulus(stim)

trial_three= expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_rectangle_three.png")
trial_three.add_stimulus(stim)

trial_four = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_rectangle_two.png")
trial_four.add_stimulus(stim)

block_two.add_trial(trial_one)
block_two.add_trial(trial_two)
block_two.add_trial(trial_three)
block_two.add_trial(trial_four)

exp.add_block(block_two)
block_two.shuffle_trials()

block_three = expyriment.design.Block(name="shape and filling block")

trial_one = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_diamond_three.png")
stim.preload()
trial_one.add_stimulus(stim)

trial_two = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_diamond_two.png")
trial_two.add_stimulus(stim)

trial_three= expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_rectangle_three.png")
trial_three.add_stimulus(stim)

trial_four = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("shape_rectangle_two.png")
trial_four.add_stimulus(stim)

trial_five = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_diamond_three.png")
stim.preload()
trial_one.add_stimulus(stim)

trial_six = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_diamond_two.png")
trial_two.add_stimulus(stim)

trial_seven= expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_rectangle_three.png")
trial_three.add_stimulus(stim)

trial_eight = expyriment.design.Trial()
stim = expyriment.stimuli.Picture("filling_rectangle_two.png")
trial_four.add_stimulus(stim)

block_three.add_trial(trial_one)
block_three.add_trial(trial_two)
block_three.add_trial(trial_three)
block_three.add_trial(trial_four)
block_three.add_trial(trial_five)
block_three.add_trial(trial_six)
block_three.add_trial(trial_seven)
block_three.add_trial(trial_eight)

exp.add_block(block_three)
block_three.shuffle_trials()

expyriment.control.start()

for block in exp.blocks:
    for trial in block.trials:
        trial.stimuli[0].present()
        key, rt = exp.keyboard.wait([expyriment.misc.constants.K_LEFT,
                                     expyriment.misc.constants.K_RIGHT])
        exp.data.add([block.name, trial.id, key, rt])

expyriment.control.end()

