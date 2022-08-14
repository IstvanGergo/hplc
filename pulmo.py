import pandas as pd
# Debugolni kell a fájlba írást sima metódusoknál


def gradiens(nev):
    a = [0, "mL"]  # a eluens mennyisége
    b = [0, "mL"]  # b eluens mennyisége
    # eluens sebesség
    while True:
        try:
            grad_seb = float(input("Add meg az eluens sebességét (mL/min): \n"))  # ml/min
            assert 5 > grad_seb > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy 5-nél kisebb pozitív számot!")
    # arányok száma
    while True:
        try:
            aranyok = int(input("Adja meg, hány aránypárt fog használni: "))
            assert 6 > aranyok > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy pozitív egész számot!")
    # minták száma
    while True:
        mintak_szama = input("Adja meg a minták számát: ")
        try:
            mintak_szama = int(mintak_szama)
            assert mintak_szama > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy pozitív egész számot!")
    # standardek száma
    while True:
        try:
            std_szama = int(input("Adja meg a standardek számát: "))
            assert std_szama > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy pozitív egész számot!")
    a_arany = []
    b_arany = []
    # A és B eluens arányai
    while len(a_arany) != aranyok:
        try:
            megadott = int(input(f"Adja meg az {len(a_arany) + 1}. százalékát az A eluensnek (0-100): "))
            if megadott > 100:
                print("Nem lehet a százalék nagyobb 100-nál!")
            if megadott <= 100:
                a_arany.append(megadott)
                b_arany.append(100 - megadott)
        except ValueError:
            print("írj be egy érvényes számot!")
    print(f"A eluenshez tartozó arányok: {a_arany}")
    print(f"B eluenshez tartozó arányok: {b_arany}")
    while len(a_arany) < 5:
        a_arany.append(0)
        b_arany.append(0)
    idok = []
    # Arányok futási idejei
    while len(idok) != aranyok:
        try:
            megadott = int(input(f"Adja meg az {len(idok) + 1}. arány futási idejét: "))
            assert 50 > megadott > 0
            idok.append(megadott)
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy 50-nél kisebb pozitív egész számot!")

    ossz_ido = (sum(idok) * (mintak_szama + std_szama))
    # A és B eluens mennyiségének kiszámolása
    for _ in range(mintak_szama + std_szama):
        for i, j in zip(a_arany, idok):
            a[0] += i/100 * j * grad_seb
        for i, j in zip(b_arany, idok):
            b[0] += i/100 * j * grad_seb
    while len(idok) < 5:
        idok.append(0)
    #  Dataframe-be írás
    df2 = pd.DataFrame([[nev, grad_seb, a_arany[0], a_arany[1], a_arany[2], a_arany[3], a_arany[4], b_arany[0],
                        b_arany[1], b_arany[2], b_arany[3], b_arany[4], idok[0], idok[1], idok[2], idok[3],
                        idok[4], mintak_szama, std_szama, a[0], b[0]]])
    #  Fileba írás
    df2.to_csv('gradiens.csv', sep=";", mode='a', index=False, header=False, encoding="cp1250")
    if a[0] > 1000:
        a[1] = "L"
        a[0] /= 1000
    if b[0] > 1000:
        b[1] = "L"
        b[0] /= 1000
    a[0] = round(a[0], 4)
    b[0] = round(b[0], 4)
    print(f"Az A eluensből {a[0]} {a[1]}, a B eluensből {b[0]} {b[1]} szükséges a méréshez.")
    print(f"A mérés összesen {int(ossz_ido/60)} óra {ossz_ido%60} percig tart tart")


def gradiens_fajlbol(fnev):
    index = df[df['Mérés neve'] == fnev].index.item()
    a = [0, "mL"]
    b = [0, "mL"]
    grad_seb = df.iloc[index, 1]
    # Arányok és  futási idejeik
    a_arany = [df.iloc[index, i] for i in range(2, 7)]
    b_arany = [df.iloc[index, i] for i in range(7, 12)]
    idok = [[df.iloc[index, i] for i in range(12, 17)]][0]
    #  Minták száma
    mintak_szama = df.iloc[index, 17]
    helyes_e = input(f"A minták száma {mintak_szama.astype(int)}, ezt használja?")  # kérdés hogy a fájlban lévő jó-e
    if helyes_e != "i".lower():
        while True:
            mintak_szama = input("Adja meg a minták számát: ")
            try:
                mintak_szama = int(mintak_szama)
                assert mintak_szama > 0
                break
            except ValueError:
                print("írj be egy érvényes számot!")
            except mintak_szama < 1:
                print("írj be egy pozitív egész számot!")
    std_szama = df.iloc[index, 18]
    ossz_ido = (sum(idok) * (mintak_szama + std_szama))
    #  A és B eluens mennyiségének kiszámolása
    for _ in range(int(mintak_szama + std_szama)):
        for i, j in zip(a_arany, idok):
            a[0] += i/100 * j * grad_seb
        for i, j in zip(b_arany, idok):
            b[0] += i/100 * j * grad_seb
    # Fájl mentése, még a kerekítés előtt
    if pd.isnull(df.iloc[index, 19:20]).any:
        df.iloc[index, 19] = a[0]
        df.iloc[index, 20] = b[0]
        df.to_csv("gradiens.csv", index=False, encoding="cp1250", sep=";")

    if a[0] > 1000:
        a[1] = "L"
        a[0] /= 1000
    if b[0] > 1000:
        b[1] = "L"
        b[0] /= 1000
    a[0] = round(a[0], 4)
    b[0] = round(b[0], 4)

    print(f"Az A eluensből {a[0]} {a[1]}, a B eluensből {b[0]} {b[1]} szükséges a méréshez.")
    print(f"A mérés összesen {int(ossz_ido/60)} óra {ossz_ido%60} percig tart tart")


def izokratikus(nev):
    # eluens sebesség
    while True:
        try:
            izo_seb = float(input("Add meg az eluens sebességét (mL/min): \n"))  # ml/min
            assert 5 > izo_seb > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy 5-nél kisebb pozitív számot!")
    # minták száma
    while True:
        mintak_szama = input("Adja meg a minták számát: ")
        try:
            mintak_szama = int(mintak_szama)
            assert mintak_szama > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy pozitív egész számot!")
    # standardek száma
    while True:
        try:
            std_szama = int(input("Adja meg a standardek számát: "))
            assert std_szama > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy pozitív egész számot!")
    # minta mérési ideje
    while True:
        try:
            minta_ido = int(input("Adja meg egy minta mérési idejét: "))
            assert 120 > minta_ido > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy 120-nál kisebb pozitív számot!")
    # standard mérési ideje
    while True:
        try:
            std_ido = int(input("Adja meg egy standard mérési idejét: "))
            assert 120 > std_ido > 0
            break
        except ValueError:
            print("írj be egy érvényes számot!")
        except AssertionError:
            print("írj be egy 120-nál kisebb pozitív  számot!")
    mintak_osszido = minta_ido * mintak_szama
    std_osszido = std_ido * std_szama
    a = izo_seb * mintak_osszido + izo_seb * std_osszido  # eluens mennyisége
    ossz_ido = std_osszido + mintak_osszido
    # Dataframe-be írás
    df2 = pd.DataFrame([[nev, izo_seb, mintak_szama, std_szama, minta_ido, std_ido, a]])
    # Fileba írás
    df2.to_csv('izokratikus.csv', sep=";", mode='a', index=False, header=False, encoding="cp1250")
    if a > 1000:
        print(f'{a/1000} L eluens szükséges a méréshez.')
    if a < 1000:
        print(f'{a} mL eluens szükséges a méréshez.')
    print(f"A mérés összesen {int(ossz_ido / 60)} óra {ossz_ido % 60} percig tart tart")


def izokratikus_fajlbol(fnev):
    index = df[df['Mérés neve'] == fnev].index.item()
    izo_seb = df.iloc[index, 1]
    mintak_szama = df.iloc[index, 2]
    helyes_e = input(f"A minták száma {mintak_szama.astype(int)}, ezt használja?")  # kérdés hogy a fájlban lévő jó-e
    if helyes_e != "i".lower():
        while True:
            mintak_szama = input("Adja meg a minták számát: ")
            try:
                mintak_szama = int(mintak_szama)
                assert 50 > mintak_szama > 0
                break
            except ValueError:
                print("írj be egy érvényes számot!")
            except mintak_szama < 1:
                print("írj be egy 50-nél kisebb pozitív egész számot!")
    std_szama = df.iloc[index, 3]
    minta_ido = df.iloc[index, 4]
    std_ido = df.iloc[index, 5]
    mintak_osszido = minta_ido * mintak_szama
    std_osszido = std_ido * std_szama
    eluens = izo_seb * mintak_osszido + izo_seb * std_osszido  # eluens mennyisége
    ossz_ido = std_osszido + mintak_osszido
    if pd.isnull(df.iloc[index, 6]):
        df.iloc[index, 6] = eluens
        df.to_csv("izokratikus.csv", index=False, encoding="cp1250", sep=";")

    print(f'{eluens} mL eluens szükséges a méréshez.')
    print(f"A mérés összesen {int(ossz_ido / 60)} óra {ossz_ido % 60} percig tart tart")

nev = ''
df = pd.read_csv("gradiens.csv", sep=';', skipinitialspace=True, encoding="cp1250")

while True:
    #    nev = input("Adja meg a mérés nevét: ")
    #    meres_tipusa = input("Izokratikus vagy Gradiens mérés?")
    meres_tipusa = ''

    if "g" in meres_tipusa.lower():
        df = pd.read_csv("gradiens.csv", sep=';', skipinitialspace=True, encoding="cp1250")
        if (df['Mérés neve'] == nev).any():
            gradiens_fajlbol(nev)
        else:
            gradiens(nev)
    if "izo" in meres_tipusa.lower():
        df = pd.read_csv("izokratikus.csv", sep=';', skipinitialspace=True, encoding="cp1250")
        if (df['Mérés neve'] == nev).any():
            izokratikus_fajlbol(nev)
        else:
            izokratikus(nev)
