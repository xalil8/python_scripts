import re

tapa_list1 = ['91V E2 123423 562494 077430', 'E13 RT 078546 392772 829250', '3MS M3 660071 713956 069164',
              '2EV Q3 256566 880134 165653', 'AS3 AQ 284945 987709 427633', '94M M0 058921 283188 466709',
              '0EV M5 233333 204641 077430', '23D SM 329511 135877 348643', 'M55 K3 580703 021743 363111',
              'S1V G9 346366 115397 380428', 'C23 KS 506019 739575 360746', 'KM3 I5 868575 120893 357870',
              '51Y K9 002042 729510 855414', 'B2F MK 224387 486849 297275', 'SP3 E4 488107 366773 734109']


tapa_list2 = ['91V E2 123423 562494 077430', 'E13 RT 078546 392772 829250', '3MS M3 660071 713956 069164',
              '2EV Q3 256566 880134 165653', 'AS3 AQ 284945 987709 427633', '94M M0 058921 283188 466709',
              '0EV M5 233333 204641 077430', '23D SM 329511 135877 348643', 'M55 K3 580703 021743 363111',
              'S1V G9 346366 115397 380428', 'C23 KS 506019 739575 360746', 'KM3 I5 868575 120893 357870',
              '51Y K9 002042 729510 855414', 'B2F AQ 224387 486849 297275', 'M3A E4 12J5N3 232SS0 93934M',
              '95M 9S ZZ3Y46 F457NK RETLF2', 'OER 3M 432555 D34MDK 32MSMD', 'KDS QQ KDM32M 99DMVK SDIF4M']

ocr_data = ['206358 E4 91J 214657 203233', 'B2F MK 224387 486849 297275', 'S1V G9 346366 115397 380428']


def match(inp1):
    for i in range(len(tapa_list1)):
        word_list = inp1[i].split()
        print(len(word_list))
        for j in range(len(word_list)):
            #print(tapa_list1[i][j])
            pass


def trying(tapa, ocr):
    matching_list = []
    for i in ocr:
        for t in i.split():
            key = t
            for j in tapa:
                for m in j.split():
                    if re.search(key, m):
                        if extra_check(i, j):
                            #print(f"tapa {tapa.index(i)} and {ocr.index(j)} exactly matching")
                            matching_list.append(f"ocr{ocr.index(j)}----tapa{tapa.index(i)}")

                        #print(key, "found", "in", j)

    return matching_list


def extra_check(ocr, tapa):
    """succes = 0
    for i in ocr.split():
        for a in tapa.split():
            print(i,"  ", a)"""
    if ocr == tapa:
        #print(f"{ocr} and {tapa} exactly same ")
        return True
    else:
        return False


#print(set(trying(tapa_list1, ocr_data)))


def letter_matching(tapa, ocr):
    tapa = tapa.replace(" ", "")
    ocr = ocr.replace(" ", "")

    print(tapa, ocr)
    error = []
    if len(tapa) > len(ocr):

        for i in range(len(ocr)):
            if tapa[i] != ocr[i]:
                error.append(f"{tapa} and {ocr} '{i}' letter not matching")

    elif len(ocr) > len(tapa):

        for i in range(len(tapa)):
            if tapa[i] != ocr[i]:
                error.append(f"{tapa} and {ocr} '{i}' letter not matching")

    elif len(tapa) == len(ocr):

        for i in range(len(tapa)):
            if tapa[i] != ocr[i]:
                error.append(f"{tapa} and {ocr} '{i}' letter not matching")

    error_percentage = (len(error) / len(tapa)) * 100

    return error_percentage







