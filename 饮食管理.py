import re

# 🍽️ 食物成分库（每100g：热量（千卡）、碳水比例、蛋白质比例、脂肪比例）
food_database = {
    "和牛汉堡肉": [232, 0.02, 0.64, 0.34],
    "香煎鸡胸肉": [128, 0.05, 0.72, 0.23],
    "煮鸡蛋": [143, 0.00, 0.34, 0.66],
    "苹果": [53, 0.94, 0.03, 0.03],
    "洋葱": [40, 0.86, 0.10, 0.04],
    "酸黄瓜": [11, 0.74, 0.11, 0.15],
    "全麦吐司": [255, 0.72, 0.12, 0.16]
}

def parse_food_input(input_str):
    foods = input_str.strip().split('，')
    result = []
    for item in foods:
        match = re.match(r"(.+?)(\d+)$", item.strip())
        if match:
            name = match.group(1).strip()
            grams = float(match.group(2))
        else:
            name = item.strip()
            grams = 100.0
        result.append((name, grams))
    return result

def calculate_nutrition(parsed_foods):
    total_kcal = 0
    carb_kcal = 0
    fat_kcal = 0
    protein_kcal = 0
    for food, grams in parsed_foods:
        if food in food_database:
            kcal_per_100g, carb_ratio, protein_ratio, fat_ratio = food_database[food]
            kcal = kcal_per_100g * grams / 100
            total_kcal += kcal
            carb_kcal += kcal * carb_ratio
            fat_kcal += kcal * fat_ratio
            protein_kcal += kcal * protein_ratio
    carb_protein_ratio = carb_kcal / protein_kcal if protein_kcal else 0
    carb_fat_ratio = carb_kcal / fat_kcal if fat_kcal else 0
    return total_kcal, carb_kcal, fat_kcal, protein_kcal, carb_protein_ratio, carb_fat_ratio

def calculate_bmr_tdee(age, weight, training_days):
    height = 168
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    if training_days == 0:
        m = 1.2
    elif 1 <= training_days <= 3:
        m = 1.375
    elif 3 < training_days <= 5:
        m = 1.55
    else:
        m = 1.725
    tdee = bmr * m
    return bmr, tdee

def calculate_target_calories(tdee, goal):
    if goal == "维持":
        return tdee
    elif goal == "减重":
        return tdee - 500
    elif goal == "增重":
        return tdee + 500
    else:
        return tdee

def main():
    print("🍽️ 欢迎使用《每日营养摄入分析小助手》")
    print("📌 说明：")
    print("1. 请输入你今天吃的食物（例如：和牛汉堡肉200，煮鸡蛋100），单位为克，不需要加g")
    print("2. 每日摄入热量、碳蛋比、剩余可摄入热量将自动计算")
    print("3. 食物热量数据参考APP《薄荷健康》，食物估重可参考其中内容")
    print("4. 本网页食物库持续更新，如需添加新食谱，请联系作者发送如下格式：")
    print('   "新食物名": [热量, 碳水比例, 蛋白质比例, 脂肪比例],')
    print("   示例：\"酸黄瓜\": [11, 0.74, 0.11, 0.15],")
    print("📮 联系方式：请通过项目页面或邮箱联系作者提交新数据\n")

    input_str = input("请输入你今天吃的食物（例如：和牛汉堡肉200，鸡蛋100）：")
    parsed = parse_food_input(input_str)
    total_kcal, carb_kcal, fat_kcal, protein_kcal, cp_ratio, cf_ratio = calculate_nutrition(parsed)

    print("\n📊 当前摄入分析：")
    print(f"总热量：{total_kcal:.2f} 千卡")
    print(f"碳水：{carb_kcal:.2f} 千卡")
    print(f"脂肪：{fat_kcal:.2f} 千卡")
    print(f"蛋白质：{protein_kcal:.2f} 千卡")
    print(f"碳蛋比：{cp_ratio:.2f}")
    print(f"碳脂比：{cf_ratio:.2f}")

    cont = input("\n是否继续计算热量建议？(是/否)：").strip()
    if cont != "是":
        print("程序已结束 ✅")
        return

    age = int(input("\n请输入年龄："))
    weight = float(input("请输入当前体重（kg）："))
    training_days = int(input("请输入本周训练天数："))
    goal = input("请输入体重管理目标（维持/减重/增重）：")

    bmr, tdee = calculate_bmr_tdee(age, weight, training_days)
    target = calculate_target_calories(tdee, goal)
    remaining = target - total_kcal

    print("\n📈 热量建议：")
    print(f"基础代谢率（BMR）：{bmr:.2f} 千卡")
    print(f"每日总消耗（TDEE）：{tdee:.2f} 千卡")
    print(f"目标摄入热量：{target:.2f} 千卡")
    print(f"剩余可摄入热量：{remaining:.2f} 千卡")

main()
