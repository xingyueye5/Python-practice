import imageio.v2 as imageio
import glob

outfilename = "my.gif"  # 转化的GIF图片名称

filenames = glob.glob('D:/Desktop/giftest/*.jpg')
frames = []
for image_name in filenames:
    im = imageio.imread(image_name)
    frames.append(im)
imageio.mimsave(outfilename, frames, 'GIF', duration=0.01)  # 生成方式也差不多
