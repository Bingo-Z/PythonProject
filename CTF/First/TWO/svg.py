import svgwrite
from datetime import datetime
import warnings
import logging
import os

# 过滤掉 libpng 警告
warnings.filterwarnings("ignore", category=UserWarning)

# 或者重定向警告到日志
logging.getLogger('libpng').setLevel(logging.ERROR)

class NameScoreSVG:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.padding = 50
        
    def create_score_chart(self, name, score, rating, message, details):
        """创建名字评分SVG图表"""
        # 创建SVG文档，添加viewBox以支持响应式缩放
        dwg = svgwrite.Drawing(size=(self.width, self.height), viewBox=f'0 0 {self.width} {self.height}')
        
        # 添加背景（使用纯色代替渐变）
        dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), 
                        fill='#FFE4B5', rx=10, ry=10))
        
        # 添加标题
        title = dwg.g(style='font-family: Microsoft YaHei')
        title.add(dwg.text('名字评分报告',
                         insert=(self.width/2, 50),
                         text_anchor='middle',
                         font_size=24,
                         font_weight="bold",
                         fill='#8B4513'))
        dwg.add(title)
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dwg.add(dwg.text(f'生成时间：{timestamp}',
                        insert=(self.width-self.padding, 30),
                        text_anchor='end',
                        font_family="Microsoft YaHei",
                        font_size=12,
                        fill='#8B4513'))
        
        # 添加名字
        dwg.add(dwg.text(f'姓名：{name}',
                        insert=(self.padding, 100),
                        font_family="Microsoft YaHei",
                        font_size=18,
                        fill='#8B4513'))
        
        # 添加分数圆环
        circle_center = (self.width/2, 200)
        # 背景圆
        dwg.add(dwg.circle(center=circle_center, r=60,
                          fill='#FFDAB9', stroke='none'))
        # 分数圆环
        dwg.add(dwg.circle(center=circle_center, r=50,
                          fill='none', stroke='#FFA500', stroke_width=8))
        # 分数文本
        score_text = dwg.g(style='font-family: Microsoft YaHei')
        score_text.add(dwg.text(f'{score}',
                              insert=(circle_center[0], circle_center[1]+10),
                              text_anchor='middle',
                              font_size=36,
                              font_weight="bold",
                              fill='#FF8C00'))
        score_text.add(dwg.text('分',
                              insert=(circle_center[0]+40, circle_center[1]+10),
                              font_size=20,
                              fill='#8B4513'))
        dwg.add(score_text)
        
        # 添加评级和寄语
        info_group = dwg.g(style='font-family: Microsoft YaHei; fill: #8B4513')
        info_group.add(dwg.text(f'评级：{rating}',
                              insert=(self.padding, 300),
                              font_size=18))
        info_group.add(dwg.text(f'寄语：{message}',
                              insert=(self.padding, 340),
                              font_size=18))
        dwg.add(info_group)
        
        # 添加详细分数
        y = 400
        for category, detail_score in details.items():
            # 分数条背景
            dwg.add(dwg.rect(insert=(self.padding, y),
                           size=(300, 20),
                           fill='#FFDAB9',
                           rx=5, ry=5))
            # 实际分数条
            width = detail_score * 3  # 将分数转换为宽度
            dwg.add(dwg.rect(insert=(self.padding, y),
                           size=(width, 20),
                           fill='#FFA500',
                           rx=5, ry=5))
            # 分类名称和分数
            dwg.add(dwg.text(f'{category}: {detail_score}分',
                           insert=(self.padding+320, y+15),
                           font_family="Microsoft YaHei",
                           font_size=14,
                           fill='#8B4513'))
            y += 30
        
        return dwg

def save_name_score_svg(name, score, rating, message, details, filename):
    """保存名字评分为SVG文件"""
    try:
        import contextlib
        import io
        
        # 捕获警告输出
        warning_output = io.StringIO()
        with contextlib.redirect_stderr(warning_output):
            chart = NameScoreSVG()
            dwg = chart.create_score_chart(name, score, rating, message, details)
            dwg.saveas(filename, pretty=True, indent=2)
        
        # 验证文件是否成功保存
        if not os.path.exists(filename):
            raise Exception("文件保存失败")
            
    except Exception as e:
        raise Exception(f"保存SVG文件时出错: {str(e)}")
