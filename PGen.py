import random

Uppercases='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Lowercases='abcdefghijklmnopqyrstuvwxyz'
Numbers='0123456789'
Symbols='!@#$&*?_-'

n=int(input("\nEnter the length of the password: "))
def typeselect():
    print("\nSelect from the following combinations to generate the password:\n")
    print("1. UPPERCASE LETTERS")
    print("2. LOWERCASE LETTERS")
    print("3. NUMBERS")
    print("4. SYMBOLS")
    print("5. UPPERCASE LETTERS + LOWERCASE LETTERS")
    print("6. UPPERCASE LETTERS + NUMBERS")
    print("7. UPPERCASE LETTERS + SYMBOLS")
    print("8. LOWERCASE LETTERS + NUMBERS")
    print("9. LOWERCASE LETTERS + SYMBOLS")
    print("10. NUMBERS + SYMBOLS")
    print("11. UPPERCASE LETTERS + LOWERCASE LETTERS + NUMBERS")
    print("12. UPPERCASE LETTERS + LOWERCASE LETTERS + SYMBOLS")
    print("13. LOWERCASE LETTERS + NUMBERS + SYMBOLS")
    print("14. UPPERCASE LETTERS + NUMBERS + SYMBOLS")
    print("15. UPPERCASE LETTERS + LOWERCASE LETTERS +  SYMBOLS")
    choice=int(input("\nEnter your choice: "))
    return choice

def lsgen(choice):
    ls=""
    if choice==1:
        ls+=Uppercases
    elif choice==2:
        ls+=Lowercases
    elif choice==3:
        ls+=Numbers
    elif choice==4:
        ls+=Symbols
    elif choice==5:
        ls=ls+Uppercases+Lowercases
    elif choice==6:
        ls=ls+Uppercases+Numbers
    elif choice==7:
        ls=ls+Uppercases+Symbols
    elif choice==8:
        ls=ls+Lowercases+Numbers
    elif choice==9:
        ls=ls+Lowercases+Symbols
    elif choice==10:
        ls=ls+Numbers+Symbols
    elif choice==11:
        ls=ls+Uppercases+Lowercases+Numbers
    elif choice==12:
        ls=ls+Uppercases+Lowercases+Symbols
    elif choice==13:
        ls=ls+Lowercases+Numbers+Symbols
    elif choice==14:
        ls=ls+Uppercases+Numbers+Symbols
    elif choice==15:
        ls=ls+Uppercases+Lowercases+Numbers+Symbols
    return ls
def rangen(str1):
    strf=""
    for i in range(n):
        a=random.randint(0,len(str1)-1)
        strf+=str1[a]
    print(strf)
choice=typeselect()
strchr=lsgen(choice)
rangen(strchr)