import pandas as pd
import sys
# Read argument from command line
filename = sys.argv[1]

data = pd.read_csv('colordata/data.csv')
output = pd.DataFrame(columns=['R', 'G', 'B', 'Tag'])

# Read text and extract keywords from prompt file
with open('colordata/prompt.txt', 'r') as file:
    prompt = file.read()
    keywords = prompt.split(',')

# Iterate over the keywords and filter the DataFrame
for word in keywords:
    filtered_data = data[data['Name'].str.contains(word, case=False, na=False)]
    rgb = filtered_data['Color_Code (R,G,B)']
    # RGB format is (R,G,B) so we need to split the string and convert to int
    rgb = rgb.str.split(',', expand=True)
    # Create a new row with the RGB values and the keyword
    new_row = pd.DataFrame({'R': rgb[0], 'G': rgb[1], 'B': rgb[2], 'Tag': word})
    output = output.append(new_row)

output.to_csv('colordata/output_'+filename+'.csv', index=False)

    