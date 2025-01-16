from celestia_control import capture_starfields
from image_comparison import load_images, find_best_match

def main():
    input_image_path = 'input_starfield.jpg'

    # Step 1: Initial coarse grid search
    capture_starfields(step=10, grid_size=18, output_directory='celestia_starfields')
    images = load_images('celestia_starfields')
    best_coords, best_score = find_best_match(input_image_path, images)
    print(f"Initial Best Match: Longitude {best_coords[0]}°, Latitude {best_coords[1]}° with score {best_score}")

    # Step 2: Refined search around the best match
    capture_starfields(start_longitude=best_coords[0], start_latitude=best_coords[1], step=1, grid_size=2, output_directory='refined_celestia_starfields')
    refined_images = load_images('refined_celestia_starfields')
    refined_coords, refined_score = find_best_match(input_image_path, refined_images)
    print(f"Refined Best Match: Longitude {refined_coords[0]}°, Latitude {refined_coords[1]}° with score {refined_score}")

if __name__ == "__main__":
    main()
