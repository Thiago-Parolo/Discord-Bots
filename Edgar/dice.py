from random import choices

while True:
    user_input = input()
    split_input = user_input.split(' ')
    
    dice = split_input[0].split("d")

    die, times = dice[1], dice[0]

    rolls = choices(range(1, int(die)+1), k=int(times))

    msg = f"{rolls} → {sum(rolls)}"

    if len(split_input) == 2:
        skill = int(split_input[1])

        for roll in rolls:
            if roll > skill:
                msg += "\nFalhou!"
            elif roll > skill//2:
                msg += "\nSucesso normal!"
            elif roll > skill//5:
                msg += "\nSucesso bom!"
            else:
                msg += "\nSucesso extremo!"


    print(msg)