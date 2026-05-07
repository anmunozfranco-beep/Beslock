(() => {
  const cards = document.querySelectorAll('[data-beslock-product-card]');
  if (!cards.length) {
    return;
  }

  cards.forEach((card) => {
    card.setAttribute('data-beslock-ready', 'true');
  });
})();
