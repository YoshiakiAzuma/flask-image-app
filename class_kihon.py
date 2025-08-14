class SchoolReport:
    def __init__(self,student_name, math_score, jp_score, en_score):
        self.name = student_name
        self.math = math_score
        self.jp = jp_score
        self.en = en_score

    def calc_ave_score(self):
        sum_score = (self.math + self.jp + self.en) 
        ave_score = sum_score / 3
        return ave_score
        
sr_a = SchoolReport("田中",80,90,75)
ave_a = sr_a.calc_ave_score()
print(f"田中さんの平均点は{ave_a}点です")
