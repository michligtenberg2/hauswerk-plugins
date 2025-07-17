// Theme Shop browser
function getActiveTags() {
  return [...document.querySelectorAll('.filter-button.active')].map(b => b.innerText);
}

function uniqueTags(items) {
  const all = items.flatMap(p => p.tags || []);
  return [...new Set(all)];
}

function renderTagFilters() {
  const filterDiv = document.getElementById('tagFilters');
  const tags = uniqueTags(window.themes);
  filterDiv.innerHTML = '';
  tags.forEach(tag => {
    const btn = document.createElement('span');
    btn.className = 'filter-button';
    btn.innerText = tag;
    btn.onclick = () => {
      btn.classList.toggle('active');
      renderThemes(document.getElementById('searchInput').value);
    };
    filterDiv.appendChild(btn);
  });
}

function renderThemes(filter = '') {
  const container = document.getElementById('pluginContainer');
  container.innerHTML = '';
  const q = filter.toLowerCase();
  const activeTags = getActiveTags();
  let count = 0;
  let sorted = [...window.themes];
  sorted.sort((a, b) => a.name.localeCompare(b.name));
  sorted.forEach(t => {
    const matchQuery =
      t.name.toLowerCase().includes(q) ||
      t.tags.join(' ').toLowerCase().includes(q) ||
      (t.description || '').toLowerCase().includes(q);
    const matchTags = activeTags.length === 0 || activeTags.every(x => t.tags.includes(x));
    if (matchQuery && matchTags) {
      count++;
      const card = document.createElement('div');
      card.className = 'plugin-card';
      const tags = t.tags.map(tag => `<span class='tag'>${tag}</span>`).join(' ');
      const jsonStr = JSON.stringify(t, null, 2);
      card.innerHTML = `
        <h2>${t.name} ${tags}</h2>
        <img src="${t.preview}" alt="preview" style="width:100%;max-width:400px;cursor:pointer;" onclick="showPreview('${t.preview}')">
        <p>${t.description}</p>
        <p><a class="button" href="${t.zip_url}" download>Download</a>
           <button onclick='copyJSON(`${jsonStr}`)'>JSON</button></p>
        <details><summary>Bekijk JSON</summary><pre><code>${jsonStr}</code></pre></details>
      `;
      container.appendChild(card);
    }
  });
  const countEl = document.getElementById('pluginCount');
  if (countEl) {
    countEl.innerText = `(${count})`;
  }
}

function copyJSON(text) {
  navigator.clipboard.writeText(text).then(() => alert('Gekopieerd!'));
}

function showPreview(src) {
  const overlay = document.getElementById('previewOverlay');
  document.getElementById('previewImage').src = src;
  overlay.style.display = 'flex';
}

window.addEventListener('DOMContentLoaded', () => {
  renderTagFilters();
  renderThemes();
  document.getElementById('searchInput').addEventListener('input', e => {
    renderThemes(e.target.value);
  });
});
