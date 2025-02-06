from PIL import Image, ImageDraw

def create_folder_icon():
    # 创建32x32的透明背景图像
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 文件夹主体颜色 - 使用蓝色
    folder_color = '#3498db'
    
    # 绘制文件夹主体
    draw.rectangle([(4, 8), (28, 26)], fill=folder_color)
    # 绘制文件夹顶部
    draw.rectangle([(4, 6), (14, 8)], fill=folder_color)
    
    # 保存图标
    img.save('assets/folder.png')

def create_file_icon():
    # 创建32x32的透明背景图像
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 文件颜色 - 使用浅灰色
    file_color = '#95a5a6'
    
    # 绘制文件主体
    draw.rectangle([(8, 4), (24, 28)], fill=file_color)
    # 绘制文件折角
    draw.polygon([(20, 4), (24, 8), (20, 8)], fill='#7f8c8d')
    
    # 保存图标
    img.save('assets/file.png')

if __name__ == '__main__':
    create_folder_icon()
    create_file_icon() 