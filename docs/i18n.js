const LANG = localStorage.getItem("hauswerk-lang") || "nl";
document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("lang-select");
  if (select) {
    select.value = LANG;
    select.addEventListener("change", e => {
      localStorage.setItem("hauswerk-lang", e.target.value);
      location.reload();
    });
  }
});

const TEXTS = {
  nl: {
    search: "Zoek plugins...",
    status_verified: "✅ Geverifieerd",
    status_unverified: "⚠️ Ongecontroleerd",
    copy_success: "✅ JSON gekopieerd!",
    description: "Omschrijving:",
    download: "📥 Download",
    copy_json: "📋 Kopieer JSON",
    view_json: "🔍 Bekijk plugin.json"
  },
  en: {
    search: "Search plugins...",
    status_verified: "✅ Verified",
    status_unverified: "⚠️ Unverified",
    copy_success: "✅ JSON copied!",
    description: "Description:",
    download: "📥 Download",
    copy_json: "📋 Copy JSON",
    view_json: "🔍 View plugin.json"
  },
  de: {
    search: "Plugins durchsuchen...",
    status_verified: "✅ Verifiziert",
    status_unverified: "⚠️ Ungeprüft",
    copy_success: "✅ JSON kopiert!",
    description: "Beschreibung:",
    download: "📥 Herunterladen",
    copy_json: "📋 JSON kopieren",
    view_json: "🔍 Plugin.json anzeigen"
  },
  fr: {
    search: "Rechercher des plugins...",
    status_verified: "✅ Vérifié",
    status_unverified: "⚠️ Non vérifié",
    copy_success: "✅ JSON copié !",
    description: "Description :",
    download: "📥 Télécharger",
    copy_json: "📋 Copier le JSON",
    view_json: "🔍 Voir le plugin.json"
  },
  zh: {
    search: "搜索插件...",
    status_verified: "✅ 已验证",
    status_unverified: "⚠️ 未验证",
    copy_success: "✅ JSON 已复制！",
    description: "描述：",
    download: "📥 下载",
    copy_json: "📋 复制 JSON",
    view_json: "🔍 查看 plugin.json"
  }
};

function t(key) {
  return (TEXTS[LANG] && TEXTS[LANG][key]) || key;
}