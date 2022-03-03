from libcardet import libcardet as lcd

def main():
    vehicle_num = input(f"{lcd.tmcolors.OKCYAN}[*] Enter vehicle number to get details: {lcd.tmcolors.ENDC}")
    data = lcd.get_details(vehicle_num)
    for i in list(data):
        print(f"{lcd.tmcolors.OKGREEN}[+] {i}: {data[i]}{lcd.tmcolors.ENDC}")

if __name__ == '__main__':
    main()