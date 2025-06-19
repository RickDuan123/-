import streamlit as st
import re

# ✅ 默认数据库
food_database = {
    "和牛汉堡肉": [232, 0.02, 0.64, 0.34],
    "香煎鸡胸肉": [128, 0.05, 0.72, 0.23],
    "煮鸡蛋": [143, 0.00, 0.34, 0.66],
    "苹果": [53, 0.94, 0.03, 0.03],
    "洋葱": [40, 0.86, 0.10, 0.04],
    "酸黄瓜": [11, 0.74, 0.11, 0.15],
    "全麦吐司": [255, 0.72, 0.12, 0.16],
    "燕麦": [338, 0.88, 0.11, 0.01],
    "韭菜炒千张": [130, 0.14, 0.28, 0.58],
    "泡腾片": [500, 1.0, 0.0, 0.0],
    "面条": [107, 0.83, 0.14, 0.03],
    "猪脚饭": [189, 0.19, 0.27, 0.54],
    "豆浆": [31, 0.16, 0.38, 0.46]，
    "米饭"：[116, 0.89, 0.09, 0.02],
    "蛋炒饭": [141, 0.52, 0.15, 0.33]
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
    total_kcal = carb_kcal = fat_kcal = protein_kcal = 0
    for food, grams in parsed_foods:
        if food in food_database:
            kcal, carb_r, protein_r, fat_r = food_database[food]
            amount = kcal * grams / 100
            total_kcal += amount
            carb_kcal += amount * carb_r
            protein_kcal += amount * protein_r
            fat_kcal += amount * fat_r
    cp_ratio = carb_kcal / protein_kcal if protein_kcal else 0
    cf_ratio = carb_kcal / fat_kcal if fat_kcal else 0
    return total_kcal, carb_kcal, fat_kcal, protein_kcal, cp_ratio, cf_ratio

def calculate_bmr_tdee(age, weight, training_days, height=168):
    bmr = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age
    m = 1.2 if training_days == 0 else 1.375 if training_days <= 3 else 1.55 if training_days <= 5 else 1.725
    return bmr, bmr * m

def calculate_target_calories(tdee, goal):
    return tdee if goal == "维持" else tdee - 500 if goal == "减重" else tdee + 500

# --- Streamlit App ---
st.title("🥦 每日营养摄入分析助手")

st.markdown("""
📌 **使用说明：**  
1. 请输入你今天吃的食物（格式如：苹果200，煮鸡蛋100）  
2. 固体默认以g为单位，液体默认以ml为单位，无需手动添加  
3. 食物成分参考APP“薄荷健康”  
4. 如需新增食物，请通过下方模块提交数据
""")

tab1, tab2, tab3 = st.tabs(["🍱 食物营养分析", "🔥 热量建议", "📬 提交新食谱"])

with tab1:
    input_str = st.text_input("📥 输入今日食物清单：", placeholder="例如：苹果200，煮鸡蛋100")
    if input_str:
        parsed = parse_food_input(input_str)
        total_kcal, carb_kcal, fat_kcal, protein_kcal, cp_ratio, cf_ratio = calculate_nutrition(parsed)

        st.success("✅ 分析结果如下：")
        st.write(f"**总热量**：{total_kcal:.2f} 千卡")
        st.write(f"**碳水**：{carb_kcal:.2f} 千卡")
        st.write(f"**蛋白质**：{protein_kcal:.2f} 千卡")
        st.write(f"**脂肪**：{fat_kcal:.2f} 千卡")
        st.write(f"**碳蛋比**：{cp_ratio:.2f}")
        st.write(f"**碳脂比**：{cf_ratio:.2f}")

with tab2:
    st.subheader("📈 计算热量建议")
    age = st.number_input("年龄", 10, 100, 25)
    weight = st.number_input("当前体重（kg）", 30.0, 200.0, 60.0)
    days = st.slider("本周训练天数", 0, 7, 3)
    goal = st.radio("体重管理目标", ["维持", "减重", "增重"])
    run = st.button("计算推荐热量")
    if run:
        bmr, tdee = calculate_bmr_tdee(age, weight, days)
        target = calculate_target_calories(tdee, goal)
        remaining = target - total_kcal if input_str else "（需输入食物）"
        st.write(f"基础代谢率 BMR：{bmr:.2f} 千卡")
        st.write(f"每日总消耗 TDEE：{tdee:.2f} 千卡")
        st.write(f"推荐摄入热量：{target:.2f} 千卡")
        if input_str:
            st.write(f"剩余可摄入热量：{remaining:.2f} 千卡")

with tab3:
    st.subheader("📬 食谱补充提案")
    name = st.text_input("食物名称")
    kcal = st.number_input("每100g热量（千卡）", 1, 1000)
    carb = st.number_input("碳水比例", 0.0, 1.0)
    protein = st.number_input("蛋白质比例", 0.0, 1.0)
    fat = st.number_input("脂肪比例", 0.0, 1.0)

    if st.button("生成分享格式"):
        if name:
            st.code(f'"{name}": [{kcal}, {carb}, {protein}, {fat}],', language="python")
            st.info("你可以将以上格式复制发送给开发者添加到系统中 ✉️")
        else:
            st.warning("请先填写食物名称")

