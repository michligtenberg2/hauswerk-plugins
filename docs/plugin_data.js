fetch("https://raw.githubusercontent.com/michligtenberg2/hauswerk-plugins/main/plugins.json")
  .then(res => res.json())
  .then(data => {
    window.plugins = data;
    renderTagFilters();
    renderPlugins();
  });