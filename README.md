# G(alactic)PS

A Python project using Celestia to estimate the galactic position based on a starfield image. This project simulates starfield images at various galactic coordinates and compares them with an input image to determine the most likely position in the galaxy.

## Features
- **Starfield Simulation**: Uses Celestia to capture images of the galaxy at different coordinates.
- **Image Comparison**: Matches the input starfield image to simulated images to estimate the galactic position.
- **Refinement Process**: Conducts a second round of simulation around the initial best match to refine the estimated location.
- **Python Integration**: Entire process controlled through Python scripts.

## Requirements
- Python 3.x
- OpenCV
- Celestia
- NumPy

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/G(alactic)PS.git
   cd galactic-position-estimator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Celestia**:
   Follow the instructions on the [Celestia website](https://celestia.space) to install Celestia.

## Usage
1. **Prepare the input image**: Place your starfield image as `input_starfield.jpg` in the project directory.
2. **Run the main script**:
   ```bash
   python main.py
   ```
3. **View results**: The script will output the estimated galactic longitude and latitude. It will also generate directories with simulated starfield images.

## Project Structure
- `main.py`: The main script that orchestrates the simulation and comparison process.
- `celestia_control.py`: Controls Celestia to capture starfield images at specified coordinates.
- `image_comparison.py`: Handles the loading and comparison of images to find the best match.
- `requirements.txt`: Lists the Python dependencies required for the project.

## Roadmap
1. **Initial Simulation**: Capture a coarse grid of starfield images across the galaxy.
2. **Image Comparison**: Compare the input image to the simulated images to find the best match.
3. **Refinement Simulation**: Capture a finer grid of images around the initial best match.
4. **Final Comparison**: Refine the location estimate using the refined images.

## Future Enhancements
- **Machine Learning Integration**: Incorporate machine learning to improve matching accuracy and efficiency.
- **GUI Development**: Create a graphical user interface for easier interaction with the program.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for improvements and bug fixes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

