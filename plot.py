import csv
import matplotlib.pyplot as plt

# Read the CSV file
with open('locations_coords.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        name = row[0]
        coords = row[1:]

        # Extract x and y coordinates from each point
        x_coords = []
        y_coords = []
        for coord in coords:
            coord = coord.strip().strip('"')  # Remove leading/trailing whitespace and quotes
            if '|' in coord:
                x, y = coord.split('|')
                x_coords.append(float(x))
                y_coords.append(float(y))
            else:
                coord_parts = coord.split(', ')
                if len(coord_parts) == 2:
                    x, y = coord_parts
                    x_coords.append(float(x))
                    y_coords.append(float(y))
                else:
                    print(f"Invalid coordinate format: {coord}")

        if len(x_coords) > 0 and len(y_coords) > 0:
            # Add the first point to the end to close the polygon
            x_coords.append(x_coords[0])
            y_coords.append(y_coords[0])

            # Plot the polygon
            plt.plot(x_coords, y_coords, marker='o', linestyle='-', label=name)
        else:
            print(f"No valid coordinates found for {name}")

# Set labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Polygon Visualization')

# Add a legend
plt.legend()

# Display the plot
plt.show()
