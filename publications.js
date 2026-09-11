(() => {
  'use strict';
  const search = document.getElementById('publication-search');
  const sort = document.getElementById('publication-sort');
  const container = document.getElementById('publication-years');
  const papers = [...document.querySelectorAll('.archive-publication')];
  const groups = [...document.querySelectorAll('.year-group')];
  const buttons = [...document.querySelectorAll('[data-venue-filter]')];
  const empty = document.getElementById('publication-empty');
  const status = document.getElementById('publication-status');
  let selectedVenue = 'all';

  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    papers.forEach(paper => {
      const matchesVenue = selectedVenue === 'all' || paper.dataset.venue === selectedVenue;
      const matchesText = !query || paper.textContent.toLocaleLowerCase().includes(query);
      paper.hidden = !(matchesVenue && matchesText);
      if (!paper.hidden) count++;
    });
    groups.forEach(group => {
      const visible = [...group.querySelectorAll('.archive-publication')].filter(paper => !paper.hidden).length;
      group.hidden = visible === 0;
      group.querySelector('h2 span').textContent = `${visible} publication${visible === 1 ? '' : 's'}`;
      const link = document.querySelector(`.year-nav a[href="#${group.id}"]`);
      if (link) link.hidden = group.hidden;
    });
    empty.hidden = count > 0;
    status.textContent = `Showing ${count} of ${papers.length} publications${selectedVenue === 'all' ? '' : ` in ${selectedVenue}`}.`;
  }
  search.addEventListener('input', filter);
  buttons.forEach(button => button.addEventListener('click', () => {
    selectedVenue = button.dataset.venueFilter;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    filter();
  }));
  sort.addEventListener('change', () => {
    const direction = sort.value === 'asc' ? 1 : -1;
    groups.sort((a,b) => direction * (Number(a.dataset.year) - Number(b.dataset.year))).forEach(group => container.insertBefore(group, empty));
    const yearNav = document.querySelector('.year-nav');
    groups.forEach(group => { const link=yearNav.querySelector(`a[href="#${group.id}"]`);if(link)yearNav.append(link); });
  });
  function revealHashTarget() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (!target || !target.matches('.archive-publication, .year-group')) return;
    if (target.hidden || target.closest('.year-group')?.hidden) {
      selectedVenue = 'all'; search.value = '';
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.venueFilter === 'all')));
      filter(); target.scrollIntoView({block:'start'});
    }
  }
  window.addEventListener('hashchange', revealHashTarget);
})();
