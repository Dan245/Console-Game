'''
Please ignore the fact that I forgot classes were a thing
'''

import json
import random

# grab json save file
def open_json():
  # open file and return it. If there's an error return an empty template
    with open('saves.json') as f:
        try:
            return json.load(f)
        except:
            return [None, None, None]


# save to json file
def save_json(data, ans):
  # make a copy of data if it's not empty
    data = data.copy() if data else data
    # save the save to the saves list
    saves[ans] = data
    # write the saves string to the json file
    with open('saves.json', 'w') as f:
        json.dump(saves, f, indent=4, sort_keys=True)

# load and initialize a save
def load_save(saves, ans, i):
  if not ans:
    # saves the save file to a var for reference
    save = saves[i]
    # if sasve is empty, initalize a new game
    if not save:
      # create dict
      save = {}
      save['char'] = {}
      save['char']['line'] = 0
      # ask for name
      save['char']['name'] = input(
                    "Please enter your Character's name: ").upper()
      # ask for gender
      save['char']['gender'] = list_verify(
                    "What is your character's gender? (biologically): ",
                    genders)
      # ask for race
      save['char']['race'] = list_verify(
                    f"What race is {save['char']['name']}?: ", r_list)
      # ask for weapon
      save['char']['weapon'] = list_verify(
                    "Pick your Weapon:", w_list[save['char']['race']])
      # ask for armour
      save['char']['armour'] = list_verify("Pick your Armour:",
                                       a_list)
      # add together stats of race, weapon, and armour choices for the different stats
      save['char']['stats'] = {
                    'spd':
                    races[r_list[save['char']['race']]]['spd'] +
                    weapons[save['char']['race']][w_list[save['char']['race']][
                        save['char']['weapon']]]['spd'] +
                    armours[a_list[save['char']['armour']]]['spd'],
                    'def':
                    races[r_list[save['char']['race']]]['def'] +
                    weapons[save['char']['race']][w_list[save['char']['race']][
                        save['char']['weapon']]]['def'] +
                    armours[a_list[save['char']['armour']]]['def'],
                    'str':
                    races[r_list[save['char']['race']]]['str'] +
                    weapons[save['char']['race']][w_list[save['char']['race']][
                        save['char']['weapon']]]['str'],
                    'ide_ran':
                    weapons[save['char']['race']][w_list[save['char']['race']][
                        save['char']['weapon']]]['ide_ran']
                }
      # initialize the party
      save['party'] = {
                    'members': [None, None],
                    'fame': 0
                }
      #initialize more vars and fame
      save['char']['fame'] = 0
      save['char']['battle'] = {'pos': 0, 'str_debuff': 1, 'def_debuff': 1, 'spd_debuff': 1, 'OH_kill': False}
      save['recruits'] = []
  # save the file
  save_json(save, i)
  # load the global vars
  load_vars(save)
  # return save
  return save

# displays a list in a cool print
def display(options):
    # initialize the msg to print
    msg = "\n"
    # add every val in list to the msg, with it's corresponding index
    for i, j in enumerate(options):
        if j:
            msg += f"\t{{{i}}} {j}\n"
    # print the message and return the user input
    print(msg)
    return input("\t> ")

# verify input is valid
def list_verify(msg, options, go_back = False):
    # while they haven't entered a vali input
    while True:
        # copy the options so we don't change the original
        op = options.copy()
        # if user can choose to go back, add the option to the list
        if go_back:
          op.append("Return")
        # print question and options and save input
        print(msg)
        inp = display(op)
        # if input is an integer within the list range, break, otherwise print error msg and loop. If user selected return, return value as string instead of int
        try:
            if int(inp) > -1 and int(inp) <= len(op) - 1:
              if op[int(inp)] == op[-1] and go_back:
                return inp
              else:
                return int(inp)
            else:
                print("Please select one of the options above.")
                input("Press Enter to Continue\n")
        except:
            print("Please select one of the options above.")
            input("Press Enter to Continue\n")

# loading the global vars
def load_vars(save):
    global char
    char = save['char']
    global party
    party = save['party']
    global recruits
    recruits = save['recruits']
    global stats
    stats = save['char']['stats']

# sorting a dictionary, basically grabs the values of a dict, sorts the values, matches the values with their key and put it into a new dict before returning it
def sort_dict(dic):
  sorted_vals = sorted(dic.values())
  sorted_dict = {}
  for i in sorted_vals:
    for j in dic.keys():
        if dic[j] == i:
            sorted_dict[j] = dic[j]
            break
  return sorted_dict

# updates the save variable with all the global reference vars
def update_save(save):
    global char
    save['char'] = char
    global party
    save['party'] = party
    global recruits
    save['recruits'] = recruits
    global stats
    save['stats'] = stats
    return save

# special function for making list of save files
def grab_saves():
    op = []
    global saves
    for i, j in enumerate(saves):
      try:
        op.append(
            "[New Game]" if not j else
            f"[{saves[i]['char']['name']}: {saves[i]['char']['fame']} Fame]"
        )
      except:
        saves[i] = None
        op.append("[New Game]")
    return op

# create npc function
def create_npc():
    npc = {} # create npc dict
    # generate random values for the npc traits. Grab name from json file of either male or female names (dependent on their gender)
    npc['gender'] = random.randint(0, len(genders) - 1)
    if not npc['gender']:
        with open('m_names.json') as f:
            names = json.load(f)
            npc['name'] = names[random.randint(0, len(names) - 1)].upper()
    else:
        with open('f_names.json') as f:
            names = json.load(f)
            npc['name'] = names[random.randint(0, len(names) - 1)].upper()
    npc['race'] = random.randint(0, len(r_list) - 1)
    npc['weapon'] = random.randint(0, len(w_list[npc['race']]) - 1)
    npc['armour'] = random.randint(0, len(a_list) - 1)
    npc['stats'] = {
        'spd':
        races[r_list[npc['race']]]['spd'] +
        weapons[npc['race']][w_list[npc['race']][npc['weapon']]]['spd'] +
        armours[a_list[npc['armour']]]['spd'],
        'def':
        races[r_list[npc['race']]]['def'] +
        weapons[npc['race']][w_list[npc['race']][npc['weapon']]]['def'] +
        armours[a_list[npc['armour']]]['def'],
        'str':
        races[r_list[npc['race']]]['str'] +
        weapons[npc['race']][w_list[npc['race']][npc['weapon']]]['str'],
        'ide_ran':
        weapons[npc['race']][w_list[npc['race']][
            npc['weapon']]]['ide_ran']
    }
    npc['line'] = 0
    global char
    npc['fame'] = random.randint(0 if char['fame'] < 50 else char['fame'] - 50,
                                 char['fame'] + 50)
    npc['battle'] = {'pos': 0, 'str_debuff': 1, 'def_debuff': 1, 'spd_debuff': 1, 'OH_kill': False}

    return npc

# party screen
def party_screen(c, p):
  global party
  global save
  global char
  options = ["View Members", "Remove Members", "Edit Lineup"]
  while True:
    # ask users what they would like to do
    option = list_verify(f"Your Party ({party['fame']} Fame): ", options, True)
    if type(option) == str: # you'll see this a lot, just checks if they chose "Return", since the function would return a string if they did
      break
    members = [c['name'] + " (You)"]
    for i in range(len(p['members'])):
      if p['members'][i]:
        members.append(p['members'][i]['name'])
    if not option: # if they chose view members
      # get them to pick a 
      member = list_verify("Members:", members, True)
      if type(member) == str:
        continue
      else:
        global a_list
        global w_list
        global r_list
        global genders
        # selects member (if statement is bcuz the character is stored in a different location compared to the members)
        if p['members'][0]:
          member = c if not member else p['members'][member-1]
        else:
          member = c if not member else p['members'][member]
        # print nicely formatted info sheet of characters
        print(f"\t{member['name']}\n\t\tRace: {r_list[member['race']]}\n\t\tGender: {genders[member['gender']]}\n\t\tWeapon: {w_list[member['race']][member['weapon']]}\n\t\tArmour: {a_list[member['armour']]}\n\t\tStats:\n\t\t\tIdeal Attack Range: {member['stats']['ide_ran']} Tiles\n\t\t\tStrength: {member['stats']['str']}\n\t\t\tDefense: {member['stats']['def']}\n\t\t\tSpeed: {member['stats']['spd']}\n\t\t\t")
        #allow the character to read it before getting hit with the party screen again
        input("\nHit Enter to return to main party screen")
    elif option == 1: # if they chose remove member
      members.pop(0) # they cant remove themselves
      # ask which member to remove, delete the member from list, and update the save var
      remove = list_verify("Select a party member to remove from the group: ", members, True)
      if type(remove) == str:
        continue
      party['members'][remove] = None
      update_save(save)
    elif option == 2: # if they chose edit lineup
      # init strings for the 2 rows
      front = ""
      back = ""
      # for each member, check if they are front line or back line (0 or 1), and append them to the appropriate string
      for i in range(len(members)):
        m = c if not i else p['members'][i-1]
        if m:
          if not m['line']:
            front += F"\t\t{members[i]}\n"

          else:
            back += F"\t\t{members[i]}\n"
      # prin the 2 strings
      print(f"Current Lineup:\n\tFront Line (2 Tiles from enemy front line)\n{front}\tBack Line (4 Tiles from enemy front line)\n{back}")
      # grab who they want to swap, get the dict of that member, and invert the line value to switch their position
      swap = list_verify("\nWho would you like to switch their starting line?: ", members, True)
      if type(swap) == str:
        continue
      m = c if not swap else p['members'][swap-1]
      if m == c:
        char['line'] = not char['line']
      else:
        party['members'][swap-1]['line'] = not party['members'][swap-1]['line']
      print("Position Switched")
      # update the save
      update_save(save)
      # update the local vars (since this loops without updating otherwise)
      c = char
      p = party

  else: # if they chose quit
    # exit function
    return


# simulate people randomly leaving the tavern
def get_pot_recs():
    #gets a list of the recruits, and for each one there's a 50% chance they leave and are removed from the list, otherwise they get added to a new list
    pot_recs = []
    global recruits
    rec = recruits.copy()
    for i, j in enumerate(rec):
            if not random.randint(0, 1):
                print(f"\n{rec[i]['name']} has left the tavern")
                recruits.remove(j)
            else:
                pot_recs.append(j)
    # return the new list
    return pot_recs

# gen the tavern
def gen_tavern():
    global recruits
    # get previous recruits
    pot_recs = get_pot_recs()
    # add a variable amount of people to the tavern based off of the current number of people
    num = len(pot_recs) if len(pot_recs) < 5 else 4
    for i in range(random.randint(0, 4 - num)):
        # for every new person that needs to be made, create a new npc
        npc = create_npc()
        # append the npc to both the global var and the local var
        recruits.append(npc)
        pot_recs.append(npc)
    # part of message for list verify
    msg2 = "Who would you like to try and recuit?"
    # custom message for list verify based on number of people in the tavern
    if len(pot_recs) > 3:
        msg1 = "There are several people in the tavern right now."
    elif len(pot_recs) > 2:
        msg1 = "There are a few people in the tavern right now."
    elif len(pot_recs) == 0:
        print("No one's here. Maybe check back later?")
        return
    elif len(pot_recs) > 1:
        msg1 = "There's a couple people in the tavern right now."
    else:
        msg1 = "There's only one person in the tavern right now."
        msg2 = ""
    # create a list of strings with each recruits info
    lst = []
    global races
    global armours
    global weapons
    for i in range(len(pot_recs)):
        lst.append(
            f"{pot_recs[i]['name']} \n\t\t\tRace: {r_list[pot_recs[i]['race']]}\n\t\t\tGender: {genders[pot_recs[i]['gender']]}\n\t\t\tWeapon: {w_list[pot_recs[i]['race']][pot_recs[i]['weapon']]}\n\t\t\tArmour: {a_list[pot_recs[i]['armour']]}"
        )
    # return dict of recruits, lst of strings, and message
    return pot_recs, lst, f"{msg1} {msg2}"

# tavern function
def tavern():
  global recruits
  global party
  # checking if there is a spot on the team
  if not(None in party['members']):
    print("Your party is full!")
    input("Hit Enter to Continue")
    return
  # generate the tavern
  tavern = gen_tavern()
  # if no one's in the tavern return
  if not tavern:
    return
  # safety feature in case my code is broken, ensures global list has all the members in the local list
  for i in tavern[0]:
    if i not in recruits:
      recruits.append(i)
  while True:
    # ask user who they'd like to recuit (with custom made strings and message!)
    pot_rec = list_verify(tavern[2], tavern[1], True)
    if type(pot_rec) == str:
      return
    # if the recruit has more or lessthan 120% of the party's fame, recruit has 100% chance of declining/accepting, otherwise it's a 50/50
    if tavern[0][pot_rec]['fame'] > party['fame'] * 1.2:
      rec = False
    elif tavern[0][pot_rec]['fame'] < party['fame'] * 1.2:
      rec = True
    else:
      rec = random.randint(0, 1)
    # if the recruit accepts, display accepting message, add them to an empty slot on the member list, and remove them from the recruit lists
    if rec:
      print(f"{tavern[0][pot_rec]['name']} has decided to join your party!")
      input("Hit Enter to continue")
      print("\n")
      for i, j in enumerate(party['members']):
        if not j:
          party['members'][i] = tavern[0][pot_rec]
          recruits.remove(party['members'][i])
          tavern[1].pop(pot_rec)
          tavern[0].pop(pot_rec)
          break # ensures it stops after it's found an empty spot
    else:
      # if recruit doesn't accept, display rejection message, have them leave the tavern, and remove them from all lists
      print(
          f"{tavern[0][pot_rec]['name']} told you to get lost.")
      print(f"\n{tavern[0][pot_rec]['name']} has left the tavern")
      recruits.remove(tavern[0][pot_rec])
      tavern[1].pop(pot_rec)
      tavern[0].pop(pot_rec)
      input("Hit Enter to Continue")
      print("\n")
    # if party is now full, return to homescreen
    if not(None in party['members']):
      print("Your party is full!")
      input("Hit Enter to Continue")
      return
    # quits if no ones is left in the tavern
    if not recruits:
      print("There's no one left in the tavern to recruit...")
      input("Hit Enter to continue")
      print("\n")
      return
      

# creates a list of enemies with predefined values and returns it
def create_enemies(num):
  template = { 'stats': {
                      "def": 5,
                      "ide_ran": 2,
                      "spd": 1,
                      "str": 5}, 'battle': {'pos': 0, 'str_debuff': 1, 'def_debuff': 1, 'spd_debuff': 1, 'OH_kill': False}}
  enemies = []
  for i in range(num):
    t = template.copy()
    t['name'] = f"Ghoul {i+1}"
    t['line'] = 0
    enemies.append(t)
  return enemies

    
# checks if the attack is dodged. Does so by generating a number and checking if that number is greater than the cool formula I made for calculating the defender's chance of dodge
def dodge_check(spd, debuff, ide_ran, dst, part):
  chance = random.randint(1, 7)
  if chance > spd*debuff*part['spd']+abs(ide_ran-dst):
    return False
  else:
    return True

# check if the attack is blocked by armour. Does so in same why as dodge check, except now it incorporates the strength of the attacker
def defense_check(srn, dfn, debuff1, debuff2, ide_ran, dst, part):
  chance = random.randint(1, 7)
  if chance > dfn*debuff1*part['def']-srn*debuff2+abs(ide_ran-dst):
    return False
  else:
    return True

# get turn order (I didn't used the sort dict function because I had to do stuff a little differently)
def get_order(c, p):
  # create list of friendlies
  friendlies = [c]
  for i, j in enumerate(p['members']):
    if j:
      friendlies.append(p['members'][i])
  # grab list of enemies
  enemies = create_enemies(random.randint(len(friendlies), 2+len(friendlies)))
  # get speed values for everyone
  speed = {}
  for i in friendlies:
    i['battle'] = {'pos': 0, 'str_debuff': 1, 'def_debuff': 1, 'spd_debuff': 1, 'OH_kill': False}.copy()
    speed[i['name']] = i['stats']['spd']
  for i in enemies:
    i['battle'] = {'pos': 0, 'str_debuff': 1, 'def_debuff': 1, 'spd_debuff': 1, 'OH_kill': False}.copy()
    speed[i['name']] = i['stats']['spd']
  # sort the values with highest first
  sorted_vals = sorted(speed.values(), reverse=True)
  turn_order = {}
  coopy = speed.copy()
  # attach keys to their matching values in the correct order
  for i in sorted_vals:
    for j in speed.keys():
        if coopy[j] == i:
            turn_order[j] = speed[j]
            coopy[j] = None
            break
  # return turn list, friendlies list, and enemies list
  return list(turn_order.keys()), friendlies, enemies

def battle(c, p):
  # gets the order
  info = get_order(c, p)
  # puts the vars into new ones that make more sense
  turn_order = info[0]
  friendlies = info[1]
  enemies = info[2]
  # initializing lists needed for calculations and asking usr r for input
  moves = ["Move", "Attack"]
  body_parts = {'Head': {'spd': 2.5, 'def': 0.75}, 'Chest': {'spd': 0.75, 'def': 2}, 'Left Arm': {'spd': 1, 'def': 1}, 'Right Arm': {'spd': 1, 'def': 1}, 'Left Leg': {'spd': 1, 'def': 1}, 'Right Leg': {'spd': 1, 'def': 1}}
  part_list = list(body_parts.keys())
  # make lsit of enemy and friendly names, and initilize neccessary vars for battle
  fr_names = []
  for i in friendlies:
    i['pos'] = (i['line']+1)*2-1
    i['battle']['parts'] = part_list.copy()
    fr_names.append(i['name'])
  en_names = []
  for i in enemies:
    i['pos'] = -1
    i['battle']['parts'] = part_list.copy()
    en_names.append(i['name'])
  print(f"You and your party are teleported to a random floor of the dungeon. There are {len(en_names)} ghouls on this floor.")
  # keep looping until round is over
  while True:
    # go through turn list
    for i, j in enumerate(turn_order):
      # if current turn is friendly
      if j in fr_names:
        # grab position values of enemies
        values = []
        for i in enemies:
          values.append(i['pos'])
          # get dict of current character
        for k in p['members']:
          try:
            if k['name'] == j:
              current = k
              break
            else:
              current = c
          except:
            current = c
        # temporarily remove moves options, and add it back the char can move in any of the directions
        if "Move" in moves:
          moves.pop(0)
        if current['pos'] < 5 or current['pos'] > min(values)+1:
          moves.insert(0, "Move")
        # get num of enemies
        enemy_num = len(enemies)
        # making choices
        while True:
          # copy enemies
          targets = enemies.copy()
          # if all enemies are dead, add fame to char and party, and quit out of function
          if not targets:
            global party
            global char
            num = random.randint(0, 3)
            party['fame'] += 3+(len(friendlies)-1)*2+2*enemy_num + num
            char['fame'] += 3+2*enemy_num + num
            print(f"Enemies Defeated!\nPlayer Fame Up! {char['name']} now has {char['fame']} Fame!\nParty Fame Up! Your party now has {party['fame']} Fame!\nA door opens and you see the staircase that leads back to the Courtyard.")
            input("Press Enter to Continue")
            print("\n")
            return
          # list of target names
          tr_names = []
          for i in targets:
            tr_names.append(i['name'])
          # ask usr iif they want char to move or attack
          move = list_verify(f"\n{j} is ready to move or attack: ", moves)
          #if they want to move
          if not move:
            # give options based on their position (can't go past enemies, can't go beyond pos 5)
            options = []
            if current['pos'] > min(values)+1:
              options.append("Move Forward 1 Tile")
            if current['pos'] < 5:
              options.append("Move Backward 1 Tile")
            # print current location and how far off it is from ideal weapon range, and ask if they'd like to move forward or backward
            print(f"{current['name']} is currently {abs(current['pos']-targets[0]['pos'])} Tile(s) away from enemy line ({abs(abs(current['pos']-targets[0]['pos'])-current['stats']['ide_ran'])} off from ideal weapon range)")
            movement = list_verify("Move options: ", options, True)
            if type(movement) is str:
              continue
            # move either forward or backward depending on selection, and display how far they are  from enemy front line
            elif options[movement] == "Move Forward 1 Tile":
              current['pos'] -= 1
              print(f"{current['name']} is now {abs(current['pos']-targets[0]['pos'])} Tile(s) from the enemy front line")
              input("Press Enter to Continue")
              print("\n")
              break
            else:
              current['pos'] += 1 
              print(f"{current['name']} is now {abs(current['pos']-targets[0]['pos'])} Tile(s) from the enemy front line")
              input("Press Enter to Continue")
              print("\n")
              break
          else: # if they want to attack
            # ask usr for target
            t = list_verify(f"Targets ({abs(current['pos']-targets[0]['pos'])} tiles away)", tr_names, True)
            if type(t) is str:
              continue
            # get dict of target
            target = targets[t]
            # ask usr for body part
            body_part = list_verify("Pick a body part to attack:", target['battle']['parts'], True)
            if type(body_part) is str:
              continue
            # check if they dodged or defended attack (with all the juicy stats and debuffs)
            if dodge_check(target['stats']['spd'], target['battle']['spd_debuff'], current['stats']['ide_ran'], abs(current['pos']-targets[0]['pos']), body_parts[target['battle']['parts'][body_part]]):
              print(f"{target['name']} dodged the attack!")
              input("Press Enter to Continue")
              print("\n")
              break
            if defense_check(current['stats']['str'], target['stats']['def'], target['battle']['def_debuff'], current['battle']['str_debuff'], current['stats']['ide_ran'], abs(current['pos']-targets[0]['pos']), body_parts[target['battle']['parts'][body_part]]):
              print(f"The attack hit {target['name']} but was unable to penetrate it's armour!")
              input("Press Enter to Continue")
              print("\n")
              break
            # if loop wasnt broken, display that attack was successful
            print(f"The attack connected and penetrated through {target['name']}'s armour!")
            print(f"{target['name']}'s {target['battle']['parts'][body_part]} is wounded.")
            # if target was head or 3 body parts have been hit, target is dead; remove them from enemy list
            if target['battle']['OH_kill'] >= 2 or target['battle']['parts'][body_part] == "Head":
              print(f"{target['name']} is now dead.")
              enemies.remove(target)
              en_names.remove(target['name'])
            # else add one to hit counter, add debuff, and display appropriate messages
            elif target['battle']['parts'][body_part] == "Chest":
              target['battle']['def_debuff'] -= 0.5
              target['battle']['OH_kill'] += 1
              print(f"{target['name']}'s defense down!")
              target['battle']['str_debuff'] -= 0.25
              print(f"{target['name']}'s strength down!")
            elif target['battle']['parts'][body_part] == "Left Arm" or target['battle']['parts'][body_part] == "Right Arm":
              target['battle']['str_debuff'] -= 0.3
              target['battle']['OH_kill'] += 1
              print(f"{target['name']}'s strength down!")
            elif target['battle']['parts'][body_part] == "Left Leg" or target['battle']['parts'][body_part] == "Right Leg":
              target['battle']['spd_debuff'] -= 0.3
              target['battle']['OH_kill'] += 1
              print(f"{target['name']}'s speed down!")
            # remove wounded body part from part selection
            target['battle']['parts'].remove(target['battle']['parts'][body_part])
            input("Press Enter to Continue")
            print("\n")
            break
      elif j in en_names: # if enemy's turn
        # get position values of friendlies
        values = []
        for k in friendlies:
          values.append(k['pos'])
        # get dict of enemy
        for k in enemies:
          if k['name'] == j:
            current = k
        # make copy of friendlies
        targets = friendlies.copy()
        #if needs to move
        # grab distance to front line, if ghoul is not at ideal range, move accordingly
        dist = abs(current['pos']-min(values))
        if dist != current['stats']['ide_ran']:
          if current['pos'] > min(values)+1 and dist - current['stats']['ide_ran'] > 0:
            print(f"{current['name']} moved forward 1 Tile.")
            current['pos'] += 1
            print(f"{current['name']} is now {abs(current['pos']-min(values))} Tile(s) from your front line")
            input("Press Enter to Continue")
            print("\n")
            continue
          elif current['pos'] < 5 and dist - current['stats']['ide_ran'] < 0: 
            print(f"{current['name']} moved backward 1 Tile.")
            current['pos'] -= 1 
            print(f"{current['name']} is now {abs(current['pos']-min(values))} Tile(s) from your front line")
            input("Press Enter to Continue")
            print("\n")
            continue
        #else
        # pick random valid target (at front line)
        target = targets[random.randint(0, len(targets)-1)]
        while target['pos'] != min(values):
          target = targets[random.randint(0, len(targets)-1)]
        # pick random body part
        body_part = random.randint(0, len(target['battle']['parts'])-1)
        print(f"{current['name']} attacked {target['name']}.")
        # do dodge and defense check
        if dodge_check(target['stats']['spd'], target['battle']['spd_debuff'], current['stats']['ide_ran'], abs(current['pos']-targets[0]['pos']), body_parts[target['battle']['parts'][body_part]]):
          print(f"{target['name']} dodged the attack!")
          input("Press Enter to Continue")
          print("\n")
          continue
        if defense_check(current['stats']['str'], target['stats']['def'], target['battle']['def_debuff'], current['battle']['str_debuff'], current['stats']['ide_ran'], abs(current['pos']-targets[0]['pos']), body_parts[target['battle']['parts'][body_part]]):
          print(f"The attack hit {target['name']} but was unable to penetrate it's armour!")
          input("Press Enter to Continue")
          print("\n")
          continue
        # if attack succesful do the normal stuff
        print(f"The attack connected and penetrated through {target['name']}'s armour!")
        print(f"{target['name']}'s {target['battle']['parts'][body_part]} is wounded.")
        if target['battle']['OH_kill'] >= 2 or target['battle']['parts'][body_part] == "Head":
          # if character is killed, delete the save and show game over screen, otherwise remove party member from party and battle lists
          print(f"{target['name']} is now dead.")
          if target == c:
            global save
            save = None
            input(f"You have died! Your final Fame was {c['fame']}. Press Enter to return to the main menu")
            print("\n")
            return
          friendlies.remove(target)
          fr_names.remove(target['name'])
          for b, z in enumerate(party['members']):
            if z:
              if z['name'] == target['name']:
                party['members'][b] = None
          input("Press Enter to Continue")
          print("\n")
          continue
        elif target['battle']['parts'][body_part] == "Chest":
          target['battle']['def_debuff'] -= 0.5
          target['battle']['OH_kill'] += 1
          print(f"{target['name']}'s defense down!")
          target['battle']['str_debuff'] -= 0.25
          print(f"{target['name']}'s strength down!")
        elif target['battle']['parts'][body_part] == "Left Arm" or target['battle']['parts'][body_part] == "Right Arm":
          target['battle']['str_debuff'] -= 0.3
          target['battle']['OH_kill'] += 1
          print(f"{target['name']}'s strength down!")
        elif target['battle']['parts'][body_part] == "Left Leg" or target['battle']['parts'][body_part] == "Right Leg":
          target['battle']['spd_debuff'] -= 0.3
          target['battle']['OH_kill'] += 1
          print(f"{target['name']}'s speed down!")
        target['battle']['parts'].remove(target['battle']['parts'][body_part])
        input("Press Enter to Continue")
        print("\n")
        continue
        


          

# gets saves from json file
saves = open_json()
# option lists
start = ["Play", "Delete Save", "Quit"]
save_op = [
    "Select one of the saves below:",
    "Please paste the JSON object into the console: ",
    "Select one of the saves below:"
]
people_types = ["NPC", "Party Member", "Enemy"]
genders = ["Male", "Female"]
locations = ["Tavern", "Dungeon", "View Your Party"]

# global vars
save = None
char = None
party = None
recruits = None
stats = None

# dicts of values for different race, weapon, and armor choices, as well as lists of the choice names. (this takes up so many lines)
races = {
    'Human': {
        'spd': 3,
        'def': 2,
        'str': 2
    },
    'Elf': {
        'spd': 5,
        'def': 1,
        'str': 3
    },
    'Dwarf': {
        'spd': 1,
        'def': 5,
        'str': 4
    },
    'Orc': {
        'spd': 2,
        'def': 3,
        'str': 3
    }
}
r_list = list(races.keys())
weapons = [{
    'Short Sword': {
        'spd': 0,
        'str': 2,
        'ide_ran': 2,
        'def': 0
    },
    '2H Sword': {
        'spd': -2,
        'str': 4,
        'ide_ran': 3,
        'def': 0
    },
    'Crossbow': {
        'spd': -1,
        'str': 5,
        'ide_ran': 5,
        'def': 0
    }
}, {
    'Bow and Arrow': {
        'spd': 0,
        'str': 4,
        'ide_ran': 5,
        'def': 0
    },
    'Daggers': {
        'spd': 0,
        'str': 3,
        'ide_ran': 1,
        'def': 0
    },
    'Staff': {
        'spd': 0,
        'str': 2,
        'ide_ran': 3,
        'def': 0
    }
}, {
    'War Hammer': {
        'spd': -2,
        'str': 5,
        'ide_ran': 2,
        'def': 0
    },
    'Pickaxe': {
        'spd': -1,
        'str': 3,
        'ide_ran': 2,
        'def': 0
    },
    'Studded Shield': {
        'spd': -3,
        'str': 0,
        'ide_ran': 1,
        'def': 3
    }
}, {
    'Battle Axe': {
        'spd': -1,
        'str': 4,
        'ide_ran': 3,
        'def': 0
    },
    'Poleaxe': {
        'spd': -3,
        'str': 5,
        'ide_ran': 4,
        'def': 0
    },
    'Mace': {
        'spd': 0,
        'str': 2,
        'ide_ran': 2,
        'def': 0
    }
}]
w_list = []
for i in weapons:
    w_list.append(list(i.keys()))
armours = {
    'Leather Armour': {
        'spd': 0,
        'def': 1
    },
    'Chainmail Armour': {
        'spd': -1,
        'def': 2
    },
    'Plated Armour': {
        'spd': -3,
        'def': 4
    }
}
a_list = list(armours.keys())

# run forever unless broken
while True:
  # ask usr if they want to play, delete save, or quit
  ans = list_verify("Dungeon Crawler Sim", start)
  # get the custom list of save names
  save_list = grab_saves()
  # gets message based off of selected input
  msg = save_op[ans]
  if not ans: # if they want to play the game
    save_i = list_verify(msg, save_list, True) # asks usr which save
    if type(save_i) is str:
      continue
    save = load_save(saves, ans, save_i) # loads the save, and makes a new one if the save slot is empty
          # asks them which location they'd like to go
    print("To Quit at any time, hit Ctrl+C\n")
    while True:
      try:
          save = load_save(saves, ans, save_i) # loads the save when it loops to update info
          new_location = list_verify("You step into the Courtyard, it's peaceful. You shouldn't stay for long, there's work to be done. Where would you like to go?", locations)
          # based off of answer, run the appropriate function
          if not new_location:
            tavern()
          elif new_location == 1:
            battle(char, party)
          else:
            party_screen(char, party)
          if not save:
            save_json(save, save_i)
            break
      except KeyboardInterrupt:
        # if they hit ctrl+c save the game to the json file and return
          print("\nSaving and Quitting to Home Screen...\n")
          save_json(save, save_i)
          break
  elif ans == 1: # if usr wants to delete a save
    # if there are no sves, display that and skip over the rest
    if not save_list:
      print("You have no saves")
    else:
      # else ask usr which save slot they'd like to clear
      remove = list_verify("Pick a save slot to clear: ", save_list, True)
      if type(remove) is str:
        continue
      # find the save slot they referenced and save an empty value to it
      print("Save Slot Cleared") if saves[remove] else print("Save slot is already empty")
      saves[remove] = None
      save_json(None, remove)
  else: # if they want to quit, break the loop
    break

#