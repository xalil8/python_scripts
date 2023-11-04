import cv2
import numpy as np
import pandas as pd
from collections import Counter

# Define map names
map_names = ["long", "short"]
# Define copy variable for file naming
copy = "2"

# Process images for each map name
for map_name in map_names:
    # Read the map image
    image = cv2.imread(f'{map_name}.png')
    # Read the heatmap data from CSV
    data = pd.read_csv(f'{map_name}_heatmap.csv')

    # Define polygon points based on the map name
    if map_name == "short":
        # Define polygon for the 'short' map
        POLYGON_POINTS = np.array([[761, 714], [289, 28], [162, 70], [349, 711]], np.int32)
        # Adjust the x coordinates based on y coordinate ranges
        data.loc[data['y'] > 400, 'x'] += 70
        data.loc[(data['y'] > 300) & (data['y'] <= 400), 'x'] += 45
        data.loc[(data['y'] > 180) & (data['y'] <= 300), 'x'] += 15
        # No change is needed for y <= 180
    else:
        # Define polygon for other maps (e.g., 'long')
        POLYGON_POINTS = np.array([[393, 47], [448, 714], [847, 715], [559, 24]], np.int32)
    
    # Create a binary mask for the polygon area
    mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    cv2.fillPoly(mask, [POLYGON_POINTS], 255)  # 255 for the area inside the polygon

    # Determine if points are within the polygon using the mask
    data['in_polygon'] = [mask[y, x] for x, y in zip(data['x'], data['y'])]
    # Filter out data points outside the polygon
    filtered_data = data[data['in_polygon'] == 255]

    # Apply a frequency limit to points within the polygon
    # Here we are keeping points with occurrences less than or equal to 5000
    filtered_data = filtered_data.groupby(['x', 'y']).filter(lambda group: len(group) <= 5000)

    # Count occurrences of each coordinate within the polygon after frequency filtering
    coordinate_counts = Counter(zip(filtered_data['x'], filtered_data['y']))

    # Initialize the heatmap with zeros
    heat_map = np.zeros_like(image[:, :, 0]).astype(np.float32)
    # Get the maximum count to normalize the heatmap intensity
    max_count = max(coordinate_counts.values()) if coordinate_counts else 1  # Avoid division by zero
    
    # Populate the heatmap based on coordinate counts
    for (x, y), count in coordinate_counts.items():
        # Apply a power law scaling to emphasize differences
        scaled_intensity = (count / max_count) ** 0.02
        heat_map[y, x] = scaled_intensity * 255

    # Smooth the heatmap with GaussianBlur
    smooth_heat_map = cv2.GaussianBlur(heat_map, (15, 15), 0)

    # Convert heatmap to 8-bit format to apply the color map
    heat_map_8bit = np.uint8(smooth_heat_map)
    # Apply a color map to heatmap for visualization
    colored_heat_map = cv2.applyColorMap(heat_map_8bit, cv2.COLORMAP_JET)

    # Overlay the heatmap onto the original image
    alpha = 0.5  # Transparency factor for overlay
    final_image = cv2.addWeighted(colored_heat_map, alpha, image, 1 - alpha, 0)

    # Add a text label to the heatmap
    label = "1X " if map_name == "short" else "1.58 X "
    final_image = cv2.putText(final_image, label, (1000,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 2, cv2.LINE_AA)

    # Save the final image with heatmap overlay
    cv2.imwrite(f'outputs/{map_name}{copy}.png', final_image)

# To display an image with OpenCV, uncomment the following lines:
# selected_image = 'long'  # Change as needed
# cv2.imshow('Heatmap', cv2.imread(f'outputs/{selected_image}{copy}.png'))
# cv2.waitKey(0)
# cv2.destroyAllWindows()
