import { EVENT_NAMES } from '../shared/constants.js';
import { qsa } from '../shared/dom-utils.js';

export function createFilterController({ root, options, eventBus }) {
  function renderCheckboxList(title, key, entries) {
    return [
      `<fieldset class="filter-group"><legend>${title}</legend>`,
      ...entries.map((entry) => {
        const id = `filter-${key}-${entry}`;
        return `<label for="${id}" class="check-row"><input id="${id}" data-filter-key="${key}" type="checkbox" value="${entry}">${entry}</label>`;
      }),
      '</fieldset>',
    ].join('');
  }

  function render() {
    root.innerHTML = [
      renderCheckboxList('Arten', 'species', options.species),
      renderCheckboxList('Status', 'status', options.status),
    ].join('');
  }

  function readStateFromDom() {
    const selected = { species: [], status: [] };
    qsa('input[type="checkbox"][data-filter-key]', root).forEach((input) => {
      if (input.checked) {
        const key = input.getAttribute('data-filter-key');
        selected[key].push(input.value);
      }
    });
    return selected;
  }

  function bind() {
    return {
      apply: () => eventBus.emit(EVENT_NAMES.FILTER_APPLY, readStateFromDom()),
      reset: () => {
        qsa('input[type="checkbox"]', root).forEach((node) => {
          node.checked = false;
        });
        eventBus.emit(EVENT_NAMES.FILTER_RESET);
      },
    };
  }

  render();

  return {
    bind,
  };
}
