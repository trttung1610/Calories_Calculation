import gradio as gr

def calculate_bmi(height, weight):
    # Calculate BMI using the provided height and weight
    # BMI Formula: weight (kg) / (height (m) ** 2)
    height_m = height / 100  # Convert height from cm to m
    bmi = weight / (height_m ** 2)
    return bmi

def calculate_bmr(age, gender, height, weight):
    # Calculate Basal Metabolic Rate (BMR) using the provided age, gender, height, and weight
    if gender == "Nam":
        # BMR Formula for males: 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        # BMR Formula for females: 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_tdee(bmr, activity_level):
    # Calculate Total Daily Energy Expenditure (TDEE) using the provided BMR and activity level
    tdee = bmr * activity_level
    return tdee

def calculate_daily_calories_goal(tdee, goal):
    # Calculate the daily calorie goal based on the provided TDEE and goal
    if goal == "Giảm cân":
        calories_goal = tdee - 500  # Aim for a 500 calorie deficit per day for weight loss
    elif goal == "Tăng cân":
        calories_goal = tdee + 500  # Aim for a 500 calorie surplus per day for weight gain
    else:
        calories_goal = tdee  # Maintain current weight
    if calories_goal < 0 : 
        return 0
    else :
        return calories_goal

def get_activity_factor(activity_input):
    """
    Get the activity factor based on the selected option.

    Args:
        activity_input (str): Selected activity option.

    Returns:
        float: Activity factor based on the selected option.
    """
    activity_factor_map = {
        'Không': 1.2,
        'Có': 1.55,
        'Thường Xuyên': 1.725
    }

    return activity_factor_map.get(activity_input, 1.2)

def process(height, weight, age, gender, activities, goal):
    # Determine activity level
    activity_level = get_activity_factor(activities)

    # Calculate BMR
    bmr = calculate_bmr(age, gender, height, weight)

    # Calculate TDEE
    tdee = calculate_tdee(bmr, activity_level)
    
    # Calculate BMI
    bmi = calculate_bmi(height, weight)
    
    # Determine BMI category based on gender
    bmi_category = ""
    if gender == "Nam":
        if bmi < 20:
            bmi_category = "Thiếu cân, cần có chế độ ăn phù hợp để cải thiện tình trạng này"
        elif 20 <= bmi < 25:
            bmi_category = "Bình thường, thậm chí ở trong tình trạng tốt nếu bạn thường xuyên tập thể dục và ăn một chế độ ăn hợp lý"
        elif 25 <= bmi < 30:
            bmi_category = "Thừa cân, cần áp dụng biện pháp để khắc phục tình trạng trên"
        else:
            bmi_category = "Béo phì nặng, nếu không cải thiện sớm có thể gây ra các vấn đề liên quan đến tiêu hóa, hệ tuần hoàn, v.v."
    else:
        if bmi < 18:
            bmi_category = "Thiếu cân, thiếu dinh dưỡng"
        elif 18 <= bmi < 23:
            bmi_category = "Bình thường"
        elif 23 <= bmi < 30:
            bmi_category = "Thừa cân"
        else:
            bmi_category = "Béo phì"

    # Calculate daily calorie goal
    calo_suggestion = calculate_daily_calories_goal(tdee, goal)

    return bmi, bmr, tdee, bmi_category, calo_suggestion

inputs = [
    gr.inputs.Number(label=" Chiều Cao (cm)"),
    gr.inputs.Number(label=" Cân Nặng (kg)"),
    gr.inputs.Number(label="Tuổi"),
    gr.inputs.Radio(['Nam', 'Nữ'], label="Giới Tính"),
    gr.inputs.Radio(['Không', "Có", 'Thường Xuyên'], label="Hoạt Động Thể Thao", default="Không" ),
    gr.inputs.Radio(['Giảm cân', 'Tăng cân', 'Duy trì'], label="Mục Tiêu", default="Giảm cân")
]

outputs = [
    gr.outputs.Textbox(label="Chỉ số BMI"),
    gr.outputs.Textbox(label="Chỉ số BMR"),
    gr.outputs.Textbox(label="Chỉ số TDEE"),
    gr.outputs.Textbox(label="Lượng Calories mỗi ngày nên là:")
]

def do(height, weight, age, gender, activities, goal):
    bmi, bmr, tdee, bmi_category, calorie_goal = process(height, weight, age, gender, activities, goal)

    # Format the values with 2 decimal places
    bmi = "{:.1f}".format(bmi)
    bmr = "{:.1f}".format(bmr)
    tdee = "{:.1f}".format(tdee)
    calorie_goal = "{:.1f}".format(calorie_goal)
    
    bmr = f"{bmr} / Ngày"
    tdee = f"{tdee} / Ngày"
    calorie_goal = f"{calorie_goal} / Ngày "
    return bmi,bmr,tdee, calorie_goal


# Create a Gradio interface
interface = gr.Interface(fn=do, inputs=inputs, outputs=outputs,allow_flagging="never")

# Launch the interface
interface.launch()
