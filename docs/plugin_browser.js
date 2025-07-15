// 🔍 Zoek- en filterfunctionaliteit
function getActiveTags() {
  return [...document.querySelectorAll(".filter-button.active")].map(b => b.innerText);
}

function uniqueTags(plugins) {
  const all = plugins.flatMap(p => p.tags || []);
  return [...new Set(all)];
}

function renderTagFilters() {
  const filterDiv = document.getElementById("tagFilters");
  const tags = uniqueTags(window.plugins);
  filterDiv.innerHTML = "";
  tags.forEach(tag => {
    const btn = document.createElement("span");
    btn.className = "filter-button";
    btn.innerText = tag;
    btn.onclick = () => {
      btn.classList.toggle("active");
      renderPlugins(document.getElementById("searchInput").value);
    };
    filterDiv.appendChild(btn);
  });
}

function renderStars(rating = 0) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  return "⭐".repeat(full) + (half ? "½" : "");
}

const TAG_DESCRIPTIONS = {
  "audio": "🎧 Audio plugin",
  "video": "📹 Video tool",
  "official": "✅ Officiële plugin",
  "beta": "🧪 Experimenteel",
  "effect": "✨ Visueel effect",
  "utility": "🛠️ Hulpprogramma"
};

function copyJSON(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert(t("copy_success"));
  });
}

function showPreview(src) {
  const overlay = document.getElementById("previewOverlay");
  document.getElementById("previewImage").src = src;
  overlay.style.display = "flex";
}

function renderPlugins(filter = "") {
  const container = document.getElementById("pluginContainer");
  container.innerHTML = "";
  const q = filter.toLowerCase();
  const activeTags = getActiveTags();
  let count = 0;

  let sorted = [...window.plugins];
  const sort = document.getElementById("sort-select").value;
  if (sort === "name") {
    sorted.sort((a, b) => a.name.localeCompare(b.name));
  } else if (sort === "verified") {
    sorted.sort((a, b) => (b.verified === true) - (a.verified === true));
  }

  sorted.forEach(p => {
    const matchQuery =
      p.name.toLowerCase().includes(q) ||
      p.tags.join(" ").toLowerCase().includes(q) ||
      (p.description || "").toLowerCase().includes(q);

    const matchTags = activeTags.length === 0 || activeTags.every(t => p.tags.includes(t));
    if (matchQuery && matchTags) {
      count++;
      const card = document.createElement("div");
      card.className = "plugin-card";
      const tags = p.tags.map(t => {
        const cls = `tag-${t.toLowerCase().replace(/\s+/g, '-')}`;
        const tip = TAG_DESCRIPTIONS[t.toLowerCase()] || t;
        return `<span class='tag ${cls}' title='${tip}'>${tip}</span>`;
      }).join(" ");
      const verified = p.verified ? t("status_verified") : t("status_unverified");
      const jsonStr = JSON.stringify(p, null, 2);

      card.innerHTML = `
        <h2>${p.name} ${tags}</h2>
        <p class="rating">${renderStars(p.rating || 0)}</p>
        <img src="${p.path}/${p.preview}" alt="preview" style="width: 100%; max-width: 400px; cursor: pointer;" onclick="showPreview('${p.path}/${p.preview}')">
        <p><strong>Status:</strong> ${verified}</p>
        <p><strong>${t("description")}</strong> ${p.description || ""}</p>
        <p>
          <a class="button" href="${p.path}/${p.zip}" download>${t("download")}</a>
          <button onclick='copyJSON(`${jsonStr}`)'>${t("copy_json")}</button>
        </p>
        <details>
          <summary>${t("view_json")}</summary>
          <pre><code>${jsonStr}</code></pre>
        </details>
      `;
      container.appendChild(card);
    }
  });
  document.getElementById("pluginCount").innerText = `(${count})`;
}

// Event listeners
window.addEventListener("DOMContentLoaded", () => {
  renderTagFilters();
  renderPlugins();
  document.getElementById("searchInput").placeholder = t("search");

  document.getElementById("searchInput").addEventListener("input", e => {
    renderPlugins(e.target.value);
  });

  document.getElementById("sort-select").addEventListener("change", () => {
    renderPlugins(document.getElementById("searchInput").value);
  });

  // Info overlay
  document.getElementById("about-toggle").addEventListener("click", () => {
    document.getElementById("aboutOverlay").style.display = "flex";
  });
  document.getElementById("aboutOverlay").addEventListener("click", (e) => {
    if (e.target.id === "aboutOverlay") {
      e.target.style.display = "none";
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.getElementById("aboutOverlay").style.display = "none";
      document.getElementById("previewOverlay").style.display = "none";
    }
  });
});