$('body').html('');

getList();

function getList() {
    console.log('Getting list...');
    var list = [];
    $.each(index_data, function(i, value) {
        list.push('https://' + app_config.domain+user.run_sessions_path+value[0] + '.gpx');
    });

    $('<a/>', {
        'href' : 'data:text/plain;charset=utf-8,' + encodeURIComponent(list.join('\r\n')),
        'download' : 'list',
        'id' : 'mylist'
    }).html('mylist')
    .after('<br/>')
    .prependTo('body');

    $('#mylist')[0].click();
}