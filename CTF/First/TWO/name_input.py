import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from stroke_dict import get_stroke_count
import random
from svg import save_name_score_svg
from datetime import datetime

class NameEvaluator(QWidget):
    def __init__(self):
        super().__init__()
        # 添加评分相关的属性
        self.latest_result = None
        self.san_cai_score = 0
        self.wu_ge_score = 0
        self.yun_lv_score = 0
        self.meaning_score = 0
        self.bagua_score = 0
        # 初始化UI
        self.initUI()
        self.setStyleSheet("""
            QWidget {
                background-color: #FFE4B5;
                font-family: 'Microsoft YaHei';
            }
            QLabel {
                color: #8B4513;
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px 10px;
                border: 1px solid #DEB887;
                border-radius: 4px;
                background-color: #FFEFD5;
                min-width: 200px;
                font-size: 14px;
                color: #8B4513;
            }
            QLineEdit:focus {
                border-color: #FFA500;
                outline: 0;
                box-shadow: 0 0 8px rgba(255,165,0,.6);
                background-color: #FFE4C4;
            }
            QPushButton {
                padding: 6px 20px;
                background-color: #FF8C00;
                border: none;
                border-radius: 4px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
                transition: all 0.2s;
                position: relative;
                top: 0;
                box-shadow: 0 4px 0 #D26900;
            }
            QPushButton:hover {
                background-color: #FFA500;
                transform: translateY(-2px);
                box-shadow: 0 6px 0 #D26900;
            }
            QPushButton:pressed {
                background-color: #FF7F24;
                transform: translateY(4px);
                box-shadow: 0 0 0 #D26900;
                padding-top: 8px;
                padding-bottom: 4px;
            }
            QTableWidget {
                background-color: #FFEFD5;
                border: 1px solid #DEB887;
                border-radius: 4px;
                gridline-color: #FFE4C4;
                color: #8B4513;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #FFE4C4;
                color: #8B4513;
            }
            QHeaderView::section {
                background-color: #FFDAB9;
                padding: 5px;
                border: none;
                border-right: 1px solid #DEB887;
                border-bottom: 1px solid #DEB887;
                font-weight: bold;
                color: #8B4513;
            }
        """)

    def initUI(self):
        self.setWindowTitle('名字评分系统')
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 添加标题标签
        title_label = QLabel('好名字，上上签')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #D4A017;
                margin: 20px;
                font-family: 'STKaiti', 'KaiTi', '楷体';
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 创建水平布局来放置输入框和按钮
        input_layout = QHBoxLayout()
        input_layout.setSpacing(15)
        
        # 添加输入提示标签
        input_label = QLabel('请输入姓名：')
        input_layout.addWidget(input_label)
        
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('输入2-4个汉字')
        self.name_input.returnPressed.connect(self.evaluate_name)  # 添加回车响应
        input_layout.addWidget(self.name_input)

        self.query_button = QPushButton('查询', self)
        self.query_button.setCursor(Qt.PointingHandCursor)
        self.query_button.clicked.connect(self.evaluate_name)
        input_layout.addWidget(self.query_button)
        
        layout.addLayout(input_layout)

        # 创建表格
        self.result_table = QTableWidget(0, 4)
        # 设置加粗的表头标签
        header_labels = []
        for label in ['名字', '评分', '评级', '寄语']:
            item = QTableWidgetItem(label)
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            header_labels.append(item)
        
        self.result_table.setHorizontalHeaderLabels(['名字', '评分', '评级', '寄语'])
        header = self.result_table.horizontalHeader()
        for i in range(4):
            header.setSectionResizeMode(i, QHeaderView.Stretch)
            # 设置表头字体加粗
            font = header.font()
            font.setBold(True)
            header.setFont(font)
        
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setAlternatingRowColors(True)
        layout.addWidget(self.result_table)

        # 添加导出SVG按钮
        self.export_button = QPushButton('导出SVG报告')
        self.export_button.clicked.connect(self.export_svg)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def evaluate_name(self):
        """评估名字"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, '提示', '请输入姓名')
            return
        
        if not 2 <= len(name) <= 4:
            QMessageBox.warning(self, '提示', '请输入2-4个汉字')
            return
        
        # 检查是否全是汉字
        if not all('\u4e00' <= char <= '\u9fff' for char in name):
            QMessageBox.warning(self, '提示', '请输入汉字')
            return
        
        # 获取评分结果
        score, rating, message = self.get_name_evaluation(name)
        
        # 在界面显示结果
        self.add_result_to_table(name, score, rating, message)
        
        try:
            # 自动生成SVG报告
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"name_score_{name}_{timestamp}.svg"
            current_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(current_dir, filename)
            
            # 保存SVG
            save_name_score_svg(
                self.latest_result['name'],
                self.latest_result['score'],
                self.latest_result['rating'],
                self.latest_result['message'],
                self.latest_result['details'],
                filepath
            )
            
            # 显示成功消息
            QMessageBox.information(self, '评分完成', 
                f'评分结果已显示在表格中\n'
                f'SVG报告已保存为：\n{filepath}')
        except Exception as e:
            QMessageBox.warning(self, '提示', 
                f'评分结果已显示在表格中\n'
                f'但SVG报告生成失败：{str(e)}')
        
        # 清空输入框，准备下一次输入
        self.name_input.clear()

    def add_result_to_table(self, name, score, rating, message):
        row_position = self.result_table.rowCount()
        self.result_table.insertRow(row_position)
        
        # 添加名字
        self.result_table.setItem(row_position, 0, QTableWidgetItem(name))
        
        # 添加分数（加粗显示，添加"分"字）
        score_item = QTableWidgetItem(f"{score}分")
        score_item.setFont(QFont('Microsoft YaHei', weight=QFont.Bold))
        self.result_table.setItem(row_position, 1, score_item)
        
        # 添加评级和寄语
        self.result_table.setItem(row_position, 2, QTableWidgetItem(rating))
        self.result_table.setItem(row_position, 3, QTableWidgetItem(message))
        
        # 存储最新结果
        self.latest_result = {
            'name': name,
            'score': score,
            'rating': rating,
            'message': message,
            'details': {
                '三才评分': round(self.san_cai_score, 1),
                '五格评分': round(self.wu_ge_score, 1),
                '韵律评分': round(self.yun_lv_score, 1),
                '字形字义': round(self.meaning_score, 1),
                '八卦六爻': round(self.bagua_score, 1)
            }
        }

    def get_name_evaluation(self, name):
        """使用三才五格评分"""
        # 计算三才
        if len(name) < 2:
            return 60, '一般', '名字太短，建议用更多字'
        
        # 天格数（复姓取第一字）
        tian_ge = get_stroke_count(name[0]) + 1
        
        # 人格数（复姓取第二字）
        if len(name) == 2:
            ren_ge = get_stroke_count(name[0]) + get_stroke_count(name[1])
        else:
            ren_ge = get_stroke_count(name[1]) + get_stroke_count(name[-1])
        
        # 地格数
        di_ge = get_stroke_count(name[-1]) + 1
        
        # 外格数
        if len(name) == 2:
            wai_ge = get_stroke_count(name[0]) + 1
        else:
            wai_ge = (get_stroke_count(name[0]) + 1) + (get_stroke_count(name[-1]) + 1) - 1
        
        # 总格数（姓名各字笔画总和）
        zong_ge = sum(get_stroke_count(char) for char in name)
        
        # 计算三才分数
        self.san_cai_score = self.get_san_cai_score(tian_ge, ren_ge, di_ge)
        
        # 计算五格分数
        self.wu_ge_score = self.get_wu_ge_score(tian_ge, ren_ge, di_ge, wai_ge, zong_ge)
        
        # 计算韵律分数
        self.yun_lv_score = self.get_yun_lv_score(name)
        
        # 计算字形字义分数
        self.meaning_score = 80  # 暂时使用固定分数
        
        # 计算八卦分数
        self.bagua_score = 80  # 暂时使用固定分数
        
        # 综合评分（各项权重可调整）
        total_score = (
            self.san_cai_score * 0.3 + 
            self.wu_ge_score * 0.4 + 
            self.yun_lv_score * 0.1 +
            self.meaning_score * 0.1 +
            self.bagua_score * 0.1
        )
        
        # 根据分数返回评级和寄语
        if total_score >= 90:
            return round(total_score, 1), '顶级', '前程似锦'
        elif total_score >= 85:
            return round(total_score, 1), '优秀', '福禄双全'
        elif total_score >= 80:
            return round(total_score, 1), '中上', '平安顺遂'
        elif total_score >= 70:
            return round(total_score, 1), '良好', '平安是福'
        else:
            return round(total_score, 1), '一般', '谨慎行事'

    def get_san_cai_score(self, tian, ren, di):
        """计算三才分数"""
        # 天人地配置表（完整版）
        san_cai_table = {
            # 上上配置（100分）
            (1, 6, 8): 100, (1, 8, 8): 100, (3, 6, 8): 100, (3, 8, 8): 100,
            (5, 6, 8): 100, (5, 8, 8): 100, (7, 6, 8): 100, (7, 8, 8): 100,
            
            # 上配置（90分）
            (1, 6, 6): 90, (1, 8, 6): 90, (3, 6, 6): 90, (3, 8, 6): 90,
            (5, 6, 6): 90, (5, 8, 6): 90, (7, 6, 6): 90, (7, 8, 6): 90,
            (2, 6, 8): 90, (2, 8, 8): 90, (4, 6, 8): 90, (4, 8, 8): 90,
            (6, 6, 8): 90, (6, 8, 8): 90, (8, 6, 8): 90, (8, 8, 8): 90,
            
            # 中上配置（85分）
            (1, 1, 8): 85, (1, 3, 8): 85, (1, 5, 8): 85, (1, 7, 8): 85,
            (3, 1, 8): 85, (3, 3, 8): 85, (3, 5, 8): 85, (3, 7, 8): 85,
            (5, 1, 8): 85, (5, 3, 8): 85, (5, 5, 8): 85, (5, 7, 8): 85,
            (7, 1, 8): 85, (7, 3, 8): 85, (7, 5, 8): 85, (7, 7, 8): 85,
            
            # 中配置（80分）
            (2, 1, 6): 80, (2, 3, 6): 80, (2, 5, 6): 80, (2, 7, 6): 80,
            (4, 1, 6): 80, (4, 3, 6): 80, (4, 5, 6): 80, (4, 7, 6): 80,
            (6, 1, 6): 80, (6, 3, 6): 80, (6, 5, 6): 80, (6, 7, 6): 80,
            (8, 1, 6): 80, (8, 3, 6): 80, (8, 5, 6): 80, (8, 7, 6): 80,
            
            # 中下配置（75分）
            (1, 2, 8): 75, (1, 4, 8): 75, (3, 2, 8): 75, (3, 4, 8): 75,
            (5, 2, 8): 75, (5, 4, 8): 75, (7, 2, 8): 75, (7, 4, 8): 75,
            (2, 2, 6): 75, (2, 4, 6): 75, (4, 2, 6): 75, (4, 4, 6): 75,
            (6, 2, 6): 75, (6, 4, 6): 75, (8, 2, 6): 75, (8, 4, 6): 75,
            
            # 下配置（70分）
            (1, 2, 6): 70, (1, 4, 6): 70, (3, 2, 6): 70, (3, 4, 6): 70,
            (5, 2, 6): 70, (5, 4, 6): 70, (7, 2, 6): 70, (7, 4, 6): 70,
            (2, 2, 8): 70, (2, 4, 8): 70, (4, 2, 8): 70, (4, 4, 8): 70,
            (6, 2, 8): 70, (6, 4, 8): 70, (8, 2, 8): 70, (8, 4, 8): 70,
            
            # 特殊配置
            (1, 1, 1): 88, (3, 3, 3): 88, (5, 5, 5): 88, (7, 7, 7): 88,
            (2, 2, 2): 66, (4, 4, 4): 66, (6, 6, 6): 66, (8, 8, 8): 66,
        }
        
        # 获取最接近的配置
        min_diff = float('inf')
        best_score = 60  # 默认分数调整为60分
        
        for config, score in san_cai_table.items():
            # 计算当前配置与实际数值的差异
            diff = abs(config[0] - tian) + abs(config[1] - ren) + abs(config[2] - di)
            
            # 如果找到完全匹配的配置
            if diff == 0:
                return score
            
            # 更新最接近的配置
            if diff < min_diff:
                min_diff = diff
                best_score = score
            
            # 如果差异相同，选择分数更高的
            elif diff == min_diff:
                best_score = max(best_score, score)
        
        # 据差异度调整分数
        if min_diff <= 3:
            return best_score - 5  # 轻微差异，略微降分
        elif min_diff <= 6:
            return best_score - 10  # 中等差异，适度降分
        else:
            return best_score - 15  # 较大差异，显著降分

    def get_wu_ge_score(self, tian, ren, di, wai, zong):
        """计算五格分数"""
        # 定义数理五行属性评分
        def get_number_score(num):
            # 上等数理
            if num in [1, 3, 7, 11, 13, 15, 21, 25, 31, 37]:
                return 100
            # 中上数理
            elif num in [5, 8, 9, 23, 27, 29, 33, 35, 39]:
                return 90
            # 中等数理
            elif num in [2, 4, 12, 14, 16, 18, 24, 28, 32, 36]:
                return 80
            # 中下数理
            elif num in [6, 10, 17, 19, 20, 22, 26, 30, 34, 38]:
                return 70
            # 下等数理
            else:
                return 60

        # 天格评分（主外在环境）
        tian_score = get_number_score(tian)
        if tian in [1, 3, 5, 7]:  # 特别有利的天格数
            tian_score += 10
        
        # 人格评分（主个性特征）- 最重要
        ren_score = get_number_score(ren)
        if ren in [1, 3, 5, 7, 8, 11, 13, 15, 21]:  # 传统上最佳的人格数
            ren_score += 15
        elif ren in [2, 4, 6, 9, 10, 12, 14, 16]:  # 次的人格数
            ren_score += 5
        
        # 地格评分（主事业发展）
        di_score = get_number_score(di)
        if di in [1, 3, 5, 7, 11, 13, 15, 21]:  # 有利的地格数
            di_score += 10
        
        # 外格评分（主社交环境）
        wai_score = get_number_score(wai)
        if wai in [1, 3, 5, 7, 8, 11, 13, 15]:  # 有利的外格数
            wai_score += 5
        
        # 总格评分（主人生总体）- 次重要
        zong_score = get_number_score(zong)
        if zong in [1, 3, 5, 7, 8, 11, 13, 15, 21, 23, 25]:  # 最佳的总格数
            zong_score += 10
        elif zong in [2, 4, 6, 9, 10, 12, 14, 16, 24]:  # 次佳的总格数
            zong_score += 5

        # 五格数理关系评分
        relation_score = 80  # 基础分
        
        # 检查五格数理是否和谐
        all_numbers = [tian, ren, di, wai, zong]
        
        # 检查是否有相生关系（如金木水火土相生）
        def check_wuxing_relation(nums):
            wuxing_groups = {
                '金': [4, 9, 14, 19, 24, 29, 34, 39],
                '木': [1, 6, 11, 16, 21, 26, 31, 36],
                '水': [2, 7, 12, 17, 22, 27, 32, 37],
                '火': [3, 8, 13, 18, 23, 28, 33, 38],
                '土': [5, 10, 15, 20, 25, 30, 35, 40]
            }
            
            # 统计五行属性
            elements = []
            for num in nums:
                for element, numbers in wuxing_groups.items():
                    if num in numbers:
                        elements.append(element)
                        break
            
            # 检查相生关系
            sheng_relations = [
                ('金', '水'), ('水', '木'), ('木', '火'),
                ('火', '土'), ('土', '金')
            ]
            
            good_relations = 0
            for i in range(len(elements)):
                for j in range(i + 1, len(elements)):
                    if (elements[i], elements[j]) in sheng_relations or \
                       (elements[j], elements[i]) in sheng_relations:
                        good_relations += 1
            
            return good_relations * 5  # 每个相生关系加5分

        relation_score += check_wuxing_relation(all_numbers)

        # 计算加权平均分
        weighted_score = (
            tian_score * 0.1 +    # 天格权重10%
            ren_score * 0.3 +     # 人格权重30%
            di_score * 0.2 +      # 地格权重20%
            wai_score * 0.1 +     # 外格权重10%
            zong_score * 0.2 +    # 总格权重20%
            relation_score * 0.1   # 五格关系权重10%
        )
        
        return weighted_score

    def get_yun_lv_score(self, name):
        """计算韵律分数"""
        PINYIN_DICT = {
            # 一声
            '平': 'ping2', '东': 'dong1', '明': 'ming2', '清': 'qing1',
            '天': 'tian1', '华': 'hua2', '光': 'guang1', '永': 'yong3',
            # 二声
            '国': 'guo2', '安': 'an1', '文': 'wen2', '德': 'de2',
            '和': 'he2', '兴': 'xing1', '荣': 'rong2', '贵': 'gui4',
            # 三声
            '志': 'zhi4', '伟': 'wei3', '建': 'jian4', '海': 'hai3',
            '晓': 'xiao3', '勇': 'yong3', '智': 'zhi4', '礼': 'li3',
            # 四声
            '力': 'li4', '强': 'qiang2', '立': 'li4', '信': 'xin4',
            '义': 'yi4', '达': 'da2', '耀': 'yao4', '远': 'yuan3'
        }

        def get_tone(pinyin):
            """获取拼音的声调"""
            if not pinyin:
                return 0
            tone_number = pinyin[-1]
            return int(tone_number) if tone_number.isdigit() else 0

        score = 80  # 基础分

        # 名字长度评分
        if len(name) == 2:
            score += 5  # 二字名较为简洁
        elif len(name) == 3:
            score += 10  # 三字名最为常见
        else:
            score -= 5  # 过长或过短都不太适合

        # 获取每个字的声调
        tones = []
        for char in name:
            pinyin = PINYIN_DICT.get(char, '')
            tone = get_tone(pinyin)
            if tone:
                tones.append(tone)

        # 声调评分规则
        if len(tones) >= 2:
            # 相邻声调不宜相同
            for i in range(len(tones)-1):
                if tones[i] == tones[i+1]:
                    score -= 5
            
            # 一声和四声搭配加分
            if 1 in tones and 4 in tones:
                score += 5
            
            # 二声和三声搭配加分
            if 2 in tones and 3 in tones:
                score += 5
            
            # 避免连续上声（三声）
            for i in range(len(tones)-1):
                if tones[i] == 3 and tones[i+1] == 3:
                    score -= 10

            # 末字声调评分
            last_tone = tones[-1]
            if last_tone in [2, 4]:  # 末字用仄声（二声或四声）较好
                score += 5
            elif last_tone == 3:  # 末字避免用上声（三声）
                score -= 5

        # 确保分数在合理范围内
        return max(60, min(100, score))

    def export_svg(self):
        """导出SVG报告"""
        if not self.latest_result:
            QMessageBox.warning(self, '提示', '请先评估名字后再导出报告')
            return
        
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"name_score_{timestamp}.svg"
            
            # 获取当前目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(current_dir, filename)
            
            # 保存SVG
            save_name_score_svg(
                self.latest_result['name'],
                self.latest_result['score'],
                self.latest_result['rating'],
                self.latest_result['message'],
                self.latest_result['details'],
                filepath
            )
            
            # 显示成功消息，包含完整路径
            QMessageBox.information(self, '成功', f'报告已导出为：\n{filepath}')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'导出失败：{str(e)}')

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        try:
            # 清理资源
            self.cleanup()
            event.accept()
        except Exception as e:
            print(f"关闭时发生错误: {str(e)}")
            event.accept()

    def cleanup(self):
        """清理资源"""
        # 在这里添加任何需要的清理代码
        pass

def main():
    """主函数"""
    try:
        app = QApplication(sys.argv)
        evaluator = NameEvaluator()
        evaluator.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"程序运行错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()