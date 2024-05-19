import pt13, pt14, pt15

s_0 = 100               # starting units of grass
l_0 = (1,1,1,1)         # starting condition of cows

while 1:
    while 1:
        try:
            comm = int(input("Which communication (13, 14 or 15)? "))
            if comm not in [13, 14, 15]:
                continue
            print(f"retrieving data from communication{comm} ...")
            break
        except ValueError as e:
            print("Invalid, please enter 13, 14 or 15")
            continue

    if comm == 13:
        # model
        pt13.revenue(0,s_0)

        while 1:
            # week
            while 1:
                try:
                    t = int(input("Which week are you in (0~51)? "))
                    if t not in range(52):
                        print("Invalid, please enter integer 0~51")
                        continue
                    break
                except ValueError as e:
                    print("Invalid, please enter integer 0~51")
                    continue
            # grass
            while 1:
                try:
                    s = int(input("How much grass is there on the field? "))
                    if s < pt13.required(t):
                        print("Insufficient pasture. Enjoy the steak!!")
                    break
                except ValueError as e:
                    print("Invalid, please enter an integer")
                    continue

            if (t,s) in pt13._revenue:
                print(f"feed the herd {pt13.required(t)+pt13._revenue[t, s][1]} units of grass")
                print(f"Keep following the strategy, the expected revenue would be ${round(pt13._revenue[t, s][0],2)}")
            else:
                print("Such situation should not occur based on given information.")

            if input("Do you wish to check another week, pasture combination for communication 13? (Y/N) ") not in "Yy":
                break

    elif comm == 14:
        pt14.revenue(0, s_0, 0)

        while 1:
            # week
            while 1:
                try:
                    t = int(input("Which week are you in (0~51)? "))
                    if t not in range(52):
                        print("Invalid, please enter integer 0~51")
                        continue
                    break
                except ValueError as e:
                    print("Invalid, please enter integer 0~51")
                    continue

            # number of dried cows
            while 1:
                try:
                    d = int(input("How many cows have been dried (0~4)? "))
                    if d not in range(5):
                        print("Invalid, please enter an integer (0~4)")
                        continue
                    break
                except ValueError as e:
                    print("Invalid, please enter an integer (0~4)")
                    continue

            # grass
            while 1:
                try:
                    s = int(input("How much grass is there on the field? "))
                    if s < pt14.required(t) - d * pt14.dryFeed:
                        print("Insufficient pasture. Enjoy the steak!!")
                    break
                except ValueError as e:
                    print("Invalid, please enter an integer")
                    continue

            if (t,s,d) in pt14._revenue:
                print(f"feed the herd {pt14.required(t)+pt14._revenue[t, s, d][1][0]} units of grass")
                print(f"additionally, dry {pt14._revenue[t, s, d][1][1]-d} cow")
                print(f"Keep following the strategy, the expected revenue would be ${round(pt14._revenue[t, s, d][0],2)}")
            else:
                print("Such situation should not occur based on given information.")

            if input("Do you wish to check another combination for communication 14? (Y/N) ") not in "Yy":
                break

    else:
        # model
        pt15.revenue(0, s_0, l_0)

        while 1:
            # week
            while 1:
                try:
                    t = int(input("Which week are you in (0~51)? "))
                    if t not in range(52):
                        print("Invalid, please enter integer 0~51")
                        continue
                    break
                except ValueError as e:
                    print("Invalid, please enter integer 0~51")
                    continue

            l = list(l_0)

            # Lily
            while 1:
                d = input("Is Lily dried? (Y/N) ")
                if d not in "YyNn":
                    print("Invalid, please enter (Y/N)")
                    continue
                if d in "Yy":
                    l[0] = 0
                if d in "Nn":
                    l[0] = 1
                break

            # Betty
            while 1:
                d = input("Is Betty dried? (Y/N) ")
                if d not in "YyNn":
                    print("Invalid, please enter (Y/N)")
                    continue
                if d in "Yy":
                    l[1] = 0
                if d in "Nn":
                    l[1] = 1
                break

            # Clover
            while 1:
                d = input("Is Clover dried? (Y/N) ")
                if d not in "YyNn":
                    print("Invalid, please enter (Y/N)")
                    continue
                if d in "Yy":
                    l[2] = 0
                if d in "Nn":
                    l[2] = 1
                break

             # Rosie
            while 1:
                d = input("Is Rosie dried? (Y/N) ")
                if d not in "YyNn":
                    print("Invalid, please enter (Y/N)")
                    continue
                if d in "Yy":
                    l[3] = 0
                if d in "Nn":
                    l[3] = 1
                break

            l = tuple(l)

            # grass
            while 1:
                try:
                    s = int(input("How much grass is there on the field? "))
                    if s < pt15.dryenergy(t, l):
                        print("Insufficient pasture. Enjoy the steak!!")
                    break
                except ValueError as e:
                    print("Invalid, please enter an integer")
                    continue

            if (t,s,l) in pt15._revenue:
                print(f"feed the herd {pt15.dryenergy(t, l)+pt15._revenue[t, s, l][1][0]} units of grass")
                for i in range(4):
                    if l[i] != pt15._revenue[t, s, l][1][1][i]:
                        print(f"additionally, dry {pt15.names[i]}")
                print(f"Keep following the strategy, the expected revenue would be ${round(pt15._revenue[t, s, l][0],2)}")
            else:
                print("Such situation should not occur based on given information.")

            if input("Do you wish to check another combination for communication 15? (Y/N) ") not in "Yy":
                break

    if input("Do you wish to quit (Y/N)? ") in "Yy":
        break

