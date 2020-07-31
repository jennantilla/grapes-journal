'use strict';

const displayEntries = (res) => {
    for (let item in res) {
        $('#entry-view-btn').html(res[item]['date']);
        $('.modal-title').html(res[item]['date']);
        $('#entry-id').val(res[item]['entry_id'])
        $('#grateful').val(res[item]['grateful']);
        $('#resolution').val(res[item]['resolution']);
        $('#affirmation').val(res[item]['affirmation']);
        $('#proud').val(res[item]['proud']);
        $('#excited').val(res[item]['excited']);
        $('#self-care').val(res[item]['self_care']);
        $('#jam').html(res[item]['jam']);
        $('#whine').val(res[item]['whine']);
    };
};


$("#filter-entry-view").on('submit', (evt) => {
  evt.preventDefault();

  const formData = $('#filter-entry-view').serialize();
  $.post('/entries.json', formData, displayEntries);
});

  
