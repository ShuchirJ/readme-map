# readme-map
A Github README plugin to generate map-data based on profile visits!

<img width="990" height="490" alt="image" src="https://github.com/user-attachments/assets/9eb622a2-bcfb-447f-acd1-ab62ad00b6d9" />

# Features
- Light/dark mode
- Top 5 regions
- Highlighted map with all country visits

# Usage
1. Add the following to your README:
   ```html
   <a href="https://readme-map.shuchir.dev/add/USERNAME_HERE" target="_blank">
       <img src="https://readme-map.shuchir.dev/map/?theme=dark" alt="Map of my profile visits" />
   </a>
   ```
   (or alternatively, use `?theme=light` for light mode)
2. Replace `USERNAME_HERE` with your GitHub username.
3. Visit https://readme-map.shuchir.dev/add/USERNAME_HERE so readme-map has some data to generate a map from.
4. Deploy the action workflow in actions_template.yml to your repository.
5. Run the workflow to generate the initial map.

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
