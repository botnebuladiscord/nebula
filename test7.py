pets = ['butterfly', 'ladybug', 'dog', 'cat', 'pig', 'chipmunk', 'hamster', 'swan', 'rabbit', 'peacock', 'frog', 'dolphin', 'horse', 'octopus', 'monkey', 'hedgehog', 'beaver', 'elephant', 'giraffe', 'rhino', 'panda', 'flamingo', 'llama', 'badger', 'sloth', 'raccoon', 'zebra', 'polar bear', 'penguin', 'orangutan']
pprice = [50, 75, 100, 150, 175, 175, 200, 250, 300, 350, 400, 450, 500, 500, 550, 600, 600, 650, 675, 700, 750, 800, 850, 900, 950, 950, 975, 1000, 1000, 1000]
petlevels = [9, 15]

pets_choice = []
pet_type = 'common'
if pet_type == 'common':
    pets_choice = pets[:petlevels[0]]
elif pet_type == 'uncommon':
    pets_choice = pets[petlevels[0]:petlevels[1]]
elif pet_type == 'rare':
    pets_choice = pets[petlevels[1]:]
print(pets_choice)

a = {"[]":[{'name':'test'}]}