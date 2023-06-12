import pandas as pd

df = pd.read_excel("./vietnamekcal.xlsx")

def convert_quantity(quantity):
    quantity_parts = quantity.strip().split(' ')
    amount = quantity_parts[0]
    detail = ' '.join(quantity_parts[1:])
    try:
        return float(amount), detail
    except ValueError:
        return amount, detail

new_df = pd.DataFrame()
new_df['food'] = df['THỨC ĂN'].str.lower().str.strip()
new_df['amount'], new_df['detail'] = zip(*df['SỐ LƯỢNG'].apply(convert_quantity))
new_df['calo'] = (df['CALO (kcal)'] / new_df['amount'].apply(lambda x: float(x) if isinstance(x, str) else x)).astype(int)
new_df['amount'] = 1 

new_df.to_excel('calories.xlsx', index=False)  # Save as Excel file without including the index