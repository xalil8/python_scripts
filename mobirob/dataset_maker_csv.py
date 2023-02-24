import cv2
import numpy as np
import random
from os import listdir
import pandas as pd


def letter_finder(name):
    if name == "colon":
        return ":"

    elif name == "left_parentheses":
        return "("

    elif name == "right_parentheses":
        return ")"

    elif name == "coma":
        return ","

    elif name == "weird_a":
        return "Ã"

    elif name == "weird_a_2":
        return "Â"

    elif name == "slash":
        return "/"

    elif name == "low_s":
        return "s"

    elif name == "low_p":
        return "p"

    elif name == "low_l":
        return "l"

    elif name == "low_k":
        return "k"

    elif name == "low_i":
        return "i"

    elif name == "low_g":
        return "g"

    elif name == "low_b":
        return "b"

    elif name == "low_a":
        return "a"

    elif name == "dot":
        return "."

    # özel caseler dışındaki diğer harflerin isimlendirmesinde sıkıntı olmadığı için kendini string olarak dönüyor
    else:
        return name


def word_maker(num_of_let):
    empty_matrix_color = 255
    oversize = 100
    add_size = int(oversize / 2)
    letter_path = "letters_new"     #show path here
    letter_list = [f for f in listdir(letter_path)]

    b = 1/20
    a = 15/20
    c = 4/20

    letter_prob= {'+.png':b,
                  ',.png':b,
                  '-.png':b,
                  '0.png':b,
                  '1.png':a,
                  '2.png':a,
                  '3.png':a,
                  '4.png':a,
                  '5.png':a,
                  '6.png':a,
                  '7.png':a,
                  '8.png':a,
                  '9.png':a,
                  '@.png':b,
                  'A.png':a,
                  'B.png':a,
                  'C.png':a,
                  'colon.png':b,
                  'coma.png':b,
                  'D.png':a,
                  'dot.png':b,
                  'E.png':a,
                  'F.png':a,
                  'G.png':a,
                  'H.png':a,
                  'I.png':a,
                  'J.png':a,
                  'K.png':a,
                  'L.png':a,
                  'left_parentheses.png':b,
                  'low_a.png':c,
                  'low_b.png':c,
                  'low_g.png':c,
                  'low_i.png':c,
                  'low_k.png':c,
                  'low_l.png':c,
                  'low_p.png':c,
                  'low_s.png':c,
                  'M.png':a,
                  'N.png':a,
                  'O.png':a,
                  'P.png':a,
                  'Q.png':a,
                  'R.png':a,
                  'right_parentheses.png':b,
                  'S.png':a,
                  'slash.png':a,
                  'T.png':a,
                  'U.png':a,
                  'V.png':a,
                  'W.png':a,
                  'weird_a.png':b,
                  'weird_a_2.png':b,
                  'X.png':a,
                  'Y.png':a,
                  'Z.png':a}

    probab = tuple(letter_prob.values())
    word = []
    g_adjust_list = []
    pad_thick = 125
    h_key = 480
    image_list = []


    for i in range(num_of_let):

        random_letter_path = random.choices(letter_list, weights=probab, k=56)
        letter_path = random.choice(random_letter_path)
        word.append(letter_finder(letter_path[:-4]))
        image = cv2.imread("letters/" + letter_path)

        if letter_path[:-4] == "low_p" or letter_path[:-4] == "low_g":
            g_adjust_list.append(60)

        elif letter_path[:-4] =="+" or letter_path[:-4] =="-":
            g_adjust_list.append(-40)

        else:
            g_adjust_list.append(0)

        image_list.append(image)

    key = "".join(word)


    if num_of_let == 2:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]

        vis = np.zeros((h_key, w1 + w2 , 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]



    elif num_of_let == 3:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]

        vis = np.zeros((h_key, w1 + w2 + w3 , 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]
        vis[h_key-h3-pad_thick+g_adjust_list[2]:h_key-pad_thick+g_adjust_list[2],\
        w1 + w2:w1 + w2 + w3, :3] = image_list[2]


    elif num_of_let == 4:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]

        vis = np.zeros((h_key, w1 + w2 + w3 + w4, 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]
        vis[h_key-h3-pad_thick+g_adjust_list[2]:h_key-pad_thick+g_adjust_list[2],\
        w1 + w2:w1 + w2 + w3, :3] = image_list[2]
        vis[h_key-h4-pad_thick+g_adjust_list[3]:h_key-pad_thick+g_adjust_list[3],\
        w1 + w2 + w3:w1 + w2 + w3 + w4 , :3] = image_list[3]

    elif num_of_let == 5:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]

        vis = np.zeros((h_key, w1 + w2 + w3 + w4 + w5 , 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]
        vis[h_key-h3-pad_thick+g_adjust_list[2]:h_key-pad_thick+g_adjust_list[2],\
        w1 + w2:w1 + w2 + w3, :3] = image_list[2]
        vis[h_key-h4-pad_thick+g_adjust_list[3]:h_key-pad_thick+g_adjust_list[3],\
        w1 + w2 + w3:w1 + w2 + w3 + w4 , :3] = image_list[3]
        vis[h_key-h5-pad_thick+g_adjust_list[4]:h_key-pad_thick+g_adjust_list[4],\
        w1 + w2 + w3 + w4:w1 + w2 + w3 + w4 + w5, :3] = image_list[4]


    elif num_of_let == 6:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]
        h6, w6 = image_list[5].shape[0:2]


        vis = np.zeros((h_key, w1 + w2 + w3 + w4 + w5 + w6, 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]
        vis[h_key-h3-pad_thick+g_adjust_list[2]:h_key-pad_thick+g_adjust_list[2],\
        w1 + w2:w1 + w2 + w3, :3] = image_list[2]
        vis[h_key-h4-pad_thick+g_adjust_list[3]:h_key-pad_thick+g_adjust_list[3],\
        w1 + w2 + w3:w1 + w2 + w3 + w4 , :3] = image_list[3]
        vis[h_key-h5-pad_thick+g_adjust_list[4]:h_key-pad_thick+g_adjust_list[4],\
        w1 + w2 + w3 + w4:w1 + w2 + w3 + w4 + w5, :3] = image_list[4]
        vis[h_key-h6-pad_thick+g_adjust_list[5]:h_key-pad_thick+g_adjust_list[5], \
        w1 + w2 + w3 + w4 + w5 :w1 + w2 + w3 + w4 + w5 + w6, :3] = image_list[5]

    elif num_of_let == 7:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]
        h6, w6 = image_list[5].shape[0:2]
        h7, w7 = image_list[6].shape[0:2]

        vis = np.zeros((h_key, w1 + w2 + w3 + w4 + w5 + w6 + w7, 3), np.uint8)
        vis.fill(empty_matrix_color)


        vis[h_key-h1-pad_thick+g_adjust_list[0]:h_key-pad_thick+g_adjust_list[0],\
        :w1, :3] = image_list[0]
        vis[h_key-h2-pad_thick+g_adjust_list[1]:h_key-pad_thick+g_adjust_list[1],\
        w1:w1 + w2, :3] = image_list[1]
        vis[h_key-h3-pad_thick+g_adjust_list[2]:h_key-pad_thick+g_adjust_list[2],\
        w1 + w2:w1 + w2 + w3, :3] = image_list[2]
        vis[h_key-h4-pad_thick+g_adjust_list[3]:h_key-pad_thick+g_adjust_list[3],\
        w1 + w2 + w3:w1 + w2 + w3 + w4 , :3] = image_list[3]
        vis[h_key-h5-pad_thick+g_adjust_list[4]:h_key-pad_thick+g_adjust_list[4],\
        w1 + w2 + w3 + w4:w1 + w2 + w3 + w4 + w5, :3] = image_list[4]
        vis[h_key-h6-pad_thick+g_adjust_list[5]:h_key-pad_thick+g_adjust_list[5],\
        w1 + w2 + w3 + w4 + w5 :w1 + w2 + w3 + w4 + w5 + w6, :3] = image_list[5]
        vis[h_key-h7-pad_thick+g_adjust_list[6]:h_key-pad_thick+g_adjust_list[6],\
        w1 + w2 + w3 + w4 + w5 + w6 :w1 + w2 + w3 + w4 + w5 + w6 + w7, :3] = image_list[6]

    else:
        print("letter number should be between 2-7")
        return

    padded = cv2.copyMakeBorder(vis, 0, 0, 60, 60, 1,(0,0,0))
    return padded, key



def sentence_maker(number_of_words=1):
    global final_sentence
    #2 tane liste , biri image dosyalarını tutuyor, diğeri text için string
    sentence = []
    words_list = []

    for i in range(number_of_words):
        word = word_maker(random.randrange(2, 8))
        words_list.append(word[0])
        sentence.append(word[1])

        final_sentence = " ".join(sentence)


    if number_of_words == 1:
        vis = words_list[0]
        return vis, final_sentence



    elif number_of_words == 2:

        h1, w1 = words_list[0].shape[0:2]
        h2, w2 = words_list[1].shape[0:2]


        vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
        vis.fill(177)

        vis[:h1, :w1, :3] = words_list[0]
        vis[:h2, w1:w1 + w2, :3] = words_list[1]
        return vis, final_sentence


    elif number_of_words == 3:
        h1, w1 = words_list[0].shape[0:2]
        h2, w2 = words_list[1].shape[0:2]
        h3, w3 = words_list[2].shape[0:2]

        vis = np.zeros((max(h1, h2, h3), w1 + w2 + w3, 3), np.uint8)
        vis.fill(255)

        vis[:h1, :w1, :3] = words_list[0]
        vis[:h2, w1:w1 + w2, :3] = words_list[1]
        vis[:h3, w1 + w2:w1 + w2 + w3, :3] = words_list[2]

        return vis, final_sentence





def write_data(number_of_image):
    list1 = []
    list2 = []

    for i in range(number_of_image):
        data = sentence_maker(random.randrange(1, 4))
        cv2.imwrite(f"C:/Users/ozcan/Desktop/dataset_for_robot/image{str(i)}.png", data[0])

        list1.append(data[1])
        list2.append(f"image{str(i)}.png")


    csv_list = {"filename": list2, "words": list1}
    df = pd.DataFrame(data=csv_list)
    csv_path = 'C:/Users/ozcan/Desktop/dataset_for_robot/out.csv'
    df.to_csv(csv_path, index=False)
    print("All process Done")


