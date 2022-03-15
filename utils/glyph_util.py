import png


def load_design_data_from_png(file_path):
    """
    从本地加载字形设计数据，并二值化
    """
    width, height, bitmap, info = png.Reader(filename=file_path).read()
    design_data = []
    for bitmap_row in bitmap:
        design_data_row = []
        bitmap_row_len = len(bitmap_row)
        pixel_step = int(bitmap_row_len / width)
        for x in range(pixel_step - 1, bitmap_row_len, pixel_step):
            alpha = bitmap_row[x]
            if alpha > 127:
                design_data_row.append(1)
            else:
                design_data_row.append(0)
        design_data.append(design_data_row)
    return design_data, width, height


def get_outlines_from_design_data(design_data, dot_size):
    """
    轮廓算法，左上坐标系
    """
    # 1. 相邻像素分组
    point_group_list = []
    for y, design_data_row in enumerate(design_data):
        for x, alpha in enumerate(design_data_row):
            if alpha > 0:
                new_point_group = {(x, y)}
                for i, point_group in enumerate(reversed(point_group_list)):
                    # 遍历方向为右下，因此只需检查左上
                    if (x - 1, y) in point_group or (x, y - 1) in point_group:
                        point_group_list.remove(point_group)
                        new_point_group = new_point_group.union(point_group)
                point_group_list.append(new_point_group)
    # 2. 对每组生成轮廓
    outlines = []
    for point_group in point_group_list:
        # 按照像素拆分线段，注意绘制顺序
        pending_line_segments = []
        for (x, y) in point_group:
            point_outline = [
                (x * dot_size, y * dot_size),
                ((x + 1) * dot_size, y * dot_size),
                ((x + 1) * dot_size, (y + 1) * dot_size),
                (x * dot_size, (y + 1) * dot_size),
            ]
            # 一个像素有左右上下四个边，如果该边没有相邻像素，则该边线段有效
            if x <= 0 or design_data[y][x - 1] <= 0:  # 左
                pending_line_segments.append([point_outline[3], point_outline[0]])
            if x >= len(design_data[y]) - 1 or design_data[y][x + 1] <= 0:  # 右
                pending_line_segments.append([point_outline[1], point_outline[2]])
            if y <= 0 or design_data[y - 1][x] <= 0:  # 上
                pending_line_segments.append([point_outline[0], point_outline[1]])
            if y >= len(design_data) - 1 or design_data[y + 1][x] <= 0:  # 下
                pending_line_segments.append([point_outline[2], point_outline[3]])
        # 连接所有的线段，注意绘制顺序
        solved_line_segments = []
        while len(pending_line_segments) > 0:
            pending_line_segment = pending_line_segments.pop()
            for i, solved_line_segment in enumerate(reversed(solved_line_segments)):
                left_line_segment = None
                right_line_segment = None
                # 一共4种连接情况
                if pending_line_segment[-1] == solved_line_segment[0]:
                    left_line_segment = pending_line_segment
                    right_line_segment = solved_line_segment
                elif pending_line_segment[-1] == solved_line_segment[-1]:
                    solved_line_segment.reverse()
                    left_line_segment = pending_line_segment
                    right_line_segment = solved_line_segment
                elif solved_line_segment[-1] == pending_line_segment[0]:
                    left_line_segment = solved_line_segment
                    right_line_segment = pending_line_segment
                elif solved_line_segment[-1] == pending_line_segment[-1]:
                    pending_line_segment.reverse()
                    left_line_segment = solved_line_segment
                    right_line_segment = pending_line_segment
                # 需要连接的情况
                if left_line_segment and right_line_segment:
                    solved_line_segments.remove(solved_line_segment)
                    # 连接的两个点是重复的
                    right_line_segment.pop(0)
                    # 判断连接的点是不是可省略
                    x, y = left_line_segment[-1]
                    xl, yl = left_line_segment[-2]
                    xr, yr = right_line_segment[0]
                    if (x == xl and x == xr) or (y == yl and y == yr):
                        left_line_segment.pop()
                    # 连接线段
                    pending_line_segment = left_line_segment + right_line_segment
            solved_line_segments.append(pending_line_segment)
        # 将连接好的线段添加到轮廓数组中，有多条线段的情况，是中间有镂空（绘制顺序与外边框相反）
        for solved_line_segment in solved_line_segments:
            # 首尾的两个点是重复的
            solved_line_segment.pop(0)
            # 判断尾点是不是可省略
            x, y = solved_line_segment[-1]
            xl, yl = solved_line_segment[-2]
            xr, yr = solved_line_segment[0]
            if (x == xl and x == xr) or (y == yl and y == yr):
                solved_line_segment.pop()
            # 添加到轮廓
            outlines.append(solved_line_segment)
    # 返回
    return outlines
