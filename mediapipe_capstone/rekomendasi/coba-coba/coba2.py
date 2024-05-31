import pandas as pd

# Data pertama
data1 = pd.DataFrame({
    'place_Id': [1, 2, 3],
    'Nama': ['Lokasi A', 'Lokasi B', 'Lokasi C']
})

# Data kedua
data2 = pd.DataFrame({
    'place_Id': [1, 2, 3],
    'Category': ['Category A', 'Category B', 'Category C'],
    'asdasdasd': ['Casdasd', 'Casdasd B', 'asdasdy C']
})

# Gabungkan DataFrame dengan memilih hanya kolom 'Category' dari data kedua
merged_data = pd.merge(data1, data2[['place_Id', 'Category']], on='place_Id', how='left')

print(merged_data)
