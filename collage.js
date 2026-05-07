document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('grid');

  contributors.forEach(c => {
    const article = document.createElement('article');
    article.className = `card card--${c.size}`;

    article.innerHTML = `
      <img
        class="card__image"
        src="${c.image}"
        alt="${c.object}"
        loading="lazy"
      >
      <div class="card__overlay" aria-hidden="true">
        <div class="card__content">
          <h3 class="card__object">${c.object}</h3>
          <p class="card__reason">${c.reason}</p>
          <span class="card__name">&mdash;&thinsp;${c.name}</span>
        </div>
      </div>
      <div class="card__caption">
        <strong>${c.object}</strong>
        <span>&mdash; ${c.name}</span>
      </div>
    `;

    // Mobile: tap toggles the overlay; second tap or tap elsewhere dismisses
    article.addEventListener('click', () => {
      const alreadyActive = article.classList.contains('is-active');
      document.querySelectorAll('.card.is-active')
        .forEach(el => el.classList.remove('is-active'));
      if (!alreadyActive) article.classList.add('is-active');
    });

    grid.appendChild(article);
  });

  // Clicking outside any card collapses all overlays
  document.addEventListener('click', e => {
    if (!e.target.closest('.card')) {
      document.querySelectorAll('.card.is-active')
        .forEach(el => el.classList.remove('is-active'));
    }
  });
});
