from PIL import Image

DIR_INPUT = 'C:/Users/ma125/OneDrive - purdue.edu/2018 Fall/CS501/Project/' 

def binary(path):
    img = Image.open(path)
    # img = img.rotate(270)
    thresh = 80
    fn = lambda x : 0 if x > thresh else 255
    r = img.convert('L').point(fn, mode='1')
    r = r.rotate(270)
    r.save(DIR_INPUT+'GUI/2.jpg')


