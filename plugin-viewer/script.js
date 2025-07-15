fetch('https://izlcnpelomuuwxijnnuh.supabase.co/storage/v1/object/public/hauswerk.official/official_plugins.json')
  .then(response => response.json())
  .then(plugins => {
    const container = document.getElementById('plugin-container');
    plugins.forEach(plugin => {
      const div = document.createElement('div');
      div.className = 'plugin';
      div.innerHTML = `
        <h2>${plugin.name}</h2>
        <img src="${plugin.preview_url}" alt="preview">
        <p><strong>Beschrijving:</strong> ${plugin.description}</p>
        <p><strong>Tags:</strong> ${plugin.tags.join(', ')}</p>
        <a href="${plugin.zip_url}" class="download-btn">⬇️ Download</a>
      `;
      container.appendChild(div);
    });
  })
  .catch(err => {
    document.getElementById('plugin-container').innerHTML = '<p style="color: red;">Fout bij laden plugins.</p>';
  });