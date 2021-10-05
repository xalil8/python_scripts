
def word_maker(num_of_let):
    oversize = 100
    add_size = int(oversize / 2)
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)

    letter_list = [f for f in listdir("letters")]
    image_list = []
    heights = {}
    widths = {}

    for i in range(num_of_let):
        #print(name, img)
        image = cv2.imread("letters/" + str(random.choice(letter_list)))
        #heights[f"h{i}"], widths[f"w{i}"]= image.shape[0:2]
        image_list.append(image)


    #word cases
    if num_of_let == 2:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        vis = np.zeros((max(h1, h2)+ oversize, w1 + w2 + oversize, 3), np.uint8)
        vis.fill(255)

        vis[add_size:h1+add_size, add_size:w1+add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1+add_size:w1+add_size + w2, :3] = image_list[1]

        cv.imshow("test", vis)
        cv.waitKey(0)

    elif num_of_let ==3:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        vis = np.zeros((max(h1, h2, h3) + oversize, w1 + w2 + w3 + oversize, 3), np.uint8)
        vis.fill(255)

        vis[add_size:h1+add_size, add_size:w1 + add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1 + add_size:w1 + w2 + add_size, :3] = image_list[1]
        vis[add_size:h3+add_size, w1 + w2 + add_size:w1 + w2 + w3 + add_size, :3] = image_list[2]

        cv.imshow("test", vis)
        cv.waitKey(0)

    elif num_of_let ==4:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        vis = np.zeros((max(h1, h2, h3, h4) + oversize, w1 + w2 + w3 + w4 + oversize, 3), np.uint8)
        vis.fill(255)

        vis[add_size:h1+add_size, add_size:w1 + add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1 + add_size:w1 + w2 + add_size, :3] = image_list[1]
        vis[add_size:h3+add_size, w1 + w2 + add_size:w1 + w2 + w3 + add_size, :3] = image_list[2]
        vis[add_size:h4+add_size, w1 + w2 + w3 + add_size:w1 + w2 + w3 + w4 + add_size, :3] = image_list[3]

        cv.imshow("test", vis)
        cv.waitKey(0)

    elif num_of_let ==5:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]
        vis = np.zeros((max(h1, h2, h3, h4, h5) + oversize, w1 + w2 + w3 + w4 + w5 + oversize, 3), np.uint8)
        vis.fill(255)

        vis[add_size:h1+add_size, add_size:w1 + add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1 + add_size:w1 + w2 + add_size, :3] = image_list[1]
        vis[add_size:h3+add_size, w1 + w2 + add_size:w1 + w2 + w3 + add_size, :3] = image_list[2]
        vis[add_size:h4+add_size, w1 + w2 + w3 + add_size:w1 + w2 + w3 + w4 + add_size, :3] = image_list[3]
        vis[add_size:h5+add_size, w1 + w2 + w3 + w4 + add_size:w1 + w2 + w3 + w4 + w5 + add_size, :3] = image_list[4]

        cv.imshow("test", vis)
        cv.waitKey(0)

    elif num_of_let ==6:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]
        h6, w6 = image_list[5].shape[0:2]
        vis = np.zeros((max(h1, h2, h3, h4, h5, h6) + oversize, w1 + w2 + w3 + w4 + w5 + w6 + oversize, 3), np.uint8)
        vis.fill(255)

        vis[add_size:h1+add_size, add_size:w1 + add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1 + add_size:w1 + w2 + add_size, :3] = image_list[1]
        vis[add_size:h3+add_size, w1 + w2 + add_size:w1 + w2 + w3 + add_size, :3] = image_list[2]
        vis[add_size:h4+add_size, w1 + w2 + w3 + add_size:w1 + w2 + w3 + w4 + add_size, :3] = image_list[3]
        vis[add_size:h5+add_size, w1 + w2 + w3 + w4 + add_size:w1 + w2 + w3 + w4 + w5 + add_size, :3] = image_list[4]
        vis[add_size:h6+add_size, w1 + w2 + w3 + w4 + w5 + add_size:w1 + w2 + w3 + w4 + w5 + w6 + add_size, :3] = image_list[5]

        cv.imshow("test", vis)
        cv.waitKey(0)

    elif num_of_let ==7:
        h1, w1 = image_list[0].shape[0:2]
        h2, w2 = image_list[1].shape[0:2]
        h3, w3 = image_list[2].shape[0:2]
        h4, w4 = image_list[3].shape[0:2]
        h5, w5 = image_list[4].shape[0:2]
        h6, w6 = image_list[5].shape[0:2]
        h7, w7 = image_list[6].shape[0:2]

        vis = np.zeros((max(h1, h2, h3, h4, h5, h6, h7)+ oversize, w1 + w2 + w3 + w4 + w5 + w6 + w7 + oversize, 3), np.uint8)
        vis.fill(255)
        vis[add_size:h1+add_size, add_size:w1+add_size, :3] = image_list[0]
        vis[add_size:h2+add_size, w1+add_size:w1 + w2+add_size, :3] = image_list[1]
        vis[add_size:h3+add_size, w1 + w2+add_size:w1 + w2 + w3+add_size, :3] = image_list[2]
        vis[add_size:h4+add_size, w1 + w2 + w3+add_size:w1 + w2 + w3 + w4+add_size, :3] = image_list[3]
        vis[add_size:h5+add_size, w1 + w2 + w3 + w4+add_size:w1 + w2 + w3 + w4 + w5+add_size, :3] = image_list[4]
        vis[add_size:h6+add_size, w1 + w2 + w3 + w4 + w5+add_size:w1 + w2 + w3 + w4 + w5 + w6+add_size, :3] = image_list[5]
        vis[add_size:h7+add_size, w1 + w2 + w3 + w4 + w5 + w6+add_size:w1 + w2 + w3 + w4 + w5 + w6 + w7+add_size, :3] = image_list[6]

        #cv2.imwrite("C:/Users/ozcan/Desktop/dataset_for_robot/deneme.png", vis)
        cv.imshow("test", vis)
        cv.waitKey(0)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        return

    cv2.destroyAllWindows()

word_maker(7)
