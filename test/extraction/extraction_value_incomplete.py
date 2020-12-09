import Spuit as sp


# sp.get_image('lowvaluecolor\lowvaluecolor1118.jpg')
for i in range(1204):
    try:    
        image_path = "lowvaluecolor\lowvaluecolor"+str(i)+".jpg"
        print(i)
        spuit_image = sp.Spuit(image_path)
        print(spuit_image.get_hex())
        print(spuit_image.get_hsv())
        # print(spuit_image.get_hsv360())
            # print(spuit_image.get_hsv_origin())
    except ValueError as e:
        # print(i,'번 에러')
        pass


   