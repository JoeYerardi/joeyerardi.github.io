const search = document.querySelector("#archive-search");
const input = document.querySelector("#query");
const status = document.querySelector("#search-status");
const clips = Array.from(document.querySelectorAll("[data-clip]"), (node) => ({
  node,
  text: node.textContent.toLowerCase().replace(/\s+/g, " "),
}));

function filterClips() {
  const query = input.value.trim().toLowerCase().replace(/\s+/g, " ");
  let count = 0;

  for (const clip of clips) {
    const matches = clip.text.includes(query);
    clip.node.hidden = !matches;
    if (matches) count += 1;
  }

  status.textContent = count === 1 ? "1 clip" : `${count} clips`;
}

input.addEventListener("input", filterClips);
search.hidden = false;
filterClips();
