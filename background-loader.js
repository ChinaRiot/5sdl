
function extractBeatmapSetId(url) {
  const match = url.match(/beatmapsets\/(\d+)/);
  return match ? match[1] : null;
}


async function loadBackgroundImages() {
  const demonEntries = document.querySelectorAll('.demon-entry');
  
  for (const entry of demonEntries) {
    const descriptionLink = entry.querySelector('.description a');
    
    if (!descriptionLink) continue; 
    
    const mapUrl = descriptionLink.href;
    const beatmapSetId = extractBeatmapSetId(mapUrl);
    
    if (!beatmapSetId) continue;
    
    try {

      const backgroundUrl = `https://assets.ppy.sh/beatmaps/${beatmapSetId}/covers/cover.jpg`;
      

      entry.style.setProperty('--bg-image', `url('${backgroundUrl}')`);
      entry.classList.add('with-background');
      
    } catch (error) {
      console.error(`Failed to load background for beatmap ${beatmapSetId}:`, error);
    }
  }
}


if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', loadBackgroundImages);
} else {
  loadBackgroundImages();
}
