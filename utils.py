

def ppf(a):
    print("[:>] " + a)


def regular_str(a, alen):
    b = str(a) + ' '*alen
    return b[:alen-1]


def pf_menu_and_chose(menu, promote="ans"):
    print()
    for i,a in enumerate(menu):
        print(f"({i}) {a}")
    ans = input(f"{promote} = ")
    if len(ans)==0:
        return None
    return ans