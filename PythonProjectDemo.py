name = input("Hey Type Your Name: ")
print("Hello "+ name + " Welcome to my game!")

should_we_play = input("Do you want to play?").lower()

if should_we_play == "yes" or 'y':
    print("Get Ready For some Adventure",name )

    direction = input("Do You want to go left or Right? (left/Right)").lower()
    if direction == 'left':
        print("You went left and fell of a cliff, game Over, Try again.")
    elif direction == "right":
        Choice = input("Okay, You now see a Bridge, do you want to swim under it or cross it?")
        if Choice == "Swim":
            print("You Got eaten by an aligater, You die, The End!")
        else:
            print("You Found The Gold And Won")
    else:
        print('Sorry not a valid replay, you die!')
else:
    print("May be someother Time Then Bye Bye!")