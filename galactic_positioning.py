import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from scipy.spatial import distance
from PIL import Image
import plotly.graph_objects as go

# Load Gaia data
def load_gaia_data(file_path, max_stars=100000):
    data = pd.read_csv(file_path)
    valid_data = data.dropna(subset=['RA_ICRS', 'DE_ICRS', 'Dist'])
    valid_data = valid_data.iloc[:max_stars]
    ra, dec, dist = valid_data['RA_ICRS'], valid_data['DE_ICRS'], valid_data['Dist']
    x = dist * np.cos(np.radians(ra)) * np.cos(np.radians(dec))
    y = dist * np.sin(np.radians(ra)) * np.cos(np.radians(dec))
    z = dist * np.sin(np.radians(dec))
    return np.vstack((x, y, z)).T

# Simulate star images
def simulate_star_images(observer_positions, observer_orientations, star_positions):
    simulated_images = []
    for pos, orientation in zip(observer_positions, observer_orientations):
        viewed_stars = transform_view(pos, orientation, star_positions)
        x_proj, y_proj = project_to_sky(viewed_stars)
        simulated_images.append((x_proj, y_proj, viewed_stars))
    return simulated_images

# Transform stars based on observer's orientation
def transform_view(observer_pos, orientation, stars):
    stars_translated = stars - observer_pos
    rotation_matrix = np.array([
        [np.cos(np.radians(orientation[2])), -np.sin(np.radians(orientation[2])), 0],
        [np.sin(np.radians(orientation[2])), np.cos(np.radians(orientation[2])), 0],
        [0, 0, 1]
    ])
    return np.dot(stars_translated, rotation_matrix.T)

# Project stars to 2D sky
def project_to_sky(stars):
    return stars[:, 0], stars[:, 1]

# Load and process sky image
def load_and_process_sky_image(image_path):
    image = Image.open(image_path).convert("L")
    image_array = np.array(image)
    threshold = 200
    return np.column_stack(np.where(image_array > threshold))

# Compare simulated images with the real image
def compare_images(real_image, simulated_images):
    max_similarity = -1
    best_match_index = -1
    real_image_2d = np.zeros((1000, 1000))
    for x, y in real_image:
        real_image_2d[int(x) % 1000, int(y) % 1000] = 1
    for idx, (sim_x_proj, sim_y_proj, _) in enumerate(simulated_images):
        simulated_image_2d = np.zeros((1000, 1000))
        for x, y in zip(sim_x_proj, sim_y_proj):
            simulated_image_2d[int(x) % 1000, int(y) % 1000] = 1
        similarity = ssim(real_image_2d, simulated_image_2d, data_range=1.0)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match_index = idx
    return best_match_index, max_similarity

# Estimate position based on the best match
def estimate_position(best_match_index, observer_positions, observer_orientations):
    return observer_positions[best_match_index], observer_orientations[best_match_index]

# Calculate the look vector based on orientation
def calculate_look_vector(orientation):
    # Assume initial look vector points along the positive Z-axis
    look_vector = np.array([0, 0, 1])
    
    # Apply yaw rotation around Z-axis
    yaw_rotation = np.array([
        [np.cos(np.radians(orientation[2])), -np.sin(np.radians(orientation[2])), 0],
        [np.sin(np.radians(orientation[2])), np.cos(np.radians(orientation[2])), 0],
        [0, 0, 1]
    ])
    
    return np.dot(look_vector, yaw_rotation.T)

def main():
    star_positions = load_gaia_data(".\\dataGaia.csv")
    observer_positions = [
        np.array([0, 0, 0]), np.array([1000, 0, 0]),
        np.array([0, 1000, 0]), np.array([0, 0, 1000]),
        np.array([500, 500, 500]),
        np.array([200, 300, 400]), np.array([800, 500, 300]),
        np.array([1500, 200, 500]), np.array([700, 800, 600]),
        np.array([1200, 100, 1500]), np.array([300, 600, 800]),
        np.array([450, 900, 200]), np.array([100, 100, 100]),
        np.array([1600, 1300, 1000]), np.array([2500, 1500, 1000])
    ]

    observer_orientations = [
        np.array([0, 0, 0]), np.array([0, 0, 0]),
        np.array([30, 45, 0]), np.array([60, 90, 180]),
        np.array([90, 180, 270]),
        np.array([45, 30, 45]), np.array([90, 60, 90]),
        np.array([120, 75, 30]), np.array([30, 60, 180]),
        np.array([90, 90, 0]), np.array([45, 180, 45]),
        np.array([60, 30, 60]), np.array([180, 45, 135]),
        np.array([0, 0, 270]), np.array([45, 45, 0])
    ]

    simulated_images = simulate_star_images(observer_positions, observer_orientations, star_positions)
    real_image_path = ".\\test1-celestia.png"
    real_image = load_and_process_sky_image(real_image_path)
    best_match_idx, similarity = compare_images(real_image, simulated_images)
    estimated_position, estimated_orientation = estimate_position(best_match_idx, observer_positions, observer_orientations)
    print(f"Best match index: {best_match_idx}, Similarity: {similarity}")
    print(f"Estimated Position: {estimated_position}, Estimated Orientation: {estimated_orientation}")
    best_sim_x, best_sim_y, best_simulated_stars = simulated_images[best_match_idx]
    
    # Calculate look vector direction
    look_vector = calculate_look_vector(estimated_orientation)
    
    # Plot the 3D map with the look vector
    fig = go.Figure()
    # Add observer's position
    fig.add_trace(go.Scatter3d(
    x=star_positions[:, 0],
    y=star_positions[:, 1],
    z=star_positions[:, 2],
    mode='markers',
    marker=dict(
        size=2,
        opacity=0.5,
        color=star_positions[:, 2],  # Color based on depth
        colorscale='Blues'  # Gradient from dark to bright blue
    ),
    name='Star Positions'
    ))
    
    # Add observer's position
    fig.add_trace(go.Scatter3d(
        x=[estimated_position[0]],
        y=[estimated_position[1]],
        z=[estimated_position[2]],
        mode='markers',
        marker=dict(size=5, color='red', symbol='circle'),
        name='Estimated Position'
    ))
    
    # Add Earth's position
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=5, color='#00BFFF', symbol='circle'),
        name='Earth'
    ))
    
    # Add look vector (direction observer is facing)
    fig.add_trace(go.Scatter3d(
        x=[estimated_position[0], estimated_position[0] + look_vector[0] * 100],
        y=[estimated_position[1], estimated_position[1] + look_vector[1] * 100],
        z=[estimated_position[2], estimated_position[2] + look_vector[2] * 100],
        mode='lines',
        line=dict(color='yellow', width=4),
        name='Look Vector'
    ))
    
    title_text = "3D Star Positions from Gaia Data (With Estimated Position, Earth, and Look Vector)"

    fig.update_layout(
        title=title_text,
        scene=dict(
            xaxis_title='X (light-years)',
            yaxis_title='Y (light-years)',
            zaxis_title='Z (light-years)',
            bgcolor='black'
        ),
        template='plotly_dark'
    )
        # Add match information as a subtitle
    subtitle_text = f"Best match index: {best_match_idx}, Similarity: {similarity:.6f} | " \
                    f"Estimated Position: {estimated_position.tolist()} | " \
                    f"Estimated Orientation: {estimated_orientation.tolist()}"

    fig.update_layout(title_text=title_text + "<br><sup>" + subtitle_text + "</sup>")

    fig.show()

if __name__ == "__main__":
    main()
