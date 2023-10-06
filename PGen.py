import random

def build_selection(Uchoice,Lchoice,Nchoice,Schoice):
    build=''
    Uppercases='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    Lowercases='abcdefghijklmnopqyrstuvwxyz'
    Numbers='0123456789'
    Symbols='!@#$&*?_-'
    if (Uchoice==1):
        build+=Uppercases
    if (Lchoice==1):
        build+=Lowercases
    if (Nchoice==1):
        build+=Numbers
    if (Schoice==1):
        build+=Symbols
    return build

def random_generation(length,Uchoice,Lchoice,Nchoice,Schoice):
    build=build_selection(Uchoice,Lchoice,Nchoice,Schoice)
    randomised_build=''
    for i in range(length):
        a=random.randint(0,len(build)-1)
        randomised_build+=build[a]
    return randomised_build