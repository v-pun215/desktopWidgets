def degrees_to_cardinal(degrees):
    directions = [
        (0, 'N'), (22.5, 'NNE'), (45, 'NE'), (67.5, 'ENE'),
        (90, 'E'), (112.5, 'ESE'), (135, 'SE'), (157.5, 'SSE'),
        (180, 'S'), (202.5, 'SSW'), (225, 'SW'), (247.5, 'WSW'),
        (270, 'W'), (292.5, 'WNW'), (315, 'NW'), (337.5, 'NNW')
    ]
    
    # Normalize the degree to be within 0-360
    degrees = degrees % 360
    
    # Find the closest direction
    for i in range(len(directions)-1):
        if degrees >= directions[i][0] and degrees < directions[i+1][0]:
            return directions[i][1]
    
    # If it's 360 degrees, it should return 'N'
    return directions[-1][1]

# Example usage:
degrees = 33
cardinal_direction = degrees_to_cardinal(degrees)
print(f"{degrees}° is {cardinal_direction}")
