import pandas as pd

df = pd.read_excel(r"C:\Projects\Stroke-awareness-TY-mini-project\current_work\cleaned_datasheet_5.xlsx")
print(df["do_you_smoke?_if_so,_how_much_and_often?"].value_counts())