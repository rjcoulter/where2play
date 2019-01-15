function calculateHours(startTime, endTime) {
    var tempHours = endTime - startTime;

    if (tempHours > 0) {
        return tempHours;
    }

    return (24 + tempHours);
}

function militaryToNormal(militaryTime) {
    ending = ' AM';

    if (12 <= militaryTime && militaryTime < 24) {
        ending = ' PM';
    }

    if (militaryTime % 12 == 0) {
        return 12 + ending;
    }

    return militaryTime % 12 + ending;
}

function getDate(date) {
    var arr = date.split('/');
    return new Date(arr[2], arr[0] - 1, arr[1]);
}

function createTable(startTime, endTime, date, days) {
    var weekday = new Array(7);
    weekday[0] = "Sun.";
    weekday[1] = "Mon.";
    weekday[2] = "Tues.";
    weekday[3] = "Weds.";
    weekday[4] = "Thurs.";
    weekday[5] = "Fri.";
    weekday[6] = "Sat.";

    var month = new Array(12);
    month[0] = 'Jan';
    month[1] = 'Feb';
    month[2] = 'Mar';
    month[3] = 'Apr';
    month[4] = 'May';
    month[5] = 'Jun';
    month[6] = 'Jul';
    month[7] = 'Aug';
    month[8] = 'Sept';
    month[9] = 'Oct';
    month[10] = 'Nov';
    month[11] = 'Dec';

    var hours = calculateHours(startTime, endTime);
    var d = getDate(date);
    var theader = '<table cellpadding="0" cellspacing="0" id="user_schedule">\n';
    var tSheader = '<table cellpadding="0" cellspacing="0" id="availability_schedule">\n';
    var tbody = '';
    var tsbody = '';

    var hourCounter = 0;

    for (var i = 0; i < hours + 1; i++) {
        if (i == 0) {
            tbody += '<tr><td class="noselect date time"></td>';
            tsbody += '<tr><td class="noselect date time"></td>';
            for (var j = 0; j < days; j++) {
                tbody += '<td class="noselect date time">' + weekday[d.getDay()] + ' ' + month[d.getMonth()] + ' ' + d.getDate() + '</td>';
                tsbody += '<td class="noselect date time">' + weekday[d.getDay()] + ' ' + month[d.getMonth()] + ' ' + d.getDate() + '</td>';
                d.setDate(d.getDate() + 1);
            }
            tbody += '</tr>\n';
            tsbody += '</tr>\n';
            d.setDate(d.getDate() - days)
        } else {
            tbody += '<tr>';
            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                if (j == 0) {
                    tbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour" id="' + militaryToNormal(parseInt(startTime + hourCounter)) + 'f' + month[d.getMonth()] + ' ' + d.getDate() + '"></td>';
                    tsbody += '<td class="noselect time">' + militaryToNormal(parseInt(startTime + hourCounter)) + '</td><td class="noselect availability full_hour"></td>';
                    d.setDate(d.getDate() + 1);
                } else {
                    tbody += '</td><td class="noselect availability full_hour" id="' + militaryToNormal(parseInt(startTime + hourCounter)) + 'f' + month[d.getMonth()] + ' ' + d.getDate() + '"></td>'
                    tsbody += '</td><td class="noselect availability full_hour"></td>';
                    d.setDate(d.getDate() + 1);
                }
            }
            d.setDate(d.getDate() - days)

            tbody += '</tr>\n';
            tsbody += '</tr>\n';
            tbody += '<tr>';
            tsbody += '<tr>';
            for (var j = 0; j < days; j++) {
                if (j == 0) {
                    tbody += '<td class="noselect time"></td><td class="noselect availability half_hour" id="' + militaryToNormal(parseInt(startTime + hourCounter)) + 'h' + month[d.getMonth()] + ' ' + d.getDate() + '"></td>'
                    tsbody += '<td class="noselect time"></td><td class="noselect availability half_hour"></td>'
                    d.setDate(d.getDate() + 1);
                } else {
                    tbody += '<td class="noselect availability half_hour" id="' + militaryToNormal(parseInt(startTime + hourCounter)) + 'h' + month[d.getMonth()] + ' ' + d.getDate() + '"></td>'
                    tsbody += '<td class="noselect availability half_hour"></td>'
                    d.setDate(d.getDate() + 1);
                }
            }
            d.setDate(d.getDate() - days)
            tbody += '</tr>\n';
            tsbody += '</tr>\n';

            hourCounter += 1;
        }
    }
    var tfooter = '</table>';
    var tsfooter = '</table>';

    document.getElementById('user_table_container').innerHTML = theader + tbody + tfooter
    document.getElementById('availability_table_container').innerHTML = tSheader + tsbody + tsfooter;
}

$(function () {
    let colors = ["highlighted1", "highlighted2", "highlighted3", "highlighted4", "highlighted5", "highlighted6", "highlighted7", "highlighted8", "highlighted9"]
    var isMouseDown = false;
    var isMouseDown1 = false;
    var hasSpace = true;
    $("#availability_schedule td.availability")
        .mousedown(function () {
            isMouseDown = true;
            let current_count = $(this).html()
            if (current_count == '') {
                $(this).html(1)
            }
            else {
                $(this).html(parseInt(current_count) + 1)
            }
            if (parseInt($(this).html()) - 1 < colors.length) {
                $(this).toggleClass(colors[$(this).html() - 1])
            }
            return false; // prevent text selection
        })
        .mouseover(function () {
            if (isMouseDown) {
                let current_count = $(this).html()
                if (current_count == '') {
                    $(this).html(1)
                }
                else {
                    $(this).html(parseInt(current_count) + 1)
                }
                if (parseInt($(this).html()) - 1 < colors.length) {
                    $(this).toggleClass(colors[$(this).html() - 1])
                }
            }
        });
    $(document)
        .mouseup(function () {
            isMouseDown = false;
        });


    $("#user_schedule td.availability")
        .mousedown(function () {
            isMouseDown1 = true
            if ($(this).html() == " ") {
                $(this).toggleClass("highlighted9")
                hasSpace = false
                $(this).html("")
            }
            else {
                $(this).toggleClass("highlighted9")
                hasSpace = true
                $(this).html(" ")
            }
            return false; // prevent text selection
        })
        .mouseover(function () {
            if (isMouseDown1 && !hasSpace && $(this).html() == " ") {
                $(this).toggleClass("highlighted9")
                $(this).html("")
            }
            if (isMouseDown1 && hasSpace && $(this).html() == "") {
                $(this).toggleClass("highlighted9")
                $(this).html(" ")
            }
        });

    $(document)
        .mouseup(function () {
            isMouseDown1 = false;
        });
});

$(document).ready(function () {
    $("a.submit").click(function () {
        document.getElementById("availability_form").submit();
    });
});

function gatherHighlighted() {
    let full_hours = document.getElementsByClassName("noselect availability full_hour highlighted9")
    let half_hours = document.getElementsByClassName("noselect availability half_hour highlighted9")
    let all_hours = []
    for (var i = 0; i < full_hours.length; i++) {
        all_hours.push(full_hours[i].id)
    }
    for (var i = 0; i < half_hours.length; i++) {
        all_hours.push(half_hours[i].id)
    }
    console.log(all_hours)
}