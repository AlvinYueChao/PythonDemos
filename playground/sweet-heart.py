import random
from math import sin, cos, pi, log
from tkinter import *
from concurrent.futures import ThreadPoolExecutor

CANVAS_WIDTH = 640  # 画布宽度
CANVAS_HEIGHT = 480  # 画布高度
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的x坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的y坐标
IMAGE_ENLARGE = 11  # 图像放大的比例

HEART_COLOR = "#FF99CC"  # 设置爱心的颜色
TXT_DATE = "Yue ❤ Huang"  # 设置文本内容
TXT_COLOR = "#FF99CC"  # 设置字体颜色
Frames_Number = 60  # 动画刷新的帧数


# 窗口居中显示的辅助函数
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
    screenheight = root.winfo_screenheight()  # 获取显示屏高度
    size = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2,
                            (screenheight - height) / 2)  # 设置窗口居中参数
    root.geometry(size)  # 让窗口居中显示


# 定义计算爱心形状的函数
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    # 使用参数t计算爱心形状的x和y坐标，并根据缩放比例进行缩放
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # 根据缩放比例进行缩放
    x *= shrink_ratio
    y *= shrink_ratio

    # 将计算出的坐标移动到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    # 返回整型的坐标值
    return int(x), int(y)


# 在爱心内部根据beta值生成随机点
def scatter_inside(x, y, beta=0.15):
    # 根据beta值计算随机偏移量
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
    # 计算并返回偏移后的坐标
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


# 定义缩小点的函数
def shrink(x, y, ratio):
    # 计算力量
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    # 计算并返回缩小后的坐标
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


# 定义曲线函数
def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)  # 根据参数p计算并返回曲线值


# 定义Heart类，用于生成和渲染爱心形状
class Heart:
    def __init__(self, generate_frame=Frames_Number):  # 初始化方法，生成爱心形状的点集合
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {}  # 每帧动态点坐标
        self.build(2000)  # 构建爱心形状的点集合
        self.random_halo = 500  # 初始化光环点的数量
        self.generate_frame = generate_frame  # 动画帧数

        for frame in range(generate_frame):  # 循环计算每一帧的点
            self.calc(frame)

    def build(self, number):  # 构建爱心形状的点集合的方法
        # 使用heart_function函数生成number个点，构成原始爱心形状
        self._points = {heart_function(random.uniform(0, 2 * pi)) for _ in range(number)}

        # 爱心内扩散，生成边缘扩散效果点坐标集合
        edge_diffusion_points = set()
        for _x, _y in self._points:
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                edge_diffusion_points.add((x, y))
        self._edge_diffusion_points = edge_diffusion_points

        # 爱心内再次扩散，生成中心扩散效果点坐标集合
        center_diffusion_points = set()
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            center_diffusion_points.add((x, y))
        self._center_diffusion_points = center_diffusion_points

    # 计算点位置的静态方法
    @staticmethod
    def calc_position(x, y, ratio):
        # 计算力量
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        # 计算并返回偏移后的坐标
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    # 计算每一帧的点的方法
    def calc(self, generate_frame):
        # 根据动画帧数计算比例和光环半径
        ratio = 10 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
        all_points = []
        points_to_add = []

        # 预生成随机偏移量和点的大小
        random_offsets = [(random.randint(-14, 14), random.randint(-14, 14)) for _ in range(halo_number)]
        random_sizes = [random.randint(0, 2) for _ in range(halo_number)]

        # 使用线程池并行生成光环点
        def generate_halo_points(halo_number, random_offsets, ratio, halo_radius, all_points):
            heart_halo_point = set()  # 生成光环点的集合
            for i in range(halo_number):
                t = random.uniform(0, 2 * pi)
                x, y = heart_function(t, shrink_ratio=11.6)
                x, y = shrink(x, y, halo_radius)

                if (x, y) not in heart_halo_point:
                    heart_halo_point.add((x, y))
                    x_offset, y_offset = random_offsets[i]
                    x += x_offset
                    y += y_offset
                    size = random_sizes[i]
                    all_points.append((x, y, size))

            # 生成轮廓、边缘扩散点和中心扩散点
            for x, y in self._points:
                x, y = self.calc_position(x, y, ratio)
                size = random.randint(0, 2)
                points_to_add.append((x, y, size))

            for x, y in self._edge_diffusion_points:
                x, y = self.calc_position(x, y, ratio)
                size = random.randint(0, 2)
                points_to_add.append((x, y, size))

            for x, y in self._center_diffusion_points:
                x, y = self.calc_position(x, y, ratio)
                size = random.randint(0, 2)
                points_to_add.append((x, y, size))

            # 将生成的点添加到 all_points
            all_points.extend(points_to_add)
            self.all_points[generate_frame] = all_points

        # 创建线程池
        with ThreadPoolExecutor(max_workers=1) as executor:
            # 提交光环点生成任务
            executor.submit(generate_halo_points, halo_number, random_offsets, ratio, halo_radius, all_points)

    # 在指定的画布上渲染爱心形状
    def render(self, render_canvas, render_frame):
        frame_key = render_frame % self.generate_frame
        if frame_key in self.all_points:
            points = self.all_points[frame_key]
        else:
            points = []
        for x, y, size in points:
            render_canvas.create_rectangle(
                x, y, x + size, y + size, width=0, fill=HEART_COLOR)


# 定义绘制爱心并实现动画效果的函数
def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')  # 清除画布上的所有内容，并重新渲染爱心形状
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)  # 递归调用draw函数以实现动画效果


if __name__ == '__main__':
    root = Tk()
    root.title("爱心")
    root.resizable(0, 0)  # 锁定界面大小
    center_window(root, CANVAS_WIDTH, CANVAS_HEIGHT)  # 窗口居中显示

    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)  # 创建画布并添加到窗口
    canvas.pack()

    heart = Heart()  # 创建爱心对象并开始绘制
    draw(root, canvas, heart)  # 调用draw函数开始动画

    # 在画布中心显示文本
    Label(root,
          text=TXT_DATE,
          bg="black",
          fg=TXT_COLOR,
          font="Helvetic 20 bold").place(relx=.5, rely=.5, anchor=CENTER)

    root.mainloop()  # 启动Tkinter事件循环
