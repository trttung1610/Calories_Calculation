from fuzzywuzzy import fuzz
import pandas as pd
import gradio as gr

def calculate_total_calories(user_input):
    df_menu = pd.read_excel('calories.xlsx')

    # Split the user input into individual menu items
    menu_items = user_input.split(',')

    total_calories = 0
    results = []

    for item in menu_items:
        # Split the menu item into quantity and item name or unit and item name
        parts = item.strip().split(' ', 1)

        if len(parts) == 2:
            first_part = parts[0]
            second_part = parts[1]

            # Check if the first part is a valid quantity (e.g., "200g")
            try:
                quantity = float(first_part)
                item_name = second_part
            except ValueError:
                quantity = 1.0  # Assume a default quantity of 1 if not specified
                unit = first_part
                item_name = second_part
        else:
            quantity = 1.0  # Assume a default quantity of 1 if not specified
            item_name = item.strip()

        # Calculate the similarity scores between the item name and menu item names
        similarity_scores = df_menu['food'].apply(lambda x: fuzz.token_set_ratio(x.lower(), item_name.lower()))

        # Find the closest match with the highest similarity score
        closest_match_index = similarity_scores.idxmax()
        closest_match_score = similarity_scores[closest_match_index]

        # Check if the similarity score is above a certain threshold
        threshold = 60
        if closest_match_score < threshold:
            results.append("Không tìm thấy thông tin thức ăn: " + item_name)
            continue

        # Get the closest match menu item details
        closest_match = df_menu.loc[closest_match_index]
        menu_name = closest_match['food']
        item_unit = closest_match['unit']
        calories = closest_match['calo']

        if quantity != 1.0:
            # Check if the quantity is in grams or milliliters
            if item_unit.lower() == 'g' or item_unit.lower() == 'gram':
                quantity = float(quantity)
            elif item_unit.lower() == 'l' or item_unit.lower() == 'lit':
                quantity = float(quantity) * 1000

        # Calculate the total calories for the current menu item
        item_calories = (calories / item_unit) * quantity
        total_calories += item_calories
        results.append("Tên món ăn: " + menu_name)
        results.append("Lượng: " + str(quantity) + " " + item_unit)
        results.append("Lượng calories: " + str(item_calories) + " Kcals")
        results.append("")  # Add an empty entry for spacing

    results.append(str(total_calories) + " Kcals")
    return "\n".join(results[0:-1]), results[-1]

output_text = [
    gr.outputs.Textbox(label="Thông tin các thành phần trong bữa ăn"),
    gr.outputs.Textbox(label="Tổng lượng calories của bữa ăn")
]

def gradio_interface():
    input_text = gr.inputs.Textbox(label="Hãy cho tôi biết bữa ăn hôm nay của bạn")
    gr_interface = gr.Interface(fn=calculate_total_calories, inputs=input_text, outputs=output_text, title="Tính Toán Thực Đơn Hằng Ngày", examples=["1 phần cơm tấm sườn bì, 2 trái chuối", "1 phần phở bò, 1 phần bánh Flan"])
    return gr_interface

if __name__ == "__main__":
    gr_interface = gradio_interface()
    gr_interface.launch()
