A Github README plugin to generate map-data based on profile visits!

# Features
- Light/dark mode
- Top 5 regions
- Highlighted map with all country visits

# Usage
1. Add the following to your README:
   ```markdown
   ![Map](https://readme-map.shuchir.dev/USERNAME_HERE?theme=light)
   ```
2. Make sure to add a hyperlink to your map as well! Maybe something along the lines of "Add yourself to the map"- Github proxies the svg through it's own servers, so you won't be able to get a user's location through the README directly.

(or alternatively, use `?theme=dark` for dark mode)
2. Replace `USERNAME_HERE` with your GitHub username.

# Self-Hosting
1. Clone the repository:
   ```bash
   git clone https://github.com/ShuchirJ/readme-map.git
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```
