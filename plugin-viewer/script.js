let plugins = [];
const container = document.getElementById('plugin-container');
const searchInput = document.getElementById('search');
const tagFilter = document.getElementById('tag-filter');
const toggleCRT = document.getElementById('toggle-crt');

const detail = document.getElementById('plugin-detail');
const detailName = document.getElementById('detail-name');
const detailPreview = document.getElementById('detail-preview');
const detailDescription = document.getElementById('detail-description');
const detailTags = document.getElementById('detail-tags');
const detailDownload = document.getElementById('detail-download');
const detailRating = document.getElementById('detail-rating');
const detailChangelog = document.getElementById('detail-changelog');

fetch('https://izlcnpelomuuwxijnnuh.supabase.co/storage/v1/object/public/hauswerk.official/official_plugins.json')
  .then(r => r.json())
  .then(data => {
    plugins = data;
    updateFilterOptions();
    const slug = new URLSearchParams(window.location.search).get("slug");
    if (slug) {
      showPluginDetail(slug);
    } else {
      renderPlugins();
    }
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
  detail.classList.add('hidden');
  container.classList.remove('hidden');

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
      <a href="?slug=${plugin.name}" class="download-btn">🔍 Bekijk details</a>
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

function incrementDownload(name) {
  const key = `downloads_${name}`;
  const count = parseInt(localStorage.getItem(key) || "0") + 1;
  localStorage.setItem(key, count);
}
function getRating(name) {
  return localStorage.getItem(`downloads_${name}`) || 0;
}

function showPluginDetail(slug) {
  const plugin = plugins.find(p => p.name === slug);
  if (!plugin) return;
  detail.classList.remove('hidden');
  container.classList.add('hidden');
  detailName.textContent = plugin.name;
  detailPreview.src = plugin.preview_url;
  detailDescription.innerHTML = `<p>${plugin.description}</p>`;
  detailTags.textContent = `Tags: ${plugin.tags.join(', ')}`;
  detailDownload.href = plugin.zip_url;
  detailRating.textContent = `⭐ ${getRating(plugin.name)} downloads`;
  if (plugin.changelog) {
    detailChangelog.innerHTML = "<h3>📜 Changelog:</h3><pre>" + plugin.changelog + "</pre>";
  } else {
    detailChangelog.innerHTML = "";
  }
  document.getElementById('feedback').value = "";
}

document.getElementById('back-btn').addEventListener('click', () => {
  history.pushState({}, "", window.location.pathname);
  renderPlugins();
});

function submitFeedback() {
  const text = document.getElementById('feedback').value.trim();
  if (text.length > 0) {
    alert("Bedankt voor je feedback! (nog lokaal)");
    document.getElementById('feedback').value = "";
  }
}