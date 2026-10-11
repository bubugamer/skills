async function loadOverview() {
  const response = await fetch("/api/overview", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return response.json();
}

function renderCards(payload) {
  const grid = document.getElementById("summary-grid");
  const manifest = payload.manifest || {};
  const review = payload.review || {};
  const cards = [
    ["Files", manifest.total_files ?? 0],
    ["Directories", manifest.total_dirs ?? 0],
    ["Junk Candidates", review.junk_candidates ?? 0],
    ["Low Confidence", review.low_confidence_files ?? 0],
    ["Exact Groups", review.exact_duplicate_groups ?? 0],
    ["Plan Items", payload.plan?.item_count ?? 0]
  ];

  grid.innerHTML = cards
    .map(
      ([label, value]) => `
        <article class="card">
          <h3>${label}</h3>
          <div class="metric">${value}</div>
        </article>
      `
    )
    .join("");
}

function renderJson(id, value) {
  const node = document.getElementById(id);
  node.textContent = JSON.stringify(value, null, 2);
}

async function refresh() {
  const reviewNode = document.getElementById("review-summary");
  const planNode = document.getElementById("plan-summary");
  reviewNode.textContent = "Loading...";
  planNode.textContent = "Loading...";
  try {
    const payload = await loadOverview();
    renderCards(payload);
    renderJson("review-summary", payload.review || {});
    renderJson("plan-summary", payload.plan || { message: "No para plan generated yet." });
  } catch (error) {
    reviewNode.textContent = `Failed to load overview: ${error}`;
    planNode.textContent = "Unavailable";
  }
}

document.getElementById("refresh").addEventListener("click", refresh);
refresh();
