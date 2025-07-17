fetch("https://raw.githubusercontent.com/michligtenberg2/hauswerk-plugins/main/themes.json")
  .then(res => res.json())
  .then(data => {
    window.themes = data;
    renderTagFilters();
    renderThemes();
  });
