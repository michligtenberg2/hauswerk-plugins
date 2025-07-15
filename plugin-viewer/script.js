const container = document.getElementById('plugin-container');
const searchInput = document.getElementById('search');
const tagFilter = document.getElementById('tag-filter');
const toggleCRT = document.getElementById('toggle-crt');

let plugins = [];

fetch('https://izlcnpelomuuwxijnnuh.supabase.co/storage/v1/object/public/hauswerk.official/official_plugins.json')
  .then(r => r.json())
  .then(data => {
    plugins = data;
    updateFilterOptions();
    renderPlugins();
  });

function updateFilterOptions() {
  const tags = new Set();
  plugins.forEach(p => p.tags.forEach(t => tags.add(t)));
  tags.forEach(tag => {
    const opt = document.createElement('option');
    opt.value = tag;
    opt.textContent = tag;
    tagFilter.appendChild(opt);
  });
}

function renderPlugins() {
  container.innerHTML = '';
  const term = searchInput.value.toLowerCase();
  const tag = tagFilter.value;
  plugins.filter(p => {
    return (!tag || p.tags.includes(tag)) &&
           (p.name.toLowerCase().includes(term) || p.description.toLowerCase().includes(term));
  }).forEach(plugin => {
    const div = document.createElement('div');
    div.className = 'plugin';
    const stars = getRating(plugin.name);
    div.innerHTML = `
      <h2>${plugin.name}</h2>
      <img src="${plugin.preview_url}" alt="preview" data-full="${plugin.preview_url}">
      <p><strong>Beschrijving:</strong> ${plugin.description}</p>
      <p><strong>Tags:</strong> ${plugin.tags.join(', ')}</p>
      <a href="${plugin.zip_url}" class="download-btn" onclick="incrementDownload('${plugin.name}')">⬇️ Download</a>
      <div class="rating">⭐ ${stars} downloads</div>
    `;
    container.appendChild(div);
  });
}

searchInput.addEventListener('input', renderPlugins);
tagFilter.addEventListener('change', renderPlugins);
toggleCRT.addEventListener('click', () => {
  document.body.classList.toggle('crt-amber');
  document.body.classList.toggle('crt-invert');
});

// Downloads counter via localStorage
function incrementDownload(name) {
  const key = `downloads_${name}`;
  const count = parseInt(localStorage.getItem(key) || "0") + 1;
  localStorage.setItem(key, count);
  renderPlugins();
}
function getRating(name) {
  return localStorage.getItem(`downloads_${name}`) || 0;
}

// Preview modal
document.addEventListener('click', (e) => {
  if (e.target.tagName === 'IMG' && e.target.dataset.full) {
    const modal = document.getElementById('modal');
    const modalImg = document.getElementById('modal-img');
    modalImg.src = e.target.dataset.full;
    modal.classList.remove('hidden');
  }
});
document.getElementById('modal-close').addEventListener('click', () => {
  document.getElementById('modal').classList.add('hidden');
});